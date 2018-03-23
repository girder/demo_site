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
          v-text-field.pl-3(placeholder="Search...", prepend-icon="search", v-model="search")
          v-layout(row)
            v-flex.pl-3(xs6)
              v-menu(lazy, :close-on-content-click="false", v-model="startDateMenu", offset-y,
                  full-width, min-width="290px", :return-value.sync="startDate", :nudge-right="40",
                  ref="startDateMenuRef", transition="scale-transition")
                v-text-field(label="Start date", prepend-icon="date_range", slot="activator",
                    v-model="startDate")
                v-date-picker(v-model="startDate", @change="$refs.startDateMenuRef.save(startDate)",
                    :max="endDate", no-title)
            v-flex.pl-3(xs6)
              v-menu(lazy, :close-on-content-click="false", v-model="endDateMenu", offset-y,
                  full-width, min-width="290px", :return-value.sync="endDate", :nudge-right="40",
                  ref="endDateMenuRef", transition="scale-transition")
                v-text-field(label="End date", prepend-icon="date_range", slot="activator",
                    v-model="endDate")
                v-date-picker(v-model="endDate", @change="$refs.endDateMenuRef.save(endDate)",
                    :min="startDate", no-title)
        v-flex(xs5)
    v-flex(xs12)
      v-data-table(no-data-text="No studies found.", no-results-text="No matching studies.",
          :items="studies", :headers="headers", :loading="loading", :search="search",
          :custom-filter="customFilter", :filter="filter", :rows-per-page-items="rowsPerPageItems",
          rows-per-page-text="Studies per page:")
        template(slot="items", slot-scope="props")
          tr.study-row(@click="$emit('selectStudy', props.item)")
            td {{ props.item.studyId }}
            td
              v-tooltip(bottom)
                span(slot="activator" ) {{ dateformat(props.item.studyDate, 'mmm d, yyyy') }}
                span {{ props.item.studyDate }}
            td {{ props.item.studyModality }}
            td {{ props.item.description }}
            td {{ props.item.nSeries }}
            td.text-xs-right
              v-btn(icon, color="primary", flat)
                v-icon visibility
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
    }, {
      text: 'Actions',
      sortable: false,
      align: 'right',
    }],
    rowsPerPageItems: [10, 25, 50, { text: 'All', value: -1 }],
    startDate: null,
    endDate: null,
    startDateMenu: false,
    endDateMenu: false,
    search: '',
  }),
  methods: {
    dateformat,
    customFilter(items, search, filter) {
      search = search.toString().toLowerCase().trim();
      const start = this.startDate && new Date(this.startDate);
      const end = this.endDate && new Date(this.endDate);
      return items.filter(i => filter(i, search, start, end));
    },
    filter(item, search, start, end) {
      if (start || end) {
        const date = new Date(item.studyDate);
        if (start && date < start) {
          return false;
        }
        if (end && date > end) {
          return false;
        }
      }

      if (search) {
        return item.studyId.toLowerCase().includes(search) ||
          item.studyModality.toLowerCase().includes(search) ||
          item.description.toLowerCase().includes(search);
      }
      return true;
    },
  },
};
</script>

<style lang="stylus" scoped>
.kw-logo
  height 36px

.study-row
  cursor pointer
</style>
