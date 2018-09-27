<template lang="pug">
v-card
  form(@submit.prevent="")
    v-card-text
      v-text-field(v-model="username", label="Username or email", autofocus)
      v-text-field(v-model="password", type="password", label="Password",
          :error-messages="errorMessages")
    v-card-actions
      v-btn(type="submit", color="primary", :disabled="loginInProgress",
          :loading="loginInProgress", @click="login") Login
      v-btn(type="submit", flat, :disabled="loginInProgress", @click="guestLogin") Login as guest
</template>

<script>
export default {
  props: {
    errorMessage: {
      default: '',
      type: String,
    },
    loginInProgress: {
      default: false,
      type: Boolean,
    },
  },
  data() {
    return {
      username: '',
      password: '',
    };
  },
  computed: {
    errorMessages() {
      return this.errorMessage ? [this.errorMessage] : [];
    },
  },
  methods: {
    guestLogin() {
      this.$emit('login', {
        username: 'guest',
        password: '',
      });
    },
    login() {
      this.$emit('login', {
        username: this.username,
        password: this.password,
      });
    },
    reset() {
      this.username = '';
      this.password = '';
    },
  },
};
</script>
