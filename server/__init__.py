import datetime
import json
import os

from girder import events
from girder.api import access
from girder.api.describe import Description, autoDescribeRoute
from girder.api.rest import Resource, filtermodel
from girder.constants import AccessType
from girder.models.collection import Collection
from girder.models.folder import Folder
from girder.models.item import Item
from girder.plugins.jobs.models.job import Job
from girder.utility import setting_utilities
from girder.utility.server import staticFile
from girder.utility.plugin_utilities import registerPluginWebroot
from girder_worker.docker.tasks import docker_run
from girder_worker.docker.transforms import VolumePath
from girder_worker.docker.transforms.girder import (
    GirderFolderIdToVolume, GirderUploadVolumePathToItem)


class PluginSettings(object):
    STUDIES_COLL_ID = 'stroke_ct.studies_collection_id'


def _handleUpload(event):
    upload, file = event.info['upload'], event.info['file']

    try:
        reference = json.loads(upload.get('reference'))
    except (TypeError, ValueError):
        return

    if isinstance(reference, dict) and 'photomorphOrdinal' in reference:
        item = Item().load(file['itemId'], force=True, exc=True)
        item['name'] = '%05d_%s' % (reference['photomorphOrdinal'], item['name'])
        Item().save(item)


class Photomorph(Resource):
    def __init__(self):
        super(Photomorph, self).__init__()
        self.resourceName = 'photomorph'

        self.route('POST', (), self.createPhotomorph)
        self.route('POST', (':id', 'process'), self.runPhotomorph)

    @access.user
    @filtermodel(Folder)
    @autoDescribeRoute(
        Description('Create a new photomorph.')
        .notes('Returns the folder into which input images should be uploaded.')
    )
    def createPhotomorph(self):
        user = self.getCurrentUser()
        name = 'Photomorph %s' % datetime.datetime.utcnow()
        folder = Folder().createFolder(
            user, name=name, parentType='user', public=False, creator=user)
        return Folder().createFolder(folder, name='_input', creator=user)

    @access.user
    @filtermodel(Job)
    @autoDescribeRoute(
        Description('Run photomorph on a folder of images.')
        .modelParam('id', 'The ID of the folder containing the input images.',
                    model=Folder, level=AccessType.READ)
    )
    def runPhotomorph(self, folder):
        user = self.getCurrentUser()
        mpegOut = VolumePath('__output__/out.mpeg')
        gifOut = VolumePath('__output__/out.gif')

        parent = Folder().load(folder['parentId'], level=AccessType.WRITE, exc=True, user=user)
        outputFolder = Folder().createFolder(
            parent, '_output', public=False, creator=user, reuseExisting=True)
        outputMpeg = Item().createItem('out.mpeg', creator=user, folder=outputFolder)
        outputGif = Item().createItem('out.gif', creator=user, folder=outputFolder)

        job = docker_run.delay(
            'photomorph:latest', container_args=[
                GirderFolderIdToVolume(folder['_id'], folder_name='input'),
                '--mpeg', mpegOut,
                '--gif', gifOut
            ], girder_job_title='Photomorph: %s' % folder['name'],
            girder_result_hooks=[
                GirderUploadVolumePathToItem(mpegOut, outputMpeg['_id'], upload_kwargs={
                    'reference': json.dumps({
                        'photomorph': True,
                        'input_folder': str(folder['_id']),
                    })
                }),
                GirderUploadVolumePathToItem(gifOut, outputGif['_id'], upload_kwargs={
                    'reference': json.dumps({
                        'photomorph': True,
                        'input_folder': str(folder['_id']),
                    })
                })
            ]).job

        job['photomorphInputFolderId'] = folder['_id']
        job['photomorphOutputItems'] = {
            'mpeg': outputMpeg['_id'],
            'gif': outputGif['_id']
        }
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
    Folder().exposeFields(level=AccessType.READ, fields={
        'isStudy', 'nSeries', 'studyDate', 'patientId', 'studyModality'})

    Item().ensureIndex(('isPhotomorph', {'sparse': True}))
    Item().exposeFields(level=AccessType.READ, fields={'isSeries', 'isPhotomorph'})

    Job().exposeFields(level=AccessType.READ, fields={
        'photomorphInputFolderId', 'photomorphOutputItems'
    })

    events.bind('model.file.finalizeUpload.after', info['name'], _handleUpload)
    events.bind('model.item.remove', info['name'], _itemDeleted)
