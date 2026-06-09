<template>
  <DashboardShell :items="navigationItems" :username="authStore.username" @logout="handleLogout">
    <div class="space-y-6">
      <section class="rounded-2xl border border-white/10 bg-white/5 p-4 shadow-2xl shadow-slate-950/20 backdrop-blur sm:rounded-3xl sm:p-6">
      <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div class="min-w-0">
          <p class="text-xs font-semibold uppercase tracking-[0.25em] text-indigo-300 sm:text-sm">Dashboard</p>
          <h1 class="mt-2 text-2xl font-bold text-white sm:mt-3 sm:text-3xl">Panorama do sistema ATA</h1>
          <p class="mt-3 max-w-4xl text-sm leading-6 text-slate-300 sm:mt-4 sm:leading-7">
            Acompanhe membros, reuniões, atas, presenças, igrejas parceiras, amigos do Gideão e agendamentos.
          </p>
        </div>

        <button
          type="button"
          class="w-full shrink-0 rounded-2xl border border-white/10 px-4 py-3 text-sm font-medium text-slate-200 transition hover:bg-white/5 sm:w-auto"
          @click="loadDashboard"
        >
          Atualizar painel
        </button>
      </div>

        <div v-if="errorMessage" class="mt-5 rounded-2xl border border-rose-400/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
          {{ errorMessage }}
        </div>
      </section>

      <section class="grid grid-cols-2 gap-3 sm:gap-4 lg:grid-cols-3 xl:grid-cols-4">
        <article v-for="card in summaryCards" :key="card.title" class="rounded-2xl border border-white/10 bg-slate-900/70 p-3 sm:rounded-3xl sm:p-5">
          <div class="flex items-start justify-between gap-2">
            <p class="text-xs text-slate-400 sm:text-sm">{{ card.title }}</p>
            <span :class="card.icon" class="shrink-0 text-xl text-indigo-300 sm:text-2xl" />
          </div>
          <p class="mt-3 text-2xl font-semibold text-white sm:mt-6 sm:text-3xl">{{ loading ? '...' : card.value }}</p>
          <p class="mt-1 hidden text-sm text-slate-400 sm:mt-2 sm:block">{{ card.description }}</p>
        </article>
      </section>

      <section class="grid gap-4 sm:gap-6 xl:grid-cols-[minmax(0,1.6fr)_minmax(0,1fr)]">
        <div class="space-y-6">
          <div class="rounded-2xl border border-white/10 bg-slate-900/70 p-4 sm:rounded-3xl sm:p-6">
            <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <h2 class="text-lg font-semibold text-white">Últimas reuniões</h2>
                <p class="mt-1 text-sm text-slate-400">Dados reais vindos de `/api/meetings/`.</p>
              </div>
              <router-link :to="{ name: 'meetings' }" class="text-sm font-medium text-indigo-300 transition hover:text-indigo-200">
                Ver módulo
              </router-link>
            </div>

            <div v-if="recentMeetings.length" class="mt-5 grid gap-3">
              <div v-for="meeting in recentMeetings" :key="String(meeting.id ?? meeting.title)" class="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div class="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                  <div class="min-w-0">
                    <p class="font-medium text-white break-words">{{ formatValue(meeting.title) }}</p>
                    <p class="mt-1 text-sm text-slate-400">{{ formatValue(meeting.meeting_type) }} • {{ formatValue(meeting.date) }}</p>
                  </div>
                  <span class="self-start rounded-full border border-indigo-400/20 bg-indigo-500/10 px-3 py-1 text-xs font-medium text-indigo-200">
                    {{ formatValue(meeting.status) }}
                  </span>
                </div>
                <p class="mt-3 text-sm text-slate-300">Local: {{ formatValue(meeting.location) }}</p>
              </div>
            </div>

            <p v-else class="mt-5 rounded-2xl border border-dashed border-white/10 bg-white/5 px-4 py-6 text-sm text-slate-400">
              Nenhuma reunião encontrada no backend até agora.
            </p>
          </div>

          <div class="rounded-2xl border border-white/10 bg-slate-900/70 p-4 sm:rounded-3xl sm:p-6">
            <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <h2 class="text-lg font-semibold text-white">Atas recentes</h2>
                <p class="mt-1 text-sm text-slate-400">Resumo real das atas cadastradas.</p>
              </div>
              <router-link :to="{ name: 'minutes' }" class="text-sm font-medium text-indigo-300 transition hover:text-indigo-200">
                Ver módulo
              </router-link>
            </div>

            <div v-if="recentMinutes.length" class="mt-5 space-y-3">
              <div v-for="minute in recentMinutes" :key="String(minute.id ?? minute.meeting_title)" class="rounded-2xl border border-white/10 bg-white/5 p-4">
                <p class="font-medium text-white">{{ formatValue(minute.meeting_title) }}</p>
                <p class="mt-1 text-sm text-slate-400">Status: {{ formatValue(minute.status) }}</p>
                <p class="mt-3 line-clamp-2 text-sm text-slate-300">{{ formatValue(minute.full_text) }}</p>
              </div>
            </div>

            <p v-else class="mt-5 rounded-2xl border border-dashed border-white/10 bg-white/5 px-4 py-6 text-sm text-slate-400">
              Nenhuma ata encontrada no backend até agora.
            </p>
          </div>
        </div>

        <aside class="space-y-4 sm:space-y-6">
          <div class="rounded-2xl border border-white/10 bg-slate-900/70 p-4 sm:rounded-3xl sm:p-6">
            <h2 class="text-lg font-semibold text-white">Acessos rápidos</h2>
            <p class="mt-2 hidden text-sm leading-7 text-slate-300 sm:mt-3 sm:block">
              Cada módulo mostra a quantidade real de registros já salvos no backend.
            </p>

            <div class="mt-4 grid gap-2 sm:mt-6 sm:gap-3">
              <router-link
                v-for="item in quickAccessItems"
                :key="item.key"
                :to="{ name: item.key }"
                class="flex items-center justify-between gap-2 rounded-2xl border border-white/10 bg-white/5 px-3 py-3 text-sm text-slate-200 transition hover:bg-white/10 hover:text-white sm:gap-3 sm:px-4"
              >
                <div class="flex min-w-0 items-center gap-2 sm:gap-3">
                  <span :class="item.icon" class="shrink-0 text-lg text-indigo-300 sm:text-xl" />
                  <div class="min-w-0">
                    <p class="truncate font-medium text-white">{{ item.label }}</p>
                    <p class="hidden truncate text-xs text-slate-400 sm:block">{{ item.description }}</p>
                  </div>
                </div>
                <div class="flex shrink-0 items-center gap-2 sm:gap-3">
                  <span class="rounded-full border border-white/10 bg-slate-950/60 px-2.5 py-1 text-xs font-semibold text-white sm:px-3">
                    {{ loading ? '...' : moduleCounts[item.key] ?? 0 }}
                  </span>
                  <span class="mdi mdi-chevron-right text-lg text-slate-500" />
                </div>
              </router-link>
            </div>
          </div>

          <div class="rounded-2xl border border-white/10 bg-slate-900/70 p-4 sm:rounded-3xl sm:p-6">
            <h2 class="text-lg font-semibold text-white">Agendamento às igrejas</h2>
            <p class="mt-2 text-sm text-slate-400">Prévia real dos compromissos cadastrados nesse módulo.</p>

            <div v-if="recentSchedules.length" class="mt-5 space-y-3">
              <div v-for="schedule in recentSchedules" :key="String(schedule.id ?? schedule.church_name)" class="rounded-2xl border border-white/10 bg-white/5 p-4">
                <p class="font-medium text-white">{{ formatValue(schedule.church_name) }}</p>
                <p class="mt-1 text-sm text-slate-400">{{ formatValue(schedule.commitment_type) }} • {{ formatValue(schedule.date) }} às {{ formatValue(schedule.time) }}</p>
                <p class="mt-2 text-sm text-slate-300">Status: {{ formatValue(schedule.status) }}</p>
              </div>
            </div>

            <p v-else class="mt-5 rounded-2xl border border-dashed border-white/10 bg-white/5 px-4 py-6 text-sm text-slate-400">
              Nenhum agendamento às igrejas encontrado no backend até agora.
            </p>
          </div>
        </aside>
      </section>
    </div>
  </DashboardShell>
