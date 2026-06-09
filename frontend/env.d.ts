/// <reference types="vite/client" />
/// <reference types="vite-plugin-vue-layouts-next/client" />

interface ImportMetaEnv {
  /** local = backend local | production = PythonAnywhere */
  readonly VITE_API_MODE?: 'local' | 'production'
  /** Sobrescreve o preset. Deixe vazio ("") para usar o proxy do Vite (/api). */
  readonly VITE_API_BASE_URL?: string
  readonly VITE_PROXY_TARGET?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
