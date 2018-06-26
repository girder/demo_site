<template lang="pug">
v-app
  v-content
    v-toolbar(height="100px")
      v-toolbar-title
        img.kw-logo(src="@/assets/kw_AaaS.svg")

    .kw-info-ctr.my-5
      .headline.
        Kitware is a leader in scientific software research, development, and consulting for
        medical, computer vision, high-performance computing, informatics, and numerous other
        domains.
      .text-xs-center.mt-2
        v-btn(outline, large, color="primary", href="https://www.kitware.com") Learn more

    .banner-ctr
      .banner-bg(:style="{'background-image': `url(${require('@/assets/CV_Band.jpg')})`}")
      .title-ctr Computer Vision

    v-list.pa-0.list-ctr
      v-list-tile.py-2(to="/timelapse")
        v-list-tile-content #[v-list-tile-title.alg-title Timelapse Video Creation]
        v-list-tile-action
          v-icon(large) keyboard_arrow_right
      v-divider
      v-list-tile.py-2(disabled)
        v-list-tile-content #[v-list-tile-title.alg-title Photo Hole Filling (coming soon)]
        v-list-tile-action
          v-icon(large) keyboard_arrow_right

    .banner-ctr
      .banner-bg(:style="{'background-image': `url(${require('@/assets/Med_Band.jpg')})`}")
      .title-ctr Medical Imaging

    v-list.mb-4.pa-0.list-ctr
      v-list-tile.py-2(to="/ct_terms")
        v-list-tile-content #[v-list-tile-title.alg-title CT Visualization]
        v-list-tile-action
          v-icon(large) keyboard_arrow_right
      v-divider
      v-list-tile.py-2(disabled)
        v-list-tile-content #[v-list-tile-title.alg-title Stroke Assessment (coming soon)]
        v-list-tile-action
          v-icon(large) keyboard_arrow_right

    hr.mx-5.mb-2(color="#ddd")
    .text-xs-center.mb-4
      .subtitle &copy; Kitware, Inc.
</template>

<style lang="stylus" scoped>
.kw-logo
  height 140px

.kw-info-ctr
  padding-left 5%
  padding-right 5%

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

.list-ctr
  border 1px solid #ddd
  border-radius 3px
  margin-top -44px
  z-index 3
  position relative
  margin-left 5%
  margin-right 5%
  margin-bottom 60px

  .alg-title
    font-size 23px
    color #0d47a1
</style>
