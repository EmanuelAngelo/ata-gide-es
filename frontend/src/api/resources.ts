import { apiJson } from './api'

export type ResourceRecord = Record<string, unknown> & {
  id?: number | string
}

type PaginatedResponse<T> = {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export type ResourceCollection<T extends ResourceRecord> = {
  items: T[]
  count: number
  next: string | null
  previous: string | null
}

function isPaginatedResponse<T extends ResourceRecord>(value: unknown): value is PaginatedResponse<T> {
  return Boolean(
    value &&
      typeof value === 'object' &&
      'results' in value &&
      Array.isArray((value as PaginatedResponse<T>).results),
  )
}

export async function getResourceCollection<T extends ResourceRecord>(endpoint: string, token: string, search = ''): Promise<ResourceCollection<T>> {
  const url = new URL(endpoint, 'http://local.api')

  if (search.trim()) {
    url.searchParams.set('search', search.trim())
  }

  const response = await apiJson<T[] | PaginatedResponse<T>>(`${url.pathname}${url.search}`, {
    method: 'GET',
    token,
  })

  if (isPaginatedResponse<T>(response)) {
    return {
      items: response.results,
      count: response.count,
      next: response.next,
      previous: response.previous,
    }
  }

  return {
    items: response,
    count: response.length,
    next: null,
    previous: null,
  }
}

export async function listResources<T extends ResourceRecord>(endpoint: string, token: string, search = '') {
  const collection = await getResourceCollection<T>(endpoint, token, search)
  return collection.items
}

export function createResource<T extends ResourceRecord>(endpoint: string, token: string, payload: ResourceRecord) {
  return apiJson<T>(endpoint, {
    method: 'POST',
    token,
    body: payload,
  })
}

export function updateResource<T extends ResourceRecord>(endpoint: string, id: number | string, token: string, payload: ResourceRecord) {
  return apiJson<T>(`${endpoint}${id}/`, {
    method: 'PATCH',
    token,
    body: payload,
  })
}

export function deleteResource(endpoint: string, id: number | string, token: string) {
  return apiJson<unknown>(`${endpoint}${id}/`, {
    method: 'DELETE',
    token,
  })
}
