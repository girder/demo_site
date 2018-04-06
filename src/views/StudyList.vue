<template lang="pug">
v-app(dark)
  v-toolbar(app)
    v-toolbar-title
      img.kw-logo(src="@/assets/KWLogo.svg")
    v-spacer
    .headline Stroke Assessment
  v-content
    v-flex(xs12, md10, offset-md1)
      v-layout(row, wrap)
        // Filtering form
        v-flex.mt-3.px-3(xs12, md6)
          v-text-field(placeholder="Search...", prepend-icon="search", v-model="search")
          v-layout(row)
            v-flex(xs6)
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

        // Upload button and login message
        v-flex.text-xs-right(xs12, md6)
          v-btn.my-4(large, color="success", to="upload")
            v-icon.mr-2 file_upload
            | Upload

    // Study list
    v-flex(xs12, md10, offset-md1)
      v-data-table(no-data-text="No studies found.", no-results-text="No matching studies.",
          :items="studies", :headers="headers", :loading="loading", :search="search",
          :custom-filter="customFilter", :filter="filter", :rows-per-page-items="rowsPerPageItems",
          rows-per-page-text="Studies per page:")
        template(slot="items", slot-scope="props")
          tr.study-row(@click="$emit('select', props.item)",
              :active="selectedStudy && selectedStudy._id === props.item._id")
            td {{ props.item.patientId }}
            td
              v-tooltip(bottom)
                span(slot="activator" ) {{ dateformat(props.item.studyDate, 'mmm d, yyyy') }}
                span {{ props.item.studyDate }}
            td {{ props.item.studyModality }}
            td {{ props.item.description }}
            td {{ props.item.nSeries }}
            td.text-xs-right
              v-btn(icon, flat, @click.stop="")
                v-icon visibility

    // Series list
    v-flex.mt-3(xs12, md10, offset-md1 v-if="selectedStudy")
      v-card
        v-card-title
          h3.headline Series for study {{ selectedStudy.studyId }}
        v-layout.py-3(justify-center, align-center, v-if="loadingSeries")
          v-progress-circular(indeterminate, color="primary")
        v-alert.my-0(:value="!loadingSeries && !series.length", color="info")
          v-icon(dark) info
          span.ml-2.body-2 There are no series in this study.

        v-layout.mb-4.pb-4(v-if="series.length", row, wrap, justify-center, align-center)
          v-flex.text-xs-center.mb-4.mx-2(v-for="img in series", :key="img._id")
            series(:series="img")
</template>

<script>
import dateformat from 'dateformat';
import Series from './Series';

export default {
  components: { Series },
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
    loadingSeries: {
      type: Boolean,
      default: false,
    },
    selectedStudy: {
      type: Object,
      default: null,
    },
    series: {
      type: Array,
      required: true,
    },
    studies: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    headers: [{
      text: 'Patient Identifier',
      value: 'patientId',
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
