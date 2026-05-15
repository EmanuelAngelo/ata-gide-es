export class ApiError extends Error {
  status: number
  data: unknown

  constructor(message: string, status: number, data: unknown) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.data = data
  }
}

type PrimitiveBody = BodyInit | null | undefined

type JsonValue = Record<string, unknown> | unknown[]

type ApiRequestOptions = Omit<RequestInit, 'body'> & {
  body?: PrimitiveBody | JsonValue
  token?: string | null
}

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL as string | undefined)?.replace(/\/$/, '') || 'http://127.0.0.1:8000'

export function buildUrl(path: string) {
  if (/^https?:\/\//i.test(path)) {
    return path
  }

  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  return `${API_BASE_URL}${normalizedPath}`
}

function isJsonBody(body: ApiRequestOptions['body']): body is JsonValue {
  if (body == null) return false
  if (typeof body !== 'object') return false
  if (body instanceof FormData) return false
  if (body instanceof URLSearchParams) return false
  if (body instanceof Blob) return false
  if (ArrayBuffer.isView(body)) return false
  if (body instanceof ArrayBuffer) return false

  return true
}

export async function apiJson<T>(path: string, options: ApiRequestOptions = {}): Promise<T> {
  const { body, headers, token, ...init } = options
  const requestHeaders = new Headers(headers)

  requestHeaders.set('Accept', 'application/json')

  if (token) {
    requestHeaders.set('Authorization', `Bearer ${token}`)
  }

  let requestBody: PrimitiveBody = body as PrimitiveBody

  if (isJsonBody(body)) {
    requestHeaders.set('Content-Type', 'application/json')
    requestBody = JSON.stringify(body)
  }

  const response = await fetch(buildUrl(path), {
    ...init,
    headers: requestHeaders,
    body: requestBody,
  })

  const contentType = response.headers.get('content-type') || ''
  const isJsonResponse = contentType.includes('application/json')
  const data = isJsonResponse ? await response.json() : await response.text()

  if (!response.ok) {
    const message =
      typeof data === 'object' && data && 'detail' in data && typeof data.detail === 'string'
        ? data.detail
        : `Request failed with status ${response.status}`

    throw new ApiError(message, response.status, data)
  }

  return data as T
}
