<template lang="pug">
upload(:multiple="multiple", :error-message="errorMessage", :uploading="uploading", :files="files",
    @start="start", @resume="start", @clear="files = []", @filesChanged="filesChanged",
    @removeFile="removeFile")
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
    files: [],
    folder: null,
  }),
  computed: mapState('auth', ['user']),
  methods: {
    filesChanged(files) {
      this.files = [...files].map(file => ({
        file,
        status: 'pending',
        progress: {},
        upload: null,
        result: null,
      }));
    },
    removeFile(i) {
      this.files.splice(i, 1);
    },
    async createUploadFolder() {
      const { data } = await rest.post('folder', formEncode({
        name: `Photomorph Upload ${new Date().toISOString()}`,
        parentType: 'user',
        parentId: this.user._id,
      }));
      return data;
    },
    async processUpload() {
      const { data } = await rest.post('photomorph', formEncode({
        folderId: this.folder._id,
      }));
      return data;
    },
    async start() {
      this.uploading = true;
      this.errorMessage = null;

      if (!this.folder) {
        try {
          this.folder = await this.createUploadFolder();
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
              file.result = await uploadFile(file.file, this.folder, { progress });
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

      const job = await this.processUpload(this.folder);

      this.uploading = false;
      this.showToast({
        text: 'Upload complete',
        color: 'success',
        icon: 'check_circled',
        ms: 3000,
      });
      this.files = [];
      this.folder = null;
      this.$emit('done', {
        job,
        results,
      });
    },
    ...mapActions('toast', ['showToast']),
  },
};
</script>
