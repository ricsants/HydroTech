<template>
  <div class="minha-conta">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Minha Conta</h1>
        <p class="page-subtitle">Gerencie suas informacoes pessoais e credenciais de acesso</p>
      </div>
    </div>

    <!-- Profile Section -->
    <div class="profile-section">
      <div class="profile-card-header">
        <div class="profile-avatar" :style="{ background: avatarColor }">
          {{ initials }}
        </div>
        <div class="profile-summary">
          <h2>{{ name }}</h2>
          <span class="badge" :class="userData.is_defesa_civil ? 'badge--admin' : 'badge--user'">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            {{ userData.is_defesa_civil ? 'Defesa Civil Admin' : 'Usuario Comum' }}
          </span>
        </div>
      </div>

      <!-- Tabs Navigation -->
      <div class="tabs-nav">
        <button :class="{ active: activeTab === 'dados' }" @click="activeTab = 'dados'">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          Meus Dados
        </button>
        <button v-if="!userData.is_defesa_civil" :class="{ active: activeTab === 'preferencias' }" @click="activeTab = 'preferencias'">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
          Favoritos e Alertas
        </button>
      </div>

      <!-- Tab Content: Dados Pessoais -->
      <div v-if="activeTab === 'dados'" class="tab-content">
        <form @submit.prevent="handleSave" class="form-grid">
          <div class="form-group">
            <label>Nome Completo</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              <input v-model="form.nome" type="text" required placeholder="Seu nome" />
            </div>
          </div>

          <div class="form-group">
            <label>E-mail de Acesso</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
              <input v-model="form.email" type="email" placeholder="seu@email.com" />
            </div>
          </div>

          <div class="form-group">
            <label>Telefone</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
              <input v-model="form.telefone" type="tel" placeholder="(00) 00000-0000" />
            </div>
          </div>

          <div class="form-group">
            <label>Data de Nascimento</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
              <input v-model="form.data_nascimento" type="date" required />
            </div>
          </div>

          <div class="form-group">
            <label>Nova Senha (Opcional)</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              <input v-model="form.senha" type="password" placeholder="Preencha apenas para alterar" />
            </div>
          </div>
          
          <div class="form-actions">
            <p class="error-msg" v-if="errorMsg">{{ errorMsg }}</p>
            <p class="success-msg" v-if="successMsg">{{ successMsg }}</p>
            <button type="submit" class="btn-save" :disabled="loading">
              {{ loading ? 'Salvando...' : 'Salvar Alterações' }}
            </button>
          </div>
        </form>
      </div>

      <!-- Tab Content: Favoritos e Alertas -->
      <div v-if="activeTab === 'preferencias' && !userData.is_defesa_civil" class="tab-content preferences-tab">
        <div class="pref-section">
          <h3>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" class="icon-fav"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
            Pontos de Risco Favoritos
          </h3>
          <p class="empty-state" v-if="mappedFavs.length === 0">Nenhum ponto favoritado ainda.</p>
          <div class="list-cards" v-else>
            <div class="list-card" v-for="item in mappedFavs" :key="item.id">
              <div class="list-info" style="cursor: pointer;" @click="goToMonitoramento(item.id)">
                <strong>{{ item.rioNome }}</strong>
                <span>{{ item.descricao }}</span>
              </div>
              <div class="list-actions">
                <button class="btn-remove" :class="{'btn-active': alerts.has(item.id)}" @click="toggleAlertInline(item.id)" :title="alerts.has(item.id) ? 'Desativar Alerta' : 'Ativar Alerta'">
                  <svg width="18" height="18" viewBox="0 0 24 24" :fill="alerts.has(item.id) ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                </button>
                <button class="btn-remove" @click="removeFav(item.id)" title="Remover dos Favoritos">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="pref-section">
          <h3>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" class="icon-alert"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            Recebendo Alertas
          </h3>
          <p class="empty-state" v-if="mappedAlerts.length === 0">Nenhum alerta configurado.</p>
          <div class="list-cards" v-else>
            <div class="list-card" v-for="item in mappedAlerts" :key="item.id">
              <div class="list-info" style="cursor: pointer;" @click="goToMonitoramento(item.id)">
                <strong>{{ item.rioNome }}</strong>
                <span>{{ item.descricao }}</span>
              </div>
              <button class="btn-remove" @click="removeAlert(item.id)" title="Desativar Alerta">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

