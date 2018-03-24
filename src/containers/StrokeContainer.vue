<template lang="pug">
stroke(:series="series", :studies="studies", :selected-study="selectedStudy", :loading="fetching",
    :loading-series="fetchingSeries", @select="selectStudy")
</template>

<script>
import rest from '@/rest';
import Stroke from '@/views/Stroke';
import { fetchingContainer, pagingContainer } from '@/utils/mixins';

export default {
  components: { Stroke },
  mixins: [fetchingContainer, pagingContainer],
  data: () => ({
    studies: [],
    series: [],
    fetching: false,
    fetchingSeries: false,
    selectedStudy: null,
  }),
  methods: {
    fetch() {
      this.fetching = true;
      rest.get('/study', {
        params: this.pagingParams,
      }).then(({ data }) => {
        this.studies = this.transformDataPage(data);
      }).finally(() => {
        this.fetching = false;
      });
    },
    selectStudy(study) {
      this.selectedStudy = study;
      this.series = [];
      this.fetchingSeries = true;
      rest.get('/series', {
        params: {
          studyId: study._id,
        },
      }).then(({ data }) => {
        this.series = data;
      }).finally(() => {
        this.fetchingSeries = false;
      });
    },
  },
};
</script>
