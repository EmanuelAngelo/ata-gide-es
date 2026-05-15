import type { AppRouteName } from './navigation'

export type ResourceFieldOption = {
  label: string
  value: string
}

export type ResourceField = {
  name: string
  label: string
  type: 'text' | 'email' | 'date' | 'time' | 'textarea' | 'select' | 'datalist'
  required?: boolean
  placeholder?: string
  options?: ResourceFieldOption[]
}

export type ResourceColumn = {
  key: string
  label: string
}

export type ResourceConfig = {
  routeName: Exclude<AppRouteName, 'dashboard'>
  endpoint: string
  title: string
  singularTitle: string
  description: string
  emptyMessage: string
  columns: ResourceColumn[]
  fields: ResourceField[]
}

const memberClassificationOptions = [
  { label: 'Gideão', value: 'Gideão' },
  { label: 'Auxiliar', value: 'Auxiliar' },
]

const memberBondOptions = [
  { label: 'Membro', value: 'Membro' },
  { label: 'Oficial', value: 'Oficial' },
]

const memberStatusOptions = [
  { label: 'Ativo', value: 'Ativo' },
  { label: 'Inativo', value: 'Inativo' },
]

const memberRoleOptions = [
  'Presidente',
  'Vice-presidente',
  'Capelão',
  'Secretário',
  'Tesoureiro',
  'Nenhum',
].map((value) => ({ label: value, value }))

const sexOptions = ['Masculino', 'Feminino'].map((value) => ({ label: value, value }))
const meetingTypeOptions = ['Administrativa', 'Ordinária', 'Extraordinária', 'Culto', 'Oração'].map((value) => ({ label: value, value }))
const meetingStatusOptions = ['Agendada', 'Realizada', 'Cancelada'].map((value) => ({ label: value, value }))
const minutesStatusOptions = ['Rascunho', 'Revisão', 'Aprovada', 'Arquivada'].map((value) => ({ label: value, value }))
const attendanceStatusOptions = ['Presente', 'Ausente', 'Justificada'].map((value) => ({ label: value, value }))
const partnershipStatusOptions = ['Ativa', 'Inativa', 'Pendente'].map((value) => ({ label: value, value }))
const scheduleCommitmentOptions = ['Reunião', 'Visita', 'Apresentação', 'Culto Parceiro', 'Ação Evangelística'].map((value) => ({ label: value, value }))
const scheduleStatusOptions = ['Agendado', 'Confirmado', 'Realizado', 'Cancelado'].map((value) => ({ label: value, value }))

