<template lang="pug">
select-mask(@start="processUpload", :image-url="imageUrl")
</template>

<script>
import rest, { getApiUrl } from '@/rest';
import SelectMask from '@/views/SelectMask';

export default {
  components: { SelectMask },
  props: {
    folderId: {
      type: String,
      required: true,
    },
    fileId: {
      type: String,
      required: true,
    },
  },
  computed: {
    imageUrl() {
      return `${getApiUrl()}/file/${this.fileId}/download`;
    },
  },
  methods: {
    async processUpload() {
      const job = (await rest.post(`photomorph/${this.folder._id}/process`)).data;

      // do something
    },
  },
};
</script>
