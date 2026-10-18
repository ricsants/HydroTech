<template>
  <div class="login-page">
    <!-- Ambient Background Layers -->
    <div class="ambient" aria-hidden="true">
      <div class="ambient-gradient"></div>
      <div class="ambient-grid"></div>
      <div class="ambient-topo"></div>
      <div class="ambient-orbs">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
      </div>
      <div class="ambient-particles">
        <div v-for="i in 12" :key="i" class="particle" :style="particleStyle(i)"></div>
      </div>
    </div>

    <!-- Animated Waves -->
    <div class="waves" aria-hidden="true">
      <svg class="wave-svg" viewBox="0 0 2880 160" preserveAspectRatio="none">
        <path class="wave-path wave-1" d="M0,80 C240,20 480,140 720,80 C960,20 1200,140 1440,80 C1680,20 1920,140 2160,80 C2400,20 2640,140 2880,80 L2880,160 L0,160 Z" />
        <path class="wave-path wave-2" d="M0,100 C360,40 720,160 1080,100 C1440,40 1800,160 2160,100 C2520,40 2880,160 2880,100 L2880,160 L0,160 Z" />
      </svg>
    </div>

    <!-- Main Content -->
    <div class="content">
      <div class="content-inner">
        <!-- Left: Ambient Data Panel -->
        <div class="ambient-panel">
          <div class="live-badge">
            <span class="live-dot"></span>
            <span class="live-text">SISTEMA ATIVO</span>
            <span class="live-time">{{ currentTime }}</span>
          </div>

          <div class="system-grid">
            <div class="sys-card">
              <span class="sys-label">RIOS MONITORADOS</span>
              <span class="sys-value">{{ sysInfo.totalRios }}</span>
            </div>
            <div class="sys-card">
              <span class="sys-label">PONTOS DE RISCO</span>
              <span class="sys-value">{{ sysInfo.totalPontos }}</span>
            </div>
            <div class="sys-card">
              <span class="sys-label">STATUS</span>
              <span class="sys-value sys-status">{{ sysInfo.status }}</span>
            </div>
          </div>
        </div>

        <!-- Right: Login Card -->
        <div class="login-card">
          <div class="card-accent"></div>

          <div class="card-header">
            <div class="brand">
              <div class="brand-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
                  <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z" fill="rgba(255,255,255,0.08)"/>
                  <path d="M12 6v12" />
                  <path d="M6 12h12" />
                </svg>
              </div>
              <div class="brand-text">
                <span class="brand-name">HydroTech</span>
                <span class="brand-sub">MONITORAMENTO HIDROLÓGICO</span>
              </div>
            </div>
            <div class="brand-badge">v2.0</div>
          </div>

          <div class="card-body">
            <div class="card-title">
              <span class="title-eyebrow">ACESSO RESTRITO</span>
              <h1>Autenticação</h1>
              <p>Informe suas credenciais para acessar o painel de monitoramento</p>
            </div>

            <div class="mode-tabs" role="tablist">
              <button :class="{ active: loginMode === 'email' }" @click="loginMode = 'email'" role="tab" :aria-selected="loginMode === 'email'" type="button">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
                E-mail
              </button>
              <button :class="{ active: loginMode === 'telefone' }" @click="loginMode = 'telefone'" role="tab" :aria-selected="loginMode === 'telefone'" type="button">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                Telefone
              </button>
            </div>

            <form @submit.prevent="login" class="login-form" novalidate>
              <Transition name="fade" mode="out-in">
                <div v-if="loginMode === 'email'" key="email" class="field-group">
                  <label for="login-email">E-mail corporativo</label>
                  <div class="field-wrap" :class="{ 'field-error': errors.email }">
                    <input id="login-email" v-model="form.email" type="email" placeholder="seu@email.com" autocomplete="email" :aria-invalid="errors.email" @input="clearError('email')" @blur="validateField('email')" />
                    <span class="field-glow"></span>
                    <svg v-if="!errors.email && form.email" class="field-check" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
                  </div>
                  <p v-if="errors.email" class="field-msg error-msg">Informe um e-mail válido</p>
                </div>
                <div v-else key="phone" class="field-group">
                  <label for="login-phone">Telefone</label>
                  <div class="field-wrap" :class="{ 'field-error': errors.telefone }">
                    <input id="login-phone" :value="form.telefone" @input="onPhoneInput($event, 'telefone')" type="tel" inputmode="numeric" placeholder="(00) 00000-0000" autocomplete="tel" :aria-invalid="errors.telefone" @focus="clearError('telefone')" @blur="validateField('telefone')" />
                    <span class="field-glow"></span>
                  </div>
                  <p v-if="errors.telefone" class="field-msg error-msg">Informe um telefone válido</p>
                </div>
              </Transition>

              <div class="field-group">
                <label for="login-password">Senha</label>
                <div class="field-wrap" :class="{ 'field-error': errors.senha }">
                  <input id="login-password" v-model="form.senha" :type="showSenha ? 'text' : 'password'" placeholder="••••••••" autocomplete="current-password" :aria-invalid="errors.senha" @input="clearError('senha')" @blur="validateField('senha')" />
                  <span class="field-glow"></span>
                  <button type="button" class="btn-eye" @click="showSenha = !showSenha" tabindex="-1" :aria-label="showSenha ? 'Ocultar senha' : 'Mostrar senha'">
                    <svg v-if="!showSenha" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                    <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                  </button>
                </div>
                <p v-if="errors.senha" class="field-msg error-msg">A senha é obrigatória</p>
              </div>

              <div class="form-options">
                <label class="check-label">
                  <input type="checkbox" v-model="remember" class="check-input" />
                  <span class="check-box">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
                  </span>
                  Manter sessão
                </label>
                <a href="#" class="forgot-link" @click.prevent>Recuperar senha</a>
              </div>

              <Transition name="fade">
                <p class="form-error" v-if="error" role="alert">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
                  {{ error }}
                </p>
              </Transition>

              <button class="btn-submit" type="submit" :disabled="loading">
                <span class="btn-content" :class="{ 'btn-hidden': loading }">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
                  Acessar Plataforma
                </span>
                <span class="btn-loading" :class="{ 'btn-visible': loading }">
                  <svg class="spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32">
                      <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="0.8s" repeatCount="indefinite"/>
                    </circle>
                  </svg>
                  Autenticando...
                </span>
              </button>
            </form>
          </div>

          <div class="card-footer">
            <p>Novo usuário? <router-link to="/registro">Criar conta</router-link></p>
            <div class="secure-badge">
              <span class="secure-dot"></span>
              <span>Conexão segura</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Status Bar -->
      <div class="status-bar">
        <div class="status-item">
          <span class="status-dot status-green"></span>
          <span>Sistema operacional</span>
        </div>
        <div class="status-item">
          <span class="status-dot status-green"></span>
          <span>Uptime: {{ uptime }}</span>
        </div>
        <div class="status-item">
          <span class="status-dot" :class="signalClass"></span>
          <span>Sinal: {{ signalStrength }}</span>
        </div>
        <div class="status-item status-right">
          <span>HydroTech © 2026</span>
          <span class="status-sep"></span>
          <span>Defesa Civil</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const loginMode = ref('email')
