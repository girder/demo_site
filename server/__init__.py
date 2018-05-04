import datetime
import json
import os
import six

from girder import events, logger
from girder.api import access
from girder.api.describe import Description, autoDescribeRoute
from girder.api.rest import Resource, filtermodel
from girder.constants import AccessType, SortDir
from girder.models.collection import Collection
from girder.models.file import File
from girder.models.folder import Folder
from girder.models.item import Item
from girder.plugins.jobs.models.job import Job
from girder.plugins.thumbnails.worker import createThumbnail
from girder.utility import setting_utilities
from girder.utility.server import staticFile
from girder.utility.plugin_utilities import registerPluginWebroot
from girder_worker.docker.tasks import docker_run
from girder_worker.docker.transforms import VolumePath
from girder_worker.docker.transforms.girder import (
    GirderFolderIdToVolume, GirderUploadVolumePathToItem)
from PIL import Image


class PluginSettings(object):
    STUDIES_COLL_ID = 'stroke_ct.studies_collection_id'


def _extractDate(file):
    with File().open(file) as fd:
        data = fd.read()

        try:
            img = Image.open(six.BytesIO(data))
            return img._getexif().get(36867)  # EXIF field DateTimeOriginal
        except Exception:
            return None


def _handleUpload(event):
    upload, file = event.info['upload'], event.info['file']

    try:
        reference = json.loads(upload.get('reference'))
    except (TypeError, ValueError):
        return

    if not isinstance(reference, dict) or 'photomorph' not in reference:
        return

    if 'photomorphOrdinal' in reference:
        item = Item().load(file['itemId'], force=True, exc=True)
        item['originalName'] = item['name']
        item['name'] = '%05d_%s' % (reference['photomorphOrdinal'], item['name'])
        item['photomorphTakenDate'] = _extractDate(file)

        Item().save(item)

        try:
            createThumbnail(
                width=128, height=128, crop=True, fileId=file['_id'], attachToType='item',
                attachToId=item['_id'])
        except Exception:
            logger.exception('Failure during photomorph thumbnailing')

    elif reference.get('photomorph') and 'resultType' in reference:
        photomorph = Folder().load(reference['folderId'], force=True, exc=True)
        photomorph['photomorphOutputItems'][reference['resultType']] = file['_id']
        Folder().save(photomorph)


class Photomorph(Resource):
    def __init__(self):
        super(Photomorph, self).__init__()
        self.resourceName = 'photomorph'

        self.route('GET', (), self.listPhotomorphs)
        self.route('POST', (), self.createPhotomorph)
        self.route('POST', (':id', 'process'), self.runPhotomorph)

    @access.user
    @filtermodel(Folder)
    @autoDescribeRoute(
        Description('List photomorphs.')
        .pagingParams(defaultSort='created', defaultSortDir=SortDir.DESCENDING)
    )
    def listPhotomorphs(self, limit, offset, sort):
        user = self.getCurrentUser()
        # Right now just find photomorphs for the current user. TODO support shared ones?
        cursor = Folder().find({
            'isPhotomorph': True,
            'parentId': user['_id']
        }, sort=sort)
        return list(Folder().filterResultsByPermission(
            cursor, user, level=AccessType.READ, limit=limit, offset=offset))

    @access.user
    @filtermodel(Folder)
    @autoDescribeRoute(
        Description('Create a new timelapse sequence.')
        .param('name', 'Name for the sequence.', required=False, strip=True)
        .notes('Returns the folder into which input images should be uploaded.')
    )
    def createPhotomorph(self, name):
        user = self.getCurrentUser()
        name = name or 'Timelapse %s' % datetime.datetime.utcnow()
        folder = Folder().createFolder(
            user, name=name, parentType='user', public=False, creator=user)
        input = Folder().createFolder(folder, name='_input', creator=user)

        folder['isPhotomorph'] = True
        folder['photomorphInputFolderId'] = input['_id']
        Folder().save(folder)

        return input

    @access.user
    @filtermodel(Job)
    @autoDescribeRoute(
        Description('Run photomorph on a folder of images.')
        .modelParam('id', 'The ID of the folder containing the input images.',
                    model=Folder, level=AccessType.READ)
    )
    def runPhotomorph(self, folder):
        user = self.getCurrentUser()
        mp4Out = VolumePath('__output__.mp4')
        gifOut = VolumePath('__output__.gif')

        parent = Folder().load(folder['parentId'], level=AccessType.WRITE, exc=True, user=user)
        outputFolder = Folder().createFolder(
            parent, '_output', public=False, creator=user, reuseExisting=True)
        outputMp4 = Item().createItem('out.mp4', creator=user, folder=outputFolder)
        outputGif = Item().createItem('out.gif', creator=user, folder=outputFolder)

        parent['photomorphOutputFolderId'] = outputFolder['_id']
        parent['photomorphOutputItems'] = {}

        job = docker_run.delay(
            'photomorph:latest', container_args=[
                '--mp4-out', mp4Out,
                '--gif-out', gifOut,
                GirderFolderIdToVolume(folder['_id'], folder_name='_input')
            ], girder_job_title='Photomorph: %s' % folder['name'],
            girder_result_hooks=[
                GirderUploadVolumePathToItem(mp4Out, outputMp4['_id'], upload_kwargs={
                    'reference': json.dumps({
                        'photomorph': True,
                        'folderId': str(parent['_id']),
                        'resultType': 'mp4'
                    })
                }),
                GirderUploadVolumePathToItem(gifOut, outputGif['_id'], upload_kwargs={
                    'reference': json.dumps({
                        'photomorph': True,
                        'folderId': str(parent['_id']),
                        'resultType': 'gif'
                    })
                })
            ], pull_image=False).job  # TODO pull the image for real.

        parent['photomorphJobId'] = job['_id']
        Folder().save(parent)

        job['photomorphId'] = parent['_id']
        return Job().save(job)