export const resourceConfigs: Record<Exclude<AppRouteName, 'dashboard'>, ResourceConfig> = {
  members: {
    routeName: 'members',
    endpoint: '/api/members/',
    title: 'Membros',
    singularTitle: 'membro',
    description: 'Cadastre, consulte e atualize os membros da ATA.',
    emptyMessage: 'Nenhum membro encontrado ainda.',
    columns: [
      { key: 'full_name', label: 'Nome' },
      { key: 'classification', label: 'Classificação' },
      { key: 'bond', label: 'Vínculo' },
      { key: 'official_role', label: 'Função' },
      { key: 'status', label: 'Status' },
    ],
    fields: [
      { name: 'full_name', label: 'Nome completo', type: 'text', required: true },
      { name: 'sex', label: 'Sexo', type: 'select', required: true, options: sexOptions },
      { name: 'classification', label: 'Classificação', type: 'select', required: true, options: memberClassificationOptions },
      { name: 'bond', label: 'Vínculo', type: 'select', required: true, options: memberBondOptions },
      { name: 'official_role', label: 'Cargo oficial', type: 'select', required: true, options: memberRoleOptions },
      { name: 'phone', label: 'Telefone', type: 'text' },
      { name: 'email', label: 'E-mail', type: 'email' },
      { name: 'field', label: 'Campo', type: 'text' },
      { name: 'status', label: 'Status', type: 'select', required: true, options: memberStatusOptions },
    ],
  },
  meetings: {
    routeName: 'meetings',
    endpoint: '/api/meetings/',
    title: 'Reuniões',
    singularTitle: 'reunião',
    description: 'Gerencie calendário, liderança e andamento das reuniões.',
    emptyMessage: 'Nenhuma reunião cadastrada ainda.',
    columns: [
      { key: 'title', label: 'Título' },
      { key: 'meeting_type', label: 'Tipo' },
      { key: 'date', label: 'Data' },
      { key: 'location', label: 'Local' },
      { key: 'status', label: 'Status' },
    ],
    fields: [
      { name: 'title', label: 'Título', type: 'text', required: true },
      { name: 'meeting_type', label: 'Tipo de reunião', type: 'select', required: true, options: meetingTypeOptions },
      { name: 'date', label: 'Data', type: 'date', required: true },
      { name: 'start_time', label: 'Hora inicial', type: 'time', required: true },
      { name: 'end_time', label: 'Hora final', type: 'time' },
      { name: 'location', label: 'Local', type: 'text', required: true },
      { name: 'leader', label: 'Dirigente', type: 'text' },
      { name: 'bible_reading', label: 'Leitura bíblica', type: 'text' },
      { name: 'agenda_items', label: 'Pauta', type: 'textarea' },
      { name: 'observations', label: 'Observações', type: 'textarea' },
      { name: 'status', label: 'Status', type: 'select', required: true, options: meetingStatusOptions },
    ],
  },
  minutes: {
    routeName: 'minutes',
    endpoint: '/api/minutes/',
    title: 'Atas',
    singularTitle: 'ata',
    description: 'Produza e revise o conteúdo oficial das atas das reuniões.',
    emptyMessage: 'Nenhuma ata cadastrada ainda.',
    columns: [
      { key: 'meeting_title', label: 'Reunião' },
      { key: 'opening_time', label: 'Abertura' },
      { key: 'closing_time', label: 'Encerramento' },
      { key: 'status', label: 'Status' },
      { key: 'approval_date', label: 'Aprovação' },
    ],
    fields: [
      { name: 'meeting_id', label: 'Reunião cadastrada', type: 'select', required: true },
      { name: 'opening_time', label: 'Hora de abertura', type: 'text' },
      { name: 'closing_time', label: 'Hora de encerramento', type: 'text' },
      { name: 'full_text', label: 'Texto completo', type: 'textarea', required: true },
      { name: 'approval_date', label: 'Data de aprovação', type: 'date' },
      { name: 'signers', label: 'Assinantes', type: 'textarea' },
      { name: 'status', label: 'Status', type: 'select', required: true, options: minutesStatusOptions },
    ],
  },
  attendances: {
    routeName: 'attendances',
    endpoint: '/api/attendances/',
    title: 'Presenças',
    singularTitle: 'presença',
    description: 'Controle a participação e presença dos membros nas reuniões.',
    emptyMessage: 'Nenhum registro de presença encontrado ainda.',
    columns: [
      { key: 'member_name', label: 'Membro' },
      { key: 'meeting_title', label: 'Reunião' },
      { key: 'member_classification', label: 'Classificação' },
      { key: 'status', label: 'Status' },
      { key: 'arrival_time', label: 'Chegada' },
    ],
    fields: [
      { name: 'meeting_id', label: 'Reunião cadastrada', type: 'select', required: true },
      { name: 'member_id', label: 'Membro cadastrado', type: 'select', required: true },
      { name: 'member_name', label: 'Nome do membro', type: 'text', required: true },
      { name: 'member_classification', label: 'Classificação', type: 'text' },
      { name: 'member_role', label: 'Função', type: 'text' },
      { name: 'status', label: 'Status', type: 'select', required: true, options: attendanceStatusOptions },
      { name: 'arrival_time', label: 'Hora de chegada', type: 'text' },
      { name: 'observations', label: 'Observações', type: 'textarea' },
    ],
  },
  'partner-churches': {
    routeName: 'partner-churches',
    endpoint: '/api/partner-churches/',
    title: 'Igrejas Parceiras',
    singularTitle: 'igreja parceira',
    description: 'Mantenha o relacionamento e os dados das igrejas parceiras.',
    emptyMessage: 'Nenhuma igreja parceira cadastrada ainda.',
    columns: [
      { key: 'name', label: 'Nome' },
      { key: 'pastor_name', label: 'Pastor' },
      { key: 'city', label: 'Cidade' },
      { key: 'phone', label: 'Telefone' },
      { key: 'partnership_status', label: 'Parceria' },
    ],
    fields: [
      { name: 'name', label: 'Nome da igreja', type: 'text', required: true },
      { name: 'pastor_name', label: 'Nome do pastor', type: 'text' },
      { name: 'phone', label: 'Telefone', type: 'text' },
      { name: 'email', label: 'E-mail', type: 'email' },
      { name: 'address', label: 'Endereço', type: 'text' },
      { name: 'neighborhood', label: 'Bairro', type: 'text' },
      { name: 'city', label: 'Cidade', type: 'text', required: true },
      { name: 'observations', label: 'Observações', type: 'textarea' },
      { name: 'partnership_status', label: 'Status da parceria', type: 'select', required: true, options: partnershipStatusOptions },
    ],
  },
  'church-schedules': {
    routeName: 'church-schedules',
    endpoint: '/api/church-schedules/',
    title: 'Agendamento às Igrejas',
    singularTitle: 'agendamento à igreja',
    description: 'Organize compromissos, visitas e programações com igrejas parceiras ou informadas manualmente.',
    emptyMessage: 'Nenhum agendamento às igrejas encontrado ainda.',
    columns: [
      { key: 'church_name', label: 'Igreja' },
      { key: 'date', label: 'Data' },
      { key: 'time', label: 'Hora' },
      { key: 'commitment_type', label: 'Compromisso' },
      { key: 'status', label: 'Status' },
    ],
    fields: [
      { name: 'church_id', label: 'Igreja parceira vinculada', type: 'text' },
      { name: 'church_name', label: 'Nome da igreja', type: 'datalist', required: true, placeholder: 'Escolha uma igreja parceira ou digite manualmente' },
      { name: 'pastor_name', label: 'Nome do pastor', type: 'text' },
      { name: 'church_phone', label: 'Telefone da igreja', type: 'text' },
      { name: 'address', label: 'Endereço', type: 'text' },
      { name: 'neighborhood', label: 'Bairro', type: 'text' },
      { name: 'city', label: 'Cidade', type: 'text' },
      { name: 'date', label: 'Data', type: 'date', required: true },
      { name: 'time', label: 'Hora', type: 'time', required: true },
      { name: 'commitment_type', label: 'Tipo de compromisso', type: 'select', required: true, options: scheduleCommitmentOptions },
      { name: 'responsible', label: 'Responsável', type: 'text' },
      { name: 'observations', label: 'Observações', type: 'textarea' },
      { name: 'status', label: 'Status', type: 'select', required: true, options: scheduleStatusOptions },
    ],
  },
}
