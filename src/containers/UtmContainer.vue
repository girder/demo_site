<template lang="pug">
div
  utm(v-if="isLoggedIn", @run="run", :image-progress="imageProgress",
      :mask-progress="maskProgress", :uploading="uploading", :mask-id="maskId",
      :image-id="imageId", @cancelImage="cancelImage", :demo-data="demoData", @loadItem="loadItem",
      :jobs="jobs", @logout="logout")
  auth-container(v-else,
      :description="description",
      title="Unbalanced Optimal Transport Morphometry",
      endpoint="utm/example")
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex';
import rest from '@/rest';
import { fetchingContainer } from '@/utils/mixins';
import AuthContainer from '@/containers/AuthContainer';
import Utm from '@/views/Utm/Utm.vue';

const description = `This application allows you upload MRI images 
and have our system generate a web view that does some fancy things you'll probably enjoy.`;

export default {
  components: { AuthContainer, Utm },
  mixins: [fetchingContainer],
  data() {
    return {
      description,
      demoData: {},
      jobs: [],
    };
  },
  computed: {
    ...mapState('auth', ['user']),
    ...mapGetters('auth', ['isLoggedIn']),
  },
  methods: {
    ...mapActions('auth', ['logout']),
    async fetch() {
      if (this.isLoggedIn) {
        this.demoData = (await rest.get('utm/demo')).data;
      }
    },
  },
};
</script>