class Study(Resource):
    def __init__(self):
        super(Study, self).__init__()
        self.resourceName = 'study'

        self.route('GET', (), self.listStudies)
        self.route('POST', (), self.createStudy)

    @access.public
    @filtermodel(Folder)
    @autoDescribeRoute(
        Description('List studies.')
        .pagingParams(defaultSort='patientId', defaultLimit=500)
    )
    def listStudies(self, limit, offset, sort):
        cursor = Folder().find({'isStudy': True}, sort=sort)
        return list(Folder().filterResultsByPermission(
            cursor, level=AccessType.READ, user=self.getCurrentUser(), limit=limit, offset=offset))

    @access.user
    @filtermodel(Folder)
    @autoDescribeRoute(
        Description('Create a new study.')
        .param('patentId', 'The anonymized patient identifier or MRN.')
        .param('date', 'Study date.', dataType='dateTime')
        .param('modality', 'Study modality.')
        .param('description', 'Study description.')
    )
    def createStudy(self, identifier, date, modality, description):
        user = self.getCurrentUser()
        study = Folder().createFolder(
            parent=user, name=identifier, description=description, parentType='user', public=False,
            creator=user, allowRename=True)
        study['isStudy'] = True
        study['nSeries'] = 0
        study['studyDate'] = date
        study['patientId'] = identifier
        study['studyModality'] = modality
        return Folder().save(study)


class Series(Resource):
    def __init__(self):
        super(Series, self).__init__()
        self.resourceName = 'series'

        self.route('GET', (), self.listSeries)
        self.route('POST', (), self.createSeries)

    @access.public
    @filtermodel(Item)
    @autoDescribeRoute(
        Description('List series in a study.')
        .modelParam('studyId', 'The ID of the parent study.', paramType='query', model=Folder,
                    level=AccessType.READ)
        .pagingParams(defaultSort='name', defaultLimit=500)
    )
    def listSeries(self, folder, limit, offset, sort):
        return list(Folder().childItems(folder, limit=limit, offset=offset, sort=sort, filters={
            'isSeries': True
        }))

    @access.user
    @filtermodel(Item)
    @autoDescribeRoute(
        Description('Create a new series.')
        .modelParam('studyId', 'The parent study.', model=Folder, level=AccessType.WRITE,
                    paramType='query')
        .param('name', 'The name of the series.')
    )
    def createSeries(self, folder, name):
        series = Item().createItem(name, creator=self.getCurrentUser(), folder=folder)
        series['isSeries'] = True
        series = Item().save(series)

        Folder().update({
            '_id': folder['_id']
        }, {
            '$inc': {'nSeries': 1}
        }, multi=False)

        return series


def _itemDeleted(event):
    item = event.info
    if item.get('isSeries') is True:
        Folder().update({
            '_id': item['folderId']
        }, {
            '$inc': {'nSeries': -1}
        }, multi=False)


@setting_utilities.validator(PluginSettings.STUDIES_COLL_ID)
def _validateStudiesColl(doc):
    Collection().load(doc['value'], exc=True, force=True)


def load(info):
    webroot = staticFile(os.path.join(info['pluginRootDir'], 'dist', 'index.html'))
    registerPluginWebroot(webroot, info['name'])

    info['config']['/stroke_ct_static'] = {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(info['pluginRootDir'], 'dist', 'stroke_ct_static')
    }

    info['apiRoot'].study = Study()
    info['apiRoot'].series = Series()
    info['apiRoot'].photomorph = Photomorph()

    Folder().ensureIndex(('isStudy', {'sparse': True}))
    Folder().ensureIndex(('isPhotomorph', {'sparse': True}))
    Folder().exposeFields(level=AccessType.READ, fields={
        'isStudy', 'nSeries', 'studyDate', 'patientId', 'studyModality', 'photomorphJobId',
        'isPhotomorph', 'photomorphInputFolderId', 'photomorphOutputItems'})
    Item().exposeFields(level=AccessType.READ, fields={
        'isSeries', 'isPhotomorph', 'originalName', 'photomorphTakenDate'})
    Job().exposeFields(level=AccessType.READ, fields={'photomorphId'})

    events.bind('model.file.finalizeUpload.after', info['name'], _handleUpload)
    events.bind('model.item.remove', info['name'], _itemDeleted)
