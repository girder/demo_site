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
    uploadComplete() {
      this.$router.push('/photomorphs');
    },
  },
};
</script>
