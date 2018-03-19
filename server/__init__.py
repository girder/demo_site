import os
from girder.api import access
from girder.api.describe import Description, autoDescribeRoute
from girder.api.rest import Resource, filtermodel
from girder.constants import AccessType
from girder.models.collection import Collection
from girder.models.folder import Folder
from girder.models.setting import Setting
from girder.utility import setting_utilities
from girder.utility.server import staticFile
from girder.utility.plugin_utilities import registerPluginWebroot


class PluginSettings(object):
    STUDIES_COLL_ID = 'stroke_ct.studies_collection_id'


class Study(Resource):
    def __init__(self):
        super(Resource, self).__init__()
        self.resourceName = 'study'

        self.route('GET', (), self.listStudies)
        self.route('POST', (), self.createStudy)

    @access.public
    @filtermodel(Folder)
    @autoDescribeRoute(
        Description('List studies.')
        .pagingParams(defaultSort='studyId')
    )
    def listStudies(self, limit, offset, sort):
        studies = Folder().find({'studyId': {'$exists': True}}, sort=sort)
        return list(Folder().filterResultsByPermission(
            studies, level=AccessType.READ, user=self.getCurrentUser()))

    @access.user
    @filtermodel(Folder)
    @autoDescribeRoute(
        Description('Create a new study.')
        .param('identifier', 'The unique ID of the study.')
        .param('date', 'Study date.', dataType='dateTime')
        .param('description', 'Study description.')
    )
    def createStudy(self, identifier, date, description):
        studiesCollId = Setting().get(PluginSettings.STUDIES_COLL_ID)
        if not studiesCollId:
            raise Exception('You must specify a studies collection.')

        studiesColl = Collection().load(
            studiesCollId, exc=True, level=AccessType.WRITE, user=self.getCurrentUser())

        study = Folder().createFolder(
            parent=studiesColl, name=identifier, description=description, parentType='collection',
            public=False, creator=self.getCurrentUser(), allowRename=True)
        study['isStudy'] = True
        study['nSeries'] = 0
        study['studyDate'] = date
        study['studyId'] = identifier
        return Folder().save(study)


class Series(Resource):
    def __init__(self):
        super(Resource, self).__init__()
        self.resourceName = 'series'

        self.route('GET', (), self.listSeries)

    @access.public
    @filtermodel(Folder)
    @autoDescribeRoute(
        Description('List series in a study.')
        .pagingParams(defaultSort='name')
    )
    def listSeries(self, limit, offset, sort):
        # TODO implement
        studies = Folder().find({'studyId': {'$exists': True}}, sort=sort)
        return list(Folder().filterResultsByPermission(
            studies, level=AccessType.READ, user=self.getCurrentUser()))


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

    Folder().ensureIndex('studyId')
    Folder().exposeFields(level=AccessType.READ, fields={
        'isStudy', 'nSeries', 'studyDate', 'studyId'})
