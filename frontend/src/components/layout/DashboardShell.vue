<template>
  <div class="min-h-screen overflow-x-clip bg-slate-950 text-slate-100">
    <div class="flex min-h-screen min-w-0">
      <aside
        :class="[
          'fixed inset-y-0 left-0 z-30 flex w-72 max-w-[calc(100%-1rem)] flex-col border-r border-white/10 bg-slate-900/95 px-3 py-5 backdrop-blur transition-transform duration-300 sm:max-w-xs sm:px-4 sm:py-6 lg:static lg:max-w-none lg:translate-x-0',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full',
        ]"
      >
        <div class="flex items-center justify-between gap-2 px-1 sm:px-2">
          <div class="min-w-0">
            <p class="text-[10px] font-semibold uppercase tracking-[0.15em] text-indigo-300 sm:text-xs sm:tracking-[0.3em]">ATA</p>
            <h1 class="mt-1 truncate text-lg font-semibold text-white sm:mt-2 sm:text-xl">Painel administrativo</h1>
          </div>
          <button class="rounded-xl p-2 text-slate-400 hover:bg-white/5 lg:hidden" @click="sidebarOpen = false">
            <span class="mdi mdi-close text-xl" />
          </button>
        </div>

        <div class="mt-8 rounded-2xl border border-white/10 bg-white/5 p-4">
          <p class="text-sm font-medium text-white">{{ username || 'Usuário autenticado' }}</p>
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
            <span :class="item.icon" class="shrink-0 text-xl" />
            <span class="min-w-0 truncate">{{ item.label }}</span>
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

      <div class="flex min-h-screen min-w-0 flex-1 flex-col lg:pl-0">
        <header class="sticky top-0 z-20 border-b border-white/10 bg-slate-950/80 px-3 py-3 backdrop-blur sm:px-6 sm:py-4 lg:px-10">
          <div class="flex items-center justify-between gap-3">
            <div class="flex min-w-0 flex-1 items-center gap-2 sm:gap-3">
              <button class="shrink-0 rounded-2xl border border-white/10 p-2.5 text-slate-200 hover:bg-white/5 sm:p-3 lg:hidden" @click="sidebarOpen = true">
                <span class="mdi mdi-menu text-xl" />
              </button>
              <div class="min-w-0">
                <p class="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500 sm:text-xs sm:tracking-[0.25em]">Módulo ativo</p>
                <h2 class="mt-0.5 truncate text-base font-semibold text-white sm:mt-1 sm:text-lg">{{ currentLabel }}</h2>
              </div>
            </div>
            <div v-if="username" class="hidden shrink-0 rounded-2xl border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-slate-300 sm:block sm:px-4 sm:py-2 sm:text-sm">
              {{ username }}
            </div>
          </div>
        </header>

        <main class="flex-1 overflow-x-hidden px-3 py-4 sm:px-6 sm:py-6 lg:px-10 lg:py-8">
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
  import { computed, onUnmounted, ref, watch } from 'vue'
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

  const currentRouteName = computed(() => {
    const name = String(route.name ?? 'dashboard')
    if (name === 'meeting-detail') return 'meetings'
    return name
  })
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

  watch(sidebarOpen, (open) => {
    document.body.style.overflow = open ? 'hidden' : ''
  })

  onUnmounted(() => {
    document.body.style.overflow = ''
  })
</script>
