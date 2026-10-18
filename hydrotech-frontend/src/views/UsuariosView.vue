<template>
  <div class="usuarios">

    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Usuários Cadastrados</h1>
        <p class="page-subtitle">Gerencie os usuários do sistema de monitoramento</p>
      </div>
    </div>

    <!-- Form Card -->
    <div class="form-section">
      <div class="form-section-header">
        <div class="form-section-icon">
          <svg v-if="!form.id" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" y1="8" x2="19" y2="14"/><line x1="22" y1="11" x2="16" y2="11"/></svg>
          <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>
        </div>
        <div>
          <h2>{{ form.id ? 'Editar Usuário' : 'Cadastrar Novo Usuário' }}</h2>
          <p v-if="form.id">Editando: <strong>{{ form.nome }}</strong></p>
        </div>
      </div>

      <div class="form-grid">
        <div class="form-group">
          <label for="user-nome">Nome Completo</label>
          <div class="input-wrapper">
            <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <input id="user-nome" v-model="form.nome" placeholder="Ex: João Silva" />
          </div>
        </div>
        <div class="form-group">
          <label for="user-email">E-mail</label>
          <div class="input-wrapper">
            <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
            <input id="user-email" v-model="form.email" type="email" placeholder="Ex: joao@email.com" />
          </div>
        </div>
        <div class="form-group">
          <label for="user-senha">Senha</label>
          <div class="input-wrapper">
            <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            <input id="user-senha" v-model="form.senha" type="password" placeholder="Digite a senha" />
          </div>
        </div>
        <div class="form-group">
          <label for="user-nascimento">Data de Nascimento</label>
          <div class="input-wrapper">
            <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <input id="user-nascimento" v-model="form.data_nascimento" type="date" />
          </div>
        </div>
        <div class="form-group">
          <div class="toggle-wrapper">
            <label class="toggle-label" for="user-defesa-civil">
              <span class="toggle-text">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                Defesa Civil
              </span>
              <span class="toggle-hint">Usuário com permissões de administrador do sistema</span>
            </label>
            <div class="toggle-switch" :class="{ active: form.is_defesa_civil }" @click="form.is_defesa_civil = !form.is_defesa_civil">
              <div class="toggle-knob"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="form-actions">
        <button class="btn-primary" @click="save" :disabled="saving">
          <svg v-if="saving" class="spinner" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32"><animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="0.8s" repeatCount="indefinite"/></circle></svg>
          <svg v-else-if="form.id" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          {{ saving ? 'Salvando...' : form.id ? 'Atualizar' : 'Cadastrar' }}
        </button>
        <button class="btn-secondary" v-if="form.id" @click="reset">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          Cancelar
        </button>
      </div>
    </div>

    <!-- Table Card -->
    <div class="table-section">
      <div class="table-header">
        <h2 class="table-title">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          Lista de Usuários
        </h2>
        <span class="table-count">{{ usuarios.length }} registros</span>
      </div>

      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Usuário</th>
              <th>E-mail</th>
              <th>Função</th>
              <th>Nascimento</th>
              <th>Cadastro</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="usuarios.length === 0">
              <td colspan="6" class="empty-state">
                <div class="empty-content">
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
                  <p>Nenhum usuário cadastrado</p>
                  <span>Use o formulário acima para cadastrar o primeiro usuário</span>
                </div>
              </td>
            </tr>
            <tr v-for="usuario in usuarios" :key="usuario.id" class="table-row-animated">
              <td>
                <div class="user-cell">
                  <div class="user-avatar" :style="{ background: getAvatarColor(usuario.nome) }">
                    {{ getInitials(usuario.nome) }}
                  </div>
                  <div class="user-info">
                    <span class="user-name">{{ usuario.nome }}</span>
                    <span class="user-id">#{{ usuario.id }}</span>
                  </div>
                </div>
              </td>
              <td class="td-email">{{ usuario.email }}</td>
              <td>
                <span class="role-badge" :class="{ 'role-badge--admin': usuario.is_defesa_civil }">
                  {{ usuario.is_defesa_civil ? 'Defesa Civil' : 'Usuário' }}
                </span>
              </td>
              <td>{{ formatDate(usuario.data_nascimento) }}</td>
              <td>
                <span class="date-badge">{{ formatDate(usuario.data_criacao) }}</span>
              </td>
              <td class="td-actions">
                <button class="btn-action btn-action--edit" @click="edit(usuario)" title="Editar">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>
                </button>
                <button class="btn-action btn-action--delete" @click="remove(usuario.id)" title="Excluir">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <ConfirmModal ref="confirmRef" />
  </div>