// Initial Local Storage Data
const userData = ref(JSON.parse(localStorage.getItem('user_data') || '{}'))
const favs = ref(new Set(JSON.parse(localStorage.getItem('ht_favs') || '[]')))
const alerts = ref(new Set(JSON.parse(localStorage.getItem('ht_alerts') || '[]')))

const activeTab = ref('dados')
const loading = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

// Form State
const form = ref({
  nome: userData.value.nome || '',
  email: userData.value.email || '',
  telefone: userData.value.telefone || '',
  data_nascimento: userData.value.data_nascimento || '',
  senha: ''
})

const rios = ref([])
const pontos = ref({})

onMounted(async () => {
  try {
    // Busca os dados do usuário do DB
    const resMe = await api.me()
    userData.value = resMe.data
    form.value.nome = resMe.data.nome
    form.value.email = resMe.data.email
    form.value.telefone = resMe.data.telefone
    form.value.data_nascimento = resMe.data.data_nascimento

    // Sincroniza localStorage com o DB do usuário logado
    localStorage.setItem('user_data', JSON.stringify(resMe.data))
    if (resMe.data.favoritos) {
      favs.value = new Set(resMe.data.favoritos)
      localStorage.setItem('ht_favs', JSON.stringify([...favs.value]))
    }
    if (resMe.data.alertas) {
      alerts.value = new Set(resMe.data.alertas)
      localStorage.setItem('ht_alerts', JSON.stringify([...alerts.value]))
    }

    if (resMe.data.deve_alterar_senha) {
      successMsg.value = 'Esse é seu primeiro acesso. Altere sua senha para continuar.'
    }

    // Busca os rios para exibir os nomes nos Favoritos
    const resRios = await api.getRiosPublico()
    rios.value = Array.isArray(resRios.data) ? resRios.data : resRios.data.results || []
    await Promise.all(rios.value.map(async rio => {
      try {
        const pr = await api.getPontosRiscoPublico(rio.id)
        pontos.value[rio.id] = Array.isArray(pr.data) ? pr.data : pr.data.results || []
      } catch { pontos.value[rio.id] = [] }
    }))
  } catch (err) {
    console.error('Erro ao carregar dados:', err)
  }
})

const handleSave = async () => {
  errorMsg.value = ''
  successMsg.value = ''
  loading.value = true
  try {
    const payload = {
      nome: form.value.nome,
      email: form.value.email,
      telefone: form.value.telefone,
      data_nascimento: form.value.data_nascimento
    }
    if (form.value.senha) payload.senha = form.value.senha
    
    const res = await api.updateMe(payload)
    userData.value = res.data
    localStorage.setItem('user_data', JSON.stringify(res.data))
    localStorage.setItem('user_name', res.data.nome)
    window.dispatchEvent(new Event('storage-update'))
    
    successMsg.value = 'Dados atualizados com sucesso!'
    
    if (form.value.senha) {
      successMsg.value = 'Senha atualizada! Faça login novamente.'
      setTimeout(() => {
        localStorage.removeItem('user_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
      }, 2000)
    }
  } catch (err) {
    if (err.response && err.response.data) {
      const msgs = []
      for (const key in err.response.data) {
        msgs.push(`${key}: ${err.response.data[key]}`)
      }
      errorMsg.value = msgs.join(' | ')
    } else {
      errorMsg.value = 'Erro ao atualizar dados. Tente novamente.'
    }
  } finally {
    loading.value = false
  }
}

const removeFav = async (id) => {
  favs.value.delete(id)
  localStorage.setItem('ht_favs', JSON.stringify([...favs.value]))
  try { await api.toggleFavorite(id) } catch (e) {}
}

const removeAlert = async (id) => {
  alerts.value.delete(id)
  localStorage.setItem('ht_alerts', JSON.stringify([...alerts.value]))
  try { await api.toggleAlert(id) } catch (e) {}
}

const toggleAlertInline = async (id) => {
  if (alerts.value.has(id)) {
    alerts.value.delete(id)
  } else {
    alerts.value.add(id)
  }
  localStorage.setItem('ht_alerts', JSON.stringify([...alerts.value]))
  try { await api.toggleAlert(id) } catch (e) {}
}

const goToMonitoramento = (id) => {
  router.push({ path: '/monitoramento', query: { ponto: id } })
}

const name = computed(() => userData.value.nome || 'Usuário')

const initials = computed(() => {
  const parts = name.value.trim().split(' ')
  if (parts.length >= 2) return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
  return parts[0][0].toUpperCase()
})

const avatarColors = [
  'linear-gradient(135deg, #667eea, #764ba2)',
  'linear-gradient(135deg, #f093fb, #f5576c)',
  'linear-gradient(135deg, #4facfe, #00f2fe)',
  'linear-gradient(135deg, #43e97b, #38f9d7)',
  'linear-gradient(135deg, #fa709a, #fee140)'
]

const avatarColor = computed(() => {
  let hash = 0
  for (let i = 0; i < name.value.length; i++) hash = name.value.charCodeAt(i) + ((hash << 5) - hash)
  return avatarColors[Math.abs(hash) % avatarColors.length]
})

const mappedFavs = computed(() => {
  const list = []
  Object.entries(pontos.value).forEach(([rId, pts]) => {
    pts.forEach(p => {
      if (favs.value.has(p.id)) {
        const rio = rios.value.find(r => r.id === Number(rId))
        list.push({ ...p, rioNome: rio ? rio.nome : 'Rio Desconhecido' })
      }
    })
  })
  return list
})

const mappedAlerts = computed(() => {
  const list = []
  Object.entries(pontos.value).forEach(([rId, pts]) => {
    pts.forEach(p => {
      if (alerts.value.has(p.id)) {
        const rio = rios.value.find(r => r.id === Number(rId))
        list.push({ ...p, rioNome: rio ? rio.nome : 'Rio Desconhecido' })
      }
    })
  })
  return list
})
</script>

<style scoped>
.minha-conta {
  display: flex;
  flex-direction: column;
  gap: 24px;
  animation: fadeInUp 0.4s ease-out;
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
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

/* Profile Section */
.profile-section {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 40px;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.profile-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--accent-gradient);
}

.profile-card-header {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 32px;
}

.profile-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: var(--radius-full);
  color: white;
  font-size: 1.75rem;
  font-weight: 800;
  flex-shrink: 0;
  box-shadow: var(--shadow-sm);
}

