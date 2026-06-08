<template>
  <div class="login-page">
    <div class="login-split">
      <!-- Left Panel -->
      <div class="login-panel-left">
        <div class="panel-content">
          <div class="status-chip">
            <span class="status-dot"></span>
            Sistema Operacional
          </div>
          <h1>Sistema de Monitoramento<br>Hidrológico</h1>
          <p>Plataforma institucional de alta precisão para gestão de riscos de enchente e coordenação de infraestrutura crítica.</p>
          <div class="panel-features">
            <div class="feature-item">
              <div class="feature-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                  <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                </svg>
              </div>
              <span>Monitoramento em tempo real</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                </svg>
              </div>
              <span>Mapeamento de pontos de risco</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                  <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
                </svg>
              </div>
              <span>Alertas instantâneos</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Form -->
      <div class="login-panel-right">
        <div class="login-card">
          <div class="login-card-header">
            <h2>Acessar Sistema</h2>
            <p>Insira suas credenciais para continuar</p>
          </div>

          <!-- Login Mode Toggle -->
          <div class="login-mode-toggle">
            <button :class="{ active: loginMode === 'email' }" @click="loginMode = 'email'">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
              E-mail
            </button>
            <button :class="{ active: loginMode === 'telefone' }" @click="loginMode = 'telefone'">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
              Telefone
            </button>
          </div>

          <form @submit.prevent="login" class="login-form">
            <!-- Email field -->
            <div v-if="loginMode === 'email'" class="form-group">
              <label for="login-email">E-mail</label>
              <div class="input-wrapper">
                <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                  <rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
                </svg>
                <input id="login-email" v-model="form.email" type="email" placeholder="seu@email.com" autocomplete="email"/>
              </div>
            </div>

            <!-- Phone field -->
            <div v-else class="form-group">
              <label for="login-phone">Telefone</label>
              <div class="input-wrapper">
                <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/>
                </svg>
                <input id="login-phone" :value="form.telefone" @input="onPhoneInput($event, 'telefone')" type="tel" inputmode="numeric" placeholder="(11) 99999-9999" autocomplete="tel"/>
              </div>
            </div>

            <div class="form-group">
              <label for="login-password">Senha</label>
              <div class="input-wrapper">
                <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                  <rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
                <input id="login-password" v-model="form.senha" :type="showSenha ? 'text' : 'password'" placeholder="••••••••" autocomplete="current-password"/>
                <button type="button" class="btn-toggle-pw" @click="showSenha = !showSenha" tabindex="-1">
                  <svg v-if="!showSenha" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                </button>
              </div>
            </div>

            <p class="error-msg" v-if="error">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>
              </svg>
              {{ error }}
            </p>

            <button class="btn-login" type="submit" :disabled="loading">
              <svg v-if="loading" class="spin" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32">
                  <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="0.8s" repeatCount="indefinite"/>
                </circle>
              </svg>
              <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/>
              </svg>
              {{ loading ? 'Autenticando...' : 'Acessar Sistema' }}
            </button>
          </form>

          <div class="login-card-footer">
            <p>Novo usuário? <router-link to="/registro">Criar Conta</router-link></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const loginMode = ref('email')
const form = ref({ email: '', telefone: '', senha: '' })
const loading = ref(false)
const error = ref('')
const showSenha = ref(false)

const onPhoneInput = (e, field) => {
  let digits = e.target.value.replace(/\D/g, '').slice(0, 11)
  let formatted = ''
  if (digits.length > 0) formatted += '(' + digits.slice(0, 2)
  if (digits.length >= 2) formatted += ') '
  if (digits.length > 2) formatted += digits.slice(2, 7)
  if (digits.length > 7) formatted += '-' + digits.slice(7, 11)
  form.value[field] = formatted
  e.target.value = formatted
}

const login = async () => {
  const credential = loginMode.value === 'email' ? form.value.email : form.value.telefone
  if (!credential || !form.value.senha) { error.value = 'Preencha todos os campos.'; return }
  loading.value = true; error.value = ''
  try {
    const payload = { senha: form.value.senha }
    if (loginMode.value === 'email') {
      payload.email = form.value.email
    } else {
      payload.telefone = form.value.telefone
    }
    const response = await api.login(payload)
    const { access, refresh, usuario } = response.data
    localStorage.setItem('user_token', access)
    localStorage.setItem('refresh_token', refresh)
    localStorage.setItem('user_name', usuario.nome)
    localStorage.setItem('user_data', JSON.stringify(usuario))
    if (usuario.favoritos) localStorage.setItem('ht_favs', JSON.stringify(usuario.favoritos))
    if (usuario.alertas) localStorage.setItem('ht_alerts', JSON.stringify(usuario.alertas))
    window.dispatchEvent(new Event('storage-update'))
    if (usuario.deve_alterar_senha) {
      router.push('/minha-conta')
    } else {
      router.push('/')
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Credenciais inválidas.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page { min-height: 100vh; background: var(--bg-primary); }

.login-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 100vh;
}

/* Left Panel */
.login-panel-left {
  background: var(--bg-secondary);
  border-right: 1px solid var(--border);
  padding: 40px 48px;
  display: flex;
  flex-direction: column;
  gap: 48px;
}

.panel-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--text-primary);
}