</template>

<script setup>
import { ref, inject, onMounted } from 'vue'
import api from '../services/api'
import ConfirmModal from '@/components/ConfirmModal.vue'

const toast = inject('toast')
const confirmRef = ref(null)

const usuarios = ref([])
const saving = ref(false)
const form = ref({ id: null, nome: '', email: '', senha: '', data_nascimento: '' })

const avatarColors = [
  'linear-gradient(135deg, #667eea, #764ba2)',
  'linear-gradient(135deg, #f093fb, #f5576c)',
  'linear-gradient(135deg, #4facfe, #00f2fe)',
  'linear-gradient(135deg, #43e97b, #38f9d7)',
  'linear-gradient(135deg, #fa709a, #fee140)',
  'linear-gradient(135deg, #a18cd1, #fbc2eb)',
  'linear-gradient(135deg, #fccb90, #d57eeb)',
  'linear-gradient(135deg, #29ABE2, #1B6FA8)',
]

const getInitials = (name) => {
  if (!name) return '?'
  const parts = name.trim().split(' ')
  if (parts.length >= 2) return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
  return parts[0][0].toUpperCase()
}

const getAvatarColor = (name) => {
  if (!name) return avatarColors[0]
  let hash = 0
  for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash)
  return avatarColors[Math.abs(hash) % avatarColors.length]
}

const load = async () => {
  try {
    const res = await api.getUsuarios()
    usuarios.value = Array.isArray(res.data) ? res.data : (res.data.results || [])
  } catch (err) {
    toast?.error('Erro ao carregar', 'Não foi possível carregar a lista de usuários.')
  }
}

const save = async () => {
  if (!form.value.nome || !form.value.email || !form.value.data_nascimento) {
    toast?.warning('Campos obrigatórios', 'Preencha nome, e-mail e data de nascimento.')
    return
  }
  if (!form.value.id && !form.value.senha) {
    toast?.warning('Campos obrigatórios', 'A senha é obrigatória para cadastrar um novo usuário.')
    return
  }
  saving.value = true
  try {
    if (form.value.id) {
      await api.updateUsuario(form.value.id, form.value)
      toast?.success('Usuário atualizado', `"${form.value.nome}" foi atualizado com sucesso.`)
    } else {
      await api.createUsuario(form.value)
      toast?.success('Usuário cadastrado', `"${form.value.nome}" foi cadastrado no sistema.`)
    }
    reset()
    load()
  } catch (err) {
    let msg = 'Ocorreu um erro ao salvar os dados do usuário.'
    if (err.response && err.response.data) {
      const data = err.response.data
      if (typeof data === 'object' && !Array.isArray(data)) {
        const errors = Object.values(data).flat()
        if (errors.length > 0) msg = errors[0]
      } else if (typeof data === 'string') {
        msg = data
      }
    }
    toast?.error('Erro ao salvar', msg)
  } finally {
    saving.value = false
  }
}

const edit = (usuario) => {
  form.value = { ...usuario }
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const remove = async (id) => {
  const confirmed = await confirmRef.value?.show({
    title: 'Excluir usuário',
    message: 'Tem certeza que deseja excluir este usuário? Esta ação não pode ser desfeita.',
    confirmText: 'Sim, excluir',
    type: 'danger'
  })

  if (confirmed) {
    try {
      await api.deleteUsuario(id)
      toast?.success('Usuário excluído', 'O usuário foi removido do sistema.')
      load()
    } catch (err) {
      toast?.error('Erro ao excluir', 'Não foi possível excluir o usuário.')
    }
  }
}

const reset = () => {
  form.value = { id: null, nome: '', email: '', senha: '', data_nascimento: '', is_defesa_civil: false }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  const date = new Date(dateStr)
  return date.toLocaleDateString('pt-BR')
}

onMounted(load)
</script>

<style scoped>
.usuarios {
  display: flex;
  flex-direction: column;
  gap: 24px;
  animation: fadeInUp 0.4s ease-out;
}

/* Page Header */
.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-top: 4px;
}

