<template lang="pug">
v-app
  v-content
    .image-wrapper(v-if="file")
      v-toolbar(app)
        .body-1.mx-3 Click and drag to mark areas of the image to fill.
        v-spacer
        v-btn(@click="run", color="primary")
          v-icon.mr-2 play_arrow
          | Run
        v-tooltip(bottom)
          v-btn(icon, slot="activator", @click="resetCanvas")
            v-icon delete_forever
          | Reset selection
        v-tooltip(bottom)
          v-btn(icon, slot="activator", @click="file = null")
            v-icon arrow_back
          | Choose new file
      canvas(ref="canvas", :height="imageHeight", :width="imageWidth", @mousedown="canvasDown",
          @mousemove="canvasMove", @mouseup="canvasUp")
      img(ref="image", @load="imageLoaded", @error="imageLoadError")

    .dropzone-wrapper(
        v-else, :class="dropzoneClass", @dragenter="dropzoneClass = 'animate'",
        @dragleave="dropzoneClass = null", @drop="dropzoneClass = null")
      .dropzone-message
        v-icon(size="50px") add_a_photo
        .title.mt-3 Drag an image here or click to select one
      input.file-input(type="file", @change="fileSelected")
</template>

<script>
import { mapActions } from 'vuex';

export default {
  props: {
    errorMessage: {
      default: null,
      type: String,
    },
  },
  data: () => ({
    file: null,
    dragover: false,
    dropzoneClass: null,
    imageHeight: 0,
    imageWidth: 0,
    dragging: false,
    drawSize: 20,
  }),
  watch: {
    file(val) {
      if (val) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.$refs.image.src = e.target.result;
        };
        reader.readAsDataURL(val);
      }
    },
  },
  methods: {
    canvasDown({ offsetX, offsetY }) {
      this.dragging = true;
      this.erase(offsetX, offsetY);
    },
    canvasMove({ offsetX, offsetY }) {
      if (this.dragging) {
        this.erase(offsetX, offsetY);
      }
    },
    canvasUp() {
      this.dragging = false;
    },
    erase(x, y) {
      const ctx = this.$refs.canvas.getContext('2d');
      ctx.fillStyle = '#fff';
      ctx.fillRect(x, y, this.drawSize, this.drawSize);
    },
    fileSelected({ target }) {
      this.file = target.files.length ? target.files[0] : null;
    },
    imageLoadError() {
      this.showToast({
        text: `Error: couldn't read ${this.file.name}. Is it an image file?`,
        icon: 'error',
        color: 'error',
        ms: 6000,
      });
      this.file = null;
    },
    imageLoaded({ target }) {
      this.imageHeight = target.naturalHeight;
      this.imageWidth = target.naturalWidth;
    },
    resetCanvas() {
      const { width, height } = this.$refs.canvas;
      this.$refs.canvas.getContext('2d').clearRect(0, 0, width, height);
    },
    run() {
      this.$emit('run', {

      });
    },
    ...mapActions('toast', ['showToast']),
  },
};
</script>

<style lang="stylus" scoped>
$stripeColor = #f0f0f3
$img = linear-gradient(
  -45deg, $stripeColor 25%, transparent 25%, transparent 50%, $stripeColor 50%,
  $stripeColor 75%, transparent 75%, transparent)

.dropzone-wrapper
  position relative
  cursor pointer
  min-height 260px
  height 100%
  text-align center
  background-color #f6f6f9
  background-repeat repeat
  background-size 30px 30px

  &:hover
    background-image $img

  &.animate
    animation stripes 2s linear infinite
    background-image $img

  .file-input
    position absolute
    top 0
    right 0
    bottom 0
    left 0
    height 100%
    width 100%
    opacity 0
    z-index 1
    cursor pointer

@keyframes stripes
  from
    background-position 0 0
  to
    background-position 30px 60px

.dropzone-message
  position absolute
  left 50%
  top 50%
  transform translateX(-50%) translateY(-50%)

.image-wrapper
  overflow-x scroll
  position relative

  img
    z-index -1

  canvas
    user-select none
    cursor url(../assets/eraser.svg), crosshair
    position absolute
</style>
