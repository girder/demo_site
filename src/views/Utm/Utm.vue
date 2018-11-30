<template lang="pug">
v-app
  v-container(fluid)
    v-layout(row wrap justify-space-between)
      v-flex(xs12 column)
        v-card.ma-2
          v-card-title(primary-title)
            div
              h2.display-2 Tumors & Traumatic Brain Injury
              v-subheader.pl-0
                h4.headline Choose one of the options below.
          v-card-text
            v-btn-toggle(v-model="modeToggle", max=20, color="primary", mandatory)
              v-btn(flat)
                v-icon.pa-2 restore_page
                | Demo
              v-btn(flat)
                v-icon.pa-2 folder
                | Choose
              v-btn(flat)
                v-icon.pa-2 cloud_upload
                | Upload
              v-btn(flat)
                v-icon.pa-2 settings
                | Jobs
      v-flex(md5 sm12)
        v-card.ma-2
          v-card-title.pb-0(primary-title)
            div
              h2.display-1 Instructions
              v-subheader.pl-0
                p.subheading(v-if="modeToggle == 0") Launch Demo Session
                p.subheading(v-if="modeToggle == 1") {{ chooseDirectoryInstructions }}
                p.subheading(v-if="modeToggle == 2") {{ uploadDataInstructions }}

          div(v-if="modeToggle == 0")
            v-card-text
              p.subheading {{ launchDemoInstructions }}
            v-card-text
              p.subheading Folder:
                v-chip
                  b {{ demoData.folder.name }}
              p.subheading Param File:
                v-chip
                  b {{ demoData.paramsFile.name }}
            v-card-actions
              v-btn(color="primary" large)
                v-icon.pa-2 launch
                | Launch

          div(v-if="modeToggle !== 0")
            v-card-text
              p.subheading {{ dataRequirements }}
              ul.subheading
                li(v-for="row in variableFileDescription" :key="row") {{ row }}
            v-card-text
              p.subheading Folder:
                v-chip
                  b  {{ runData.folder.name || 'Not Found' }}
              p.subheading Param File:
                v-chip
                  b  {{ runData.paramsFile.name || 'Not Found' }}
            v-card-actions
              v-btn(v-if="modeToggle == 2", color="primary", large, @click="upload")
                v-icon.pa-2 cloud_upload
                | Upload Data
              v-btn(color="primary" large, @click="run", :disabled="!canRun")
                v-icon.pa-2 launch
                | Run job
              v-btn(color="primary", large, v-if="currentJob")
                | Results
      v-flex(md7 sm12)
        v-card.ma-2
          girder-data-browser(
              v-if="modeToggle < 2 && location",
              ref="girderBrowser",
              :location="location",
              @update:location="setLocation($event)",
              :select-enabled="false",
              :multi-select-enabled="false",
              :upload-enabled="modeToggle === 2",
              :new-item-enabled="false",
              :new-folder-enabled="false")
          girder-upload(
              v-else-if="uploadLocation",
              :dest="uploadLocation",
              @done="refresh++;",
              :multiple="true")
</template>

<script>
import { mapState } from 'vuex';
import { formEncode } from '@/rest';
import {
  DataBrowser as GirderDataBrowser,
  Upload as GirderUpload,
} from '@girder/components/src/components';

const launchDemoInstructions = `Using the data displayed, 
you will be launched into an interactive RShiny session.
The outputs have been pre-generated so no processing is
necessary and you can view the results immediately.`;

const chooseDirectoryInstructions = 'Use the browser to find a directory with your input data.';

const uploadDataInstructions = 'Upload your own data for processing.';

const dataRequirements = `Your data should consist of any number of PNG images,
and a single variable file named "variables.csv", which has a row for every PNG.
Its columns are:`;

const variableFileDescription = [
  '"name", the name of the PNG file without the file extension',
  '"ratio", ',
  '"mass", ',
  '"addative", ',
];

export default {
  components: {
    GirderDataBrowser,
    GirderUpload,
  },
  props: {
    demoData: {
      type: Object,
      required: true,
    },
  },
  inject: ['girderRest'],
  data() {
    return {
      uploader: false,
      browserLocation: null,
      uploadLocation: null,
      demoLocation: null,
      modeToggle: 0,
      refresh: 0,
      launchDemoInstructions,
      chooseDirectoryInstructions,
      uploadDataInstructions,
      dataRequirements,
      variableFileDescription,
    };
  },
  computed: {
    ...mapState('auth', ['user']),
    canRun() {
      const { folder, paramsFile } = this.runData;
      return !!folder._id && !!paramsFile._id 
    }
  },
  methods: {
    setLocation(loc) {
      if ([1, 2].indexOf(this.modeToggle) !== -1) {
        this.browserLocation = loc;
      }
    },
    async upload() {
      if (!this.uploader) {
        const { data } = await this.girderRest.post('folder', formEncode({
          parentType: this.location._modelType,
          parentId: this.location._id,
          name: `UTM_${new Date().toISOString()}`,
        }));
        this.uploadLocation = data;
        this.uploader = true;
      }
    },
    async run() {
      const { folder, paramsFile } = this.runData;
      if (!folder._id || !paramsFile._id) {
        console.error('Insufficient data to run.');
      }
      try {
        const { data: files } = await this.girderRest.get(`item/${paramsFile._id}/files`);
        if (files.length === 0 || files.length > 1) {
          console.error(`ParamsFile ${paramsFile.name} should have exactly 1 data file.`);
        }
        const { data: folderCreated } = await this.girderRest.post('folder', formEncode({
          parentId: folder._id,
          name: 'output',
          description: 'Output of UTM run.',
          reuseExisting: true,
        }));
        const { data: resp } = await this.girderRest.post('utm', formEncode({
          folderId: folder._id,
          paramsId: files[0]._id,
          outputFolderId: folderCreated._id,
        })); 
        console.log(resp);
      } catch (err) {
        console.error(err);
      }
    },
  },
  asyncComputed: {
    location: {
      default() { return { _modelType: 'user', _id: this.user._id }; },
      async get() {
        let loc = this.browserLocation || { _modelType: 'user', _id: this.user._id };
        if (this.modeToggle === 0) {
          const { folder } = this.demoData;
          console.log(folder._id);
          loc = { _modelType: 'folder', _id: folder._id };
        }
        return loc;
      },
    },
    jobs: {
      default: [],
      async get() {
        const { data } = this.girderRest.get('job', formEncode({
          userId: this.user._id,
          types: JSON.stringify(["celery"]),
        }));
        return data;
      }
    },
    currentJob() {
      return this.jobs[0];
    },
    runData: {
      default: { folder: {}, paramsFile: {} },
      async get() {
        if (this.location._modelType !== 'folder'
            || this.modeToggle === 0
            || (this.modeToggle === 2 && !this.uploadLocation)) {
          return { folder: {}, paramsFile: {} };
        }
        const folderId = this.modeToggle === 1 ? this.location._id : this.uploadLocation._id;
        const folderPromise = this.girderRest.get(`folder/${folderId}`);
        const itemPromise = this.girderRest.get('item', {
          params: {
            folderId,
            text: 'csv',
            limit: 1,
          },
        });
        try {
          const resolves = await Promise.all([folderPromise, itemPromise]);
          const paramsFileList = resolves[1].data;
          return {
            folder: resolves[0].data,
            paramsFile: paramsFileList.length ? paramsFileList[0] : {},
          };
        } catch (err) {
          return {
            folder: {},
            paramsFile: {},
          };
        }
      },
      watch() {
        return [
          this.refresh,
          this.uploadLocation,
        ];
      },
    },
  },
};
</script>