/* Form Section */
.form-section {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 36px 32px;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
}

.form-section:hover {
  box-shadow: var(--shadow-md);
}

.form-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--accent-gradient);
}

.form-section-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 24px;
}

.form-section-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  background: var(--accent-soft);
  color: var(--accent);
  flex-shrink: 0;
}

.form-section-header h2 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.form-section-header p {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-top: 2px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 22px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
}

.input-wrapper input {
  padding-left: 40px;
}

.form-actions {
  display: flex;
  gap: 10px;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--accent-gradient);
  color: white;
  padding: 10px 22px;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 0.875rem;
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-glow);
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border);
  padding: 10px 22px;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 0.875rem;
}

.btn-secondary:hover {
  background: var(--bg-tertiary);
}

.spinner {
  animation: spin 0.8s linear infinite;
}

/* Table Section */
.table-section {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
}

.table-section:hover {
  box-shadow: var(--shadow-md);
}

.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-light);
}

.table-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
}

.table-title svg { color: var(--accent); }

.table-count {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-weight: 500;
  background: var(--bg-secondary);
  padding: 4px 12px;
  border-radius: var(--radius-full);
}

.table-wrapper { overflow-x: auto; }

/* User Cell */
.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  color: white;
  font-size: 0.8rem;
  font-weight: 700;
  flex-shrink: 0;
  letter-spacing: 0.02em;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-primary);
}

.user-id {
  font-size: 0.75rem;
  color: var(--text-muted);
  font-family: 'SF Mono', 'Fira Code', monospace;
}

.td-email {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.date-badge {
  display: inline-block;
  padding: 2px 10px;
  background: var(--bg-secondary);
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.td-actions {
  display: flex;
  gap: 6px;
  white-space: nowrap;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  background: var(--card-bg);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-action--edit {
  color: var(--accent);
}

.btn-action--edit:hover {
  background: var(--accent-soft);
  border-color: var(--accent);
  transform: none;
}

.btn-action--delete {
  color: var(--risk-high);
}

.btn-action--delete:hover {
  background: var(--risk-high-bg);
  border-color: var(--risk-high);
  transform: none;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 48px 24px !important;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: var(--text-muted);
}

.empty-content p {
  font-weight: 600;
  color: var(--text-secondary);
}

.empty-content span {
  font-size: 0.85rem;
}

.table-row-animated {
  animation: fadeInUp 0.3s ease-out both;
}

/* Toggle Switch */
.toggle-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0;
}

.toggle-label {
  display: flex;
  flex-direction: column;
  gap: 2px;
  cursor: pointer;
}

.toggle-text {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-primary);
}

.toggle-hint {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-left: 24px;
}

.toggle-switch {
  width: 44px;
  height: 24px;
  background: var(--border);
  border-radius: 12px;
  padding: 2px;
  cursor: pointer;
  transition: background 0.3s;
  flex-shrink: 0;
}

.toggle-switch.active {
  background: var(--accent);
}

.toggle-knob {
  width: 20px;
  height: 20px;
  background: #fff;
  border-radius: 50%;
  transition: transform 0.3s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}

.toggle-switch.active .toggle-knob {
  transform: translateX(20px);
}

/* Role Badge */
.role-badge {
  display: inline-block;
  font-size: 0.78rem;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 20px;
  background: var(--bg-primary);
  color: var(--text-secondary);
  border: 1px solid var(--border);
}

.role-badge--admin {
  background: var(--accent-soft);
  color: var(--accent);
  border-color: var(--accent);
}

/* Responsive */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-primary, .btn-secondary {
    justify-content: center;
  }

  .user-cell {
    gap: 8px;
  }
}
</style>