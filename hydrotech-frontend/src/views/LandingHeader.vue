<template>
  <header class="header" :class="{ 'header--scrolled': isScrolled }">
    <div class="header-container">

      <!-- Brand -->
      <router-link to="/" class="brand">
        <div class="brand-logo">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
          </svg>
        </div>
        <span class="brand-text">HydroTech</span>
      </router-link>

      <!-- Desktop Nav -->
      <nav class="nav" :class="{ 'nav--open': mobileOpen }">
        <!-- Minha Conta removido do centro -->
        <a v-if="!isMinimalNav" href="#servicos" class="nav-link" @click="closeMobile">Serviços Institucionais</a>
        <a v-if="!isMinimalNav" href="#contingencia" class="nav-link" @click="closeMobile">Quem pode usar?</a>

        <!-- Botão para Monitoramento Público na página Minha Conta -->
        <router-link v-if="route.path === '/minha-conta'" to="/monitoramento" class="btn-monitoring" @click="closeMobile">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
            <circle cx="12" cy="12" r="3"/>
          </svg>
          Acessar Monitoramento Público
        </router-link>

        <!-- Mobile-only auth -->
        <div class="nav-mobile-auth" v-if="mobileOpen">
          <template v-if="!isLoggedIn">
            <router-link to="/login" class="nav-link" @click="closeMobile">Entrar</router-link>
            <router-link to="/registro" class="btn-cta-mobile" @click="closeMobile">Criar Conta</router-link>
          </template>
          <button v-else class="btn-logout-mobile" @click="logout">Sair da Conta</button>
        </div>
      </nav>

      <!-- Desktop Actions -->
      <div class="actions">
        <template v-if="!isLoggedIn">
          <router-link to="/registro" class="btn-manage">Registre-se</router-link>
          <router-link to="/login" class="btn-enter">Entrar</router-link>
        </template>
        <template v-else>
          <router-link v-if="isAdmin" to="/dashboard" class="btn-admin">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
            Painel Admin
          </router-link>
          <router-link to="/minha-conta" class="user-badge" title="Ver Perfil">
            <div class="user-avatar">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </div>
            <span class="user-name">{{ userName }}</span>
          </router-link>
          <button @click="logout" class="btn-logout">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
            Sair
          </button>
        </template>

        <!-- Theme Toggle -->
        <button class="theme-toggle" @click="toggleTheme" :title="theme === 'dark' ? 'Modo claro' : 'Modo escuro'">
          <svg v-if="theme === 'dark'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
          </svg>
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
          </svg>
        </button>

        <!-- Hamburger -->
        <button class="hamburger" :class="{ 'hamburger--open': mobileOpen }" @click="mobileOpen = !mobileOpen">
          <span></span><span></span><span></span>
        </button>
      </div>

    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const isMinimalNav = computed(() => {
  return ['/login', '/registro', '/monitoramento', '/minha-conta'].includes(route.path)
})
const isLoggedIn = ref(!!localStorage.getItem('user_token'))
const userName = ref(localStorage.getItem('user_name') || 'Usuário')
const isAdmin = ref(false)
const mobileOpen = ref(false)
const isScrolled = ref(false)
const theme = ref(localStorage.getItem('theme') || 'dark')

const checkAdmin = () => {
  try {
    const data = JSON.parse(localStorage.getItem('user_data') || '{}')
    isAdmin.value = !!data.is_defesa_civil
  } catch { isAdmin.value = false }
}
checkAdmin()

const toggleTheme = () => {
  const newTheme = theme.value === 'light' ? 'dark' : 'light'
  theme.value = newTheme
  localStorage.setItem('theme', newTheme)
  document.documentElement.setAttribute('data-theme', newTheme)
  window.dispatchEvent(new Event('theme-changed'))
}

const checkLogin = () => {
  isLoggedIn.value = !!localStorage.getItem('user_token')
  userName.value = localStorage.getItem('user_name') || 'Usuário'
  checkAdmin()
}

const closeMobile = () => {
  mobileOpen.value = false
}

const logout = () => {
  localStorage.removeItem('user_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_name')
  localStorage.removeItem('user_data')
  checkLogin()
  closeMobile()
  router.push('/')
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > 10
}

onMounted(() => {
  theme.value = localStorage.getItem('theme') || 'dark'
  document.documentElement.setAttribute('data-theme', theme.value)
  window.addEventListener('storage-update', checkLogin)
  window.addEventListener('storage', checkLogin)
  window.addEventListener('scroll', handleScroll, { passive: true })
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('storage-update', checkLogin)
  window.removeEventListener('storage', checkLogin)
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.header {
  width: 100%;
  height: 60px;
  background: var(--nav-bg);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  transition: box-shadow 0.2s, background 0.3s;
}

.header--scrolled {
  box-shadow: var(--shadow-md);
}

.header-container {
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Brand */
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  z-index: 10;
}

.brand-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: var(--accent);
  color: white;
}

.brand-text {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

/* Nav */
.nav {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 0;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  color: var(--text-muted);
  font-weight: 500;
  font-size: 0.82rem;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.2s ease;
  position: relative;
}

.nav-link:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.04);
}

