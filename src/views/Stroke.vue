<template lang="pug">
v-app
  v-toolbar(app)
    v-toolbar-title
      img.kw-logo(src="@/assets/KWLogo.svg")
    v-spacer
    .headline Stroke Assessment Algorithm
  v-content
    v-flex(xs12)
      v-layout(row)
        v-flex.mt-3(xs6)
          v-text-field.pl-3(placeholder="Search...", prepend-icon="search")
          v-layout(row)
            v-flex.pl-3(xs6)
              v-menu(lazy, :close-on-content-click="false", v-model="startDateMenu", offset-y,
                  full-width, min-width="290px", :return-value.sync="startDate", :nudge-right="40",
                  ref="startDateMenuRef", transition="scale-transition")
                v-text-field(label="Start date", prepend-icon="date_range", slot="activator",
                    v-model="startDate")
                v-date-picker(v-model="startDate", @change="$refs.startDateMenuRef.save(startDate)",
                    :max="endDate")
            v-flex.pl-3(xs6)
              v-menu(lazy, :close-on-content-click="false", v-model="endDateMenu", offset-y,
                  full-width, min-width="290px", :return-value.sync="endDate", :nudge-right="40",
                  ref="endDateMenuRef", transition="scale-transition")
                v-text-field(label="End date", prepend-icon="date_range", slot="activator",
                    v-model="endDate")
                v-date-picker(v-model="endDate", @change="$refs.endDateMenuRef.save(endDate)",
                    :min="startDate")
        v-flex(xs5)
    v-flex(xs12)
     v-data-table(no-data-text="No studies found.", no-results-text="No matching studies.",
         :items="studies", :headers="headers", :loading="loading",
         :rows-per-page-items="rowsPerPageItems", rows-per-page-text="Studies per page:")
      template(slot="items", slot-scope="props")
        td {{ props.item.studyId }}
        td
          v-tooltip(bottom)
            span(slot="activator" ) {{ dateformat(props.item.studyDate, 'mmm d, yyyy') }}
            span {{ props.item.studyDate }}
        td {{ props.item.studyModality }}
        td {{ props.item.description }}
        td {{ props.item.nSeries }}
</template>

<script>
import dateformat from 'dateformat';

export default {
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
    studies: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    headers: [{
      text: 'Identifier',
      value: 'studyId',
    }, {
      text: 'Study Date',
      value: 'studyDate',
    }, {
      text: 'Modality',
      value: 'studyModality',
    }, {
      text: 'Study Description',
      value: 'description',
    }, {
      text: 'Series',
      value: 'nSeries',
    }],
    rowsPerPageItems: [10, 25, 50, { text: 'All', value: -1 }],
    startDate: null,
    endDate: null,
    startDateMenu: false,
    endDateMenu: false,
  }),
  methods: {
    dateformat,
  },
};
</script>

<style lang="stylus" scoped>
.kw-logo
  height 36px
</style>
