<template>
  <div class="w-full max-w-md rounded-3xl border border-slate-200/80 bg-white p-8 shadow-2xl shadow-slate-950/10 backdrop-blur sm:p-10">
    <div class="mb-8 text-center sm:text-left">
      <img
        src="https://gideoes.org.br/wp-content/uploads/2024/12/logo-branco-2048x665.png"
        alt="Gideões Internacionais no Brasil"
        class="mx-auto h-12 w-auto sm:mx-0"
      />
      <p class="mt-6 text-xs font-semibold uppercase tracking-[0.24em] text-indigo-600">
        Ata de reuniões
      </p>
      <h1 class="mt-3 text-3xl font-bold tracking-tight text-slate-900">
        Entrar no sistema
      </h1>
      <p class="mt-3 text-sm leading-6 text-slate-500">
        Use suas credenciais para acessar o painel administrativo e gerenciar atas,
        reuniões e presenças.
      </p>
    </div>

    <form class="space-y-5" @submit.prevent="submitForm">
      <div>
        <label for="username" class="mb-2 block text-sm font-medium text-slate-700">
          Usuário
        </label>
        <input
          id="username"
          v-model.trim="form.username"
          type="text"
          name="username"
          autocomplete="username"
          placeholder="Digite seu usuário"
          class="block w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-500/10"
        />
      </div>

      <div>
        <div class="mb-2 flex items-center justify-between gap-3">
          <label for="password" class="block text-sm font-medium text-slate-700">
            Senha
          </label>
          <button
            type="button"
            class="text-xs font-semibold text-indigo-600 transition hover:text-indigo-500"
          >
            Esqueci minha senha
          </button>
        </div>

        <div class="relative">
          <input
            id="password"
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            name="password"
            autocomplete="current-password"
            placeholder="Digite sua senha"
            class="block w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 pr-12 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-500/10"
          />
          <button
            type="button"
            class="absolute inset-y-0 right-0 flex items-center px-4 text-slate-400 transition hover:text-slate-600"
            @click="showPassword = !showPassword"
          >
            <span :class="showPassword ? 'mdi mdi-eye-off-outline' : 'mdi mdi-eye-outline'" class="text-xl" />
          </button>
        </div>
      </div>

      <div class="flex items-center justify-between gap-3 text-sm">
        <label class="flex items-center gap-3 text-slate-500">
          <input v-model="rememberMe" type="checkbox" class="h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500" />
          <span>Lembrar acesso</span>
        </label>
        <span class="font-medium text-slate-400">JWT + Django</span>
      </div>

      <div v-if="errorMessage" class="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
        {{ errorMessage }}
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="flex w-full items-center justify-center rounded-2xl bg-indigo-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500 focus:outline-none focus:ring-4 focus:ring-indigo-500/20 disabled:cursor-not-allowed disabled:opacity-70"
      >
        <span v-if="loading" class="mdi mdi-loading mr-2 animate-spin text-lg" />
        {{ loading ? 'Entrando...' : 'Entrar' }}
      </button>
    </form>

    <div class="mt-8 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4 text-sm text-slate-500">
      <p class="font-medium text-slate-700">Acesso institucional</p>
      <p class="mt-1">Caso ainda não tenha acesso, fale com a secretaria responsável pelo sistema ATA.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { reactive, ref, watch } from 'vue'

  const props = defineProps<{
    loading?: boolean
    errorMessage?: string
    initialUsername?: string
  }>()

  const emit = defineEmits<{
    submit: [payload: { username: string; password: string; rememberMe: boolean }]
  }>()

  const showPassword = ref(false)
  const rememberMe = ref(true)
  const form = reactive({
    username: props.initialUsername ?? '',
    password: '',
  })

  watch(
    () => props.initialUsername,
    (value) => {
      form.username = value ?? ''
    },
  )

  function submitForm() {
    emit('submit', {
      username: form.username,
      password: form.password,
      rememberMe: rememberMe.value,
    })
  }

</script>

<style scoped>
  @reference "../styles/tailwind.css";
</style>
