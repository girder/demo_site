<template lang="pug">
v-app
  v-content
    v-container(fluid, fill-height)
      v-layout(align-center, justify-center, column)
        v-flex(xs8)
          img.kw-logo(src="@/assets/KWLogo.svg")
        v-flex(xs12, sm8)
          .my-4.display-2 Algorithm services:
          ul.display-1
           li.ml-5.my-3 #[router-link(to="/stroke_login") Stroke Assessment]
           li.ml-5.my-3 #[router-link(to="/ct_terms") CT Visualization]
        v-flex(xs12, md8)
          .headline.
            Kitware is a leader in scientific software research, development, and consulting for
            medical, computer vision, high-performance computing, informatics, and numerous other
            domains. #[router-link(to="learn") Learn more...]
</template>

<style lang="stylus" scoped>
.kw-logo
  width 640px
  max-width 100%
</style>
