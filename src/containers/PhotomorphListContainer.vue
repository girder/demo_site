<template lang="pug">
photomorph-list(:folders="folders", :selected-folder="selectedFolder", :loading="fetchingList",
    :loading-children="fetchingChildren", @select="selectFolder", :input-items="inputItems",
    @saveFolder="saveFolder", @refreshList="fetch")
</template>

<script>
import { mapActions } from 'vuex';
import rest, { formEncode } from '@/rest';
import PhotomorphList from '@/views/PhotomorphList';
import { fetchingContainer, pagingContainer } from '@/utils/mixins';

export default {
  components: { PhotomorphList },
  mixins: [fetchingContainer, pagingContainer],
  data: () => ({
    folders: [],
    inputItems: [],
    fetchingList: false,
    fetchingChildren: false,
    selectedFolder: null,
  }),
  methods: {
    fetch() {
      this.fetchingList = true;
      rest.get('/photomorph', {
        params: this.pagingParams,
      }).then(({ data }) => {
        this.folders = this.transformDataPage(data);
      }).finally(() => {
        this.fetchingList = false;
      });
    },
    saveFolder({ folder, fields }) {
      rest.put(`/folder/${folder._id}`, formEncode(fields)).then(() => {
        this.showToast({
          text: 'Info updated',
          color: 'success',
          icon: 'check',
        });
      }).catch((err) => {
        if (err.response.data && err.response.data.message) {
          this.showToast({
            text: err.response.data.message,
            color: 'error',
            icon: 'cancel',
          });
        } else {
          // TODO handle gracefully
          throw err;
        }
      });
    },
    selectFolder(folder) {
      this.selectedFolder = folder;
      this.fetchingChildren = true;
      this.inputItems = [];

      // TODO paginate?
      rest.get(`/item?folderId=${folder.photomorphInputFolderId}&limit=300`).then(({ data }) => {
        this.inputItems = data;
      }).finally(() => {
        this.fetchingChildren = false;
      });
    },
    ...mapActions('toast', ['showToast']),
  },
};
</script>
