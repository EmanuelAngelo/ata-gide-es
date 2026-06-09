<template>
  <div class="w-full min-w-0 max-w-full space-y-4 overflow-x-clip sm:space-y-5">
    <div class="flex flex-col gap-3">
      <div class="min-w-0">
        <h3 class="text-base font-semibold text-white sm:text-lg">Lista de presença</h3>
        <p class="mt-1 text-xs text-slate-400 sm:text-sm">
          Marque os membros que participaram desta reunião.
        </p>
      </div>
      <div class="flex flex-wrap gap-1.5 text-[11px] sm:gap-2 sm:text-xs">
        <span class="rounded-full border border-emerald-400/20 bg-emerald-500/10 px-2.5 py-1 text-emerald-200 sm:px-3">
          {{ presentCount }} presente(s)
        </span>
        <span class="rounded-full border border-rose-400/20 bg-rose-500/10 px-2.5 py-1 text-rose-200 sm:px-3">
          {{ absentCount }} ausente(s)
        </span>
        <span class="rounded-full border border-amber-400/20 bg-amber-500/10 px-2.5 py-1 text-amber-200 sm:px-3">
          {{ justifiedCount }} justificada(s)
        </span>
      </div>
    </div>

    <div class="flex flex-col gap-2">
      <input
        v-model="search"
        type="search"
        placeholder="Buscar membro..."
        class="w-full min-w-0 max-w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-base text-white outline-none transition placeholder:text-slate-500 focus:border-indigo-500 sm:text-sm"
      />
      <button
        type="button"
        class="w-full rounded-2xl border border-white/10 px-4 py-3 text-sm font-medium text-slate-200 transition hover:bg-white/5"
        @click="markAllPresent"
      >
        Marcar todos presentes
      </button>
    </div>

    <div v-if="!filteredRoster.length" class="rounded-2xl border border-dashed border-white/10 bg-white/5 px-4 py-8 text-center text-sm text-slate-400">
      Nenhum membro ativo encontrado para esta lista.
    </div>

    <div v-else class="space-y-2">
      <article
        v-for="item in filteredRoster"
        :key="item.member_id"
        class="min-w-0 overflow-hidden rounded-2xl border border-white/10 bg-white/[0.03] p-3 sm:p-4"
      >
        <div class="min-w-0 space-y-3">
          <div class="min-w-0">
            <p class="break-words font-medium text-white">{{ item.member_name }}</p>
            <p class="mt-0.5 break-words text-xs text-slate-400 sm:text-sm">
              {{ item.member_classification }} • {{ item.member_role || 'Sem função' }}
            </p>
          </div>

          <div class="grid grid-cols-3 gap-1.5 sm:flex sm:flex-wrap sm:gap-2">
            <button
              v-for="status in statusOptions"
              :key="status"
              type="button"
              :class="[
                'min-w-0 rounded-xl px-1.5 py-2 text-[11px] font-medium transition sm:px-3 sm:text-sm',
                item.status === status ? statusActiveClass(status) : 'border border-white/10 text-slate-300 hover:bg-white/5',
              ]"
              @click="setStatus(item.member_id, status)"
            >
              {{ statusShort(status) }}
            </button>
          </div>
        </div>

        <div v-if="item.status === 'Presente'" class="mt-3 grid grid-cols-1 gap-2 sm:grid-cols-2">
          <input
            v-model="item.arrival_time"
            type="text"
            placeholder="Hora de chegada"
            class="w-full min-w-0 max-w-full rounded-xl border border-white/10 bg-slate-950 px-3 py-2 text-base text-white outline-none focus:border-indigo-500 sm:text-sm"
          />
          <input
            v-model="item.observations"
            type="text"
            placeholder="Observações"
            class="w-full min-w-0 max-w-full rounded-xl border border-white/10 bg-slate-950 px-3 py-2 text-base text-white outline-none focus:border-indigo-500 sm:text-sm"
          />
        </div>
      </article>
    </div>

    <div>
      <button
        type="button"
        :disabled="saving"
        class="w-full rounded-2xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-70"
        @click="submitRoster"
      >
        {{ saving ? 'Salvando...' : 'Salvar lista de presença' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { computed, ref, watch } from 'vue'
  import type { AttendanceRosterItem } from '@/api/meetings'

  const props = defineProps<{
    roster: AttendanceRosterItem[]
    saving?: boolean
  }>()

  const emit = defineEmits<{
    save: [roster: AttendanceRosterItem[]]
  }>()

  const statusOptions = ['Presente', 'Ausente', 'Justificada'] as const
  const search = ref('')
  const localRoster = ref<AttendanceRosterItem[]>([])

  watch(
    () => props.roster,
    (value) => {
      localRoster.value = value.map((item) => ({ ...item }))
    },
    { immediate: true, deep: true },
  )

  const filteredRoster = computed(() => {
    const term = search.value.trim().toLowerCase()
    if (!term) return localRoster.value
    return localRoster.value.filter((item) => item.member_name.toLowerCase().includes(term))
  })

  const presentCount = computed(() => localRoster.value.filter((item) => item.status === 'Presente').length)
  const absentCount = computed(() => localRoster.value.filter((item) => item.status === 'Ausente').length)
  const justifiedCount = computed(() => localRoster.value.filter((item) => item.status === 'Justificada').length)

  function statusShort(status: string) {
    if (status === 'Presente') return 'Presente'
    if (status === 'Ausente') return 'Ausente'
    return 'Justif.'
  }

  function statusActiveClass(status: string) {
    if (status === 'Presente') return 'border border-emerald-400/30 bg-emerald-500/15 text-emerald-200'
    if (status === 'Justificada') return 'border border-amber-400/30 bg-amber-500/15 text-amber-200'
    return 'border border-rose-400/30 bg-rose-500/15 text-rose-200'
  }

  function setStatus(memberId: number, status: string) {
    const item = localRoster.value.find((entry) => entry.member_id === memberId)
    if (item) item.status = status
  }

  function markAllPresent() {
    localRoster.value.forEach((item) => {
      item.status = 'Presente'
    })
  }

  function submitRoster() {
    emit('save', localRoster.value)
  }
</script>
