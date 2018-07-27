<template lang="pug">
v-app
  v-content.bg-grey
    v-layout(column, align-center)
      v-card.my-4
        v-card-media
          .img-wrapper
            img.input-img(:src="downloadUrl(job.inpaintingImageId)")
            img.mask-img(:src="downloadUrl(job.inpaintingMaskId)", :style="{opacity: maskOpacity}")
            .fader(:style="{opacity: 1 - imageVisibility}")
        v-card-title.title Image & Mask
        v-slider.mx-3(:min="0", :max="1", :step="0.01", v-model="imageVisibility",
            prepend-icon="brightness_6", inverse-label)
        v-slider.mx-3(:min="0", :max="1", :step="0.01", v-model="maskOpacity",
            prepend-icon="opacity")

</template>

<script>
import { getApiUrl } from '@/rest';

export default {
  props: {
    job: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    imageVisibility: 1,
    maskOpacity: 1,
  }),
  methods: {
    downloadUrl(id) {
      return `${getApiUrl()}/file/${id}/download`;
    },
  },
};
</script>

<style lang="stylus" scoped>
.bg-grey
  background-color #eee

.img-wrapper
  display block

.input-img
  max-width 800px
  vertical-align middle

.mask-img
  position absolute
  top 0
  left 0
  z-index 2

.fader
  position absolute
  z-index 1
  top 0
  bottom 0
  left 0
  right 0
  background-color black
</style>
