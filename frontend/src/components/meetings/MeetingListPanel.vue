<template>
  <div class="w-full min-w-0 max-w-full space-y-4">
    <div class="flex flex-col gap-3">
      <input
        v-model="search"
        type="search"
        placeholder="Buscar reuniões..."
        class="w-full rounded-2xl border border-white/10 bg-slate-900/70 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10"
        @keydown.enter="loadMeetings"
      />
      <button
        type="button"
        class="w-full rounded-2xl bg-indigo-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500"
        @click="openCreateModal"
      >
        Nova reunião
      </button>
    </div>

    <div v-if="loading" class="rounded-2xl border border-white/10 bg-white/5 px-4 py-8 text-center text-sm text-slate-300">
      Carregando reuniões...
    </div>

    <div v-else-if="!items.length" class="rounded-2xl border border-dashed border-white/10 bg-white/5 px-4 py-8 text-center text-sm text-slate-400">
      Nenhuma reunião cadastrada ainda.
    </div>

    <div v-else class="space-y-2">
      <button
        v-for="item in items"
        :key="String(item.id)"
        type="button"
        :class="[
          'w-full min-w-0 max-w-full rounded-2xl border px-3 py-3 text-left transition sm:px-4 sm:py-4',
          String(selectedId) === String(item.id)
            ? 'border-indigo-400/40 bg-indigo-500/10'
            : 'border-white/10 bg-white/[0.03] hover:border-white/20 hover:bg-white/[0.05]',
        ]"
        @click="emit('select', item.id as number | string)"
      >
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0">
            <p class="truncate font-semibold text-white">{{ item.title }}</p>
            <p class="mt-1 text-xs text-slate-400 sm:text-sm">
              {{ item.meeting_type }} • {{ item.date }}
            </p>
            <p class="mt-1 truncate text-xs text-slate-500">{{ item.location }}</p>
          </div>
          <div class="flex shrink-0 flex-col items-end gap-1">
            <span class="rounded-full border border-white/10 bg-slate-950/60 px-2 py-0.5 text-[10px] text-slate-300">
              {{ item.status }}
            </span>
            <span
              v-if="item.minutes"
              class="rounded-full border border-indigo-400/20 bg-indigo-500/10 px-2 py-0.5 text-[10px] text-indigo-200"
            >
              Com ata
            </span>
          </div>
        </div>
        <p class="mt-2 text-xs text-slate-500">
          {{ item.present_count ?? 0 }} presente(s) • {{ item.attendances_count ?? 0 }} registro(s)
        </p>
      </button>
    </div>

    <div v-if="isModalOpen" class="mobile-overlay fixed inset-0 z-40 flex items-end justify-center bg-slate-950/75 sm:items-center sm:p-4">
      <div class="mobile-sheet max-h-[95dvh] w-full max-w-full overflow-y-auto overscroll-contain rounded-t-3xl border border-white/10 bg-slate-900 p-4 sm:max-w-lg sm:rounded-3xl sm:p-6">
        <div class="flex items-start justify-between gap-3">
          <div>
            <h3 class="text-xl font-bold text-white">Nova reunião</h3>
            <p class="mt-1 text-sm text-slate-400">Após criar, você já poderá registrar a ata e a presença.</p>
          </div>
          <button type="button" class="rounded-2xl border border-white/10 p-2 text-slate-300" @click="closeModal">
            <span class="mdi mdi-close text-xl" />
          </button>
        </div>

        <form class="mt-6 grid gap-4" @submit.prevent="submitCreate">
          <div v-for="field in createFields" :key="field.name">
            <label :for="`create-${field.name}`" class="mb-2 block text-sm font-medium text-slate-200">{{ field.label }}</label>
            <select
              v-if="field.type === 'select'"
              :id="`create-${field.name}`"
              v-model="formState[field.name]"
              class="block w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-indigo-500"
            >
              <option v-for="option in field.options" :key="option.value" :value="option.value">{{ option.label }}</option>
            </select>
            <textarea
              v-else-if="field.type === 'textarea'"
              :id="`create-${field.name}`"
              v-model="formState[field.name]"
              rows="2"
              class="block w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-indigo-500"
            />
            <input
              v-else
              :id="`create-${field.name}`"
              v-model="formState[field.name]"
              :type="field.type"
              class="block w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-indigo-500"
            />
          </div>

          <p v-if="errorMessage" class="rounded-2xl border border-rose-400/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
            {{ errorMessage }}
          </p>

          <button
            type="submit"
            :disabled="submitting"
            class="w-full rounded-2xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:opacity-70"
          >
            {{ submitting ? 'Criando...' : 'Criar e abrir reunião' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { onMounted, reactive, ref, watch } from 'vue'
  import { ApiError } from '@/api'
  import { createResource, listResources, type ResourceRecord } from '@/api/resources'
  import { resourceConfigs } from '@/config/resources'
  import { useAuthStore } from '@/stores/auth'

  const props = defineProps<{
    selectedId?: number | string | null
  }>()

  const emit = defineEmits<{
    select: [id: number | string]
    created: [id: number | string]
  }>()

  const authStore = useAuthStore()
  const allFields = resourceConfigs.meetings.fields
  const createFields = allFields.filter((field) => !['observations', 'agenda_items'].includes(field.name))

  const items = ref<ResourceRecord[]>([])
  const loading = ref(false)
  const submitting = ref(false)
  const search = ref('')
  const isModalOpen = ref(false)
  const errorMessage = ref('')
  const formState = reactive<Record<string, string>>({})

  function resetForm() {
    allFields.forEach((field) => {
      if (field.name === 'status') formState[field.name] = 'Agendada'
      else if (field.name === 'meeting_type') formState[field.name] = 'Ordinária'
      else formState[field.name] = ''
    })
  }

  async function loadMeetings() {
    const token = authStore.accessToken
    if (!token) return

    loading.value = true
    try {
      items.value = await listResources<ResourceRecord>(resourceConfigs.meetings.endpoint, token, search.value)
    } catch {
      items.value = []
    } finally {
      loading.value = false
    }
  }

  function openCreateModal() {
    resetForm()
    errorMessage.value = ''
    isModalOpen.value = true
  }

  function closeModal() {
    isModalOpen.value = false
  }

  async function submitCreate() {
    const token = authStore.accessToken
    if (!token) return

    const missing = createFields.find((field) => field.required && !String(formState[field.name] ?? '').trim())
    if (missing) {
      errorMessage.value = `Preencha o campo: ${missing.label}.`
      return
    }

    submitting.value = true
    errorMessage.value = ''

    try {
      const payload = allFields.reduce<ResourceRecord>((acc, field) => {
        const value = formState[field.name]
        if (value !== '') acc[field.name] = value
        return acc
      }, {})

      const created = await createResource<ResourceRecord>(resourceConfigs.meetings.endpoint, token, payload)
      closeModal()
      await loadMeetings()
      if (created.id != null) {
        emit('created', created.id)
        emit('select', created.id)
      }
    } catch (error) {
      errorMessage.value = error instanceof ApiError ? error.message : 'Não foi possível criar a reunião.'
    } finally {
      submitting.value = false
    }
  }

  watch(() => props.selectedId, () => undefined)

  onMounted(() => {
    resetForm()
    loadMeetings()
  })

  defineExpose({ loadMeetings })
</script>