.panel-logo {
  width: 34px; height: 34px;
  border-radius: var(--radius-sm);
  background: var(--accent-gradient);
  display: flex; align-items: center; justify-content: center;
  color: white;
}

.panel-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
  flex: 1;
  justify-content: center;
}

.status-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px;
  border-radius: var(--radius-full);
  background: var(--status-active-bg);
  border: 1px solid rgba(16, 185, 129, 0.2);
  color: var(--status-active);
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  width: fit-content;
}

.status-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--status-active);
  animation: pulse 2s infinite;
}

.panel-content h1 {
  font-size: 2rem;
  font-weight: 800;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.panel-content p {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.7;
}

.panel-features { display: flex; flex-direction: column; gap: 12px; margin-top: 8px; }

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.feature-icon {
  width: 28px; height: 28px;
  border-radius: var(--radius-sm);
  background: var(--accent-soft);
  color: var(--accent);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

/* Right Form */
.login-panel-right {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 48px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  animation: fadeInUp 0.4s ease-out;
}

.login-card-header h2 {
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.login-card-header p {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-top: 6px;
}

/* Login Mode Toggle */
.login-mode-toggle {
  display: flex;
  gap: 0;
  background: var(--bg-secondary, #f1f5f9);
  border-radius: var(--radius-md);
  padding: 4px;
  border: 1px solid var(--border);
}
.login-mode-toggle button {
  flex: 1;
  display: flex; align-items: center; justify-content: center; gap: 8px;
  padding: 10px 16px;
  border-radius: calc(var(--radius-md) - 2px);
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.82rem;
  cursor: pointer;
  transition: all 0.2s;
}
.login-mode-toggle button.active {
  background: var(--accent);
  color: white;
  box-shadow: 0 2px 8px rgba(14, 165, 233, 0.3);
}
.login-mode-toggle button:not(.active):hover {
  color: var(--text-primary);
  background: var(--bg-primary, rgba(0,0,0,0.05));
}

.login-form { display: flex; flex-direction: column; gap: 16px; }

.form-group { display: flex; flex-direction: column; gap: 6px; }

.form-group label {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.input-wrapper { position: relative; display: flex; align-items: center; }

.input-icon {
  position: absolute; left: 13px; top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted); pointer-events: none;
}

.input-wrapper input { padding-left: 40px; padding-right: 44px; }

.btn-login {
  display: flex; align-items: center; justify-content: center; gap: 9px;
  width: 100%; padding: 13px;
  border-radius: var(--radius-md);
  background: var(--accent);
  color: white;
  font-weight: 700; font-size: 0.9rem;
  border: 1px solid var(--accent-hover);
  cursor: pointer; margin-top: 4px;
  transition: all var(--transition-normal);
  letter-spacing: 0.02em;
}

.btn-login:hover:not(:disabled) {
  background: var(--accent);
  border-color: var(--accent);
  box-shadow: var(--shadow-glow);
  transform: translateY(-1px);
}

.btn-login:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }

.error-msg {
  display: flex; align-items: center; gap: 8px;
  color: var(--risk-high);
  background: var(--risk-high-bg);
  padding: 10px 14px;
  border-radius: var(--radius-md);
  font-size: 0.82rem; font-weight: 500;
  border: 1px solid rgba(220, 38, 38, 0.2);
}

.login-card-footer { text-align: center; }

.login-card-footer p { font-size: 0.85rem; color: var(--text-muted); }

.login-card-footer a { color: var(--accent); font-weight: 600; text-decoration: none; }
.login-card-footer a:hover { text-decoration: underline; }

/* Password Toggle Button */
.btn-toggle-pw {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: color 0.2s;
}
.btn-toggle-pw:hover {
  color: var(--text-primary);
  transform: translateY(-50%);
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
  .login-split { grid-template-columns: 1fr; }
  .login-panel-left { display: none; }
  .login-panel-right { padding: 32px 24px; align-items: flex-start; padding-top: 48px; }
}
</style>