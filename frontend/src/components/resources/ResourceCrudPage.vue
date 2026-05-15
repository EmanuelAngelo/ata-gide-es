<template>
  <div class="space-y-6">
    <section class="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl shadow-slate-950/20 backdrop-blur">
      <div class="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
        <div>
          <p class="text-sm font-semibold uppercase tracking-[0.25em] text-indigo-300">CRUD</p>
          <h1 class="mt-3 text-3xl font-bold text-white">{{ config.title }}</h1>
          <p class="mt-3 max-w-3xl text-sm leading-7 text-slate-300">{{ config.description }}</p>
          <p class="mt-2 text-sm text-slate-400">
            Para cadastrar um novo item, use o botão
            <span class="font-semibold text-white">Novo {{ config.singularTitle }}</span>
            no canto direito.
          </p>
        </div>

        <div class="flex flex-col gap-3 sm:flex-row">
          <input
            v-model="search"
            type="search"
            :placeholder="`Buscar em ${config.title.toLowerCase()}`"
            class="min-w-[260px] rounded-2xl border border-white/10 bg-slate-900/70 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10"
            @keydown.enter="loadItems"
          />
          <button
            type="button"
            class="rounded-2xl border border-white/10 px-4 py-3 text-sm font-medium text-slate-200 transition hover:bg-white/5"
            @click="loadItems"
          >
            Buscar
          </button>
          <button
            type="button"
            class="rounded-2xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500"
            @click="openCreateModal"
          >
            Novo {{ config.singularTitle }}
          </button>
        </div>
      </div>
    </section>

    <section class="rounded-3xl border border-white/10 bg-slate-900/70 p-6">
      <div v-if="successMessage" class="mb-4 rounded-2xl border border-emerald-400/20 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-200">
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="mb-4 rounded-2xl border border-rose-400/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
        {{ errorMessage }}
      </div>

      <div class="mb-5 flex items-center justify-between gap-3">
        <p class="text-sm text-slate-400">
          {{ items.length }} registro<span v-if="items.length !== 1">s</span> carregado<span v-if="items.length !== 1">s</span>
        </p>
        <button
          type="button"
          class="text-sm font-medium text-slate-300 transition hover:text-white"
          @click="loadItems"
        >
          Atualizar
        </button>
      </div>

      <div v-if="loading" class="rounded-2xl border border-white/10 bg-white/5 px-4 py-10 text-center text-sm text-slate-300">
        Carregando dados do backend...
      </div>

      <div v-else-if="!items.length" class="rounded-2xl border border-dashed border-white/10 bg-white/5 px-4 py-10 text-center text-sm text-slate-400">
        <p>{{ config.emptyMessage }}</p>
        <button
          type="button"
          class="mt-5 rounded-2xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500"
          @click="openCreateModal"
        >
          Cadastrar {{ config.singularTitle }}
        </button>
      </div>

      <div v-else class="space-y-3">
        <article
          v-for="item in items"
          :key="itemKey(item)"
          class="overflow-hidden rounded-2xl border border-white/10 bg-white/5 transition duration-200 hover:border-white/20"
        >
          <button
            type="button"
            class="flex w-full flex-col gap-4 px-4 py-4 text-left transition hover:bg-white/[0.03] sm:px-5"
            @click="toggleExpanded(item)"
          >
            <div class="flex items-start justify-between gap-4">
              <div class="min-w-0 flex-1">
                <p class="text-base font-semibold text-white">
                  {{ formatValue(item[config.columns[0]?.key]) }}
                </p>
                <p class="mt-1 text-sm text-slate-400">
                  Clique para {{ isExpanded(item) ? 'ocultar' : 'exibir' }} os detalhes completos.
                </p>
              </div>

              <div class="flex items-center gap-3">
                <span class="rounded-full border border-indigo-400/20 bg-indigo-500/10 px-3 py-1 text-xs font-medium text-indigo-200">
                  {{ config.singularTitle }}
                </span>
                <span
                  :class="isExpanded(item) ? 'rotate-180' : ''"
                  class="mdi mdi-chevron-down text-2xl text-slate-400 transition-transform"
                />
              </div>
            </div>

            <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
              <div
                v-for="column in summaryColumns"
                :key="column.key"
                class="rounded-xl border border-white/8 bg-slate-950/30 px-3 py-2"
              >
                <p class="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                  {{ column.label }}
                </p>
                <p class="mt-1 truncate text-sm text-slate-100">
                  {{ formatValue(item[column.key]) }}
                </p>
              </div>
            </div>
          </button>

          <div
            v-if="isExpanded(item)"
            class="border-t border-white/10 bg-slate-950/35 px-4 py-5 sm:px-5"
          >
            <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              <div
                v-for="field in detailFields"
                :key="field.key"
                class="rounded-2xl border border-white/10 bg-white/[0.03] px-4 py-3"
              >
                <p class="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                  {{ field.label }}
                </p>
                <p class="mt-2 whitespace-pre-wrap break-words text-sm text-slate-100">
                  {{ formatValue(item[field.key]) }}
                </p>
              </div>
            </div>

            <div class="mt-5 flex flex-col gap-2 sm:flex-row sm:justify-end">
              <button
                v-if="config.routeName === 'minutes'"
                type="button"
                class="rounded-xl border border-emerald-400/20 px-4 py-2 text-sm font-medium text-emerald-200 transition hover:bg-emerald-500/10"
                @click="openMinutePdf(item)"
              >
                PDF
              </button>
              <button
                v-if="config.routeName === 'minutes'"
                type="button"
                class="rounded-xl border border-white/10 px-4 py-2 text-sm font-medium text-slate-200 transition hover:bg-white/5"
                @click="openMinutePrint(item)"
              >
                Visualizar impressão
              </button>
              <button
                type="button"
                class="rounded-xl border border-white/10 px-4 py-2 text-sm font-medium text-slate-200 transition hover:bg-white/5"
                @click="openEditModal(item)"
              >
                Editar
              </button>
              <button
                type="button"
                class="rounded-xl border border-rose-400/20 px-4 py-2 text-sm font-medium text-rose-200 transition hover:bg-rose-500/10"
                @click="removeItem(item)"
              >
                Excluir
              </button>
            </div>
          </div>
        </article>
      </div>
    </section>

    <div v-if="isModalOpen" class="fixed inset-0 z-40 flex items-center justify-center bg-slate-950/75 px-4 py-6">
      <div class="max-h-[92vh] w-full max-w-4xl overflow-y-auto rounded-3xl border border-white/10 bg-slate-900 p-6 shadow-2xl shadow-slate-950/40">
        <div class="flex items-start justify-between gap-4">
          <div>
            <p class="text-sm font-semibold uppercase tracking-[0.25em] text-indigo-300">Formulário</p>
            <h2 class="mt-2 text-2xl font-bold text-white">
              {{ editingId == null ? `Novo ${config.singularTitle}` : `Editar ${config.singularTitle}` }}
            </h2>
          </div>
          <button type="button" class="rounded-2xl border border-white/10 p-3 text-slate-300 transition hover:bg-white/5" @click="closeModal">
            <span class="mdi mdi-close text-xl" />
          </button>
        </div>

        <form class="mt-8 grid gap-5 md:grid-cols-2" @submit.prevent="submitForm">
          <div v-for="field in visibleFields" :key="field.name" :class="field.type === 'textarea' ? 'md:col-span-2' : ''">
            <label :for="field.name" class="mb-2 block text-sm font-medium text-slate-200">{{ field.label }}</label>

            <div
              v-if="config.routeName === 'church-schedules' && field.name === 'church_name'"
              class="space-y-3"
            >
              <input
                :id="field.name"
                v-model="formState[field.name]"
                type="text"
                :list="churchDatalistId"
                :placeholder="field.placeholder ?? field.label"
                class="block w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10"
                @input="handleChurchInput"
              />

              <datalist :id="churchDatalistId">
                <option
                  v-for="church in partnerChurchOptions"
                  :key="String(church.id ?? church.name)"
                  :value="String(church.name ?? '')"
                />
              </datalist>

              <p class="text-xs text-slate-400">
                Você pode selecionar uma igreja parceira já cadastrada ou apenas digitar o nome manualmente.
              </p>
            </div>

            <select
              v-else-if="field.type === 'select'"
              :id="field.name"
              v-model="formState[field.name]"
              class="block w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10"
              @change="handleSelectChange(field.name)"
            >
              <option value="">Selecione</option>
              <option v-for="option in getFieldOptions(field)" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>

            <textarea
              v-else-if="field.type === 'textarea'"
              :id="field.name"
              v-model="formState[field.name]"
              rows="4"
              :placeholder="field.placeholder ?? field.label"
              class="block w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10"
            />

            <input
              v-else
              :id="field.name"
              v-model="formState[field.name]"
              :type="field.type"
              :placeholder="field.placeholder ?? field.label"
              class="block w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10"
            />
          </div>

          <div class="md:col-span-2 flex flex-col-reverse gap-3 pt-2 sm:flex-row sm:justify-end">
            <button type="button" class="rounded-2xl border border-white/10 px-4 py-3 text-sm font-medium text-slate-300 transition hover:bg-white/5" @click="closeModal">
              Cancelar
            </button>
            <button type="submit" :disabled="submitting" class="rounded-2xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-70">
              {{ submitting ? 'Salvando...' : 'Salvar' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { computed, onMounted, reactive, ref } from 'vue'
  import { ApiError, buildUrl, createResource, deleteResource, getResourceCollection, listResources, updateResource, type ResourceRecord } from '@/api'
  import type { ResourceConfig } from '@/config/resources'
  import { useAuthStore } from '@/stores/auth'

  const props = defineProps<{
    config: ResourceConfig
  }>()

  const authStore = useAuthStore()

  const items = ref<ResourceRecord[]>([])
  const loading = ref(false)
  const submitting = ref(false)
  const errorMessage = ref('')
  const successMessage = ref('')
  const search = ref('')
  const isModalOpen = ref(false)
  const editingId = ref<number | string | null>(null)
  const expandedItemKey = ref<string | null>(null)
  const partnerChurchOptions = ref<ResourceRecord[]>([])
  const memberOptions = ref<ResourceRecord[]>([])
  const meetingOptions = ref<ResourceRecord[]>([])
  const formState = reactive<Record<string, string>>({})

  const token = computed(() => authStore.accessToken)
  const churchDatalistId = computed(() => `church-datalist-${props.config.routeName}`)
  const visibleFields = computed(() =>
    props.config.fields.filter(
      (field) => {
        if (props.config.routeName === 'church-schedules' && field.name === 'church_id') {
          return false
        }

        if (
          props.config.routeName === 'attendances' &&
          ['member_name', 'member_classification', 'member_role'].includes(field.name)
        ) {
          return false
        }

        return true
      },
    ),
  )
  const summaryColumns = computed(() => props.config.columns.slice(0, Math.min(4, props.config.columns.length)))
  const detailFields = computed(() => {
    const configFields = props.config.fields.map((field) => ({ key: field.name, label: field.label }))
    const missingColumns = props.config.columns
      .filter((column) => !configFields.some((field) => field.key === column.key))
      .map((column) => ({ key: column.key, label: column.label }))

    return [...configFields, ...missingColumns]
  })

  function itemKey(item: ResourceRecord) {
    return String(item.id ?? JSON.stringify(item))
  }

  function getFieldOptions(field: ResourceConfig['fields'][number]) {
    if (props.config.routeName === 'attendances' && field.name === 'member_id') {
      return memberOptions.value.map((member) => ({
        label: `${String(member.full_name ?? 'Membro sem nome')}${member.official_role ? ` • ${String(member.official_role)}` : ''}`,
        value: String(member.id ?? ''),
      }))
    }

    if (['attendances', 'minutes'].includes(props.config.routeName) && field.name === 'meeting_id') {
      return meetingOptions.value.map((meeting) => ({
        label: `${String(meeting.title ?? 'Reunião')} • ${String(meeting.date ?? 'Sem data')}`,
        value: String(meeting.id ?? ''),
      }))
    }

    return field.options ?? []
  }

  function isExpanded(item: ResourceRecord) {
    return expandedItemKey.value === itemKey(item)
  }

  function toggleExpanded(item: ResourceRecord) {
    const nextKey = itemKey(item)
    expandedItemKey.value = expandedItemKey.value === nextKey ? null : nextKey
  }

  function getInitialFormState() {
    return Object.fromEntries(props.config.fields.map((field) => [field.name, '']))
  }

  function resetForm(payload?: ResourceRecord) {
    const nextState = getInitialFormState()

    Object.keys(formState).forEach((key) => {
      delete formState[key]
    })

    Object.entries(nextState).forEach(([key, value]) => {
      formState[key] = payload?.[key] == null ? value : String(payload[key])
    })

    if (props.config.routeName === 'church-schedules' && payload?.church_name) {
      autoFillChurchFields(String(payload.church_name))
    }

    if (props.config.routeName === 'attendances' && payload?.member_id) {
      autoFillAttendanceFields()
    }
  }

  function formatValue(value: unknown) {
    if (value == null || value === '') return '—'
    if (typeof value === 'boolean') return value ? 'Sim' : 'Não'
    return String(value)
  }

  async function loadItems() {
    if (!token.value) {
      errorMessage.value = 'Sessão expirada. Faça login novamente.'
      return
    }

    loading.value = true
    errorMessage.value = ''

    try {
      items.value = await listResources<ResourceRecord>(props.config.endpoint, token.value, search.value)
      expandedItemKey.value = null
    } catch (error) {
      errorMessage.value =
        error instanceof ApiError ? error.message : 'Não foi possível carregar os dados deste módulo.'
    } finally {
      loading.value = false
    }
  }

  function openCreateModal() {
    editingId.value = null
    errorMessage.value = ''
    resetForm()
    isModalOpen.value = true
  }

  function openEditModal(item: ResourceRecord) {
    editingId.value = (item.id as number | string | undefined) ?? null
    errorMessage.value = ''
    resetForm(item)
    isModalOpen.value = true
  }

  function closeModal() {
    isModalOpen.value = false
    editingId.value = null
    resetForm()
  }

  function findPartnerChurchByName(name: string) {
    const normalizedName = name.trim().toLowerCase()

    return partnerChurchOptions.value.find(
      (church) => String(church.name ?? '').trim().toLowerCase() === normalizedName,
    )
  }

  function autoFillChurchFields(name: string) {
    if (props.config.routeName !== 'church-schedules') {
      return
    }

    const matchedChurch = findPartnerChurchByName(name)

    if (!matchedChurch) {
      formState.church_id = ''
      return
    }

    formState.church_id = matchedChurch.id == null ? '' : String(matchedChurch.id)
    formState.church_name = String(matchedChurch.name ?? formState.church_name ?? '')
    formState.pastor_name = String(matchedChurch.pastor_name ?? '')
    formState.church_phone = String(matchedChurch.phone ?? '')
    formState.address = String(matchedChurch.address ?? '')
    formState.neighborhood = String(matchedChurch.neighborhood ?? '')
    formState.city = String(matchedChurch.city ?? '')
  }

  function autoFillAttendanceFields() {
    if (props.config.routeName !== 'attendances') {
      return
    }

    const selectedMember = memberOptions.value.find(
      (member) => String(member.id ?? '') === String(formState.member_id ?? ''),
    )

    if (!selectedMember) {
      formState.member_name = ''
      formState.member_classification = ''
      formState.member_role = ''
      return
    }

    formState.member_name = String(selectedMember.full_name ?? '')
    formState.member_classification = String(selectedMember.classification ?? '')
    formState.member_role = String(selectedMember.official_role ?? '')
  }

  function handleChurchInput() {
    autoFillChurchFields(formState.church_name)
  }

  function handleSelectChange(fieldName: string) {
    if (props.config.routeName === 'attendances' && fieldName === 'member_id') {
      autoFillAttendanceFields()
    }
  }

  async function loadPartnerChurchOptions() {
    if (props.config.routeName !== 'church-schedules' || !token.value) {
      return
    }

    try {
      const response = await getResourceCollection<ResourceRecord>('/api/partner-churches/', token.value)
      partnerChurchOptions.value = response.items
    } catch {
      partnerChurchOptions.value = []
    }
  }

  async function loadAttendanceDependencies() {
    if (!['attendances', 'minutes'].includes(props.config.routeName) || !token.value) {
      return
    }

    try {
      const meetingsPromise = getResourceCollection<ResourceRecord>('/api/meetings/', token.value)
      const membersPromise = props.config.routeName === 'attendances'
        ? getResourceCollection<ResourceRecord>('/api/members/', token.value)
        : Promise.resolve({ items: [], count: 0, next: null, previous: null })

      const [membersResponse, meetingsResponse] = await Promise.all([membersPromise, meetingsPromise])

      memberOptions.value = membersResponse.items
      meetingOptions.value = meetingsResponse.items
    } catch {
      memberOptions.value = []
      meetingOptions.value = []
    }
  }

  function buildPayload() {
    return props.config.fields.reduce<ResourceRecord>((payload, field) => {
      const value = formState[field.name]

      if (value !== '') {
        payload[field.name] = value
      }

      return payload
    }, {})
  }

  async function submitForm() {
    if (!token.value) {
      errorMessage.value = 'Sessão expirada. Faça login novamente.'
      return
    }

    const missingRequired = props.config.fields.find((field) => field.required && !String(formState[field.name] ?? '').trim())

    if (missingRequired) {
      errorMessage.value = `Preencha o campo obrigatório: ${missingRequired.label}.`
      return
    }

    submitting.value = true
    errorMessage.value = ''
    successMessage.value = ''

    try {
      const payload = buildPayload()

      if (editingId.value == null) {
        await createResource(props.config.endpoint, token.value, payload)
        successMessage.value = `${props.config.singularTitle} cadastrado com sucesso.`
      } else {
        await updateResource(props.config.endpoint, editingId.value, token.value, payload)
        successMessage.value = `${props.config.singularTitle} atualizado com sucesso.`
      }

      closeModal()
      await loadItems()
    } catch (error) {
      errorMessage.value = error instanceof ApiError ? error.message : 'Não foi possível salvar o registro.'
    } finally {
      submitting.value = false
    }
  }


  async function fetchProtectedFile(path: string) {
    if (!token.value) {
      errorMessage.value = 'Sessão expirada. Faça login novamente.'
      return null
    }

    const response = await fetch(buildUrl(path), {
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    })

    if (!response.ok) {
      throw new Error(`Falha ao buscar arquivo: ${response.status}`)
    }

    return response
  }

  async function openMinutePdf(item: ResourceRecord) {
    const id = item.id as number | string | undefined

    if (id == null) {
      errorMessage.value = 'Não foi possível identificar esta ata para gerar PDF.'
      return
    }

    try {
      const response = await fetchProtectedFile(`/api/minutes/${id}/pdf/`)
      if (!response) return
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

  async function openMinutePrint(item: ResourceRecord) {
    const id = item.id as number | string | undefined

    if (id == null) {
      errorMessage.value = 'Não foi possível identificar esta ata para impressão.'
      return
    }

    try {
      const response = await fetchProtectedFile(`/api/minutes/${id}/print/`)
      if (!response) return
      const html = await response.text()
      const printWindow = window.open('', '_blank', 'noopener,noreferrer')
      if (!printWindow) return
      printWindow.document.open()
      printWindow.document.write(html)
      printWindow.document.close()
    } catch {
      errorMessage.value = 'Não foi possível abrir a visualização de impressão desta ata.'
    }
  }

  async function removeItem(item: ResourceRecord) {
    if (!token.value) {
      errorMessage.value = 'Sessão expirada. Faça login novamente.'
      return
    }

    const id = item.id as number | string | undefined

    if (id == null) {
      errorMessage.value = 'Não foi possível identificar este registro para exclusão.'
      return
    }

    const confirmed = window.confirm(`Deseja realmente excluir este ${props.config.singularTitle}?`)

    if (!confirmed) {
      return
    }

    try {
      await deleteResource(props.config.endpoint, id, token.value)
      await loadItems()
    } catch (error) {
      errorMessage.value = error instanceof ApiError ? error.message : 'Não foi possível excluir o registro.'
    }
  }

  onMounted(() => {
    resetForm()
    loadPartnerChurchOptions()
    loadAttendanceDependencies()
    loadItems()
  })
</script>
