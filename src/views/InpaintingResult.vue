<template lang="pug">
v-app
  v-content.bg-grey
    v-layout.my-4(column, align-center)
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
      v-card.my-4
        v-card-media
          .img-wrapper
            img.result-img(v-if="job.inpaintingImageResultId",
                :src="downloadUrl(job.inpaintingImageResultId)")
            .result-placeholder(v-else)
              v-layout(align-center, justify-center, fill-height,column)
                v-progress-circular(v-if="jobPending", indeterminate, :size="50",
                    :color="waitColor", :width="6")
                v-icon(:size="50", v-if="job.status === JobStatus.ERROR", color="error") error
                .subtitle.mt-4 {{ statusText }}
        v-card-title.title Result
</template>

<script>
import { JobStatus } from '@/constants';
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
    JobStatus,
  }),
  computed: {
    statusText() {
      switch (this.job.status) {
        case JobStatus.INACTIVE:
        case JobStatus.QUEUED:
          return 'Your image is waiting in the job queue.';
        case JobStatus.RUNNING:
          return 'Your image is being processed, please wait...';
        case JobStatus.ERROR:
          return 'An error occurred while processing your image.';
        default:
          return 'Unkown job status';
      }
    },
    waitColor() {
      switch (this.job.status) {
        case JobStatus.INACTIVE:
        case JobStatus.QUEUED:
          return 'grey';
        case JobStatus.RUNNING:
          return 'primary';
        default:
          return 'default';
      }
    },
    jobPending() {
      return ![JobStatus.ERROR, JobStatus.SUCCESS].includes(this.job.status);
    },
  },
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

.input-img,.result-image
  max-width 800px
  vertical-align middle

.result-placeholder
  width 800px
  max-width 100vw
  height 300px
  background-color #ddd

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
