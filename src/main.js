import Vue from 'vue';
import { sync } from 'vuex-router-sync';
import { RestClient } from '@girder/components';

import './utils/ui-setup.js';
import App from './App';
import { API_ROOT } from './constants';
import router from './router';
import store from './store';
import { setApiUrl, getTokenFromCookie } from './rest';

const girderRest = new RestClient({ apiRoot: API_ROOT });

sync(store, router);
setApiUrl(API_ROOT);

store.commit('auth/setToken', getTokenFromCookie());
store.dispatch('auth/whoami').then(() => new Vue({
  provide: { girderRest },
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>',
}));
