<template>
  <Teleport to="body">
    <TransitionGroup name="toast" tag="div" class="toast-container">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast"
        :class="'toast--' + toast.type"
      >
        <div class="toast-icon" v-html="iconMap[toast.type]"></div>
        <div class="toast-body">
          <p class="toast-title">{{ toast.title }}</p>
          <p class="toast-message" v-if="toast.message">{{ toast.message }}</p>
        </div>
        <button class="toast-close" @click="remove(toast.id)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
        <div class="toast-progress" :style="{ animationDuration: toast.duration + 'ms' }"></div>
      </div>
    </TransitionGroup>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'

const toasts = ref([])
let idCounter = 0

const iconMap = {
  success: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
  error: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
  info: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
  warning: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
}

const add = (type, title, message = '', duration = 4000) => {
  const id = ++idCounter
  toasts.value.push({ id, type, title, message, duration })
  setTimeout(() => remove(id), duration)
}

const remove = (id) => {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

const success = (title, message) => add('success', title, message)
const error = (title, message) => add('error', title, message)
const info = (title, message) => add('info', title, message)
const warning = (title, message) => add('warning', title, message)

defineExpose({ success, error, info, warning })
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 380px;
  width: 100%;
  pointer-events: none;
}

.toast {
  pointer-events: auto;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  border-radius: var(--radius-lg);
  background: var(--card-bg);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-lg);
  position: relative;
  overflow: hidden;
}

.toast-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
}

.toast--success .toast-icon { background: var(--risk-low-bg); color: var(--risk-low); }
.toast--error .toast-icon { background: var(--risk-high-bg); color: var(--risk-high); }
.toast--info .toast-icon { background: var(--accent-soft); color: var(--accent); }
.toast--warning .toast-icon { background: var(--risk-medium-bg); color: var(--risk-medium); }

.toast-body { flex: 1; min-width: 0; }

.toast-title {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-primary);
}

.toast-message {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-top: 2px;
}

.toast-close {
  flex-shrink: 0;
  padding: 4px;
  border-radius: var(--radius-sm);
  background: none;
  color: var(--text-muted);
  cursor: pointer;
  transition: color var(--transition-fast), background var(--transition-fast);
}

.toast-close:hover {
  color: var(--text-primary);
  background: var(--bg-secondary);
  transform: none;
}

.toast-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
  animation: toastProgress linear forwards;
}

.toast--success .toast-progress { background: var(--risk-low); }
.toast--error .toast-progress { background: var(--risk-high); }
.toast--info .toast-progress { background: var(--accent); }
.toast--warning .toast-progress { background: var(--risk-medium); }

@keyframes toastProgress {
  from { width: 100%; }
  to { width: 0%; }
}

/* Transitions */
.toast-enter-active {
  animation: toastIn 0.35s ease-out;
}
.toast-leave-active {
  animation: toastOut 0.25s ease-in forwards;
}

@keyframes toastIn {
  from { opacity: 0; transform: translateX(100px) scale(0.95); }
  to { opacity: 1; transform: translateX(0) scale(1); }
}

@keyframes toastOut {
  from { opacity: 1; transform: translateX(0) scale(1); }
  to { opacity: 0; transform: translateX(100px) scale(0.95); }
}

@media (max-width: 480px) {
  .toast-container {
    right: 10px;
    left: 10px;
    max-width: 100%;
  }
}
</style>
