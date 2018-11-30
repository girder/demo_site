<template lang="pug">
v-app
  v-toolbar
    v-toolbar-title.pl-2
      img.tb-logo(src="@/assets/KWLogo.svg")
  v-container(xs-12)
    v-layout(row, wrap)
      v-flex.pa-2(xs-12, md6, lg8)
        .headline {{ title }}
        .body-1.mt-3 {{ description }}
        .title.mt-5 Examples
        hr.mb-3.mt-1
        v-flex.text-xs-center(v-if="loadingExamples")
          v-progress-circular.my-4(indeterminate, color="primary", size="100")
        v-carousel(v-else, :interval="3000")
          v-carousel-item.showcase-carousel-item(v-for="(item, i) in exampleItems", :key="i")
            v-container(fill-height, justify-center, align-center)
              img.showcase-img(:src="videoUrl(item)")
      v-flex.pa-2(xs-12, md6, lg4)
        v-card
          v-tabs(v-model="activeTab", color="primary", slider-color="yellow", dark)
            v-tab(key="login") Existing user
            v-tab(key="register") New user
            v-tab-item(key="login")
              login-form(ref="loginForm", @login="doLogin",
                 :error-message="loginErrorMessage", :login-in-progress="loginInProgress")
            v-tab-item(key="register")
              register-form(ref="registerForm", @register="doRegister",
                  :errors="registerErrors", :register-in-progress="registerInProgress")
    hr.mt-4.mb-2
    .text-xs-center &copy; Kitware, Inc.
</template>

<script>
import { mapActions } from 'vuex';
import rest, { getApiUrl } from '@/rest';
import { fetchingContainer } from '@/utils/mixins';
import LoginForm from '@/views/LoginForm';
import RegisterForm from '@/views/RegisterForm';

const emptyRegisterErrors = () => ({
  login: null,
  email: null,
  firstName: null,
  lastName: null,
  password: null,
  NONE: null,
});

export default {
  components: { LoginForm, RegisterForm },
  mixins: [fetchingContainer],
  props: {
    description: {
      type: String,
      required: true,
    },
    endpoint: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
  },
  data: () => ({
    loginErrorMessage: '',
    loginInProgress: false,
    registerErrors: emptyRegisterErrors(),
    registerInProgress: false,
    activeTab: null,
    loadingExamples: false,
    exampleItems: [],
  }),
  methods: {
    async fetch() {
      this.loadingExamples = true;
      // TODO we should have an endpoint for faster lookup
      try {
        this.exampleItems = (await rest.get(this.endpoint)).data;
      } finally {
        this.loadingExamples = false;
      }
      // TODO fetch our examples
    },
    doLogin(credentials) {
      this.loginErrorMessage = '';
      this.loginInProgress = true;
      return this.login(credentials).then(() => {
        this.$refs.loginForm.reset();
      }).catch(({ response }) => {
        if (response) {
          this.loginErrorMessage = response.data.message;
        } else {
          this.loginErrorMessage = 'Could not connect to server.';
        }
      }).finally(() => {
        this.loginInProgress = false;
      });
    },
    doRegister(params) {
      this.registerErrors = emptyRegisterErrors();
      this.registerInProgress = true;
      return this.register(params).then(() => {
        this.$refs.registerForm.reset();
      }).catch(({ response }) => {
        if (response) {
          this.registerErrors[response.data.field || 'NONE'] = response.data.message;
        } else {
          this.registerErrors = 'Could not connect to server.';
        }
      }).finally(() => {
        this.registerInProgress = false;
      });
    },
    videoUrl(item) {
      return `${getApiUrl()}/item/${item._id}/download`;
    },
    ...mapActions('auth', ['login', 'register']),
  },
};
</script>

<style lang="stylus" scoped>
.tb-logo
  height 48px
.showcase-carousel-item
  background-color #444
.showcase-img
  max-width 100%
  max-height 100%
</style>
