import { apiJson, buildUrl } from './api'
import type { ResourceRecord } from './resources'

export type MinutesRecord = ResourceRecord & {
  id?: number
  meeting_id?: number
  meeting_title?: string
  opening_time?: string
  closing_time?: string
  full_text?: string
  approval_date?: string | null
  signers?: string
  status?: string
}

export type AttendanceRosterItem = {
  member_id: number
  member_name: string
  member_classification: string
  member_role: string
  status: string
  arrival_time: string
  observations: string
  attendance_id: number | null
}

export type MeetingWorkspaceData = {
  meeting: ResourceRecord
  minutes: MinutesRecord | null
  roster: AttendanceRosterItem[]
}

export type BulkAttendancePayload = {
  member_id: number
  status: string
  arrival_time?: string
  observations?: string
}

export function getMeetingWorkspace(meetingId: number | string, token: string) {
  return apiJson<MeetingWorkspaceData>(`/api/meetings/${meetingId}/workspace/`, {
    method: 'GET',
    token,
  })
}

export function saveMeetingMinutes(
  meetingId: number | string,
  token: string,
  payload: ResourceRecord,
  isUpdate: boolean,
) {
  return apiJson<MinutesRecord>(`/api/meetings/${meetingId}/minutes/`, {
    method: isUpdate ? 'PATCH' : 'POST',
    token,
    body: payload,
  })
}

export function saveBulkAttendances(
  meetingId: number | string,
  token: string,
  payload: BulkAttendancePayload[],
) {
  return apiJson<ResourceRecord[]>(`/api/meetings/${meetingId}/attendances/bulk/`, {
    method: 'POST',
    token,
    body: payload,
  })
}

export async function fetchProtectedMeetingFile(path: string, token: string) {
  const response = await fetch(buildUrl(path), {
    headers: { Authorization: `Bearer ${token}` },
  })

  if (!response.ok) {
    throw new Error(`Falha ao buscar arquivo: ${response.status}`)
  }

  return response
}
