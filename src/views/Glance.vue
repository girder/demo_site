<template lang="pug">
glance-app
</template>

<script>
import Vue from 'vue';
import Vuex, { mapActions } from 'vuex';
import GlanceApp from 'paraview-glance/src/components/core/App';
import ReaderFactory from 'paraview-glance/src/io/ReaderFactory';
import createStore from 'paraview-glance/src/stores';
import StoreTypes from 'paraview-glance/src/stores/types';
import 'paraview-glance/src/io/ParaViewGlanceReaders';

import vtkITKImageReader from 'vtk.js/Sources/IO/Misc/ITKImageReader';

import extensionToImageIO from 'itk/extensionToImageIO';
import readImageArrayBuffer from 'itk/readImageArrayBuffer';

Vue.use(Vuex);

vtkITKImageReader.setReadImageArrayBufferFromITK(readImageArrayBuffer);
new Set(Object.keys(extensionToImageIO).map(ext => ext.toLowerCase())).forEach((ext) => {
  ReaderFactory.registerReader({
    extension: ext,
    name: `${ext.toUpperCase()} Reader`,
    vtkReader: vtkITKImageReader,
    binary: true,
    fileNameMethod: 'setFileName',
  });
});

export default {
  components: { GlanceApp },
  props: {
    name: {
      type: String,
      default: null,
    },
    url: {
      type: String,
      default: null,
    },
  },
  store: createStore(),
  watch: {
    url() {
      this.openFiles({
        urls: [this.url],
        names: [this.name],
      });
    },
  },
  mounted() {
    if (this.name && this.url) {
      this.openFiles({
        urls: [this.url],
        names: [this.name],
      });
    }
  },
  methods: mapActions({
    openFiles: StoreTypes.Actions.OPEN_REMOTE_FILES,
  }),
};
</script>
