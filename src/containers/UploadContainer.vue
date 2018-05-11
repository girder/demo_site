<template lang="pug">
upload(:multiple="multiple", :error-message="errorMessage", :uploading="uploading",
    @start="start", @resume="start", ref="view")
</template>

<script>
import { mapActions, mapState } from 'vuex';
import rest, { formEncode } from '@/rest';
import { uploadFile, resumeUpload } from '@/utils/upload';
import Upload from '../views/Upload';

export default {
  components: { Upload },
  props: {
    multiple: {
      default: true,
      type: Boolean,
    },
  },
  data: () => ({
    errorMessage: null,
    statusMessage: null,
    uploading: false,
    folder: null,
  }),
  computed: {
    files() {
      return this.$refs.view.files;
    },
    ...mapState('auth', ['user']),
  },
  methods: {
    async createUploadFolder(name) {
      return (await rest.post('photomorph', formEncode({ name }))).data;
    },
    async start(folderName) {
      this.uploading = true;
      this.errorMessage = null;

      if (!this.folder) {
        try {
          this.folder = await this.createUploadFolder(folderName);
        } catch (error) {
          this.errorMessage = error.response.data.message;
          this.uploading = false;
          this.$emit('error', error);
          return;
        }
      }

      const results = [];

      // eslint-disable-next-line no-await-in-loop
      for (let i = 0; i < this.files.length; i += 1) {
        const file = this.files[i];

        if (file.status === 'done') {
          // We are resuming, skip already completed files
          results.push(file.result);
        } else {
          const progress = (event) => {
            file.progress = Object.assign({}, file.progress, event);
          };
          file.status = 'uploading';

          try {
            if (file.upload) {
              file.result = await resumeUpload(file.file, file.upload, { progress });
            } else {
              file.result = await uploadFile(file.file, this.folder, {
                progress,
                params: {
                  reference: JSON.stringify({
                    photomorph: true,
                    photomorphOrdinal: i,
                  }),
                },
              });
            }
            results.push(file.result);
            file.status = 'done';
          } catch (error) {
            if (error.response) {
              this.errorMessage = error.response.data.message;
            } else {
              this.errorMessage = 'Connection failed.';
            }
            file.upload = error.upload;
            file.status = 'error';
            this.uploading = false;
            this.$emit('error', error);
            return;
          }
        }
      }

      this.uploading = false;
      this.showToast({
        text: 'Upload complete',
        color: 'success',
        icon: 'check_circled',
        ms: 3000,
      });
      this.$emit('done', {
        results,
        folder: this.folder,
      });
      this.folder = null;
    },
    ...mapActions('toast', ['showToast']),
  },
};
</script>
