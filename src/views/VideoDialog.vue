<template lang="pug">
v-dialog(v-model="dialog",
    content-class="demo-video-dialog"
    :width="iframeWidth")
  template(slot="activator")
    slot(name="activator")
  v-card.video-dialog(color="black", v-resize="resize")
    iframe.responsive(
        v-if="dialog"
        :src="src",
        :width="iframeWidth",
        :height="iframeHeight",
        frameborder="0",
        webkitallowfullscreen,
        mozallowfullscreen,
        allowfullscreen)
</template>

<script>

export default {
  props: {
    src: {
      type: String,
      required: true,
    },
    width: {
      type: Number,
      required: true,
    },
    height: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      dialog: false,
      iframeWidth: this.width,
      iframeHeight: this.height,
    };
  },
  methods: {
    resize() {
      const docWidth = document.documentElement.clientWidth;
      const docHeight = document.documentElement.clientHeight;
      const aspect = this.width / this.height;

      if ((docWidth / this.width) < (docHeight / this.height)) {
        this.iframeWidth = ((docWidth > this.width) ? this.width : docWidth);
        this.iframeHeight = this.iframeWidth / aspect;
      } else {
        this.iframeHeight = ((docHeight > this.height) ? this.height : docHeight);
        this.iframeWidth = this.iframeHeight * aspect;
      }
    },
  },
};
</script>

<style lang="stylus">
.demo-video-dialog.v-dialog
    margin 0px
    &:not(.v-dialog--fullscreen)
      max-height inherit
</style>
