<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="modal-backdrop" @click.self="cancel">
        <div class="modal-card">
          <div class="modal-icon" :class="'modal-icon--' + type">
            <svg v-if="type === 'danger'" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
            <svg v-else width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>
            </svg>
          </div>
          <h3 class="modal-title">{{ title }}</h3>
          <p class="modal-message">{{ message }}</p>
          <div class="modal-actions">
            <button class="modal-btn modal-btn--cancel" @click="cancel">
              Cancelar
            </button>
            <button class="modal-btn" :class="'modal-btn--' + type" @click="confirm">
              {{ confirmText }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'

const visible = ref(false)
const title = ref('')
const message = ref('')
const confirmText = ref('Confirmar')
const type = ref('danger')

let resolvePromise = null

const show = (options = {}) => {
  title.value = options.title || 'Confirmar ação'
  message.value = options.message || 'Tem certeza que deseja continuar?'
  confirmText.value = options.confirmText || 'Confirmar'
  type.value = options.type || 'danger'
  visible.value = true

  return new Promise((resolve) => {
    resolvePromise = resolve
  })
}

const confirm = () => {
  visible.value = false
  resolvePromise?.(true)
}

const cancel = () => {
  visible.value = false
  resolvePromise?.(false)
}

defineExpose({ show })
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  padding: 20px;
}

.modal-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 32px;
  max-width: 420px;
  width: 100%;
  text-align: center;
  box-shadow: var(--shadow-xl);
}

.modal-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: var(--radius-full);
  margin-bottom: 16px;
}

.modal-icon--danger {
  background: var(--risk-high-bg);
  color: var(--risk-high);
}

.modal-icon--info {
  background: var(--accent-soft);
  color: var(--accent);
}

.modal-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.modal-message {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 24px;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.modal-btn {
  padding: 10px 24px;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  border: none;
  transition: all var(--transition-normal);
}

.modal-btn--cancel {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border);
}

.modal-btn--cancel:hover {
  background: var(--bg-tertiary);
}

.modal-btn--danger {
  background: var(--risk-high);
  color: white;
}

.modal-btn--danger:hover {
  background: var(--risk-high);
  transform: none;
}

.modal-btn--info {
  background: var(--accent);
  color: white;
}

/* Transitions */
.modal-enter-active {
  transition: opacity 0.2s ease;
}
.modal-enter-active .modal-card {
  animation: modalIn 0.25s ease-out;
}
.modal-leave-active {
  transition: opacity 0.15s ease;
}
.modal-leave-active .modal-card {
  animation: modalOut 0.15s ease-in forwards;
}

.modal-enter-from, .modal-leave-to { opacity: 0; }

@keyframes modalIn {
  from { transform: scale(0.9) translateY(10px); opacity: 0; }
  to { transform: scale(1) translateY(0); opacity: 1; }
}

@keyframes modalOut {
  from { transform: scale(1); opacity: 1; }
  to { transform: scale(0.9); opacity: 0; }
}
</style>