const form = ref({ email: '', telefone: '', senha: '' })
const errors = ref({ email: false, telefone: false, senha: false })
const loading = ref(false)
const error = ref('')
const showSenha = ref(false)
const remember = ref(true)

// System info
const sysInfo = ref({
  totalRios: '—',
  totalPontos: '—',
  status: 'OPERACIONAL'
})
const currentTime = ref('')
const uptime = ref('00:00:00')
const signalStrength = ref('Excelente')

let uptimeSeconds = 0
let clockTimer = null
let signalTimer = null
let disposed = false

const signalClass = computed(() => {
  if (signalStrength.value === 'Excelente') return 'status-green'
  if (signalStrength.value === 'Bom') return 'status-yellow'
  return 'status-red'
})

const particleStyle = (i) => {
  const seed = i * 31
  const x = (seed * 7) % 100
  const y = 100 + ((seed * 13) % 40)
  const size = 1.5 + (i % 4) * 1.2
  const dur = 14 + (i % 7) * 3
  const delay = (i * 1.1) % 12
  const drift = (i % 5) * 8 - 16
  return {
    left: `${x}%`,
    bottom: `-${size}px`,
    width: `${size}px`,
    height: `${size}px`,
    animationDuration: `${dur}s`,
    animationDelay: `${delay}s`,
    opacity: 0.15 + (i % 5) * 0.08,
    '--drift': `${drift}px`
  }
}

