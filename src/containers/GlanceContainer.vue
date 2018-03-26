<template lang="pug">
glance(:name="name", :url="url")
</template>

<script>
import rest, { getApiUrl } from '@/rest';
import Glance from '@/views/Glance';
import { fetchingContainer } from '@/utils/mixins';

export default {
  components: { Glance },
  mixins: [fetchingContainer],
  props: {
    itemId: {
      type: String,
      required: true,
    },
  },
  data: () => ({
    name: null,
    url: null,
  }),
  methods: {
    fetch() {
      return rest.get(`/item/${this.itemId}`).then(({ data }) => {
        this.name = data.name;
        this.url = `${getApiUrl()}/item/${data._id}/download`;
      });
    },
  },
};
</script>
