export type ApiMode = 'local' | 'production'

/** URLs padrão por ambiente — sobrescreva com VITE_API_BASE_URL se precisar. */
export const API_URL_PRESETS: Record<ApiMode, string> = {
  local: 'http://127.0.0.1:8002',
  production: 'https://emanuelcoutinho.pythonanywhere.com',
}

function readEnv(key: keyof ImportMetaEnv): string | undefined {
  const value = import.meta.env[key]
  if (value == null) return undefined
  const trimmed = String(value).trim()
  return trimmed === '' ? '' : trimmed
}

/**
 * Resolve a URL base da API:
 * 1. VITE_API_BASE_URL definida (mesmo vazia) → usa esse valor (vazio = proxy do Vite)
 * 2. VITE_API_MODE=local|production → preset correspondente
 * 3. Padrão → production (PythonAnywhere)
 */
export function resolveApiBaseUrl(): string {
  const explicitBase = readEnv('VITE_API_BASE_URL')

  if (explicitBase !== undefined) {
    return explicitBase.replace(/\/$/, '')
  }

  const mode = (readEnv('VITE_API_MODE') ?? 'production') as ApiMode
  const preset = API_URL_PRESETS[mode] ?? API_URL_PRESETS.production
  return preset.replace(/\/$/, '')
}

export function resolveApiMode(): ApiMode {
  const explicitBase = readEnv('VITE_API_BASE_URL')
  if (explicitBase !== undefined && explicitBase !== '') {
    return explicitBase.includes('127.0.0.1') || explicitBase.includes('localhost') ? 'local' : 'production'
  }

  const mode = readEnv('VITE_API_MODE') as ApiMode | undefined
  return mode && mode in API_URL_PRESETS ? mode : 'production'
}

export const API_BASE_URL = resolveApiBaseUrl()
export const API_MODE = resolveApiMode()