const clearError = (field) => {
  errors.value[field] = false
  if (error.value) error.value = ''
}

const validateField = (field) => {
  if (field === 'email') {
    if (!form.value.email) errors.value.email = true
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) errors.value.email = true
  } else if (field === 'telefone') {
    if (!form.value.telefone) errors.value.telefone = true
    else if (form.value.telefone.replace(/\D/g, '').length < 10) errors.value.telefone = true
  } else if (field === 'senha') {
    if (!form.value.senha) errors.value.senha = true
  }
}

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

const validate = () => {
  let valid = true
  const field = loginMode.value === 'email' ? 'email' : 'telefone'
  validateField(field)
  validateField('senha')
  if (errors.value[field]) valid = false
  if (errors.value.senha) valid = false
  return valid
}

const focusFirstInvalid = () => {
  const field = loginMode.value === 'email' ? 'email' : 'telefone'
  const id = errors.value[field] ? field : errors.value.senha ? 'senha' : null
  if (id) {
    const map = { email: 'email', telefone: 'phone', senha: 'password' }
    const el = document.getElementById(`login-${map[id]}`)
    if (el) setTimeout(() => el.focus(), 100)
  }
}

const login = async () => {
  if (!validate()) { focusFirstInvalid(); return }
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
    router.push(usuario.deve_alterar_senha ? '/minha-conta' : '/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Credenciais inválidas. Verifique os dados e tente novamente.'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (remember.value) {
    const saved = localStorage.getItem('login_email')
    if (saved) form.value.email = saved
  }

  try {
    const res = await api.getPublicSummary()
    if (disposed) return
    sysInfo.value.totalRios = res.data.total_rios
    sysInfo.value.totalPontos = res.data.total_pontos
  } catch {
    if (disposed) return
    sysInfo.value.totalRios = '—'
    sysInfo.value.totalPontos = '—'
  }

  const updateClock = () => {
    currentTime.value = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    uptimeSeconds++
    const h = String(Math.floor(uptimeSeconds / 3600)).padStart(2, '0')
    const m = String(Math.floor((uptimeSeconds % 3600) / 60)).padStart(2, '0')
    const s = String(uptimeSeconds % 60).padStart(2, '0')
    uptime.value = `${h}:${m}:${s}`
  }
  currentTime.value = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  clockTimer = setInterval(updateClock, 1000)

  const signals = ['Excelente', 'Excelente', 'Excelente', 'Bom', 'Excelente']
  let sigIdx = 0
  signalTimer = setInterval(() => {
    signalStrength.value = signals[sigIdx % signals.length]
    sigIdx++
  }, 8000)
})

onUnmounted(() => {
  disposed = true
  if (clockTimer) clearInterval(clockTimer)
  if (signalTimer) clearInterval(signalTimer)
})


</script>

<style scoped>
/* ═══════════════════════════════════════════
   HYDROTECH — LOGIN VIEW
   Command Center Aesthetic
   ═══════════════════════════════════════════ */

