<template lang="pug">
stroke(:studies="studies", :loading="fetching")
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
    fetching: false,
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
  },
};
</script>
