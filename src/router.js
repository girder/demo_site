import Vue from 'vue';
import Router from 'vue-router';
import Glance from '@/views/Glance';
import GlanceItem from '@/routes/GlanceItem';
import CTTerms from '@/views/CTTerms';
import FrontPage from '@/views/FrontPage';
import StudyListContainer from '@/containers/StudyListContainer';

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
  }],
});
