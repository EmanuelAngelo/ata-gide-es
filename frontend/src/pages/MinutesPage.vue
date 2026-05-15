<template>
  <ResourceModuleView :config="resourceConfigs.minutes" />
</template>

<script setup lang="ts">
  import ResourceModuleView from '@/components/resources/ResourceModuleView.vue'
  import { resourceConfigs } from '@/config/resources'
</script>
