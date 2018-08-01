<template lang="pug">
v-app
  v-content
    v-toolbar(height="100px")
      v-toolbar-title
        img.kw-logo(src="@/assets/kw_AaaS.svg")

    .kw-info-ctr.py-5
      .text-xs-center.headline.banner-headline.
        #[b Kitware] is a leader in scientific software research, development, and consulting for
        medical, computer vision, high-performance computing, informatics, and numerous other
        domains.
      .text-xs-center.mt-2
        v-btn.mt-3(outline, large, color="white", href="https://www.kitware.com") Learn more

    .banner-ctr
      .banner-bg(:style="{'background-image': `url(${require('@/assets/CV_Band.jpg')})`}")
      .title-ctr Computer Vision

    v-layout.demos-list(row, justify-center, wrap)
      demo-link.mx-4.mb-2(v-for="(demo, i) in demos.vision", :key="i", v-bind="demo")

    .banner-ctr
      .banner-bg(:style="{'background-image': `url(${require('@/assets/Med_Band.jpg')})`}")
      .title-ctr Medical Visualization

    v-layout.demos-list(row, justify-center, wrap)
      demo-link.mx-4.mb-2(v-for="(demo, i) in demos.medical", :key="i", v-bind="demo")

    hr.mx-5.mb-2(color="#ddd")
    .text-xs-center.mb-4
      .subtitle &copy; Kitware, Inc.
</template>

<script>
import demos from '@/utils/demos';
import DemoLink from './DemoLink';

export default {
  components: { DemoLink },
  data: () => ({
    demos,
  }),
};
</script>

<style lang="stylus" scoped>
.kw-logo
  height 140px

.kw-info-ctr
  padding-left 25px
  padding-right 25px
  background-color #313c42
  color white

.banner-headline
  max-width 980px
  margin 0 auto

.banner-ctr
  width 100%
  height 265px
  position relative

  >.banner-bg
    height 265px
    width 100%
    filter brightness(50%)
    z-index 1
    position absolute
    background-repeat repeat-x

  >.title-ctr
    color white
    font-size 50px
    filter none
    z-index 2
    position absolute
    line-height 265px
    left 4%
    max-width 100%
    overflow hidden
    white-space nowrap
    text-overflow ellipsis

.demos-list
  margin -30px 0 50px
  z-index 2
  position relative
</style>
