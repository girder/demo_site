<template lang="pug">
inpainting-result(v-if="job", :job="job", @refresh="fetch")
</template>

<script>
import { JobStatus } from '@/constants';
import rest from '@/rest';
import { fetchingContainer, fetchingRoute } from '@/utils/mixins';
import InpaintingResult from '@/views/InpaintingResult';

export default {
  components: { InpaintingResult },
  mixins: [fetchingContainer, fetchingRoute],
  data: () => ({
    _timeout: null,
    job: null,
  }),
  destroyed() {
    window.clearTimeout(this._timeout);
  },
  methods: {
    async fetch() {
      this.job = (await rest.get(`job/${this.$route.params.jobId}`)).data;

      if (![JobStatus.SUCCESS, JobStatus.ERROR].includes(this.job.status)) {
        this._timeout = window.setTimeout(() => {
          this.fetch();
        }, 5000);
      }
    },
  },
};
</script>
