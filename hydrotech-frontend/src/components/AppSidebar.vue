<template>
  <aside class="sidebar">

    <!-- Header -->
    <div class="sidebar-header">
      <div class="sidebar-brand-icon">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
      </div>
      <div>
        <p class="sidebar-org-label">Centro de Controle</p>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="sidebar-nav">
      <router-link to="/dashboard" class="sidebar-link" :class="{ 'sidebar-link--active': route.path === '/dashboard' }">
        <span class="sidebar-link-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
          </svg>
        </span>
        Monitoramento ao Vivo
      </router-link>

      <router-link to="/rios" class="sidebar-link" :class="{ 'sidebar-link--active': route.path === '/rios' }">
        <span class="sidebar-link-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
            <rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>
          </svg>
        </span>
        Gestão de Rios
      </router-link>

      <router-link to="/usuarios" class="sidebar-link" :class="{ 'sidebar-link--active': route.path === '/usuarios' }">
        <span class="sidebar-link-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>
          </svg>
        </span>
        Cadastro de Usuários
      </router-link>
    </nav>

    <!-- Spacer -->
    <div class="sidebar-spacer"></div>



  </aside>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  min-height: calc(100vh - var(--topnav-height));
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  position: sticky;
  top: var(--topnav-height);
  height: calc(100vh - var(--topnav-height));
  overflow-y: auto;
}

/* Header */
.sidebar-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 18px 16px 14px;
  border-bottom: 1px solid var(--border);
}

.sidebar-brand-icon {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  background: var(--accent-soft);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.sidebar-org-label {
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 0.02em;
  line-height: 1.3;
}

.sidebar-org-sub {
  font-size: 0.68rem;
  color: var(--text-muted);
  margin-top: 1px;
}

/* Navigation */
.sidebar-nav {
  display: flex;
  flex-direction: column;
  padding: 12px 8px;
  gap: 2px;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 10px;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: 0.8rem;
  font-weight: 500;
  text-decoration: none;
  transition: all var(--transition-fast);
  cursor: pointer;
}

.sidebar-link:hover {
  color: var(--text-primary);
  background: var(--bg-elevated);
}

.sidebar-link--active {
  color: var(--text-primary);
  background: var(--bg-elevated);
  border-left: 2px solid var(--accent);
  padding-left: 8px;
}

.sidebar-link-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: var(--text-muted);
}

.sidebar-link--active .sidebar-link-icon,
.sidebar-link:hover .sidebar-link-icon {
  color: var(--accent);
}

/* Spacer */
.sidebar-spacer { flex: 1; }

/* Footer */
.sidebar-footer {
  display: flex;
  flex-direction: column;
  padding: 8px 8px 16px;
  gap: 2px;
  border-top: 1px solid var(--border);
  padding-top: 12px;
}

.sidebar-footer-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: var(--radius-md);
  color: var(--text-muted);
  font-size: 0.78rem;
  font-weight: 500;
  background: transparent;
  border: none;
  cursor: pointer;
  text-align: left;
  transition: all var(--transition-fast);
}

.sidebar-footer-link:hover:not(:disabled) {
  color: var(--text-secondary);
  background: var(--bg-elevated);
  transform: none;
}

.btn-report {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: var(--radius-md);
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  color: var(--text-primary);
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  cursor: pointer;
  margin-top: 6px;
  transition: all var(--transition-fast);
}

.btn-report:hover:not(:disabled) {
  background: var(--bg-elevated);
  transform: none;
}
</style>
