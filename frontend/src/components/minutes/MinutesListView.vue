<template>
  <div class="space-y-4 sm:space-y-6">
    <section class="rounded-2xl border border-white/10 bg-white/5 p-4 shadow-2xl shadow-slate-950/20 backdrop-blur sm:rounded-3xl sm:p-6">
      <h1 class="text-2xl font-bold text-white sm:text-3xl">Atas</h1>
      <p class="mt-2 max-w-3xl text-sm leading-6 text-slate-300 sm:leading-7">
        Consulte e edite as atas já registradas. Para criar uma nova ata, acesse a reunião correspondente em
        <router-link :to="{ name: 'meetings' }" class="font-medium text-indigo-300 hover:text-indigo-200">Reuniões</router-link>.
      </p>

      <div class="mt-4 flex flex-col gap-2 sm:flex-row">
        <input
          v-model="search"
          type="search"
          placeholder="Buscar atas..."
          class="w-full min-w-0 flex-1 rounded-2xl border border-white/10 bg-slate-900/70 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10"
          @keydown.enter="loadItems"
        />
        <button
          type="button"
          class="rounded-2xl border border-white/10 px-4 py-3 text-sm font-medium text-slate-200 transition hover:bg-white/5"
          @click="loadItems"
        >
          Buscar
        </button>
      </div>
    </section>

    <section class="rounded-2xl border border-white/10 bg-slate-900/70 p-4 sm:rounded-3xl sm:p-6">
      <div v-if="successMessage" class="mb-4 rounded-2xl border border-emerald-400/20 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-200">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="mb-4 rounded-2xl border border-rose-400/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
        {{ errorMessage }}
      </div>

      <div class="mb-5 flex items-center justify-between gap-3">
        <p class="text-sm text-slate-400">{{ items.length }} ata(s) encontrada(s)</p>
        <button type="button" class="text-sm font-medium text-slate-300 transition hover:text-white" @click="loadItems">
          Atualizar
        </button>
      </div>

      <div v-if="loading" class="rounded-2xl border border-white/10 bg-white/5 px-4 py-10 text-center text-sm text-slate-300">
        Carregando atas...
      </div>

      <div v-else-if="!items.length" class="rounded-2xl border border-dashed border-white/10 bg-white/5 px-4 py-10 text-center text-sm text-slate-400">
        <p>Nenhuma ata registrada ainda.</p>
        <router-link
          :to="{ name: 'meetings' }"
          class="mt-5 inline-block rounded-2xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500"
        >
          Ir para Reuniões
        </router-link>
      </div>

      <div v-else class="space-y-3">
        <article
          v-for="item in items"
          :key="String(item.id)"
          class="overflow-hidden rounded-2xl border border-white/10 bg-white/5 transition hover:border-white/20"
        >
          <div class="flex flex-col gap-3 px-4 py-4 sm:flex-row sm:items-start sm:justify-between sm:px-5">
            <div class="min-w-0 flex-1">
              <p class="text-base font-semibold text-white">{{ formatValue(item.meeting_title) }}</p>
              <p class="mt-1 text-sm text-slate-400">
                {{ formatValue(item.status) }}
                <span v-if="item.approval_date"> • Aprovada em {{ formatValue(item.approval_date) }}</span>
              </p>
              <p class="mt-2 line-clamp-2 text-sm text-slate-300">{{ formatValue(item.full_text) }}</p>
            </div>
            <span class="self-start rounded-full border border-indigo-400/20 bg-indigo-500/10 px-3 py-1 text-xs font-medium text-indigo-200">
              {{ formatValue(item.status) }}
            </span>
          </div>

          <div class="flex flex-col gap-2 border-t border-white/10 bg-slate-950/30 px-4 py-3 sm:flex-row sm:flex-wrap sm:px-5">
            <button
              type="button"
              class="w-full rounded-xl border border-indigo-400/20 px-4 py-2.5 text-sm font-medium text-indigo-200 transition hover:bg-indigo-500/10 sm:w-auto"
              @click="openReadModal(item)"
            >
              Ler ata
            </button>
            <button
              type="button"
              class="w-full rounded-xl border border-white/10 px-4 py-2.5 text-sm font-medium text-slate-200 transition hover:bg-white/5 sm:w-auto"
              @click="openEditModal(item)"
            >
              Editar
            </button>
            <button
              type="button"
              class="w-full rounded-xl border border-emerald-400/20 px-4 py-2.5 text-sm font-medium text-emerald-200 transition hover:bg-emerald-500/10 sm:w-auto"
              @click="openMinutePdf(item)"
            >
              PDF
            </button>
            <button
              type="button"
              class="w-full rounded-xl border border-white/10 px-4 py-2.5 text-sm font-medium text-slate-200 transition hover:bg-white/5 sm:w-auto"
              @click="openMinutePrint(item)"
            >
              Impressão
            </button>
            <router-link
              v-if="item.meeting_id"
              :to="{ name: 'meeting-detail', params: { id: String(item.meeting_id) } }"
              class="w-full rounded-xl border border-white/10 px-4 py-2.5 text-center text-sm font-medium text-slate-200 transition hover:bg-white/5 sm:w-auto"
            >
              Abrir reunião
            </router-link>
          </div>
        </article>
      </div>
    </section>

    <!-- Modal leitura -->
    <div v-if="readingItem" class="mobile-overlay fixed inset-0 z-40 flex items-end justify-center bg-slate-950/75 sm:items-center sm:p-4">
      <div class="mobile-sheet max-h-[95dvh] w-full max-w-full overflow-y-auto overscroll-contain rounded-t-3xl border border-white/10 bg-slate-900 p-4 sm:max-h-[92dvh] sm:max-w-3xl sm:rounded-3xl sm:p-6">
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0">
            <p class="text-xs font-semibold uppercase tracking-[0.25em] text-indigo-300">Leitura</p>
            <h2 class="mt-1 text-xl font-bold text-white sm:text-2xl">{{ formatValue(readingItem.meeting_title) }}</h2>
            <p class="mt-2 text-sm text-slate-400">
              Abertura: {{ formatValue(readingItem.opening_time) }} • Encerramento: {{ formatValue(readingItem.closing_time) }}
            </p>
          </div>
          <button type="button" class="shrink-0 rounded-2xl border border-white/10 p-2 text-slate-300" @click="readingItem = null">
            <span class="mdi mdi-close text-xl" />
          </button>
        </div>

        <div class="mt-6 space-y-4">
          <div class="flex flex-wrap gap-2 text-xs">
            <span class="rounded-full border border-white/10 bg-slate-950/60 px-3 py-1 text-slate-200">
              Status: {{ formatValue(readingItem.status) }}
            </span>
            <span v-if="readingItem.approval_date" class="rounded-full border border-white/10 bg-slate-950/60 px-3 py-1 text-slate-200">
              Aprovação: {{ formatValue(readingItem.approval_date) }}
            </span>
          </div>

          <div class="rounded-2xl border border-white/10 bg-slate-950/50 p-4 sm:p-6">
            <p class="whitespace-pre-wrap break-words text-sm leading-7 text-slate-100 sm:text-base">
              {{ formatValue(readingItem.full_text) }}
            </p>
          </div>

          <div v-if="readingItem.signers" class="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
            <p class="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Assinantes</p>
            <p class="mt-2 whitespace-pre-wrap text-sm text-slate-200">{{ formatValue(readingItem.signers) }}</p>
          </div>
        </div>

        <div class="mt-6 flex flex-col gap-2 sm:flex-row sm:justify-end">
          <button
            type="button"
            class="rounded-2xl border border-white/10 px-4 py-3 text-sm font-medium text-slate-200 transition hover:bg-white/5"
            @click="openEditModal(readingItem); readingItem = null"
          >
            Editar ata
          </button>
          <button
            type="button"
            class="rounded-2xl bg-indigo-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500"
            @click="readingItem = null"
          >
            Fechar
          </button>
        </div>
      </div>
    </div>

    <!-- Modal edição -->
    <div v-if="editingItem" class="mobile-overlay fixed inset-0 z-40 flex items-end justify-center bg-slate-950/75 sm:items-center sm:p-4">
      <div class="mobile-sheet max-h-[95dvh] w-full max-w-full overflow-y-auto overscroll-contain rounded-t-3xl border border-white/10 bg-slate-900 p-4 sm:max-h-[92dvh] sm:max-w-4xl sm:rounded-3xl sm:p-6">
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0">
            <p class="text-xs font-semibold uppercase tracking-[0.25em] text-indigo-300">Edição</p>
            <h2 class="mt-1 text-xl font-bold text-white sm:text-2xl">Editar ata</h2>
            <p class="mt-1 text-sm text-slate-400">Reunião: {{ formatValue(editingItem.meeting_title) }}</p>
          </div>
          <button type="button" class="shrink-0 rounded-2xl border border-white/10 p-2 text-slate-300" @click="closeEditModal">
            <span class="mdi mdi-close text-xl" />
          </button>
        </div>

        <MeetingMinutesPanel
          class="mt-6"
          :minutes="editingItem"
          :saving="submitting"
          @save="submitEdit"
          @pdf="openMinutePdf(editingItem)"
          @print="openMinutePrint(editingItem)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { onMounted, ref } from 'vue'
  import { ApiError } from '@/api'
  import { fetchProtectedMeetingFile, type MinutesRecord } from '@/api/meetings'
  import { listResources, updateResource, type ResourceRecord } from '@/api/resources'
  import MeetingMinutesPanel from '@/components/meetings/MeetingMinutesPanel.vue'
  import { resourceConfigs } from '@/config/resources'
  import { useAuthStore } from '@/stores/auth'

  const authStore = useAuthStore()

  const items = ref<MinutesRecord[]>([])
  const loading = ref(false)
  const submitting = ref(false)
  const search = ref('')
  const errorMessage = ref('')
  const successMessage = ref('')
  const readingItem = ref<MinutesRecord | null>(null)
  const editingItem = ref<MinutesRecord | null>(null)

  function formatValue(value: unknown) {
    if (value == null || value === '') return '—'
    return String(value)
  }

  async function loadItems() {
    const token = authStore.accessToken
    if (!token) return

    loading.value = true
    errorMessage.value = ''

    try {
      items.value = await listResources<MinutesRecord>(resourceConfigs.minutes.endpoint, token, search.value)
    } catch (error) {
      errorMessage.value = error instanceof ApiError ? error.message : 'Não foi possível carregar as atas.'
    } finally {
      loading.value = false
    }
  }

  function openReadModal(item: MinutesRecord) {
    readingItem.value = item
  }

  function openEditModal(item: MinutesRecord) {
    editingItem.value = { ...item }
  }

  function closeEditModal() {
    editingItem.value = null
  }

  async function submitEdit(payload: Record<string, string>) {
    const token = authStore.accessToken
    const id = editingItem.value?.id
    if (!token || id == null) return

    if (!payload.full_text.trim()) {
      errorMessage.value = 'O texto da ata é obrigatório.'
      return
    }

    submitting.value = true
    errorMessage.value = ''
    successMessage.value = ''

    try {
      const body: ResourceRecord = { ...payload }
      if (!body.approval_date) delete body.approval_date

      await updateResource(resourceConfigs.minutes.endpoint, id, token, body)
      successMessage.value = 'Ata atualizada com sucesso.'
      closeEditModal()
      await loadItems()
    } catch (error) {
      errorMessage.value = error instanceof ApiError ? error.message : 'Não foi possível salvar a ata.'
    } finally {
      submitting.value = false
    }
  }

  async function openMinutePdf(item: MinutesRecord) {
    const token = authStore.accessToken
    const id = item.id
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
      errorMessage.value = 'Não foi possível gerar o PDF.'
    }
  }

  async function openMinutePrint(item: MinutesRecord) {
    const token = authStore.accessToken
    const id = item.id
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
      errorMessage.value = 'Não foi possível abrir a impressão.'
    }
  }

  onMounted(loadItems)
</script>
