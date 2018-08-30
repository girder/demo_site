<template lang="pug">
div
  inpainting(v-if="isLoggedIn", @run="run", :image-progress="imageProgress",
      :mask-progress="maskProgress", :uploading="uploading", :mask-id="maskId",
      :image-id="imageId", @cancelImage="cancelImage", :examples="examples", @loadItem="loadItem")
  auth-container(v-else, :description="description", title="Image Inpainting",
      endpoint="inpainting/example")
</template>

<script>
import { mapGetters, mapState } from 'vuex';
import rest, { formEncode } from '@/rest';
import { fetchingContainer } from '@/utils/mixins';
import AuthContainer from '@/containers/AuthContainer';
import Inpainting from '@/views/Inpainting';
import { uploadFile } from '@/utils/upload';

const description = `This application allows you to select a photo from your device, draw on
the parts of it you want the algorithm to fill in, and then upload it and run the algorithm
on the server. You must log in or register a user to proceed.`;

export default {
  components: { AuthContainer, Inpainting },
  mixins: [fetchingContainer],
  data() {
    return {
      description,
      imageProgress: 0,
      maskProgress: 0,
      uploading: false,
      imageId: this.$route.query.image,
      maskId: this.$route.query.mask,
      examples: [],
    };
  },
  computed: {
    ...mapState('auth', ['user']),
    ...mapGetters('auth', ['isLoggedIn']),
  },
  methods: {
    async fetch() {
      this.examples = (await rest.get('inpainting/example')).data;
    },
    cancelImage() {
      this.imageId = null;
      this.maskId = null;
    },
    async loadItem(item) {
      const [file] = (await rest.get(`item/${item._id}/files?limit=1`)).data;
      this.imageId = file._id;
    },
    async run({ image, mask }) {
      this.uploading = true;

      // Create a new folder in the user's space
      const folder = (await rest.post('folder', formEncode({
        parentType: 'user',
        parentId: this.user._id,
        name: `Inpainting ${new Date().toISOString()}`,
      }))).data;

      let imagePromise;
      if (this.imageId) {
        // If this is a re-run, just reuse existing input image
        imagePromise = Promise.resolve({ _id: this.imageId });
        this.imageProgress = 100;
      } else {
        imagePromise = uploadFile(image, folder, {
          progress: (p) => {
            if (p.indeterminate) {
              this.imageProgress = -1;
            } else {
              this.imageProgress = 100 * (p.current / p.total);
            }
          },
        });
      }

      const promises = [imagePromise, uploadFile(mask, folder, {
        progress: (p) => {
          if (p.indeterminate) {
            this.maskProgress = -1;
          } else {
            this.maskProgress = 100 * (p.current / p.total);
          }
        },
      })];
      const [imageFile, maskFile] = await Promise.all(promises);

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
