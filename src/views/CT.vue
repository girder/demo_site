<script>
import { createViewer } from 'paraview-glance';

export default {
  mounted() {
    this.glance = createViewer(this.$el);
  },
  destroyed() {
    this.glance.destroy();
  },
  template: '<div/>',
};
</script>
