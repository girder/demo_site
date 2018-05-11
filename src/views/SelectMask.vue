<template lang="pug">
v-app
  v-layout(align-center, justify-center, column)
    v-alert(:value="true", color="info").
      Please draw a box around the subject of your image that is changing over time. Click two
      points in the image below to choose the box.
    .image-container(:style="containerStyle")
      img(:src="imageUrl", @load="onImageLoad", :style="containerStyle")
      canvas(@click="onCanvasClick", :width="containerWidth", :height="containerHeight")
    v-btn(color="success", large, :disabled="!startEnabled", @click="$emit('start', { imageRect })")
      v-icon.mr-2 play_arrow
      | Start processing
</template>

<script>
export default {
  props: {
    imageUrl: {
      type: String,
      required: true,
    },
  },
  data: () => ({
    imageWidth: 0,
    imageHeight: 0,
    drawState: [],
  }),
  computed: {
    imageAr() {
      return this.imageWidth / this.imageHeight;
    },
    imageRect() {
      return this.drawState.map(([x, y]) => [
        Math.round((this.imageWidth * x) / this.containerWidth),
        Math.round((this.imageHeight * y) / this.containerHeight),
      ]);
    },
    containerWidth() {
      return Math.min(640, this.imageWidth, window.innerWidth);
    },
    containerHeight() {
      return this.containerWidth / this.imageAr;
    },
    containerStyle() {
      return {
        height: `${this.containerHeight}px`,
        width: `${this.containerWidth}px`,
      };
    },
    startEnabled() {
      return this.drawState.length === 2;
    },
  },
  methods: {
    onImageLoad({ target }) {
      this.imageHeight = target.naturalHeight;
      this.imageWidth = target.naturalWidth;
    },
    onCanvasClick({ layerX, layerY, target }) {
      const ctx = target.getContext('2d');
      ctx.clearRect(0, 0, target.width, target.height);

      this.drawState.push([layerX, layerY]);

      if (this.drawState.length > 2) {
        this.drawState = this.drawState.slice(-1);
      }

      if (this.drawState.length === 2) {
        const [p1, p2] = this.drawState;
        ctx.fillStyle = '#f008';
        ctx.fillRect(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1]);
      } else {
        this.drawState = this.drawState.slice(-1);
        const [point] = this.drawState;
        ctx.fillStyle = 'red';
        ctx.fillRect(point[0] - 4, point[1] - 4, 8, 8);
      }
    },
  },
};
</script>

<style lang="stylus" scoped>
.image-container
  position relative

  canvas
    position absolute
    left 0
    top 0
    z-index 1000
</style>
