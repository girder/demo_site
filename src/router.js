import Vue from 'vue';
import Router from 'vue-router';
import Glance from '@/views/Glance';
import GlanceItem from '@/routes/GlanceItem';
import SelectMask from '@/routes/SelectMask';
import FrontPage from '@/views/FrontPage';
import PhotomorphListRoute from '@/routes/PhotomorphListRoute';
import Inpainting from '@/containers/InpaintingContainer';
import InpaintingResultContainer from '@/containers/InpaintingResultContainer';
import StudyListContainer from '@/containers/StudyListContainer';
import UploadPage from '@/views/UploadPage';
import Utm from '@/containers/UtmContainer';

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
    path: '/upload',
    component: UploadPage,
  }, {
    path: '/utm',
    component: Utm,
  }, {
    path: '/timelapse',
    component: PhotomorphListRoute,
  }, {
    path: '/select_mask/:folderId/item/:itemId',
    component: SelectMask,
  }, {
    path: '/inpainting',
    component: Inpainting,
  }, {
    path: '/inpainting/:jobId',
    component: InpaintingResultContainer,
  }, {
    path: '/stroke_ct',
    component: StudyListContainer,
  }],
});
