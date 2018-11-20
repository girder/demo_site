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
            v-btn-toggle(v-model="modeToggle", max, color="primary", mandatory)
              v-btn(flat)
                v-icon.pa-2 restore_page
                | Launch Demo Data
              v-btn(flat)
                v-icon.pa-2 folder
                | Choose Folder
              v-btn(flat)
                v-icon.pa-2 cloud_upload
                | Upload New Data
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
                b  {{ demoData.folder.name }}
              p.subheading Param File:
                b  {{ demoData.paramsFile.name }}
            v-card-actions
              v-btn(color="primary" large)
                v-icon.pa-2 launch
                | Launch

          div(v-if="modeToggle !== 0")
            v-card-text
              p.subheading {{ dataRequirements }}
              ul.subheading
                li(v-for="row in variableFileDescription" :key="row") {{ row }}
            v-dialog(v-model="uploader", v-if="modeToggle == 2", width="70%")
              v-btn(slot="activator" color="primary" large)
                v-icon.pa-2 cloud_upload
                | Upload Data
              v-card
                girder-upload(
                    :dest="location",
                    :multiple="true")
            v-card-actions(v-if="modeToggle === 1")
              v-btn(color="primary" large)
                v-icon.pa-2 launch
                | Run job

      v-flex(md7 sm12)
        v-card.ma-2
          girder-data-browser(:location="location",
              @update:location="setLocation($event)",
              :select-enabled="false",
              :multi-select-enabled="false",
              :upload-enabled="false",
              :new-item-enabled="false",
              :new-folder-enabled="false")
</template>

<script>
import { mapState } from 'vuex';
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
      demoLocation: null,
      modeToggle: 0,
      launchDemoInstructions,
      chooseDirectoryInstructions,
      uploadDataInstructions,
      dataRequirements,
      variableFileDescription,
    };
  },
  computed: {
    ...mapState('auth', ['user']),
  },
  methods: {
    setLocation(loc) {
      if (this.modeToggle === 1) {
        this.browserLocation = loc;
      }
    },
  },
  asyncComputed: {
    location: {
      async get() {
        let loc = this.browserLocation || { type: 'user', id: this.user._id };
        if (this.modeToggle === 0 || !loc) {
          const { folder } = this.demoData;
          loc = { type: 'folder', id: folder._id };
        }
        return loc;
      },
    },
  },
};
</script>
