<template>
  <div class="min-h-screen bg-slate-950 text-slate-100">
    <div class="flex min-h-screen">
      <aside
        :class="[
          'fixed inset-y-0 left-0 z-30 flex w-72 flex-col border-r border-white/10 bg-slate-900/95 px-4 py-6 backdrop-blur transition-transform duration-300 lg:static lg:translate-x-0',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full',
        ]"
      >
        <div class="flex items-center justify-between px-2">
          <div>
            <p class="text-xs font-semibold uppercase tracking-[0.3em] text-indigo-300">ATA</p>
            <h1 class="mt-2 text-xl font-semibold text-white">Painel administrativo</h1>
          </div>
          <button class="rounded-xl p-2 text-slate-400 hover:bg-white/5 lg:hidden" @click="sidebarOpen = false">
            <span class="mdi mdi-close text-xl" />
          </button>
        </div>

        <div class="mt-8 rounded-2xl border border-white/10 bg-white/5 p-4">
          <p class="text-sm font-medium text-white">{{ username || 'Usuário autenticado' }}</p>
          <p class="mt-1 text-sm text-slate-400">Conectado via Django JWT</p>
        </div>

        <nav class="mt-8 flex-1 space-y-2">
          <button
            v-for="item in items"
            :key="item.key"
            type="button"
            :class="[
              'flex w-full items-center gap-3 rounded-2xl px-4 py-3 text-left text-sm font-medium transition',
              item.key === currentRouteName
                ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-950/30'
                : 'text-slate-300 hover:bg-white/5 hover:text-white',
            ]"
            @click="navigateTo(item.key)"
          >
            <span :class="item.icon" class="text-xl" />
            <span>{{ item.label }}</span>
          </button>
        </nav>

        <button
          type="button"
          class="mt-6 flex items-center justify-center gap-2 rounded-2xl border border-white/10 px-4 py-3 text-sm font-medium text-slate-200 transition hover:bg-white/5"
          @click="$emit('logout')"
        >
          <span class="mdi mdi-logout text-lg" />
          <span>Sair</span>
        </button>
      </aside>

      <div class="flex min-h-screen flex-1 flex-col lg:pl-0">
        <header class="sticky top-0 z-20 border-b border-white/10 bg-slate-950/80 px-4 py-4 backdrop-blur sm:px-6 lg:px-10">
          <div class="flex items-center justify-between gap-4">
            <div class="flex items-center gap-3">
              <button class="rounded-2xl border border-white/10 p-3 text-slate-200 hover:bg-white/5 lg:hidden" @click="sidebarOpen = true">
                <span class="mdi mdi-menu text-xl" />
              </button>
              <div>
                <p class="text-xs font-semibold uppercase tracking-[0.25em] text-slate-500">Módulo ativo</p>
                <h2 class="mt-1 text-lg font-semibold text-white">{{ currentLabel }}</h2>
              </div>
            </div>
            <div class="hidden rounded-2xl border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-300 sm:block">
              Conteúdo empurrado lateralmente com layout responsivo
            </div>
          </div>
        </header>

        <main class="flex-1 px-4 py-6 sm:px-6 lg:px-10 lg:py-8">
          <slot />
        </main>
      </div>
    </div>

    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-20 bg-slate-950/60 lg:hidden"
      @click="sidebarOpen = false"
    />
  </div>
</template>

<script setup lang="ts">
  import { computed, ref, watch } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import type { NavigationItem } from '@/config/navigation'

  const props = defineProps<{
    items: NavigationItem[]
    username?: string
  }>()

  defineEmits<{
    logout: []
  }>()

  const route = useRoute()
  const router = useRouter()
  const sidebarOpen = ref(false)

  const currentRouteName = computed(() => String(route.name ?? 'dashboard'))
  const currentLabel = computed(() => props.items.find((item) => item.key === currentRouteName.value)?.label || 'Dashboard')

  function navigateTo(routeName: NavigationItem['key']) {
    router.push({ name: routeName })
  }

  watch(
    () => route.fullPath,
    () => {
      sidebarOpen.value = false
    },
  )
</script>