.login-page {
  min-height: 100vh;
  background: var(--bg-primary);
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ══════════════ AMBIENT BACKGROUND ══════════════ */

.ambient {
  position: fixed; inset: 0; z-index: 0;
  pointer-events: none;
}

[data-theme='dark'] .ambient-gradient {
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(6, 182, 212, 0.06) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(59, 130, 246, 0.04) 0%, transparent 40%),
    linear-gradient(180deg, var(--bg-primary) 0%, #081426 30%, #0A1A30 60%, #060E1A 100%);
}

[data-theme='dark'] .ambient-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(59, 130, 246, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59, 130, 246, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse at center, black 30%, transparent 70%);
  -webkit-mask-image: radial-gradient(ellipse at center, black 30%, transparent 70%);
}

[data-theme='dark'] .ambient-topo {
  position: absolute; inset: 0;
  opacity: 0.08;
  background-image:
    radial-gradient(circle at 25% 35%, transparent 0%, transparent 30%, rgba(6,182,212,0.06) 32%, transparent 35%),
    radial-gradient(circle at 65% 55%, transparent 0%, transparent 25%, rgba(59,130,246,0.05) 27%, transparent 30%),
    radial-gradient(circle at 45% 75%, transparent 0%, transparent 40%, rgba(6,182,212,0.04) 42%, transparent 45%);
  background-size: 300px 300px;
}

@keyframes topoDrift {
  0% { transform: translate(0, 0); }
  50% { transform: translate(10px, -6px); }
  100% { transform: translate(0, 0); }
}

/* ── Orbs ── */

.ambient-orbs {
  position: absolute; inset: 0;
  overflow: hidden;
}

[data-theme='dark'] .orb {
  position: absolute;
  border-radius: 50%;
}

[data-theme='dark'] .orb-1 {
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(6, 182, 212, 0.1) 0%, transparent 60%);
  top: -10%; left: -5%;
}

[data-theme='dark'] .orb-2 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.08) 0%, transparent 60%);
  bottom: -10%; right: 5%;
}

.orb-3 {
  display: none;
}

@keyframes orbFloat1 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(60px, 40px) scale(1.1); }
  66% { transform: translate(-30px, 20px) scale(0.95); }
}

@keyframes orbFloat2 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(-40px, -30px) scale(1.15); }
}

@keyframes orbFloat3 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(20px, -40px) scale(1.05); }
  66% { transform: translate(-20px, 10px) scale(0.95); }
}

/* ── Water Droplet Particles ── */

.ambient-particles {
  position: absolute; inset: 0;
  pointer-events: none;
  overflow: hidden;
}

[data-theme='dark'] .particle {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, rgba(6, 182, 212, 0.5), rgba(59, 130, 246, 0.2));
  box-shadow: 0 0 4px rgba(6, 182, 212, 0.15);
  animation: dropletRise linear infinite;
  will-change: transform, opacity;
}

@keyframes dropletRise {
  0% {
    transform: translateY(0) translateX(0);
    opacity: 0;
  }
  10% {
    opacity: 0.6;
  }
  100% {
    transform: translateY(-110vh) translateX(var(--drift, 0px));
    opacity: 0;
  }
}

/* ══════════════ WAVES ══════════════ */

.waves {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 120px;
  z-index: 1;
  pointer-events: none;
}

[data-theme='dark'] .wave-svg {
  display: block;
  width: 200%;
  height: 100%;
}

.wave-path {
  fill: none;
}

[data-theme='dark'] .wave-1 {
  fill: rgba(6, 182, 212, 0.04);
}

[data-theme='dark'] .wave-2 {
  fill: rgba(59, 130, 246, 0.03);
}

