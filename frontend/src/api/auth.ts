import { apiJson } from './api'

export type JwtTokens = {
  access: string
  refresh: string
}

export type LoginPayload = {
  username: string
  password: string
}

export function obtainJwtTokens(payload: LoginPayload) {
  return apiJson<JwtTokens>('/api/auth/token/', {
    method: 'POST',
    body: payload,
  })
}

export function refreshJwtToken(refresh: string) {
  return apiJson<{ access: string }>('/api/auth/token/refresh/', {
    method: 'POST',
    body: { refresh },
  })
}
