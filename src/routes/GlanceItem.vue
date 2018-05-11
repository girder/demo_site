<template lang="pug">
glance-container(ref="wrapped", :item-id="$route.params.id")
</template>
<script>
import { fetchingRoute } from '@/utils/mixins';
import GlanceContainer from '@/containers/GlanceContainer';

export default {
  components: { GlanceContainer },
  mixins: [fetchingRoute],
};
</script>
