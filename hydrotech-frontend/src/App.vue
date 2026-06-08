<template>
  <div class="app-wrapper">

    <!-- ── APP LAYOUT (authenticated routes) ── -->
    <template v-if="isAppRoute">
      <AppTopNav />
      <div class="app-body">
        <AppSidebar />
        <main class="app-main">
          <RouterView v-slot="{ Component }">
            <Transition name="page" mode="out-in">
              <component :is="Component" />
            </Transition>
          </RouterView>
        </main>
      </div>
    </template>

    <!-- ── PUBLIC LAYOUT (landing, login, registro, monitoramento) ── -->
    <template v-else>
      <LandingHeader />
      <main class="public-main" :class="{ 'public-main--full': isFullWidthRoute }">
        <RouterView v-slot="{ Component }">
          <Transition name="page" mode="out-in">
            <component :is="Component" />
          </Transition>
        </RouterView>
      </main>
      <LandingFooter />
    </template>

    <!-- Global Overlays -->
    <ToastNotification ref="toastRef" />
    <ConfirmModal ref="modalRef" />
  </div>
</template>

<script setup>
import { ref, onMounted, provide, computed } from 'vue'
import { useRoute } from 'vue-router'

import LandingHeader from '@/views/LandingHeader.vue'
import LandingFooter from '@/views/LandingFooter.vue'
import AppTopNav from '@/components/AppTopNav.vue'
import AppSidebar from '@/components/AppSidebar.vue'
import ToastNotification from '@/components/ToastNotification.vue'
import ConfirmModal from '@/components/ConfirmModal.vue'

const route = useRoute()
const toastRef = ref(null)
const modalRef = ref(null)

// Authenticated app routes → show sidebar + topnav
const APP_ROUTES = ['/dashboard', '/rios', '/usuarios']
const isAppRoute = computed(() => APP_ROUTES.includes(route.path))

// Full-width public routes (no container padding)
const isFullWidthRoute = computed(() =>
  ['/', '/login', '/registro', '/monitoramento'].includes(route.path)
)

// Provide toast & modal globally
provide('toast', {
  success: (...args) => toastRef.value?.success(...args),
  error:   (...args) => toastRef.value?.error(...args),
  info:    (...args) => toastRef.value?.info(...args),
  warning: (...args) => toastRef.value?.warning(...args),
})

provide('modal', {
  show: (...args) => modalRef.value?.show(...args),
})

onMounted(() => {
  const theme = localStorage.getItem('theme') || 'dark'
  document.documentElement.setAttribute('data-theme', theme)
})
</script>

<style scoped>
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
}

/* ── App Layout ── */
.app-body {
  display: flex;
  flex: 1;
  min-height: calc(100vh - var(--topnav-height));
}

.app-main {
  flex: 1;
  min-width: 0;
  padding: 32px 36px;
  overflow-y: auto;
}

/* ── Public Layout ── */
.public-main {
  flex: 1;
  width: 100%;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 32px 24px;
}

.public-main--full {
  max-width: 100% !important;
  padding: 0 !important;
  margin: 0 !important;
}

/* ── Page Transitions ── */
.page-enter-active {
  animation: pageIn 0.25s ease-out;
}

.page-leave-active {
  animation: pageOut 0.12s ease-in;
}

@keyframes pageIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes pageOut {
  from { opacity: 1; }
  to   { opacity: 0; }
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .app-main { padding: 20px 16px; }
}
</style>

<style>
/* ── Skeletons (Global) ── */
.skeleton {
  background: linear-gradient(90deg, var(--bg-elevated) 25%, var(--border-light) 50%, var(--bg-elevated) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-sm);
}
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.skeleton-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.skeleton-hdr {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.skeleton-title { height: 24px; width: 40%; border-radius: 4px; }
.skeleton-sub { height: 16px; width: 60%; border-radius: 4px; }
.skeleton-body { height: 250px; width: 100%; border-radius: var(--radius-md); }
.skeleton-btn { height: 32px; width: 80px; border-radius: 8px; }

/* ── Focus Outline (Acessibilidade) ── */
a:focus-visible, button:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
</style>