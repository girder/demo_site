import Vue from 'vue';
import Router from 'vue-router';
import Glance from '@/views/Glance';
import GlanceItem from '@/routes/GlanceItem';
import CTTerms from '@/views/CTTerms';
import FrontPage from '@/views/FrontPage';
import PhotomorphListContainer from '@/containers/PhotomorphListContainer';
import StudyListContainer from '@/containers/StudyListContainer';
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
    path: '/studies',
    component: StudyListContainer,
  }, {
    path: '/upload',
    component: UploadPage,
  }, {
    path: '/photomorphs',
    component: PhotomorphListContainer,
  }],
});
