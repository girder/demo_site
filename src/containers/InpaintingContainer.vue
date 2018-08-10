<template lang="pug">
div
  inpainting(v-if="isLoggedIn", @run="run", :image-progress="imageProgress",
      :mask-progress="maskProgress", :uploading="uploading")
  auth-container(v-else, :description="description", title="Image Inpainting",
      endpoint="inpainting/example")
</template>

<script>
import { mapGetters, mapState } from 'vuex';
import rest, { formEncode } from '@/rest';
import AuthContainer from '@/containers/AuthContainer';
import Inpainting from '@/views/Inpainting';
import { uploadFile } from '@/utils/upload';

const description = `This application allows you to select a photo from your device, draw on
the parts of it you want the algorithm to fill in, and then upload it and run the algorithm
on the server. You must log in or register a user to proceed.`;

export default {
  components: { AuthContainer, Inpainting },
  data: () => ({
    description,
    imageProgress: 0,
    maskProgress: 0,
    uploading: false,
  }),
  computed: {
    ...mapState('auth', ['user']),
    ...mapGetters('auth', ['isLoggedIn']),
  },
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
        imageId: imageFile._id,
        maskId: maskFile._id,
        outputFolderId: folder._id,
      }))).data;

      // We should probably use a route component instead of this for purity later on.
      this.$router.push(`/inpainting/${job._id}`);
    },
  },
};
</script>
