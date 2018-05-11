<template lang="pug">
select-mask-container(:folder-id="$route.params.folderId", :file-id="$route.params.fileId")
</template>

<script>
import SelectMaskContainer from '@/containers/SelectMaskContainer';

export default {
  components: { SelectMaskContainer },
};
</script>
