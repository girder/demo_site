<template lang="pug">
v-app(light)
  v-toolbar(app)
    v-toolbar-title
      img.kw-logo(src="@/assets/KWLogo.svg")
    v-spacer
    .headline Timelapse generation
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

        // Upload button and refresh button
        v-flex.text-xs-right(xs12, md6)
          v-layout(column)
            v-flex
              v-btn.my-4(large, color="success", to="upload")
                v-icon.mr-2 file_upload
                | Upload
            v-tooltip(bottom)
              v-btn(icon, slot="activator", @click="$emit('refreshList')")
                v-icon replay
              | Refresh list

    // Folder list
    v-flex(xs12, md10, offset-md1)
      v-data-table(no-data-text="No timelapses found.", no-results-text="No matching timelapses.",
          :items="folders", :headers="headers", :loading="loading", :search="search",
          :custom-filter="customFilter", :filter="filter", :rows-per-page-items="rowsPerPageItems",
          rows-per-page-text="Results per page:", :pagination.sync="pagination")
        template(slot="items", slot-scope="props")
          tr.photomorph-row(@click="$emit('select', props.item)",
              :active="selectedFolder && selectedFolder._id === props.item._id")
            td {{ props.item.name }}
            td
              v-tooltip(bottom)
                span(slot="activator" ) {{ dateformat(props.item.created, 'mmm d, yyyy') }}
                span {{ props.item.created }}
            td.text-xs-right
              v-icon(:class="jobStatusClass(props.item.photomorphJobStatus)",
                  :color="jobStatusColor(props.item.photomorphJobStatus)")
                | {{ jobStatusIcon(props.item.photomorphJobStatus) }}

    // Details view
    v-flex.mt-3(xs12, md10, offset-md1 v-if="selectedFolder")
      v-card
        v-card-title
          v-text-field(v-model="selectedFolder.name", v-if="editingName", append-icon="save",
                autofocus, :append-icon-cb="saveFolderName")
          h3.headline(v-else)
            span {{ selectedFolder.name }}
            v-btn(icon, @click="editingName = true", v-if="!editingName")
              v-icon edit
            v-btn(icon, @click="deleteFolder", v-if="!editingName")
              v-icon delete

        v-layout.py-3(justify-center, align-center, v-if="loadingChildren")
          v-progress-circular(indeterminate, color="primary")
        hr
        .headline.px-2.mt-2
          | Results
          v-tooltip(right, v-if="inputItems.length")
            v-btn(icon, slot="activator",
    :to="`/select_mask/${selectedFolder.photomorphInputFolderId}/item/${inputItems[0]._id}`")
              v-icon play_circle_outline
            span Re-run processing
        .result-item-container(v-for="item in outputItems")
          .body-2.mt-3 {{ item.name }}
          img(v-if="item.type === 'gif'", :src="videoUrl(item.fileId)")
          video(v-else, :src="videoUrl(item.fileId)", controls, loop)

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
import _ from 'lodash';
import { getApiUrl } from '@/rest';
import dateformat from 'dateformat';
import confirm from '@/utils/confirm';
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
      text: 'Status',
      sortable: false,
      align: 'right',
    }],
    editingName: false,
    rowsPerPageItems: [10, 25, 50, { text: 'All', value: -1 }],
    startDate: null,
    endDate: null,
    startDateMenu: false,
    endDateMenu: false,
    search: '',
    pagination: {
      sortBy: 'created',
      descending: true,
      rowsPerPage: -1,
    },
  }),
  computed: {
    outputItems() {
      const vals = _.mapValues(this.selectedFolder.photomorphOutputItems, (items, type) =>
        items.map(v => ({
          ...v,
          type,
        })));
      return _.flatten(_.toArray(vals));
    },
  },
  watch: {
    selectedFolder() {
      this.editingName = false;
    },
  },
  methods: {
    jobStatusClass(status) {
      if (Number(status) === 2) {
        return 'rotate';
      }
      return '';
    },
    jobStatusColor(status) {
      switch (Number(status)) {
        case 0:
        case 1:
          return 'warning';
        case 2:
          return 'primary';
        case 3:
          return 'success';
        case 4:
          return 'error';
        default:
          return 'warning';
      }
    },
    jobStatusIcon(status) {
      switch (Number(status)) {
        case 0:
        case 1:
          return 'hourglass_empty';
        case 2:
          return 'cached';
        case 3:
          return 'done';
        case 4:
          return 'error';
        default:
          return 'report_problem';
      }
    },
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
      return `${getApiUrl()}/file/${fileId}/download?contentDisposition=inline`;
    },
    saveFolderName() {
      this.editingName = false;
      this.$emit('saveFolder', {
        fields: {
          name: this.selectedFolder.name,
        },
        folder: this.selectedFolder,
      });
    },
    async deleteFolder() {
      const ok = await confirm({
        markdown: 'Are you sure you want to delete all data for your timelapse series ' +
        `**${this.selectedFolder.name}**?`,
      });
      if (ok) {
        this.$emit('deleteFolder', this.selectedFolder);
      }
    },
  },
};
</script>

<style lang="stylus" scoped>
.kw-logo
  height 36px

.photomorph-row
  cursor pointer

.rotate
  animation rotate 1.5s linear infinite

@keyframes rotate
  from
    transform rotate(360deg)
  to
    transform rotate(0deg)
</style>
