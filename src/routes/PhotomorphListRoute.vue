<template lang="pug">
div
  photomorph-list-container(v-if="isLoggedIn")
  auth-container(v-else)
</template>

<script>
import { mapGetters } from 'vuex';
import AuthContainer from '@/containers/AuthContainer';
import PhotomorphListContainer from '@/containers/PhotomorphListContainer';

export default {
  components: { AuthContainer, PhotomorphListContainer },
  computed: mapGetters('auth', ['isLoggedIn']),
};
</script>
