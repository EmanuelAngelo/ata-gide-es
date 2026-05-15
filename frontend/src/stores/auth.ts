import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { obtainJwtTokens, refreshJwtToken, type JwtTokens } from '@/api'

const STORAGE_KEY = 'ata-gideoes.auth'

type StoredAuth = JwtTokens & {
  username: string
}

function loadStoredAuth(): StoredAuth | null {
  if (typeof window === 'undefined') {
    return null
  }

  const raw = window.localStorage.getItem(STORAGE_KEY)

  if (!raw) {
    return null
  }

  try {
    const parsed = JSON.parse(raw) as Partial<StoredAuth>

    if (
      typeof parsed.access !== 'string' ||
      typeof parsed.refresh !== 'string' ||
      typeof parsed.username !== 'string'
    ) {
      return null
    }

    return {
      access: parsed.access,
      refresh: parsed.refresh,
      username: parsed.username,
    }
  } catch {
    return null
  }
}

function persistStoredAuth(value: StoredAuth | null) {
  if (typeof window === 'undefined') {
    return
  }

  if (!value) {
    window.localStorage.removeItem(STORAGE_KEY)
    return
  }

  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(value))
}

export const useAuthStore = defineStore('auth', () => {
  const auth = ref<StoredAuth | null>(loadStoredAuth())

  const isAuthenticated = computed(() => Boolean(auth.value?.access))
  const accessToken = computed(() => auth.value?.access ?? null)
  const refreshToken = computed(() => auth.value?.refresh ?? null)
  const username = computed(() => auth.value?.username ?? '')

  async function login(payload: { username: string; password: string }) {
    const tokens = await obtainJwtTokens(payload)

    auth.value = {
      ...tokens,
      username: payload.username,
    }

    persistStoredAuth(auth.value)
  }

  function logout() {
    auth.value = null
    persistStoredAuth(null)
  }

  async function refreshAccessToken() {
    if (!refreshToken.value) {
      logout()
      return null
    }

    try {
      const response = await refreshJwtToken(refreshToken.value)

      if (!auth.value) {
        return null
      }

      auth.value = {
        ...auth.value,
        access: response.access,
      }

      persistStoredAuth(auth.value)
      return response.access
    } catch {
      logout()
      return null
    }
  }

  return {
    auth,
    isAuthenticated,
    accessToken,
    refreshToken,
    username,
    login,
    logout,
    refreshAccessToken,
  }
})
