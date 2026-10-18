import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
    {
    path: '/registro',
    name: 'registro',
    component: () => import('@/views/RegistroView.vue')
    },
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/LandingPage.vue')
    },
    {
      path: '/minha-conta',
      name: 'minha-conta',
      component: () => import('@/views/MinhaContaView.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue')
    },
    {
      path: '/rios',
      name: 'rios',
      component: () => import('@/views/RiosView.vue')
    },
    {
      path: '/usuarios',
      name: 'usuarios',
      component: () => import('@/views/UsuariosView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue')
    },
    {
      path: '/monitoramento',
      name: 'monitoramento',
      component: () => import('@/views/MonitoramentoView.vue')
    },
    {
      path: '/rota-de-fuga',
      name: 'rota-de-fuga',
      component: () => import('@/views/RotaFugaView.vue')
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
