<template>
  <DashboardShell :items="navigationItems" :username="authStore.username" @logout="handleLogout">
    <div class="space-y-4 sm:space-y-6">
      <section class="rounded-2xl border border-white/10 bg-white/5 p-4 sm:rounded-3xl sm:p-6">
        <h1 class="text-2xl font-bold text-white sm:text-3xl">Reuniões</h1>
        <p class="mt-2 max-w-3xl text-sm leading-6 text-slate-300 sm:leading-7">
          Crie a reunião e, no mesmo lugar, registre a ata e a lista de presença dos membros — sem precisar trocar de tela.
        </p>
      </section>

      <div class="grid gap-4 lg:grid-cols-[minmax(280px,360px)_minmax(0,1fr)] lg:gap-6">
        <aside
          :class="[
            'rounded-2xl border border-white/10 bg-slate-900/70 p-4 sm:rounded-3xl sm:p-5',
            selectedMeetingId && 'hidden lg:block',
          ]"
        >
          <MeetingListPanel
            ref="listPanelRef"
            :selected-id="selectedMeetingId"
            @select="openMeeting"
            @created="openMeeting"
          />
        </aside>

        <main class="min-w-0">
          <MeetingWorkspace
            v-if="selectedMeetingId"
            :meeting-id="selectedMeetingId"
            @back="closeMeeting"
            @updated="refreshList"
          />

          <div
            v-else
            class="hidden rounded-2xl border border-dashed border-white/10 bg-white/[0.02] px-6 py-16 text-center lg:block lg:rounded-3xl"
          >
            <span class="mdi mdi-forum-outline text-5xl text-indigo-300" />
            <p class="mt-4 text-lg font-medium text-white">Selecione uma reunião</p>
            <p class="mt-2 text-sm text-slate-400">
              Escolha uma reunião na lista ou crie uma nova para registrar ata e presença.
            </p>
          </div>
        </main>
      </div>
    </div>
  </DashboardShell>
</template>

<script setup lang="ts">
  import { computed, ref, watch } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import DashboardShell from '@/components/layout/DashboardShell.vue'
  import MeetingListPanel from '@/components/meetings/MeetingListPanel.vue'
  import MeetingWorkspace from '@/components/meetings/MeetingWorkspace.vue'
  import { navigationItems } from '@/config/navigation'
  import { useAuthStore } from '@/stores/auth'

  const authStore = useAuthStore()
  const router = useRouter()
  const route = useRoute()
  const listPanelRef = ref<InstanceType<typeof MeetingListPanel> | null>(null)

  const selectedMeetingId = computed(() => {
    const id = route.params.id
    return id ? String(id) : null
  })

  function openMeeting(id: number | string) {
    router.push({ name: 'meeting-detail', params: { id: String(id) } })
  }

  function closeMeeting() {
    router.push({ name: 'meetings' })
  }

  function refreshList() {
    listPanelRef.value?.loadMeetings()
  }

  function handleLogout() {
    authStore.logout()
    router.push({ name: 'login' })
  }

  watch(
    () => route.name,
    (name) => {
      if (name === 'meetings') refreshList()
    },
  )
</script>
