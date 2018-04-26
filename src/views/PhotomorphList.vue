<template lang="pug">
v-app(dark)
  v-toolbar(app)
    v-toolbar-title
      img.kw-logo(src="@/assets/KWLogo.svg")
    v-spacer
    .headline Timelapse photo morph
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

    // Folder list
    v-flex(xs12, md10, offset-md1)
      v-data-table(no-data-text="No videos found.", no-results-text="No matching videos.",
          :items="folders", :headers="headers", :loading="loading", :search="search",
          :custom-filter="customFilter", :filter="filter", :rows-per-page-items="rowsPerPageItems",
          rows-per-page-text="Videos per page:")
        template(slot="items", slot-scope="props")
          tr.photomorph-row(@click="$emit('select', props.item)",
              :active="selectedFolder && selectedFolder._id === props.item._id")
            td {{ props.item.name }}
            td
              v-tooltip(bottom)
                span(slot="activator" ) {{ dateformat(props.item.created, 'mmm d, yyyy') }}
                span {{ props.item.created }}
            td.text-xs-right
              a.mx-2(:href="videoUrl(fileId)", style="color: white;",
                  v-for="fileId, type in props.item.photomorphOutputItems") {{ type }}

    // Details view
    v-flex.mt-3(xs12, md10, offset-md1 v-if="selectedFolder")
      v-card
        v-card-title
          h3.headline {{ selectedFolder.name }}
        v-layout.py-3(justify-center, align-center, v-if="loadingChildren")
          v-progress-circular(indeterminate, color="primary")
        hr
        .headline.px-2.mt-2 Results
        .result-item-container(v-for="fileId, type in selectedFolder.photomorphOutputItems")
          video(v-if="type === 'mp4'", :src="videoUrl(fileId)", controls, loop)
          img(v-if="type === 'gif'", :src="videoUrl(fileId)")

        .headline.px-2.mt-2 Input images
        .input-item-container.px-2.py-2(v-for="item in inputItems", :key="item._id")
          v-layout(row, align-center)
            div #[img(:src="thumbUrl(item)")]
            v-layout.ml-3(column)
              .title {{ item.originalName }}
              .body-2
                span {{ formatDataSize(item.size) }}
                span(v-if="item.photomorphTakenDate")  - photo date {{ item.photomorphTakenDate }}
</template>

<script>
import { getApiUrl } from '@/rest';
import dateformat from 'dateformat';
import { sizeFormatter } from '@/utils/mixins';


export default {
  mixins: [sizeFormatter],
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
    loadingChildren: {
      type: Boolean,
      default: false,
    },
    selectedFolder: {
      type: Object,
      default: null,
    },
    inputItems: {
      type: Array,
      required: true,
    },
    folders: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    headers: [{
      text: 'Name',
      value: 'name',
    }, {
      text: 'Date uploaded',
      value: 'created',
    }, {
      text: 'Results',
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
        const date = new Date(item.created);
        if (start && date < start) {
          return false;
        }
        if (end && date > end) {
          return false;
        }
      }

      if (search) {
        return item.name.toLowerCase().includes(search);
      }
      return true;
    },
    thumbUrl(item) {
      return `${getApiUrl()}/file/${item._thumbnails[0]}/download`;
    },
    videoUrl(fileId) {
      return `${getApiUrl()}/file/${fileId}/download`;
    },
  },
};
</script>

<style lang="stylus" scoped>
.kw-logo
  height 36px

.photomorph-row
  cursor pointer
</style>