@keyframes waveSlide {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

/* ══════════════ MAIN CONTENT ══════════════ */

.content {
  position: relative;
  z-index: 3;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  padding: 24px 32px;
  gap: 24px;
}

.content-inner {
  width: 100%;
  max-width: 1200px;
  display: flex;
  gap: 32px;
  flex: 1;
  align-items: center;
}

/* ══════════════ AMBIENT PANEL (LEFT) ══════════════ */

.ambient-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 28px;
  padding: 24px 0;
  animation: fadeInUp 0.7s ease-out;
}

.live-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: var(--text-secondary);
  text-transform: uppercase;
}

.live-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #10B981;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
  animation: dotPulse 2s ease-in-out infinite;
}

@keyframes dotPulse {
  0%, 100% { opacity: 1; box-shadow: 0 0 8px rgba(16, 185, 129, 0.4); }
  50% { opacity: 0.5; box-shadow: 0 0 12px rgba(16, 185, 129, 0.15); }
}

.live-text {
  color: var(--status-active);
}

.live-time {
  margin-left: auto;
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-size: 0.7rem;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

/* ── System Info Grid ── */

.system-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  max-width: 320px;
}

.sys-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: border-color 0.3s, background 0.3s;
}

.sys-card:hover {
  border-color: var(--border-accent);
  background: var(--bg-tertiary);
}

.sys-label {
  font-size: 0.6rem;
  font-weight: 700;
  color: var(--text-dim);
  letter-spacing: 0.12em;
}

.sys-value {
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.01em;
}

.sys-status {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--status-active);
  letter-spacing: 0.08em;
}

/* ══════════════ LOGIN CARD (RIGHT) ══════════════ */

.login-card {
  width: 400px;
  flex-shrink: 0;
  position: relative;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 16px;
  box-shadow: var(--shadow-xl);
  animation: cardIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  overflow: hidden;
}

.card-accent {
  position: absolute;
  top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent), var(--accent-hover), var(--accent), transparent);
  background-size: 200% 100%;
  animation: accentSlide 4s ease-in-out infinite;
}

@keyframes accentSlide {
  0%, 100% { background-position: 200% 0; }
  50% { background-position: -200% 0; }
}

