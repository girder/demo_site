<template lang="pug">
inpainting-result(:job="job", @refresh="fetch")
</template>

<script>
import rest from '@/rest';
import { fetchingContainer, fetchingRoute } from '@/utils/mixins';
import InpaintingResult from '@/views/InpaintingResult';

export default {
  components: { InpaintingResult },
  mixins: [fetchingContainer, fetchingRoute],
  data: () => ({
    job: null,
  }),
  methods: {
    async fetch() {
      this.job = (await rest.get(`job/${this.$route.params.jobId}`)).data;
    },
  },
};
</script>
