<template>
  <DashboardShell :items="navigationItems" :username="authStore.username" @logout="handleLogout">
    <ResourceCrudPage :config="config" />
  </DashboardShell>
</template>

<script setup lang="ts">
  import { useRouter } from 'vue-router'
  import DashboardShell from '@/components/layout/DashboardShell.vue'
  import ResourceCrudPage from '@/components/resources/ResourceCrudPage.vue'
  import { navigationItems } from '@/config/navigation'
  import type { ResourceConfig } from '@/config/resources'
  import { useAuthStore } from '@/stores/auth'

  defineProps<{
    config: ResourceConfig
  }>()

  const authStore = useAuthStore()
  const router = useRouter()

  function handleLogout() {
    authStore.logout()
    router.push({ name: 'login' })
  }
</script>