@keyframes cardIn {
  from { opacity: 0; transform: translateY(24px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ── Card Header ── */

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 24px;
  border-bottom: 1px solid var(--border-light);
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-icon {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: var(--accent-gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 2px 16px rgba(6, 182, 212, 0.2);
  flex-shrink: 0;
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.brand-name {
  font-size: 1rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.brand-sub {
  font-size: 0.58rem;
  font-weight: 600;
  color: var(--accent);
  letter-spacing: 0.15em;
  opacity: 0.7;
}

.brand-badge {
  font-size: 0.58rem;
  font-weight: 700;
  color: var(--text-muted);
  background: var(--bg-secondary);
  padding: 3px 10px;
  border-radius: 20px;
  border: 1px solid var(--border-light);
  letter-spacing: 0.05em;
}

/* ── Card Body ── */

.card-body {
  padding: 22px 24px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.card-title {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.title-eyebrow {
  font-size: 0.6rem;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: 0.18em;
  text-transform: uppercase;
  opacity: 0.7;
}

.card-title h1 {
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.card-title p {
  font-size: 0.82rem;
  color: var(--text-secondary);
  margin-top: 4px;
  line-height: 1.5;
}

/* ── Mode Tabs ── */

.mode-tabs {
  display: flex;
  gap: 0;
  background: var(--bg-secondary);
  border-radius: 8px;
  padding: 3px;
  border: 1px solid var(--border-light);
}

.mode-tabs button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 9px 16px;
  border-radius: 6px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.78rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: inherit;
  position: relative;
}

.mode-tabs button.active {
  background: var(--accent-gradient);
  color: white;
  box-shadow: 0 2px 12px rgba(6, 182, 212, 0.25);
}

.mode-tabs button:not(.active):hover {
  color: var(--text-secondary);
  background: var(--bg-tertiary);
}

/* ── Form ── */

.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.field-group label {
  font-size: 0.65rem;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: 0.08em;
  padding-left: 2px;
  text-transform: uppercase;
}

.field-wrap {
  position: relative;
  display: flex;
  align-items: center;
  border-radius: 8px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  transition: border-color 0.3s, background 0.3s, box-shadow 0.3s;
  overflow: hidden;
}

.field-wrap:focus-within {
  border-color: var(--accent);
  background: var(--bg-tertiary);
  box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.06);
}

.field-wrap.field-error {
  border-color: var(--emergency);
  background: var(--emergency-soft);
}

.field-wrap.field-error:focus-within {
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.08);
}

.field-wrap input {
  width: 100%;
  padding: 12px 44px 12px 14px;
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-size: 0.9rem;
  font-family: inherit;
  outline: none;
}

.field-wrap input::placeholder {
  color: var(--text-dim);
}

.field-glow {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent), var(--accent-hover), var(--accent), transparent);
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.field-wrap:focus-within .field-glow {
  width: 100%;
}

.field-wrap.field-error .field-glow {
  background: linear-gradient(90deg, transparent, var(--emergency), transparent);
  width: 100%;
}

.field-check {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  animation: checkPop 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes checkPop {
  0% { transform: translateY(-50%) scale(0); }
  100% { transform: translateY(-50%) scale(1); }
}

.field-msg {
  font-size: 0.7rem;
  padding-left: 4px;
  font-weight: 500;
  min-height: 1em;
}

.field-msg.error-msg {
  color: var(--emergency);
  animation: fadeIn 0.2s ease;
}

/* ── Eye Toggle ── */

.btn-eye {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: color 0.2s, background 0.2s;
}

.btn-eye:hover {
  color: var(--text-secondary);
  background: var(--bg-tertiary);
}

/* ── Form Options ── */

.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.check-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
  color: var(--text-muted);
  cursor: pointer;
  user-select: none;
  transition: color 0.2s;
}

.check-label:hover {
  color: var(--text-secondary);
}

.check-input {
  display: none;
}

.check-box {
  width: 17px;
  height: 17px;
  border-radius: 4px;
  border: 2px solid var(--border);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.check-box svg {
  opacity: 0;
  transition: opacity 0.15s ease;
  color: white;
}

.check-input:checked + .check-box {
  background: var(--accent);
  border-color: var(--accent);
}

.check-input:checked + .check-box svg {
  opacity: 1;
}

.forgot-link {
  font-size: 0.8rem;
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.forgot-link:hover {
  opacity: 1;
}

/* ── Form Error ── */

.form-error {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--emergency);
  background: var(--emergency-soft);
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid var(--emergency-soft);
  animation: formShake 0.35s ease;
}

@keyframes formShake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-4px); }
  40% { transform: translateX(4px); }
  60% { transform: translateX(-3px); }
  80% { transform: translateX(2px); }
}

/* ── Submit Button ── */

.btn-submit {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 13px;
  border-radius: 8px;
  background: var(--accent-gradient);
  color: white;
  font-weight: 700;
  font-size: 0.88rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  min-height: 48px;
  font-family: inherit;
  letter-spacing: 0.01em;
}

.btn-submit::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(135deg, var(--accent-hover), var(--accent) 50%, var(--accent-hover) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.btn-submit::after {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: inherit;
  background: var(--accent-gradient);
  opacity: 0;
  transition: opacity 0.4s ease;
  z-index: -1;
  filter: blur(12px);
}

.btn-submit:hover:not(:disabled)::before {
  opacity: 1;
}

.btn-submit:hover:not(:disabled)::after {
  opacity: 0.35;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
}

.btn-submit:active:not(:disabled) {
  transform: translateY(0) scale(0.99);
  transition-duration: 0.1s;
}

.btn-submit:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-content,
.btn-loading {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-content {
  transition: opacity 0.2s ease;
}

.btn-loading {
  position: absolute;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.btn-hidden {
  opacity: 0;
}

.btn-visible {
  opacity: 1;
}

/* ── Card Footer ── */

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 24px;
  border-top: 1px solid var(--border-light);
  background: var(--bg-secondary);
}

.card-footer p {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.card-footer a {
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
  transition: opacity 0.2s;
}

.card-footer a:hover {
  opacity: 0.8;
}

.secure-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.65rem;
  color: var(--text-dim);
  font-weight: 600;
}

.secure-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #10B981;
  box-shadow: 0 0 6px rgba(16, 185, 129, 0.3);
  animation: dotPulse 2.5s ease-in-out infinite;
}

/* ══════════════ STATUS BAR ══════════════ */

.status-bar {
  width: 100%;
  max-width: 1200px;
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 10px 0 0;
  border-top: 1px solid var(--border-light);
  font-size: 0.68rem;
  color: var(--text-dim);
  font-weight: 500;
  animation: fadeIn 0.8s ease-out 0.3s both;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-right {
  margin-left: auto;
  gap: 8px;
}

.status-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-green {
  background: var(--status-active);
  box-shadow: 0 0 5px rgba(16, 185, 129, 0.3);
  animation: dotPulse 3s ease-in-out infinite;
}

.status-yellow {
  background: var(--risk-medium);
  box-shadow: 0 0 5px rgba(217, 119, 6, 0.3);
  animation: dotPulse 2s ease-in-out infinite;
}

.status-red {
  background: var(--emergency);
  box-shadow: 0 0 5px rgba(220, 38, 38, 0.3);
  animation: dotPulse 1.5s ease-in-out infinite;
}

.status-sep {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: var(--text-dim);
}

/* ══════════════ TRANSITIONS ══════════════ */

.fade-enter-active {
  animation: fadeIn 0.2s ease-out;
}

.fade-leave-active {
  animation: fadeOut 0.15s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

/* ══════════════ REDUCED MOTION ══════════════ */

@media (prefers-reduced-motion: reduce) {
  .ambient-topo,
  .ambient-panel,
  .status-bar,
  .particle,
  .orb,
  .login-card,
  .wave-path {
    animation: none !important;
  }
  .particle { display: none; }
  .orb { display: none; }
  .card-accent { animation: none; }
  .field-glow { display: none; }
  .form-error { animation: none; }
  .btn-submit::after { display: none; }
  .waves { display: none; }
  .fade-enter-active,
  .fade-leave-active {
    animation: none !important;
  }
}

/* ══════════════ RESPONSIVE ══════════════ */

@media (max-width: 1024px) {
  .ambient-panel {
    display: none;
  }
  .content-inner {
    justify-content: center;
  }
  .login-card {
    width: 100%;
    max-width: 440px;
  }
  .waves {
    height: 80px;
  }
}

@media (max-width: 480px) {
  .content {
    padding: 12px 16px;
  }
  .card-header {
    padding: 14px 16px;
  }
  .card-body {
    padding: 18px 16px;
    gap: 16px;
  }
  .card-footer {
    padding: 12px 16px;
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }
  .card-title h1 {
    font-size: 1.15rem;
  }
  .mode-tabs button {
    font-size: 0.72rem;
    padding: 8px 10px;
  }
  .form-options {
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }
  .status-bar {
    flex-wrap: wrap;
    gap: 10px;
    font-size: 0.62rem;
  }
  .status-right {
    margin-left: 0;
  }
  .waves {
    height: 60px;
  }
}
</style>

<!-- Global overrides for theme support (data-theme is on <html>, outside component scope) -->
<style>
[data-theme='light'] .ambient-gradient,
[data-theme='light'] .ambient-orbs,
[data-theme='light'] .ambient-particles,
[data-theme='light'] .waves {
  display: none !important;
}

[data-theme='light'] .login-page {
  background: var(--bg-primary);
}
</style>
