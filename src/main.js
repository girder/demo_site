import Vue from 'vue';
import { sync } from 'vuex-router-sync';

import App from './App';
import { API_ROOT } from './constants';
import router from './router';
import store from './store';
import { setApiUrl, getTokenFromCookie } from './rest';
import './utils/ui-setup';

sync(store, router);
setApiUrl(API_ROOT);

store.commit('auth/setToken', getTokenFromCookie());
store.dispatch('auth/whoami').then(() => new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>',
}));
