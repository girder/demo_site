<template lang="pug">
photomorph-list(:folders="folders", :selected-folder="selectedFolder", :loading="fetchingList",
    :loading-children="fetchingChildren", @select="selectFolder", :input-items="inputItems")
</template>

<script>
import rest from '@/rest';
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
    selectFolder(folder) {
      this.selectedFolder = folder;
      this.fetchingChildren = true;
      this.inputItems = [];

      // TODO paginate?
      rest.get(`/item?folderId=${folder.photomorphInputFolderId}`).then(({ data }) => {
        this.inputItems = data;
      }).finally(() => {
        this.fetchingChildren = false;
      });
    },
  },
};
</script>
