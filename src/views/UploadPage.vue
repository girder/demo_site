<template lang="pug">
v-app
  v-content
    upload-container(@done="uploadComplete")
</template>

<script>
import UploadContainer from '@/containers/UploadContainer';

export default {
  components: { UploadContainer },
  methods: {
    uploadComplete({ folder, results }) {
      this.$router.push(`/select_mask/${folder._id}/item/${results[0].itemId}`);
    },
  },
};
</script>
