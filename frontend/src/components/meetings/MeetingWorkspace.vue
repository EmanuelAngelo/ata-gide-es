<template>
  <div class="w-full min-w-0 max-w-full space-y-4 overflow-x-clip sm:space-y-6">
    <div v-if="loading" class="rounded-2xl border border-white/10 bg-white/5 px-4 py-12 text-center text-sm text-slate-300">
      Carregando reunião...
    </div>

    <template v-else-if="meeting">
      <section class="min-w-0 overflow-hidden rounded-2xl border border-white/10 bg-white/5 p-3 sm:rounded-3xl sm:p-6">
        <div class="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
          <div class="min-w-0 flex-1">
            <p class="text-[10px] font-semibold uppercase tracking-[0.15em] text-indigo-300 sm:text-xs sm:tracking-[0.25em]">Reunião</p>
            <h2 class="mt-1 break-words text-xl font-bold text-white sm:mt-2 sm:text-3xl">{{ meeting.title }}</h2>
            <p class="mt-2 break-words text-xs leading-5 text-slate-400 sm:text-sm sm:leading-6">
              <span class="block sm:inline">{{ meeting.meeting_type }}</span>
              <span class="hidden sm:inline"> • </span>
              <span class="block sm:inline">{{ meeting.date }}</span>
              <span class="hidden sm:inline"> • </span>
              <span class="block sm:inline">{{ meeting.location }}</span>
            </p>
            <div class="mt-3 flex flex-wrap gap-1.5 sm:gap-2">
              <span class="max-w-full truncate rounded-full border border-white/10 bg-slate-950/60 px-2.5 py-1 text-[11px] text-slate-200 sm:px-3 sm:text-xs">
                {{ meeting.status }}
              </span>
              <span v-if="minutes" class="rounded-full border border-indigo-400/20 bg-indigo-500/10 px-2.5 py-1 text-[11px] text-indigo-200 sm:px-3 sm:text-xs">
                Ata criada
              </span>
              <span v-else class="rounded-full border border-amber-400/20 bg-amber-500/10 px-2.5 py-1 text-[11px] text-amber-200 sm:px-3 sm:text-xs">
                Sem ata
              </span>
              <span class="rounded-full border border-emerald-400/20 bg-emerald-500/10 px-2.5 py-1 text-[11px] text-emerald-200 sm:px-3 sm:text-xs">
                {{ presentCount }} presente(s)
              </span>
            </div>
          </div>

          <button
            type="button"
            class="w-full shrink-0 rounded-2xl border border-white/10 px-4 py-3 text-sm font-medium text-slate-200 transition hover:bg-white/5 sm:w-auto lg:hidden"
            @click="emit('back')"
          >
            Voltar à lista
          </button>
        </div>

        <div v-if="errorMessage" class="mt-3 rounded-2xl border border-rose-400/20 bg-rose-500/10 px-3 py-3 text-sm text-rose-200 sm:mt-4 sm:px-4">
          {{ errorMessage }}
        </div>
        <div v-if="successMessage" class="mt-3 rounded-2xl border border-emerald-400/20 bg-emerald-500/10 px-3 py-3 text-sm text-emerald-200 sm:mt-4 sm:px-4">
          {{ successMessage }}
        </div>
      </section>

      <div class="mobile-scroll-tabs w-full min-w-0 max-w-full overflow-x-auto">
        <div class="flex w-max min-w-full gap-1.5 pb-1 sm:gap-2">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            type="button"
            :class="[
              'shrink-0 rounded-2xl px-3 py-2 text-xs font-medium transition sm:px-4 sm:py-2.5 sm:text-sm',
              activeTab === tab.key
                ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-950/30'
                : 'border border-white/10 text-slate-300 hover:bg-white/5',
            ]"
            @click="activeTab = tab.key"
          >
            <span class="sm:hidden">{{ tab.shortLabel }}</span>
            <span class="hidden sm:inline">{{ tab.label }}</span>
          </button>
        </div>
      </div>

      <section class="min-w-0 overflow-hidden rounded-2xl border border-white/10 bg-slate-900/70 p-3 sm:rounded-3xl sm:p-6">
        <div v-show="activeTab === 'info'" class="min-w-0">
          <form class="grid min-w-0 grid-cols-1 gap-4 md:grid-cols-2" @submit.prevent="saveMeeting">
            <div
              v-for="field in meetingFields"
              :key="field.name"
              class="min-w-0"
              :class="field.type === 'textarea' ? 'md:col-span-2' : ''"
            >
              <label :for="field.name" class="mb-2 block text-sm font-medium text-slate-200">{{ field.label }}</label>
              <select
                v-if="field.type === 'select'"
                :id="field.name"
                v-model="meetingForm[field.name]"
                class="block w-full min-w-0 max-w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-base text-white outline-none focus:border-indigo-500 sm:text-sm"
              >
                <option v-for="option in field.options" :key="option.value" :value="option.value">{{ option.label }}</option>
              </select>
              <textarea
                v-else-if="field.type === 'textarea'"
                :id="field.name"
                v-model="meetingForm[field.name]"
                rows="3"
                class="block w-full min-w-0 max-w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-base text-white outline-none focus:border-indigo-500 sm:text-sm"
              />
              <input
                v-else
                :id="field.name"
                v-model="meetingForm[field.name]"
                :type="field.type"
                class="block w-full min-w-0 max-w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-base text-white outline-none focus:border-indigo-500 sm:text-sm"
              />
            </div>
            <div class="min-w-0 md:col-span-2">
              <button
                type="submit"
                :disabled="savingMeeting"
                class="w-full rounded-2xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:opacity-70"
              >
                {{ savingMeeting ? 'Salvando...' : 'Salvar reunião' }}
              </button>
            </div>
          </form>
        </div>

        <MeetingMinutesPanel
          v-show="activeTab === 'minutes'"
          :minutes="minutes"
          :saving="savingMinutes"
          @save="saveMinutes"
          @pdf="openMinutePdf"
          @print="openMinutePrint"
        />

        <MeetingAttendanceRoster
          v-show="activeTab === 'attendance'"
          :roster="roster"
          :saving="savingAttendance"
          @save="saveAttendance"
        />
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
  import { computed, reactive, ref, watch } from 'vue'
  import { ApiError } from '@/api'
  import {
    fetchProtectedMeetingFile,
    getMeetingWorkspace,
    saveBulkAttendances,
    saveMeetingMinutes,
    type AttendanceRosterItem,
    type MinutesRecord,
  } from '@/api/meetings'
  import { updateResource, type ResourceRecord } from '@/api/resources'
  import MeetingAttendanceRoster from '@/components/meetings/MeetingAttendanceRoster.vue'
  import MeetingMinutesPanel from '@/components/meetings/MeetingMinutesPanel.vue'
  import { resourceConfigs } from '@/config/resources'
  import { useAuthStore } from '@/stores/auth'

  const props = defineProps<{
    meetingId: number | string
  }>()

  const emit = defineEmits<{
    back: []
    updated: []
  }>()

  const authStore = useAuthStore()
  const meetingFields = resourceConfigs.meetings.fields

  const tabs = [
    { key: 'info', label: 'Dados da reunião', shortLabel: 'Dados' },
    { key: 'minutes', label: 'Ata', shortLabel: 'Ata' },
    { key: 'attendance', label: 'Lista de presença', shortLabel: 'Presença' },
  ] as const

  type TabKey = (typeof tabs)[number]['key']

  const activeTab = ref<TabKey>('minutes')
  const loading = ref(false)
  const savingMeeting = ref(false)
  const savingMinutes = ref(false)
  const savingAttendance = ref(false)
  const errorMessage = ref('')
  const successMessage = ref('')

  const meeting = ref<ResourceRecord | null>(null)
  const minutes = ref<MinutesRecord | null>(null)
  const roster = ref<AttendanceRosterItem[]>([])
  const meetingForm = reactive<Record<string, string>>({})

  const presentCount = computed(() => roster.value.filter((item) => item.status === 'Presente').length)

  function syncMeetingForm(data: ResourceRecord) {
    meetingFields.forEach((field) => {
      meetingForm[field.name] = data[field.name] == null ? '' : String(data[field.name])
    })
  }

  async function loadWorkspace() {
    const token = authStore.accessToken
    if (!token) return

    loading.value = true
    errorMessage.value = ''

    try {
      const data = await getMeetingWorkspace(props.meetingId, token)
      meeting.value = data.meeting
      minutes.value = data.minutes
      roster.value = data.roster
      syncMeetingForm(data.meeting)
      activeTab.value = data.minutes ? 'attendance' : 'minutes'
    } catch (error) {
      errorMessage.value = error instanceof ApiError ? error.message : 'Não foi possível carregar esta reunião.'
    } finally {
      loading.value = false
    }
  }

  async function saveMeeting() {
    const token = authStore.accessToken
    if (!token || !meeting.value?.id) return

    savingMeeting.value = true
    errorMessage.value = ''
    successMessage.value = ''

    try {
      const payload = meetingFields.reduce<ResourceRecord>((acc, field) => {
        const value = meetingForm[field.name]
        if (value !== '') acc[field.name] = value
        return acc
      }, {})

      meeting.value = await updateResource('/api/meetings/', meeting.value.id, token, payload)
      successMessage.value = 'Reunião atualizada com sucesso.'
      emit('updated')
    } catch (error) {
      errorMessage.value = error instanceof ApiError ? error.message : 'Não foi possível salvar a reunião.'
    } finally {
      savingMeeting.value = false
    }
  }

  async function saveMinutes(payload: Record<string, string>) {
    const token = authStore.accessToken
    if (!token) return

    if (!payload.full_text.trim()) {
      errorMessage.value = 'Preencha o texto completo da ata.'
      activeTab.value = 'minutes'
      return
    }

    savingMinutes.value = true
    errorMessage.value = ''
    successMessage.value = ''

    try {
      const body: ResourceRecord = { ...payload }
      if (!body.approval_date) delete body.approval_date

      minutes.value = await saveMeetingMinutes(props.meetingId, token, body, Boolean(minutes.value?.id))
      successMessage.value = minutes.value?.id ? 'Ata atualizada com sucesso.' : 'Ata criada com sucesso.'
      activeTab.value = 'attendance'
      emit('updated')
    } catch (error) {
      errorMessage.value = error instanceof ApiError ? error.message : 'Não foi possível salvar a ata.'
    } finally {
      savingMinutes.value = false
    }
  }

  async function saveAttendance(items: AttendanceRosterItem[]) {
    const token = authStore.accessToken
    if (!token) return

    savingAttendance.value = true
    errorMessage.value = ''
    successMessage.value = ''

    try {
      const payload = items.map((item) => ({
        member_id: item.member_id,
        status: item.status,
        arrival_time: item.arrival_time,
        observations: item.observations,
      }))

      await saveBulkAttendances(props.meetingId, token, payload)
      await loadWorkspace()
      successMessage.value = 'Lista de presença salva com sucesso.'
      emit('updated')
    } catch (error) {
      errorMessage.value = error instanceof ApiError ? error.message : 'Não foi possível salvar a lista de presença.'
    } finally {
      savingAttendance.value = false
    }
  }

  async function openMinutePdf() {
    const token = authStore.accessToken
    const id = minutes.value?.id
    if (!token || id == null) return

    try {
      const response = await fetchProtectedMeetingFile(`/api/minutes/${id}/pdf/`, token)
      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `ata-${id}.pdf`
      document.body.appendChild(link)
      link.click()
      link.remove()
      URL.revokeObjectURL(url)
    } catch {
      errorMessage.value = 'Não foi possível gerar o PDF desta ata.'
    }
  }

  async function openMinutePrint() {
    const token = authStore.accessToken
    const id = minutes.value?.id
    if (!token || id == null) return

    try {
      const response = await fetchProtectedMeetingFile(`/api/minutes/${id}/print/`, token)
      const html = await response.text()
      const printWindow = window.open('', '_blank', 'noopener,noreferrer')
      if (!printWindow) return
      printWindow.document.open()
      printWindow.document.write(html)
      printWindow.document.close()
    } catch {
      errorMessage.value = 'Não foi possível abrir a visualização de impressão.'
    }
  }

  watch(() => props.meetingId, loadWorkspace, { immediate: true })
</script>
