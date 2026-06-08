import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import RiosView from '../views/RiosView.vue'
import UsuariosView from '../views/UsuariosView.vue'
import LoginView from '../views/LoginView.vue'
import LandingPage from '@/views/LandingPage.vue'
import RegistroView from '@/views/RegistroView.vue'
import MonitoramentoView from '@/views/MonitoramentoView.vue'
import MinhaContaView from '@/views/MinhaContaView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
    {
    path: '/registro',
    name: 'registro',
    component: RegistroView
    },
    {
      path: '/',
      name: 'home',
      component: LandingPage
    },
    {
      path: '/minha-conta',
      name: 'minha-conta',
      component: MinhaContaView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/rios',
      name: 'rios',
      component: RiosView
    },
    {
      path: '/usuarios',
      name: 'usuarios',
      component: UsuariosView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/monitoramento',
      name: 'monitoramento',
      component: MonitoramentoView
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('user_token')

  // Pages that require authentication
  const privatePages = ['/dashboard', '/rios', '/usuarios', '/minha-conta']
  const authRequired = privatePages.includes(to.path)

  // Admin pages — only for defesa civil
  const adminPages = ['/dashboard', '/rios', '/usuarios']
  const isAdminPage = adminPages.includes(to.path)

  if (authRequired && !isAuthenticated) {
    next('/login')
  } 
  else if (to.path === '/login' && isAuthenticated) {
    next('/')
  }
  else if (isAdminPage && isAuthenticated) {
    // Check if user is defesa civil
    try {
      const userData = JSON.parse(localStorage.getItem('user_data') || '{}')
      if (!userData.is_defesa_civil) {
        next('/minha-conta')
        return
      }
    } catch (e) {
      next('/minha-conta')
      return
    }
    next()
  }
  else {
    next()
  }
})


export default router