export type AppRouteName =
  | 'dashboard'
  | 'members'
  | 'meetings'
  | 'minutes'
  | 'attendances'
  | 'partner-churches'
  | 'church-schedules'

export type NavigationItem = {
  key: AppRouteName
  label: string
  icon: string
  description: string
}

export const navigationItems: NavigationItem[] = [
  {
    key: 'dashboard',
    label: 'Dashboard',
    icon: 'mdi mdi-view-dashboard-outline',
    description: 'Visão geral do sistema ATA',
  },
  {
    key: 'attendances',
    label: 'Presenças',
    icon: 'mdi mdi-account-multiple-check-outline',
    description: 'Controle de presença dos membros nas reuniões',
  },
  {
    key: 'church-schedules',
    label: 'Agendamento às Igrejas',
    icon: 'mdi mdi-calendar-clock-outline',
    description: 'Agenda e compromissos com igrejas cadastradas ou avulsas',
  },
  {
    key: 'meetings',
    label: 'Reuniões',
    icon: 'mdi mdi-forum-outline',
    description: 'Cadastro e acompanhamento das reuniões',
  },
  {
    key: 'members',
    label: 'Membros',
    icon: 'mdi mdi-account-group-outline',
    description: 'Gestão cadastral dos membros',
  },
  {
    key: 'minutes',
    label: 'Atas',
    icon: 'mdi mdi-file-document-edit-outline',
    description: 'Registro e revisão das atas',
  },
  {
    key: 'partner-churches',
    label: 'Igrejas Parceiras',
    icon: 'mdi mdi-church-outline',
    description: 'Cadastro de igrejas parceiras',
  },
]
