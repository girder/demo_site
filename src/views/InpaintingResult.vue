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
        v-slider.mx-4(:min="0", :max="1", :step="0.01", v-model="imageVisibility",
            prepend-icon="brightness_6", inverse-label)
        v-slider.mx-4(:min="0", :max="1", :step="0.01", v-model="maskOpacity",
            prepend-icon="opacity")
      v-card.my-4
        v-card-media
          .img-wrapper
            img.result-img(v-if="job.inpaintingImageResultId",
                :src="downloadUrl(job.inpaintingImageResultId)")
            .result-placeholder(v-else)
              v-layout(align-center, justify-center, fill-height,column)
                v-progress-circular(v-if="jobPending", :indeterminate="progressPercent < 0",
                    :size="50", :color="waitColor", :width="6", :value="progressPercent",
                    :rotate="-90")
                v-icon(:size="54", v-if="job.status === JobStatus.ERROR", color="error") error
                .subtitle.mt-4 {{ statusText }}
                v-btn.mt-3(v-if="job.status === JobStatus.ERROR", @click="showLog = !showLog")
                  | {{ showLog ? 'Hide log' : 'Show log' }}
        v-slide-y-transition
          code.log-container.px-2(v-if="showLog")
            pre {{ job.log && job.log.join('') }}
        v-card-title.title
          | Result
          v-spacer
          v-btn(v-if="!jobPending", icon, flat, large, color="primary", :to="rerunLink")
            v-icon repeat
          v-btn(v-if="job.inpaintingImageResultId", icon, flat, large, color="primary",
              :href="downloadUrl(job.inpaintingImageResultId)")
            v-icon save_alt
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
    showLog: false,
  }),
  computed: {
    rerunLink() {
      const { inpaintingImageId, inpaintingMaskId } = this.job;
      return `/inpainting?image=${inpaintingImageId}&mask=${inpaintingMaskId}`;
    },
    statusText() {
      switch (this.job.status) {
        case JobStatus.INACTIVE:
        case JobStatus.QUEUED:
          return 'Your image is waiting in the job queue.';
        case JobStatus.RUNNING:
          if (this.job.progress && this.job.progress.message) {
            return this.job.progress.message;
          }
          return 'Your image is being processed, please wait...';
        case JobStatus.ERROR:
          return 'An error occurred while processing your image.';
        case JobStatus.SUCCESS:
          return 'Job succeeded';
        default:
          return 'Unknown job status';
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
      return ![JobStatus.ERROR, JobStatus.SUCCESS, JobStatus.CANCELED].includes(this.job.status);
    },
    progressPercent() {
      if (!this.job.progress) {
        return -1;
      }
      const { current, total } = this.job.progress;
      return Math.round((100 * current) / total);
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
$maxWidth = 800px

.bg-grey
  background-color #eee

.img-wrapper
  display block

.input-img,.result-image
  max-width $maxWidth
  vertical-align middle

.result-placeholder
  width $maxWidth
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

.log-container
  border-radius 0
  box-shadow none
  overflow scroll
  max-height 300px
  width $maxWidth
  max-width 100vw
</style>
