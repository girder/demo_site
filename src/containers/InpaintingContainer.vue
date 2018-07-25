<template lang="pug">
inpainting(@run="run", :image-progress="imageProgress", :mask-progress="maskProgress",
    :uploading="uploading")
</template>

<script>
import { mapState } from 'vuex';
import rest, { formEncode } from '@/rest';
import Inpainting from '@/views/Inpainting';
import { uploadFile } from '@/utils/upload';

export default {
  components: { Inpainting },
  data: () => ({
    imageProgress: 0,
    maskProgress: 0,
    uploading: false,
  }),
  computed: mapState('auth', ['user']),
  methods: {
    async run({ image, mask }) {
      this.uploading = true;

      // Create a new folder in the user's space
      const folder = (await rest.post('folder', formEncode({
        parentType: 'user',
        parentId: this.user._id,
        name: `Inpainting ${new Date().toISOString()}`,
      }))).data;

      // Upload the image and mask to the new folder
      const [imageFile, maskFile] = await Promise.all([
        uploadFile(image, folder, {
          progress: (p) => {
            if (p.indeterminate) {
              this.imageProgress = -1;
            } else {
              this.imageProgress = 100 * (p.current / p.total);
            }
          },
        }),
        uploadFile(mask, folder, {
          progress: (p) => {
            if (p.indeterminate) {
              this.maskProgress = -1;
            } else {
              this.maskProgress = 100 * (p.current / p.total);
            }
          },
        }),
      ]);

      // Kick off processing job
      const job = (await rest.post('inpainting', formEncode({
        imageFileId: imageFile._id,
        maskFileId: maskFile._id,
        outputFolderId: folder._id,
      }))).data;

      // We should probably use a route component instead of this for purity later on.
      this.$router.push(`/inpainting/${job._id}`);
    },
  },
};
</script>
