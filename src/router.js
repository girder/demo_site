import Vue from 'vue';
import Router from 'vue-router';
import CT from '@/views/CT';
import CTTerms from '@/views/CTTerms';
import FrontPage from '@/views/FrontPage';
import Stroke from '@/views/Stroke';

Vue.use(Router);

export default new Router({
  routes: [{
    path: '/',
    component: FrontPage,
  }, {
    path: '/ct',
    component: CT,
  }, {
    path: '/ct_terms',
    component: CTTerms,
  }, {
    path: '/stroke',
    component: Stroke,
  }],
});
