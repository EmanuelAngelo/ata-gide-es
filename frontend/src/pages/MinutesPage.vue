<template>
  <DashboardShell :items="navigationItems" :username="authStore.username" @logout="handleLogout">
    <MinutesListView />
  </DashboardShell>
</template>

<script setup lang="ts">
  import { useRouter } from 'vue-router'
  import DashboardShell from '@/components/layout/DashboardShell.vue'
  import MinutesListView from '@/components/minutes/MinutesListView.vue'
  import { navigationItems } from '@/config/navigation'
  import { useAuthStore } from '@/stores/auth'

  const authStore = useAuthStore()
  const router = useRouter()

  function handleLogout() {
    authStore.logout()
    router.push({ name: 'login' })
  }
</script>
