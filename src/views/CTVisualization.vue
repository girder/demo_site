<template lang="pug">
v-app
  v-content
    v-container(fluid, fill-height)
      v-layout(align-center, justify-center, column)
        v-flex(xs8)
          img.kw-logo(src="@/assets/KWLogo.svg")
        v-flex(xs12, sm8, md6)
          .my-4.display-2.text-xs-center CT Visualization
          v-card.terms-container.px-3.py-3.subheading(raised).
            CT Visualization is provided as a free service. It is provided as-is and without any
            expressed or implied suitability for any purpose. It is not approved for clinical use.
            Kitware assumes no liability and by clicking on the button below you agree to indemnify
            and hold harmless Kitware for any damages occurring from your use of this free service.
            blah blah blah....
          .text-xs-center.mt-3
            v-btn(color="primary", to="/ct", large) Accept Terms and Conditions
        v-flex(xs12)
</template>

<style lang="stylus" scoped>
.kw-logo
  width 640px
  max-width 100%

.terms-container
  max-height 300px
  overflow-y scroll
</style>