.profile-summary {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.profile-summary h2 {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  align-self: flex-start;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.badge--admin { background: var(--accent-soft); color: var(--accent); }
.badge--user { background: var(--bg-tertiary); color: var(--text-secondary); }

/* Tabs Navigation */
.tabs-nav {
  display: flex;
  gap: 16px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 32px;
}

.tabs-nav button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: -1px;
}

.tabs-nav button:hover {
  color: var(--text-primary);
}

.tabs-nav button.active {
  color: var(--accent);
  border-bottom-color: var(--accent);
}

/* Tab Content */
.tab-content {
  animation: fadeIn 0.3s ease-out;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 14px;
  color: var(--text-muted);
  pointer-events: none;
}

.input-wrapper input {
  width: 100%;
  padding: 12px 16px 12px 42px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.input-wrapper input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1);
}

.form-actions {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 16px;
  margin-top: 16px;
  padding-top: 24px;
  border-top: 1px solid var(--border-light);
}

.btn-save {
  padding: 12px 24px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-glow);
}

.btn-save:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-msg { color: var(--risk-high); font-weight: 600; font-size: 0.9rem; }
.success-msg { color: var(--risk-low); font-weight: 600; font-size: 0.9rem; }

/* Preferences Tab */
.preferences-tab {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.pref-section h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon-fav { color: #f43f5e; fill: #f43f5e; }
.icon-alert { color: #f59e0b; fill: #f59e0b; }

.empty-state {
  color: var(--text-muted);
  font-size: 0.9rem;
  background: var(--bg-primary);
  padding: 16px;
  border-radius: var(--radius-md);
  border: 1px dashed var(--border);
  text-align: center;
}

.list-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.list-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  transition: all 0.2s ease;
}

.list-card:hover {
  border-color: var(--border-light);
  box-shadow: var(--shadow-sm);
}

.list-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.list-info strong {
  font-size: 0.9rem;
  color: var(--text-primary);
}

.list-info span {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.btn-remove {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 6px;
  border-radius: 50%;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-remove:hover {
  background: rgba(239, 68, 68, 0.1);
  color: var(--risk-high);
}

.btn-active {
  color: var(--accent) !important;
  background: rgba(14, 165, 233, 0.15) !important;
}

/* Animations */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 768px) {
  .form-grid, .preferences-tab {
    grid-template-columns: 1fr;
  }
}
</style>
