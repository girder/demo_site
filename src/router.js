import Vue from 'vue';
import Router from 'vue-router';
import Glance from '@/views/Glance';
import GlanceItem from '@/routes/GlanceItem';
import SelectMask from '@/routes/SelectMask';
import CTTerms from '@/views/CTTerms';
import FrontPage from '@/views/FrontPage';
import PhotomorphListRoute from '@/routes/PhotomorphListRoute';
// import StudyListContainer from '@/containers/StudyListContainer';
import UploadPage from '@/views/UploadPage';

Vue.use(Router);

export default new Router({
  routes: [{
    path: '/',
    component: FrontPage,
  }, {
    path: '/glance',
    component: Glance,
  }, {
    path: '/glance/:id',
    component: GlanceItem,
  }, {
    path: '/ct_terms',
    component: CTTerms,
  }, {
    path: '/upload',
    component: UploadPage,
  }, {
    path: '/timelapse',
    component: PhotomorphListRoute,
  }, {
    path: '/select_mask/:folderId/item/:itemId',
    component: SelectMask,
  }],
});
