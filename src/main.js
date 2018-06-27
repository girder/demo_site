import Vue from 'vue';
import { sync } from 'vuex-router-sync';
// Make sure this CSS is imported prior to importing components; this appears to matter for
// order of precedence for our CSS files that get pulled out with ExtractTextPlugin
import './utils/ui-setup';

import App from './App';
import { API_ROOT } from './constants';
import router from './router';
import store from './store';
import { setApiUrl, getTokenFromCookie } from './rest';

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
