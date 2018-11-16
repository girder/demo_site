<template lang="pug">
inpainting-result(v-if="job", :job="job", @refresh="fetch", @logout="logoutAndLeave")
</template>

<script>
import Vue from 'vue';
import { mapActions, mapGetters } from 'vuex';
import { JobStatus } from '@/constants';
import rest from '@/rest';
import { fetchingContainer } from '@/utils/mixins';
import InpaintingResult from '@/views/inpainting/InpaintingResult';

export default {
  components: { InpaintingResult },
  mixins: [fetchingContainer],
  data: () => ({
    _timeout: null,
    job: null,
  }),
  computed: mapGetters('auth', ['isLoggedIn']),
  watch: {
    $route() {
      Vue.nextTick().then(() => {
        this.fetch();
      });
    },
  },
  destroyed() {
    window.clearTimeout(this._timeout);
  },
  methods: {
    ...mapActions('auth', ['logout']),
    async logoutAndLeave() {
      await this.logout();
      this.$router.push('/inpainting');
    },
    async fetch() {
      if (this.isLoggedIn) {
        this.job = (await rest.get(`job/${this.$route.params.jobId}`)).data;

        if (![JobStatus.SUCCESS, JobStatus.ERROR, JobStatus.CANCELED].includes(this.job.status)) {
          this._timeout = window.setTimeout(() => {
            this.fetch();
          }, 3000);
        }
      } else {
        this.$router.push('/inpainting');
      }
    },
  },
};
</script>
