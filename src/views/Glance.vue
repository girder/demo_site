<script>
import { createViewer } from 'paraview-glance';

export default {
  props: {
    name: {
      type: String,
      default: null,
    },
    url: {
      type: String,
      default: null,
    },
  },
  watch: {
    url() {
      this.glance.openRemoteDataset(this.name, this.url);
    },
  },
  mounted() {
    this.glance = createViewer(this.$el);
    this.glance.updateTab('pipeline');

    if (this.name && this.url) {
      this.glance.openRemoteDataset(this.name, this.url);
    }
  },
  destroyed() {
    this.glance.unbind();
  },
  template: '<div/>',
};
</script>
