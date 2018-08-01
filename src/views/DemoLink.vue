<template lang="pug">
v-card(width="400px")
  v-card-title.py-2.px-3(primary-title)
    h3.headline
      | {{ title }}
      span.body-2.ml-1.coming-soon(v-if="!enabled") (coming soon)
  v-card-media.grey-bg(:src="imageUrl", height="180px")
  .body-1.py-2.px-3 {{ description }}
  v-card-actions(v-if="enabled")
    v-spacer
    v-btn.mr-1(color="primary", :to="to", :href="href", :target="href ? '_blank' : null")
      .mr-3 {{ buttonText }}
      v-icon {{ buttonIcon }}
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
    imageUrl: {
      type: String,
      required: true,
    },
    to: {
      type: String,
      default: null,
    },
    href: {
      type: String,
      default: null,
    },
    buttonText: {
      type: String,
      default: null,
    },
    buttonIcon: {
      type: String,
      default: null,
    },
    enabled: {
      type: Boolean,
      default: true,
    },
  },
};
</script>

<style lang="stylus" scoped>
.grey-bg
  background-color #d5d5d5

.coming-soon
  color #999
  vertical-align top
</style>
