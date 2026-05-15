/**
 * router/index.ts
 *
 * Manual routes for ./src/pages/*.vue
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router'
import AttendancesPage from '@/pages/AttendancesPage.vue'
import ChurchSchedulesPage from '@/pages/ChurchSchedulesPage.vue'
import DashboardPage from '@/pages/DashboardPage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import MeetingsPage from '@/pages/MeetingsPage.vue'
import MembersPage from '@/pages/MembersPage.vue'
import MinutesPage from '@/pages/MinutesPage.vue'
import PartnerChurchesPage from '@/pages/PartnerChurchesPage.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: { name: 'login' },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
      meta: { guestOnly: true },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/publico',
      name: 'attendances',
      component: AttendancesPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/horarios-igreja',
      name: 'church-schedules',
      component: ChurchSchedulesPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/reunioes',
      name: 'meetings',
      component: MeetingsPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/membros',
      name: 'members',
      component: MembersPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/atas',
      name: 'minutes',
      component: MinutesPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/igrejas-parceiras',
      name: 'partner-churches',
      component: PartnerChurchesPage,
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login', query: { next: to.fullPath } }
  }

  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return { name: 'dashboard' }
  }

  return true
})

export default router
