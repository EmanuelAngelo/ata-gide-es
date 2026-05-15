<template>
  <section class="min-h-screen bg-slate-950 text-slate-50">
    <div class="mx-auto flex min-h-screen max-w-7xl flex-col lg:flex-row">
      <div class="flex flex-1 items-center justify-center px-6 py-12 sm:px-10 lg:px-16">
        <LoginForm
          :loading="isSubmitting"
          :error-message="errorMessage"
          :initial-username="lastUsername"
          @submit="handleSubmit"
        />
      </div>

      <aside class="relative hidden flex-1 overflow-hidden lg:flex">
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(251,191,36,0.22),_transparent_34%),linear-gradient(160deg,_rgba(15,23,42,1)_8%,_rgba(30,41,59,1)_48%,_rgba(120,53,15,0.9)_100%)]" />
        <div class="absolute -right-24 top-24 h-72 w-72 rounded-full bg-amber-400/10 blur-3xl" />
        <div class="absolute -bottom-24 left-10 h-72 w-72 rounded-full bg-indigo-500/10 blur-3xl" />

        <div class="relative flex w-full flex-col justify-between px-12 py-16">
          <div>
            <p class="text-sm font-semibold uppercase tracking-[0.3em] text-amber-300">
              Gideões Internacionais
            </p>

            <h2 class="mt-6 max-w-md text-4xl font-bold leading-tight text-white">
              Servindo para que a Palavra de Deus chegue mais longe.
            </h2>

            <p class="mt-6 max-w-xl text-base leading-7 text-slate-300">
              Um ambiente para apoiar a organização das reuniões, o registro das atas,
              o acompanhamento das presenças e o planejamento das ações realizadas pelo ministério.
            </p>
          </div>

          <div class="grid gap-4">
            <div class="rounded-3xl border border-white/10 bg-white/5 p-5 backdrop-blur">
              <p class="text-sm font-semibold text-white">
                Missão em movimento
              </p>

              <p class="mt-2 text-sm leading-6 text-slate-300">
                Controle reuniões, decisões e encaminhamentos com mais clareza
                para fortalecer o trabalho de evangelização.
              </p>
            </div>

            <div class="rounded-3xl border border-white/10 bg-white/5 p-5 backdrop-blur">
              <p class="text-sm font-semibold text-white">
                Organização e compromisso
              </p>

              <p class="mt-2 text-sm leading-6 text-slate-300">
                Registre presenças, acompanhe igrejas parceiras e mantenha o
                histórico das ações sempre acessível à secretaria.
              </p>
            </div>

            <div class="rounded-3xl border border-white/10 bg-white/5 p-5 backdrop-blur">
              <p class="text-sm font-semibold text-white">
                Uma ata a serviço da missão
              </p>

              <p class="mt-2 text-sm leading-6 text-slate-300">
                Cada registro ajuda a preservar decisões, responsabilidades e
                próximos passos do trabalho dos Gideões.
              </p>
            </div>
          </div>
        </div>
      </aside>
    </div>
  </section>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { ApiError } from '@/api'
  import LoginForm from '@/components/LoginForm.vue'
  import { useAuthStore } from '@/stores/auth'

  const router = useRouter()
  const authStore = useAuthStore()

  const isSubmitting = ref(false)
  const errorMessage = ref('')
  const lastUsername = ref(authStore.username)

  async function handleSubmit(payload: {
    username: string
    password: string
    rememberMe: boolean
  }) {
    errorMessage.value = ''
    lastUsername.value = payload.username

    if (!payload.username.trim() || !payload.password.trim()) {
      errorMessage.value = 'Preencha usuário e senha para continuar.'
      return
    }

    isSubmitting.value = true

    try {
      await authStore.login({
        username: payload.username.trim(),
        password: payload.password,
      })

      router.push({ name: 'dashboard' })
    } catch (error) {
      if (error instanceof ApiError) {
        errorMessage.value = error.message || 'Não foi possível autenticar com o backend.'
      } else {
        errorMessage.value = 'Erro inesperado ao tentar entrar. Tente novamente.'
      }
    } finally {
      isSubmitting.value = false
    }
  }
</script>