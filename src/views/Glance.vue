<template lang="pug">
glance-app(ref="glance")
</template>

<script>
import Vue from 'vue';
import GlanceApp from 'paraview-glance/src/components/core/App';
import Config from 'paraview-glance/src/config';
import { Widgets } from 'paraview-glance/src/constants';
import CropWidget from 'paraview-glance/src/vtkwidgets/CropWidget';
import vtkListenerHelper from 'paraview-glance/src/ListenerHelper';
import vtkWidgetManager from 'paraview-glance/src/vtkwidgets/WidgetManager';
import vtkProxyManager from 'vtk.js/Sources/Proxy/Core/ProxyManager';
import 'paraview-glance/src/io/ParaViewGlanceReaders';

const proxyConfiguration = Config.Proxy;
const proxyManager = vtkProxyManager.newInstance({ proxyConfiguration });
const renderListener = vtkListenerHelper.newInstance(
  proxyManager.autoAnimateViews,
  () => [
    proxyManager.getSources(),
    proxyManager.getRepresentations(),
    proxyManager.getViews(),
  ],
);

proxyManager.onProxyRegistrationChange(renderListener.resetListeners);

const widgetManager = vtkWidgetManager.newInstance({ proxyManager });
widgetManager.registerWidgetGroup(Widgets.CROP, CropWidget);

Vue.prototype.$globalBus = new Vue();

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
  mounted() {
    if (this.name && this.url) {
      this.$refs.glance.loadRemoteDatasets([this.url], [this.name]);
    }
  },
};
</script>
