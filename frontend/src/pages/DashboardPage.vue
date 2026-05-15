<template>
  <DashboardShell :items="navigationItems" :username="authStore.username" @logout="handleLogout">
    <div class="space-y-6">
      <section class="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl shadow-slate-950/20 backdrop-blur">
        <div class="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
          <div>
            <p class="text-sm font-semibold uppercase tracking-[0.25em] text-indigo-300">Dashboard</p>
            <h1 class="mt-3 text-3xl font-bold text-white">Panorama real do sistema ATA</h1>
            <p class="mt-4 max-w-4xl text-sm leading-7 text-slate-300">
              O painel agora consolida dados reais do backend Django para acompanhar membros,
              reuniões, atas, presenças, agendamentos às igrejas e igrejas parceiras.
            </p>
          </div>

          <button
            type="button"
            class="self-start rounded-2xl border border-white/10 px-4 py-3 text-sm font-medium text-slate-200 transition hover:bg-white/5"
            @click="loadDashboard"
          >
            Atualizar painel
          </button>
        </div>

        <div v-if="errorMessage" class="mt-5 rounded-2xl border border-rose-400/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
          {{ errorMessage }}
        </div>
      </section>

      <section class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <article v-for="card in summaryCards" :key="card.title" class="rounded-3xl border border-white/10 bg-slate-900/70 p-5">
          <div class="flex items-center justify-between">
            <p class="text-sm text-slate-400">{{ card.title }}</p>
            <span :class="card.icon" class="text-2xl text-indigo-300" />
          </div>
          <p class="mt-6 text-3xl font-semibold text-white">{{ loading ? '...' : card.value }}</p>
          <p class="mt-2 text-sm text-slate-400">{{ card.description }}</p>
        </article>
      </section>

      <section class="grid gap-6 xl:grid-cols-[minmax(0,1.6fr)_minmax(360px,1fr)]">
        <div class="space-y-6">
          <div class="rounded-3xl border border-white/10 bg-slate-900/70 p-6">
            <div class="flex items-center justify-between gap-4">
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
                <div class="flex items-start justify-between gap-3">
                  <div>
                    <p class="font-medium text-white">{{ formatValue(meeting.title) }}</p>
                    <p class="mt-1 text-sm text-slate-400">{{ formatValue(meeting.meeting_type) }} • {{ formatValue(meeting.date) }}</p>
                  </div>
                  <span class="rounded-full border border-indigo-400/20 bg-indigo-500/10 px-3 py-1 text-xs font-medium text-indigo-200">
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

          <div class="rounded-3xl border border-white/10 bg-slate-900/70 p-6">
            <div class="flex items-center justify-between gap-4">
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

        <aside class="space-y-6">
          <div class="rounded-3xl border border-white/10 bg-slate-900/70 p-6">
            <h2 class="text-lg font-semibold text-white">Acessos rápidos</h2>
            <p class="mt-3 text-sm leading-7 text-slate-300">
              Cada módulo mostra a quantidade real de registros já salvos no backend.
            </p>

            <div class="mt-6 grid gap-3">
              <router-link
                v-for="item in quickAccessItems"
                :key="item.key"
                :to="{ name: item.key }"
                class="flex items-center justify-between rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-200 transition hover:bg-white/10 hover:text-white"
              >
                <div class="flex items-center gap-3">
                  <span :class="item.icon" class="text-xl text-indigo-300" />
                  <div>
                    <p class="font-medium text-white">{{ item.label }}</p>
                    <p class="text-xs text-slate-400">{{ item.description }}</p>
                  </div>
                </div>
                <div class="flex items-center gap-3">
                  <span class="rounded-full border border-white/10 bg-slate-950/60 px-3 py-1 text-xs font-semibold text-white">
                    {{ loading ? '...' : moduleCounts[item.key] ?? 0 }}
                  </span>
                  <span class="mdi mdi-chevron-right text-lg text-slate-500" />
                </div>
              </router-link>
            </div>
          </div>

          <div class="rounded-3xl border border-white/10 bg-slate-900/70 p-6">
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
      description: 'Total real de membros disponíveis no backend.',
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
      const [members, meetings, minutes, attendances, partnerChurches, churchSchedules] = await Promise.all([
        getResourceCollection(resourceConfigs.members.endpoint, token),
        getResourceCollection(resourceConfigs.meetings.endpoint, token),
        getResourceCollection(resourceConfigs.minutes.endpoint, token),
        getResourceCollection(resourceConfigs.attendances.endpoint, token),
        getResourceCollection(resourceConfigs['partner-churches'].endpoint, token),
        getResourceCollection(resourceConfigs['church-schedules'].endpoint, token),
      ])

      moduleCounts.value = {
        members: members.count,
        meetings: meetings.count,
        minutes: minutes.count,
        attendances: attendances.count,
        'partner-churches': partnerChurches.count,
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
