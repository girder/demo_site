<template lang="pug">
glance-app(ref="glance")
</template>

<script>
import Vue from 'vue';
import GlanceApp from 'paraview-glance/src/components/core/App';
import ReaderFactory from 'paraview-glance/src/io/ReaderFactory';
import Config from 'paraview-glance/src/config';
import { Widgets } from 'paraview-glance/src/constants';
import CropWidget from 'paraview-glance/src/vtkwidgets/CropWidget';
import vtkListenerHelper from 'paraview-glance/src/ListenerHelper';
import vtkWidgetManager from 'paraview-glance/src/vtkwidgets/WidgetManager';
import vtkProxyManager from 'vtk.js/Sources/Proxy/Core/ProxyManager';
import 'paraview-glance/src/io/ParaViewGlanceReaders';

import vtkITKImageReader from 'vtk.js/Sources/IO/Misc/ITKImageReader';

import extensionToImageIO from 'itk/extensionToImageIO';
import readImageArrayBuffer from 'itk/readImageArrayBuffer';


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

Vue.prototype.$globalBus = new Vue();

const proxyConfiguration = Config.Proxy;
const proxyManager = vtkProxyManager.newInstance({ proxyConfiguration });
const renderListener = vtkListenerHelper.newInstance(
  proxyManager.autoAnimateViews,
  () => [
    ...proxyManager.getSources(),
    ...proxyManager.getRepresentations(),
    ...proxyManager.getViews(),
  ],
);

proxyManager.onProxyRegistrationChange(renderListener.resetListeners);

const widgetManager = vtkWidgetManager.newInstance({ proxyManager });
widgetManager.registerWidgetGroup(Widgets.CROP, CropWidget);

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
  provide: {
    proxyManager,
    widgetManager,
  },
  watch: {
    url() {
      this.$refs.glance.loadRemoteDatasets([this.url], [this.name]);
    },
  },
  mounted() {
    if (this.name && this.url) {
      this.$refs.glance.loadRemoteDatasets([this.url], [this.name]);
    }
  },
};
</script>