</template>

<script setup lang="ts">
  import { computed, onMounted, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { getResourceCollection, type ResourceRecord } from '@/api'
  import DashboardShell from '@/components/layout/DashboardShell.vue'
  import { navigationItems } from '@/config/navigation'
  import { resourceConfigs } from '@/config/resources'
  import { useAuthStore } from '@/stores/auth'

  const router = useRouter()
  const authStore = useAuthStore()

  const loading = ref(false)
  const errorMessage = ref('')
  const moduleCounts = ref<Record<string, number>>({})
  const recentMeetings = ref<ResourceRecord[]>([])
  const recentMinutes = ref<ResourceRecord[]>([])
  const recentSchedules = ref<ResourceRecord[]>([])

  const quickAccessItems = navigationItems.filter((item) => item.key !== 'dashboard')

  const summaryCards = computed(() => [
    {
      title: 'Membros cadastrados',
      value: moduleCounts.value.members ?? 0,
      description: 'Total real de membros disponíveis.',
      icon: 'mdi mdi-account-group-outline',
    },
    {
      title: 'Reuniões registradas',
      value: moduleCounts.value.meetings ?? 0,
      description: 'Quantidade atual de reuniões cadastradas.',
      icon: 'mdi mdi-forum-outline',
    },
    {
      title: 'Atas registradas',
      value: moduleCounts.value.minutes ?? 0,
      description: 'Atas disponíveis para revisão e consulta.',
      icon: 'mdi mdi-file-document-edit-outline',
    },
    {
      title: 'Presenças lançadas',
      value: moduleCounts.value.attendances ?? 0,
      description: 'Registros reais de presença nas reuniões.',
      icon: 'mdi mdi-account-multiple-check-outline',
    },
    {
      title: 'Igrejas parceiras',
      value: moduleCounts.value['partner-churches'] ?? 0,
      description: 'Quantidade de igrejas parceiras cadastradas.',
      icon: 'mdi mdi-church-outline',
    },
    {
      title: 'Amigos do Gideão',
      value: moduleCounts.value['gideon-friends'] ?? 0,
      description: 'Amigos cadastrados com vínculo ao Gideão/Auxiliar responsável.',
      icon: 'mdi mdi-hand-heart-outline',
    },
    {
      title: 'Agendamentos às igrejas',
      value: moduleCounts.value['church-schedules'] ?? 0,
      description: 'Compromissos e programações disponíveis.',
      icon: 'mdi mdi-calendar-clock-outline',
    },
  ])

  function formatValue(value: unknown) {
    if (value == null || value === '') return '—'
    return String(value)
  }

  async function loadDashboard() {
    const token = authStore.accessToken

    if (!token) {
      errorMessage.value = 'Sessão expirada. Faça login novamente.'
      return
    }

    loading.value = true
    errorMessage.value = ''

    try {
      const [
        members,
        meetings,
        minutes,
        attendances,
        partnerChurches,
        gideonFriends,
        churchSchedules,
      ] = await Promise.all([
        getResourceCollection(resourceConfigs.members.endpoint, token),
        getResourceCollection(resourceConfigs.meetings.endpoint, token),
        getResourceCollection(resourceConfigs.minutes.endpoint, token),
        getResourceCollection(resourceConfigs.attendances.endpoint, token),
        getResourceCollection(resourceConfigs['partner-churches'].endpoint, token),
        getResourceCollection(resourceConfigs['gideon-friends'].endpoint, token),
        getResourceCollection(resourceConfigs['church-schedules'].endpoint, token),
      ])

      moduleCounts.value = {
        members: members.count,
        meetings: meetings.count,
        minutes: minutes.count,
        attendances: attendances.count,
        'partner-churches': partnerChurches.count,
        'gideon-friends': gideonFriends.count,
        'church-schedules': churchSchedules.count,
      }

      recentMeetings.value = meetings.items.slice(0, 3)
      recentMinutes.value = minutes.items.slice(0, 3)
      recentSchedules.value = churchSchedules.items.slice(0, 3)
    } catch {
      errorMessage.value = 'Não foi possível carregar o resumo do dashboard com os dados do backend.'
    } finally {
      loading.value = false
    }
  }

  onMounted(() => {
    loadDashboard()
  })

  function handleLogout() {
    authStore.logout()
    router.push({ name: 'login' })
  }
</script>