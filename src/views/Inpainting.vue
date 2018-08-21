<template lang="pug">
v-app
  v-content
    .image-wrapper(v-if="file || imageId")
      v-toolbar(app)
        v-spacer
        v-btn(@click="run", color="primary", :disabled="!enableRun", :loading="!enableRun")
          v-icon.mr-2 play_arrow
          | Run
        v-tooltip(bottom)
          v-btn(icon, slot="activator", @click="resetCanvas")
            v-icon delete_forever
          | Reset selection
        v-tooltip(bottom)
          v-btn(icon, slot="activator", @click="cancelImage")
            v-icon arrow_back
          | Choose new file
      canvas(ref="canvas", :height="imageHeight", :width="imageWidth", @mousedown="canvasDown",
          @mousemove="canvasMove", @mouseup="canvasUp")
      img(@load="imageLoaded", @error="imageLoadError", :src="imageSrc")
      v-snackbar(bottom, v-model="snackbar", :timeout="10000")
        | Drag to select areas of the image to fill.
        v-btn(dark, flat, color="primary", @click="snackbar = false") Got it

    .dropzone-wrapper(
        v-else, :class="dropzoneClass", @dragenter="dropzoneClass = 'animate'",
        @dragleave="dropzoneClass = null", @drop="dropzoneClass = null")
      .dropzone-message
        v-icon(size="50px") add_a_photo
        .title.mt-3 Drag an image here or click to select one
      input.file-input(type="file", @change="fileSelected")

    v-dialog(persistent, :value="uploading", max-width="600")
      v-card
        v-card-title.headline Uploading files
        v-card-text
          div(v-if="file")
            .subtitle.mb-4 {{ file.name }} ({{ imageSize }})
            v-progress-linear(:value="imageProgress")
          .subtitle Mask file
          v-progress-linear(:value="maskProgress")
</template>

<script>
import Vue from 'vue';
import { mapActions } from 'vuex';
import rest, { getApiUrl } from '@/rest';
import { sizeFormatter } from '@/utils/mixins';

export default {
  mixins: [sizeFormatter],
  props: {
    imageProgress: {
      type: Number,
      default: 0,
    },
    maskProgress: {
      type: Number,
      default: 0,
    },
    uploading: {
      type: Boolean,
      default: false,
    },
    imageId: {
      type: String,
      default: null,
    },
    maskId: {
      type: String,
      default: null,
    },
  },
  data: () => ({
    file: null,
    dataUrl: null,
    dragging: false,
    drawSize: 20,
    dropzoneClass: null,
    enableRun: true,
    imageHeight: 0,
    imageWidth: 0,
    snackbar: true,
  }),
  computed: {
    imageSize() {
      return this.file && this.formatDataSize(this.file.size);
    },
    imageSrc() {
      if (this.imageId) {
        return `${getApiUrl()}/file/${this.imageId}/download`;
      }
      return this.dataUrl;
    },
  },
  watch: {
    file(val) {
      if (val) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.dataUrl = e.target.result;
        };
        reader.readAsDataURL(val);
      }
    },
  },
  mounted() {
    if (this.maskId) {
      // We have to use an XHR (rather than just fetching the mask via an image src)
      // to support files served via CORS (e.g. S3 or webpack dev server). Otherwise
      // we cannot call getBlob on the resulting canvas for security reasons.
      rest.get(`file/${this.maskId}/download`, {
        responseType: 'arraybuffer',
      }).then(({ data }) => {
        const img = new Image();
        const reader = new FileReader();
        reader.onload = (e) => {
          img.onload = () => {
            this.imageWidth = img.width;
            this.imageHeight = img.height;
            Vue.nextTick(() => {
              this.$refs.canvas.getContext('2d').drawImage(img, 0, 0);
            });
          };
          img.src = e.target.result;
        };
        reader.readAsDataURL(new Blob([data]));
      });
    }
  },
  methods: {
    cancelImage() {
      this.file = null;
      this.$emit('cancelImage');
    },
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
      this.enableRun = false;
      this.$refs.canvas.toBlob((blob) => {
        blob.name = 'mask.png';

        this.$emit('run', {
          mask: blob,
          image: this.file,
        });
      }, 'image/png');
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
  text-align center

  img
    z-index -1

  canvas
    user-select none
    cursor url(../assets/eraser.svg), crosshair
    position absolute
</style>
