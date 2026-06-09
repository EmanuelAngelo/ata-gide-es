<template>
  <div class="w-full min-w-0 max-w-full space-y-4 overflow-x-clip sm:space-y-5">
    <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h3 class="text-lg font-semibold text-white">Ata da reunião</h3>
        <p class="mt-1 text-sm text-slate-400">
          {{ hasMinutes ? 'Edite o conteúdo oficial desta reunião.' : 'Crie a ata diretamente nesta reunião.' }}
        </p>
      </div>
      <div v-if="hasMinutes && minutesId" class="flex w-full flex-wrap gap-2 sm:w-auto">
        <button
          type="button"
          class="flex-1 rounded-xl border border-emerald-400/20 px-3 py-2 text-sm font-medium text-emerald-200 transition hover:bg-emerald-500/10 sm:flex-none"
          @click="emit('pdf')"
        >
          PDF
        </button>
        <button
          type="button"
          class="flex-1 rounded-xl border border-white/10 px-3 py-2 text-sm font-medium text-slate-200 transition hover:bg-white/5 sm:flex-none"
          @click="emit('print')"
        >
          Impressão
        </button>
      </div>
    </div>

    <form class="grid min-w-0 grid-cols-1 gap-4 md:grid-cols-2" @submit.prevent="submitForm">
      <div class="min-w-0">
        <label class="mb-2 block text-sm font-medium text-slate-200">Hora de abertura</label>
        <input
          v-model="form.opening_time"
          type="text"
          placeholder="Ex: 19:30"
          class="block w-full min-w-0 max-w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-base text-white outline-none transition focus:border-indigo-500 sm:text-sm"
        />
      </div>
      <div class="min-w-0">
        <label class="mb-2 block text-sm font-medium text-slate-200">Hora de encerramento</label>
        <input
          v-model="form.closing_time"
          type="text"
          placeholder="Ex: 21:00"
          class="block w-full min-w-0 max-w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-base text-white outline-none transition focus:border-indigo-500 sm:text-sm"
        />
      </div>
      <div class="min-w-0 md:col-span-2">
        <label class="mb-2 block text-sm font-medium text-slate-200">Texto completo da ata *</label>
        <textarea
          v-model="form.full_text"
          rows="8"
          placeholder="Registre aqui o conteúdo da reunião..."
          class="block w-full min-w-0 max-w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-base text-white outline-none transition focus:border-indigo-500 sm:text-sm"
        />
      </div>
      <div class="min-w-0">
        <label class="mb-2 block text-sm font-medium text-slate-200">Data de aprovação</label>
        <input
          v-model="form.approval_date"
          type="date"
          class="block w-full min-w-0 max-w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-base text-white outline-none transition focus:border-indigo-500 sm:text-sm"
        />
      </div>
      <div class="min-w-0">
        <label class="mb-2 block text-sm font-medium text-slate-200">Status</label>
        <select
          v-model="form.status"
          class="block w-full min-w-0 max-w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-base text-white outline-none transition focus:border-indigo-500 sm:text-sm"
        >
          <option v-for="option in statusOptions" :key="option" :value="option">{{ option }}</option>
        </select>
      </div>
      <div class="min-w-0 md:col-span-2">
        <label class="mb-2 block text-sm font-medium text-slate-200">Assinantes</label>
        <textarea
          v-model="form.signers"
          rows="3"
          placeholder="Nomes dos assinantes..."
          class="block w-full min-w-0 max-w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-base text-white outline-none transition focus:border-indigo-500 sm:text-sm"
        />
      </div>
      <div class="min-w-0 md:col-span-2 flex justify-end">
        <button
          type="submit"
          :disabled="saving"
          class="w-full rounded-2xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-70 sm:w-auto"
        >
          {{ saving ? 'Salvando...' : hasMinutes ? 'Atualizar ata' : 'Criar ata' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
  import { computed, reactive, watch } from 'vue'
  import type { MinutesRecord } from '@/api/meetings'

  const props = defineProps<{
    minutes: MinutesRecord | null
    saving?: boolean
  }>()

  const emit = defineEmits<{
    save: [payload: Record<string, string>]
    pdf: []
    print: []
  }>()

  const statusOptions = ['Rascunho', 'Revisão', 'Aprovada', 'Arquivada']

  const form = reactive({
    opening_time: '',
    closing_time: '',
    full_text: '',
    approval_date: '',
    signers: '',
    status: 'Rascunho',
  })

  const hasMinutes = computed(() => Boolean(props.minutes?.id))
  const minutesId = computed(() => (props.minutes?.id != null ? Number(props.minutes.id) : null))

  function syncForm(minutes: MinutesRecord | null) {
    form.opening_time = String(minutes?.opening_time ?? '')
    form.closing_time = String(minutes?.closing_time ?? '')
    form.full_text = String(minutes?.full_text ?? '')
    form.approval_date = minutes?.approval_date ? String(minutes.approval_date) : ''
    form.signers = String(minutes?.signers ?? '')
    form.status = String(minutes?.status ?? 'Rascunho')
  }

  watch(() => props.minutes, syncForm, { immediate: true, deep: true })

  function submitForm() {
    emit('save', { ...form })
  }
</script>
