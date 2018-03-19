<template lang="pug">
v-app
  v-content
    v-container(fluid, fill-height)
      v-layout(align-center, justify-center, column)
        v-flex(xs8)
          img.kw-logo(src="@/assets/KWLogo.svg")
        v-flex
          auth-container.auth-container.mt-5
        v-flex(xs12)
</template>

<script>
import { mapMutations } from 'vuex';
import AuthContainer from '@/containers/AuthContainer';

export default {
  components: { AuthContainer },
  mounted() {
    this.setAuthDialogMode('login');
  },
  methods: mapMutations('auth', ['setAuthDialogMode']),
};
</script>

<style lang="stylus" scoped>
.auth-container
  width 420px
  max-width 80vw

.kw-logo
  width 640px
  max-width 100%
</style>
