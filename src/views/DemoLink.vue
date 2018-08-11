<template lang="pug">
v-card.flexcard(width="400px")
  v-card-title.py-2.px-3(primary-title)
    h3.headline {{ title }}
  v-card-media.grey-bg(:src="imageUrl", height="180px")
  v-card-text.grow.body-1.py-2.px-3 {{ description }}
  v-card-actions
    v-spacer
    v-btn.mr-1(v-if="enabled", color="primary", :to="to", :href="href",
        :target="href ? '_blank' : null", flat) {{ buttonText }}
    v-btn(v-else, disabled, flat) Coming soon
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

.flexcard
  display flex
  flex-direction column
</style>
