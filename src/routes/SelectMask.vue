<template lang="pug">
select-mask-container(:folder-id="$route.params.folderId", :item-id="$route.params.itemId",
    @started="jobStarted")
</template>

<script>
import SelectMaskContainer from '@/containers/SelectMaskContainer';

export default {
  components: { SelectMaskContainer },
  methods: {
    jobStarted() {
      this.$router.push('/timelapse');
    },
  },
};
</script>