[data-theme='light'] .nav-link:hover {
  background: rgba(0, 0, 0, 0.04);
}

.nav-link.router-link-active {
  color: var(--accent);
  font-weight: 600;
  background: rgba(14, 165, 233, 0.08);
}

.nav-mobile-auth { display: none; }

/* Actions */
.actions {
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 10;
}

.btn-manage {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--accent);
  color: white;
  padding: 8px 20px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.8rem;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(14, 165, 233, 0.2);
}
.btn-manage:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
}

.btn-enter {
  display: inline-flex;
  align-items: center;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  padding: 8px 20px;
  border-radius: 8px;
  border: 1px solid var(--border);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.8rem;
  transition: all 0.2s;
}
.btn-enter:hover {
  border-color: var(--accent);
  color: var(--accent);
  background: rgba(14, 165, 233, 0.06);
}

.btn-admin {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(139, 92, 246, 0.1);
  color: var(--text-primary);
  padding: 8px 18px;
  border-radius: 8px;
  border: 1px solid rgba(139, 92, 246, 0.2);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.8rem;
  transition: all 0.2s;
}
.btn-admin:hover {
  background: rgba(139, 92, 246, 0.18);
  border-color: rgba(139, 92, 246, 0.35);
  transform: translateY(-1px);
}

.btn-monitoring {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--accent-soft);
  color: var(--text-primary);
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid var(--border-accent);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.82rem;
  transition: all 0.2s ease;
}
.btn-monitoring:hover {
  background: rgba(59, 130, 246, 0.2);
  border-color: var(--accent);
  color: var(--text-primary);
  transform: translateY(-1px);
}

.user-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 14px 5px 5px;
  border-radius: 999px;
  background: var(--accent-soft);
  border: 1px solid var(--border);
  transition: all 0.2s;
  text-decoration: none;
}
.user-badge:hover {
  border-color: var(--accent);
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 999px;
  background: var(--accent-gradient);
  color: white;
}

.user-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-primary);
}

.btn-logout {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  border-radius: 8px;
  background: var(--risk-high-bg);
  color: var(--risk-high);
  font-weight: 600;
  font-size: 0.82rem;
  border: 1px solid rgba(239, 68, 68, 0.15);
  cursor: pointer;
  transition: all 0.2s;
}
.btn-logout:hover {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.3);
  transform: none;
}

/* Theme Toggle */
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 6px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  color: var(--text-muted);
  cursor: pointer;
  transition: color 0.15s, border-color 0.15s;
}
.theme-toggle:hover { color: var(--accent); border-color: rgba(59,130,246,0.3); transform: none; }

/* Hamburger */
.hamburger {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 36px;
  height: 36px;
  border-radius: 6px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  gap: 5px;
  padding: 0;
  cursor: pointer;
}

.hamburger span {
  display: block;
  width: 16px;
  height: 2px;
  background: var(--text-primary);
  border-radius: 2px;
  transition: all 0.3s ease;
  transform-origin: center;
}

.hamburger--open span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.hamburger--open span:nth-child(2) { opacity: 0; transform: scaleX(0); }
.hamburger--open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }

/* Responsive */
@media (max-width: 768px) {
  .hamburger { display: flex; }

  .nav {
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--bg-primary);
    flex-direction: column;
    align-items: stretch;
    padding: 20px;
    gap: 4px;
    transform: translateX(100%);
    transition: transform 0.3s ease;
    z-index: 999;
  }

  .nav--open { transform: translateX(0); }

  .nav-link { font-size: 1rem; padding: 14px 16px; }

  .btn-monitoring {
    padding: 14px 16px;
    font-size: 1rem;
    justify-content: center;
  }

  .nav-mobile-auth {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: auto;
    padding-top: 20px;
    border-top: 1px solid var(--border);
  }

  .btn-cta-mobile {
    display: block;
    text-align: center;
    background: var(--accent);
    color: white;
    padding: 14px;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 600;
  }

  .btn-logout-mobile {
    padding: 14px;
    border-radius: 6px;
    background: var(--risk-high-bg);
    color: var(--risk-high);
    font-weight: 600;
    border: none;
    cursor: pointer;
  }

  .actions .btn-manage,
  .actions .btn-enter,
  .actions .btn-logout,
  .actions .user-badge { display: none; }
}

@media (max-width: 480px) {
  .brand-text { font-size: 0.85rem; }
}
</style>