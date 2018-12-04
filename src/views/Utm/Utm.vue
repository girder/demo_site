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
            v-tabs(v-model="modeToggle")
              v-tab(key="demo")
                v-icon.pa-2 restore_page
                | Demo
              v-tab(key="choose")
                v-icon.pa-2 folder
                | Choose
              v-tab(key="upload")
                v-icon.pa-2 cloud_upload
                | Upload
              v-tab(key="jobs")
                v-icon.pa-2 settings
                | Jobs
      v-flex(md5 sm12)
        v-card.ma-2(v-if="modeToggle < 3")
          v-card-title.pb-0(primary-title)
            div
              h2.display-1 Instructions
              v-subheader.pl-0
                p.subheading(v-if="modeToggle == 0") Launch Demo Session
                p.subheading(v-if="modeToggle == 1") {{ chooseDirectoryInstructions }}
                p.subheading(v-if="modeToggle == 2") {{ uploadDataInstructions }}

          div(v-if="modeToggle === 0")
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
              v-btn(color="primary")
                v-icon.pa-2 launch
                | Launch

          div(v-else)
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
              v-btn(color="primary", @click="run", :disabled="!canRun")
                v-icon.pa-2 play_arrow
                | Run Job
              v-btn(color="primary", v-if="currentJob && !processing")
                v-icon.pa-2 launch
                | View Results
              .jobStatus(v-if="currentJob")
                v-progress-circular.ml-3(
                    v-if="processing",
                    indeterminate,
                    :size="30",
                    :width="3",
                    :rotate="-90")
              p.subheading.px-3(v-if="currentJob") {{ statusText || " " }}
      
      v-flex(md7 sm12)
        v-card.ma-2
          girder-data-browser(
              v-if="modeToggle < 2 && !!location",
              ref="girderBrowser",
              :location="location",
              @update:location="setBrowserLocation($event)",
              :select-enabled="false",
              :multi-select-enabled="false",
              :upload-enabled="modeToggle === 2",
              :new-item-enabled="false",
              :new-folder-enabled="false")
          girder-upload(
              v-else-if="modeToggle === 2 && uploadLocation",
              :dest="uploadLocation",
              @done="refresh++;",
              :multiple="true",
              :preUpload="preUpload")
</template>

<script>
import { mapState } from 'vuex';
import { JobStatus } from '@/constants';
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

const statusEnum = [
  'inactive',
  'queued',
  'running',
  'success',
  'error',
  'cancelled',
];

const busyStatusEnum = [
  'queued',
  'running',
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
      uploadLocation: { name: `UTM_${new Date().toISOString()}` },
      demoLocation: null,
      modeToggle: 0,
      refresh: 0,
      jobs: [],
      activeJob: null, // the job returned by /utm/job
      launchDemoInstructions,
      chooseDirectoryInstructions,
      uploadDataInstructions,
      dataRequirements,
      variableFileDescription,
      interval: null,
    };
  },
  computed: {
    ...mapState('auth', ['user']),
    processing() {
      return this.currentJob
        && ![JobStatus.ERROR, JobStatus.SUCCESS, JobStatus.CANCELED].includes(this.currentJob.status);
    },
    canRun() {
      const { folder, paramsFile } = this.runData;
      return !!folder._id && !!paramsFile._id && !this.processing;
    },
    statusText() {
      const job = this.activeJob || {};
      if (!job) {
        return 'Job not found';
      }
      switch (job.status) {
        case JobStatus.INACTIVE:
        case JobStatus.QUEUED:
          return 'Your job is waiting in the job queue.';
        case JobStatus.RUNNING:
          if (job.progress && job.progress.message) {
            return job.progress.message;
          }
          return 'Your job is being processed, please wait...';
        case JobStatus.ERROR:
          return 'An error occurred while processing your job.';
        case JobStatus.SUCCESS:
          return 'Job succeeded';
        default:
          return 'Unknown job status';
      }
    },
  },
  methods: {
    setBrowserLocation(loc) {
      if (this.modeToggle === 1) {
        this.browserLocation = loc;
      }
    },
    async preUpload() {
      // Lazily create the upload destination folder.
      const parent = { _modelType: 'user', _id: this.user._id };
      const { data } = await this.girderRest.post('folder', formEncode({
        parentType: parent._modelType,
        parentId: parent._id,
        name: `UTM_${new Date().toISOString()}`,
      }));
      this.uploadLocation = data;
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
        this.refresh++;
      } catch (err) {
        console.error(err);
      }
    },
  },
  asyncComputed: {
    location: {
      default() { return { _modelType: 'user', _id: this.user._id }; },
      async get() {
        switch(this.modeToggle) {
          case 0:
            const { folder } = this.demoData;
            return { _modelType: 'folder', _id: folder._id };
          case 1:
            return this.browserLocation || { _modelType: 'user', _id: this.user._id };
          case 2:
            return this.uploadLocation;
          default:
            return null;
        }
      },
    },
    jobs: {
      default: [],
      async get() {
        const { data } = await this.girderRest.get('utm/job', { params: { limit: 100 } });
        this.jobs = data;
        return this.jobs;
      },
      watch() {return [this.refresh];},
    },
    currentJob: {
      get() {
        const currents = this.jobs.filter(j =>
          (j.utmFolderId === this.location._id) ||
          (j.utmOutputFolderId === this.location._id))
        const newActiveJob = currents.length ? currents[0] : null;
        if (!newActiveJob || !this.activeJob ||
          (this.activeJob && newActiveJob._id !== this.activeJob._id)) {
          this.activeJob = newActiveJob;
        }
        return this.activeJob;
      },
    },
    runData: {
      default: { folder: {}, paramsFile: {} },
      async get() {
        if ((this.modeToggle === 1 && this.location._modelType !== 'folder')
            || (this.modeToggle === 0)
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
          return { folder: {}, paramsFile: {} };
        }
      },
      watch() {return [this.refresh];},
    },
  },
  destroyed() {
    clearInterval(this.interval);
  },
  mounted() {
    this.interval = setInterval(async () => {
      if (this.activeJob && ![JobStatus.ERROR, JobStatus.SUCCESS, JobStatus.CANCELED].includes(this.activeJob.status)) {
        const { data } = await this.girderRest.get(`job/${this.activeJob._id}`);
        this.activeJob = Object.assign(this.activeJob, data);
      }
    }, 3000);
  },
};
</script>
