<template lang="pug">
v-app
  v-content
    v-container(fluid, fill-height)
      v-layout(align-center, justify-center, column)
        v-flex(xs12, sm8)
          .display-4.text-xs-center Kitware
        v-flex(xs12, sm8)
          .my-4.display-2 Algorithm services:
          ul.display-1
           li.ml-5.my-3 #[router-link(to="stroke") Stroke Assessment]
           li.ml-5.my-3 #[router-link(to="ct") CT Visualization]
        v-flex(xs12, md9)
          .headline.my-3.
            Kitware is a leader in scientific software research, development, and consulting for
            medical, computer vision, high-performance computing, informatics, and numerous other
            domains. #[router-link(to="learn") Learn more...]
</template>
