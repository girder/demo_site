<template lang="pug">
div
  photomorph-list-container(v-if="isLoggedIn")
  auth-container(v-else, :description="description", title="Time-Lapse Video Creation",
      endpoint="photomorph/example")
</template>

<script>
import { mapGetters } from 'vuex';
import AuthContainer from '@/containers/AuthContainer';
import PhotomorphListContainer from '@/containers/PhotomorphListContainer';

const description = `
You can use this service to select a set of photos, sort them into the proper chronological
order, and upload them to the server where we will run advanced image processing algorithms on
them to stitch them into a smooth time-lapse video. You must log in or register to proceed.`;

export default {
  components: { AuthContainer, PhotomorphListContainer },
  data: () => ({ description }),
  computed: mapGetters('auth', ['isLoggedIn']),
};
</script>
