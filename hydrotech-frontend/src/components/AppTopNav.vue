<template>
  <header class="topnav">
    <div class="topnav-inner">

      <!-- Logo -->
      <router-link to="/" class="topnav-brand">
        <div class="brand-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
            <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
          </svg>
        </div>
        <span class="brand-text">HydroTech</span>
      </router-link>



      <!-- Right Actions -->
      <div class="topnav-actions">


        <!-- Theme Toggle -->
        <button class="topnav-icon-btn" @click="toggleTheme" :title="theme === 'dark' ? 'Modo claro' : 'Modo escuro'">
          <svg v-if="theme === 'dark'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
          </svg>
          <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
          </svg>
        </button>



        <!-- User Icon -->
        <button class="topnav-user-btn" @click="toggleUserMenu" title="Conta">
          <div class="user-avatar-sm">{{ userInitials }}</div>
        </button>

        <!-- User Dropdown -->
        <div class="user-dropdown" v-if="userMenuOpen" @click.away="userMenuOpen = false">
          <div class="user-dropdown-header">
            <div class="user-avatar-lg">{{ userInitials }}</div>
            <div>
              <p class="dropdown-username">{{ userName }}</p>
              <p class="dropdown-role">Operador Regional</p>
            </div>
          </div>
          <div class="user-dropdown-divider"></div>
          <button class="dropdown-item dropdown-item--danger" @click="logout">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            Sair da Conta
          </button>
        </div>
      </div>

    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const userMenuOpen = ref(false)
const userName = ref(localStorage.getItem('user_name') || 'Usuário')
const theme = ref(localStorage.getItem('theme') || 'dark')

const toggleTheme = () => {
  const newTheme = theme.value === 'light' ? 'dark' : 'light'
  theme.value = newTheme
  localStorage.setItem('theme', newTheme)
  document.documentElement.setAttribute('data-theme', newTheme)
  window.dispatchEvent(new Event('theme-changed'))
}

const syncTheme = () => {
  theme.value = localStorage.getItem('theme') || 'dark'
}

const userInitials = computed(() => {
  const parts = userName.value.trim().split(' ')
  if (parts.length >= 2) return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
  return parts[0]?.[0]?.toUpperCase() || 'U'
})

const toggleUserMenu = () => { userMenuOpen.value = !userMenuOpen.value }

const showEmergency = () => {
  alert('⚠️ Sistema de Alerta de Emergência\nContate imediatamente a Defesa Civil.')
}

const logout = () => {
  localStorage.removeItem('user_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_name')
  window.dispatchEvent(new Event('storage-update'))
  router.push('/')
}

const handleClickOutside = (e) => {
  if (!e.target.closest('.topnav-user-btn') && !e.target.closest('.user-dropdown')) {
    userMenuOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('theme-changed', syncTheme)
  window.addEventListener('storage-update', () => {
    userName.value = localStorage.getItem('user_name') || 'Usuário'
  })
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('theme-changed', syncTheme)
})
</script>

<style scoped>
.topnav {
  position: sticky;
  top: 0;
  z-index: 200;
  width: 100%;
  height: var(--topnav-height);
  background: var(--nav-bg);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
}

.topnav-inner {
  width: 100%;
  max-width: 100%;
  padding: 0 24px;
  display: flex;
  align-items: center;
  gap: 32px;
}

/* Brand */
.topnav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  flex-shrink: 0;
}

.brand-icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.brand-text {
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

/* Nav Links */
.topnav-links {
  display: flex;
  align-items: center;
  gap: 0;
}

.topnav-link {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-decoration: none;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  border-bottom: 2px solid transparent;
  transition: color var(--transition-fast), border-color var(--transition-fast);
  height: var(--topnav-height);
}

.topnav-link:hover { color: var(--text-primary); }

.topnav-link.active {
  color: var(--text-primary);
  border-bottom-color: var(--accent);
}

/* Right Actions */
.topnav-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: auto;
  position: relative;
}

.btn-emergency {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  background: var(--emergency);
  color: white;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: none;
  cursor: pointer;
  transition: background var(--transition-fast);
}

.btn-emergency:hover:not(:disabled) {
  background: var(--emergency-hover);
  transform: none;
}

.topnav-icon-btn {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.topnav-icon-btn:hover:not(:disabled) {
  color: var(--text-primary);
  border-color: var(--border);
  background: var(--bg-tertiary);
  transform: none;
}

.topnav-user-btn {
  background: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
}

.topnav-user-btn:hover:not(:disabled) { transform: none; }

.user-avatar-sm {
  width: 34px;
  height: 34px;
  border-radius: var(--radius-full);
  background: var(--accent-gradient);
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: opacity var(--transition-fast);
}

.user-avatar-sm:hover { opacity: 0.85; }

/* User Dropdown */
.user-dropdown {
  position: absolute;
  top: calc(100% + 12px);
  right: 0;
  width: 240px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  z-index: 300;
  animation: fadeInUp 0.2s ease-out;
  overflow: hidden;
}

.user-dropdown-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
}

.user-avatar-lg {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background: var(--accent-gradient);
  color: white;
  font-size: 0.875rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.dropdown-username {
  font-weight: 600;
  font-size: 0.875rem;
  color: var(--text-primary);
  line-height: 1.3;
}

.dropdown-role {
  font-size: 0.75rem;
  color: var(--text-muted);
  line-height: 1.3;
  margin-top: 1px;
}

.user-dropdown-divider {
  height: 1px;
  background: var(--border);
}

.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-secondary);
  background: transparent;
  border: none;
  border-radius: 0;
  cursor: pointer;
  transition: background var(--transition-fast), color var(--transition-fast);
  text-align: left;
}

.dropdown-item:hover:not(:disabled) {
  background: var(--bg-elevated);
  color: var(--text-primary);
  transform: none;
}

.dropdown-item--danger:hover:not(:disabled) {
  background: var(--emergency-soft);
  color: var(--emergency);
}
</style>
