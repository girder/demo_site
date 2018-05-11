<template lang="pug">
select-mask(@start="processUpload", :image-url="imageUrl")
</template>

<script>
import rest, { formEncode, getApiUrl } from '@/rest';
import SelectMask from '@/views/SelectMask';

export default {
  components: { SelectMask },
  props: {
    folderId: {
      type: String,
      required: true,
    },
    itemId: {
      type: String,
      default: null,
    },
  },
  computed: {
    imageUrl() {
      return `${getApiUrl()}/item/${this.itemId}/download`;
    },
  },
  methods: {
    async processUpload({ imageRect }) {
      const job = (await rest.post(`photomorph/${this.folderId}/process`, formEncode({
        maskRect: JSON.stringify(imageRect),
      }))).data;

      this.$emit('started', {
        folderId: this.folderId,
        job,
      });
    },
  },
};
</script>
