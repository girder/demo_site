import Vue from 'vue';
import Router from 'vue-router';
import CTVisualization from '@/views/CTVisualization';
import FrontPage from '@/views/FrontPage';

Vue.use(Router);


export default new Router({
  routes: [{
    path: '/',
    component: FrontPage,
  }, {
    path: '/ct_terms',
    component: CTVisualization,
  }],
});
