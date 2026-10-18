<template>
  <div class="register-page">
    <div class="register-ambient" aria-hidden="true"></div>
    <div class="register-wrapper">
      <section class="register-intro" aria-label="Sobre o HydroTech">
        <span class="intro-status"><span class="intro-dot"></span> HYDROTECH · DEMONSTRAÇÃO ACADÊMICA</span>
        <h2>Seu acesso ao monitoramento começa aqui.</h2>
        <p>Acompanhe os rios cadastrados, organize seus pontos favoritos e explore os alertas simulados em um só lugar.</p>
        <div class="intro-features">
          <div><span class="feature-icon" aria-hidden="true">↗</span><span><strong>Monitore os pontos</strong><small>Consulte os gráficos e as informações cadastradas.</small></span></div>
          <div><span class="feature-icon" aria-hidden="true">☆</span><span><strong>Personalize seu acesso</strong><small>Salve favoritos e acompanhe os alertas simulados.</small></span></div>
        </div>
      </section>
      <div class="register-card">
        <div class="register-brand-row">
          <div class="register-brand">
            <span class="register-brand-icon" aria-hidden="true">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z" fill="rgba(255,255,255,0.08)"/><path d="M12 6v12"/><path d="M6 12h12"/></svg>
            </span>
            <span class="register-brand-text"><strong>HydroTech</strong><small>MONITORAMENTO HIDROLÓGICO</small></span>
          </div>
          <span class="register-badge">CADASTRO</span>
        </div>

        <div class="register-header">
          <span class="register-eyebrow">NOVO ACESSO</span>
          <h1>Criar sua conta</h1>
          <p>Informe e-mail ou telefone e crie sua senha para acompanhar o monitoramento.</p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleRegistro" class="register-form">

          <!-- Nome Completo -->
          <div class="form-group">
            <label for="reg-nome">Nome Completo</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              <input id="reg-nome" v-model="form.nome" type="text" placeholder="Seu nome completo" autocomplete="name" />
            </div>
          </div>

          <!-- E-mail -->
          <div class="form-group">
            <label for="reg-email">E-mail</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
              <input id="reg-email" v-model="form.email" type="email" placeholder="seu@email.com" autocomplete="email" />
            </div>
          </div>

          <!-- Telefone + Data Nascimento -->
          <div class="form-row">
            <div class="form-group">
              <label for="reg-telefone">Telefone</label>
              <div class="input-wrapper">
                <svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                <input id="reg-telefone" :value="form.telefone" @input="onPhoneInput" type="tel" inputmode="numeric" placeholder="(00) 00000-0000" autocomplete="tel" />
              </div>
            </div>
            <div class="form-group">
              <label for="reg-nascimento">Data de Nascimento</label>
              <div class="input-wrapper">
                <svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                <input id="reg-nascimento" :value="form.data_nascimento_display" @input="onDateInput" type="text" inputmode="numeric" placeholder="dd/mm/aaaa" maxlength="10" />
              </div>
            </div>
          </div>

          <!-- Senha + Confirmar -->
          <div class="form-row">
            <div class="form-group">
              <label for="reg-senha">Senha</label>
              <div class="input-wrapper">
                <svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                <input id="reg-senha" v-model="form.senha" :type="showSenha ? 'text' : 'password'" placeholder="Crie uma senha" autocomplete="new-password" />
                <button type="button" class="btn-toggle-pw" @click="showSenha = !showSenha" :aria-label="showSenha ? 'Ocultar senha' : 'Mostrar senha'">
                  <svg v-if="!showSenha" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                </button>
              </div>
            </div>
            <div class="form-group">
              <label for="reg-confirmar">Confirmar Senha</label>
              <div class="input-wrapper">
                <svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                <input id="reg-confirmar" v-model="form.confirmarSenha" :type="showConfirmar ? 'text' : 'password'" placeholder="Repita a senha" autocomplete="new-password" />
                <button type="button" class="btn-toggle-pw" @click="showConfirmar = !showConfirmar" :aria-label="showConfirmar ? 'Ocultar confirmação da senha' : 'Mostrar confirmação da senha'">
                  <svg v-if="!showConfirmar" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Password strength -->
          <div class="pw-strength" v-if="form.senha">
            <div class="pw-bar">
              <div class="pw-fill" :class="pwStrengthClass" :style="{ width: pwStrengthPercent + '%' }"></div>
            </div>
            <span class="pw-label-text" :class="pwStrengthClass">{{ pwStrengthLabel }}</span>
          </div>

          <!-- Password requirements -->
          <ul class="pw-requirements" v-if="form.senha">
            <li :class="{ met: form.senha.length >= 8 }">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline v-if="form.senha.length >= 8" points="20 6 9 17 4 12"/><line v-else x1="18" y1="6" x2="6" y2="18"/><line v-if="!(form.senha.length >= 8)" x1="6" y1="6" x2="18" y2="18"/></svg>
              Mínimo 8 caracteres
            </li>
            <li :class="{ met: /[A-Z]/.test(form.senha) }">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline v-if="/[A-Z]/.test(form.senha)" points="20 6 9 17 4 12"/><line v-else x1="18" y1="6" x2="6" y2="18"/><line v-if="!/[A-Z]/.test(form.senha)" x1="6" y1="6" x2="18" y2="18"/></svg>
              1 letra maiúscula
            </li>
            <li :class="{ met: /[a-z]/.test(form.senha) }">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline v-if="/[a-z]/.test(form.senha)" points="20 6 9 17 4 12"/><line v-else x1="18" y1="6" x2="6" y2="18"/><line v-if="!/[a-z]/.test(form.senha)" x1="6" y1="6" x2="18" y2="18"/></svg>
              1 letra minúscula
            </li>
            <li :class="{ met: /[0-9]/.test(form.senha) }">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline v-if="/[0-9]/.test(form.senha)" points="20 6 9 17 4 12"/><line v-else x1="18" y1="6" x2="6" y2="18"/><line v-if="!/[0-9]/.test(form.senha)" x1="6" y1="6" x2="18" y2="18"/></svg>
              1 número
            </li>
          </ul>

          <!-- Messages -->
          <p class="error-msg" v-if="error" role="alert">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
            {{ error }}
          </p>

          <p class="success-msg" v-if="success" role="status">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            {{ success }}
          </p>

          <button class="btn-register" type="submit" :disabled="loading">
            <svg v-if="loading" class="spinner" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32"><animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="0.8s" repeatCount="indefinite"/></circle></svg>
            <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" y1="8" x2="19" y2="14"/><line x1="22" y1="11" x2="16" y2="11"/></svg>
            {{ loading ? 'Processando...' : 'Criar Conta' }}
          </button>
        </form>

        <div class="register-footer">
          <p>Já tem uma conta? <router-link to="/login">Entrar</router-link></p>
          <span class="register-footer-note"><span></span> Acesso ao monitoramento</span>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

import api from '../services/api'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const success = ref('')
const showSenha = ref(false)
const showConfirmar = ref(false)

const form = ref({
  nome: '',
  email: '',
  telefone: '',
  data_nascimento: '',
  data_nascimento_display: '',
  senha: '',
  confirmarSenha: ''
})

const onDateInput = (e) => {
  let digits = e.target.value.replace(/\D/g, '').slice(0, 8)
  let formatted = ''
  if (digits.length > 0) formatted += digits.slice(0, 2)
  if (digits.length > 2) formatted += '/' + digits.slice(2, 4)
  if (digits.length > 4) formatted += '/' + digits.slice(4, 8)
  form.value.data_nascimento_display = formatted
  e.target.value = formatted
  // Convert dd/mm/yyyy to yyyy-mm-dd for API
  if (digits.length === 8) {
    const dd = digits.slice(0, 2)
    const mm = digits.slice(2, 4)
    const yyyy = digits.slice(4, 8)
    form.value.data_nascimento = `${yyyy}-${mm}-${dd}`
  } else {
    form.value.data_nascimento = ''
  }
}

const onPhoneInput = (e) => {
  let digits = e.target.value.replace(/\D/g, '').slice(0, 11)
  let formatted = ''
  if (digits.length > 0) formatted += '(' + digits.slice(0, 2)
  if (digits.length >= 2) formatted += ') '
  if (digits.length > 2) formatted += digits.slice(2, 7)
  if (digits.length > 7) formatted += '-' + digits.slice(7, 11)
  form.value.telefone = formatted
  e.target.value = formatted
}

const pwStrength = computed(() => {
  const s = form.value.senha
  if (!s) return 0
  let score = 0
  if (s.length >= 6) score++
  if (s.length >= 10) score++
  if (/[A-Z]/.test(s)) score++
  if (/[0-9]/.test(s)) score++
  if (/[^A-Za-z0-9]/.test(s)) score++
  return score
})

const pwStrengthPercent = computed(() => (pwStrength.value / 5) * 100)

const pwStrengthClass = computed(() => {
  if (pwStrength.value <= 1) return 'pw-weak'
  if (pwStrength.value <= 3) return 'pw-medium'
  return 'pw-strong'
})

const pwStrengthLabel = computed(() => {
  if (pwStrength.value <= 1) return 'Fraca'
  if (pwStrength.value <= 3) return 'Média'
  return 'Forte'
})

const handleRegistro = async () => {
  error.value = ''
  success.value = ''

  if (!form.value.nome || (!form.value.email && !form.value.telefone) || !form.value.data_nascimento || !form.value.senha) {
    error.value = 'Preencha nome, e-mail ou telefone, data de nascimento e senha.'
    return
  }

  if (form.value.senha !== form.value.confirmarSenha) {
    error.value = 'As senhas não conferem.'
    return
  }

  loading.value = true

  try {
    const data = {
      nome: form.value.nome,
      senha: form.value.senha,
      data_nascimento: form.value.data_nascimento,
    }
    if (form.value.email) data.email = form.value.email
    if (form.value.telefone) data.telefone = form.value.telefone
    const response = await api.register(data)
    const { access, refresh, usuario } = response.data

    localStorage.setItem('user_token', access)
    localStorage.setItem('refresh_token', refresh)
    localStorage.setItem('user_name', usuario.nome)
    localStorage.setItem('user_data', JSON.stringify(usuario))
    if (usuario.favoritos) localStorage.setItem('ht_favs', JSON.stringify(usuario.favoritos))
    if (usuario.alertas) localStorage.setItem('ht_alerts', JSON.stringify(usuario.alertas))
    localStorage.setItem('ht_show_onboarding', 'true')
    window.dispatchEvent(new Event('storage-update'))
    success.value = 'Conta criada com sucesso! Redirecionando...'

    setTimeout(() => {
      router.push('/')
    }, 1500)
  } catch (err) {
    if (err.response && err.response.data) {
      const msgs = []
      for (const key in err.response.data) {
        msgs.push(`${key}: ${err.response.data[key]}`)
      }
      error.value = msgs.join(' | ')
    } else {
      error.value = 'Erro ao criar conta. Tente novamente.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: calc(100vh - 58px);
  background: var(--bg-primary);
  position: relative;
  overflow: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.register-ambient {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(ellipse at 16% 42%, rgba(6, 182, 212, .08), transparent 42%),
    radial-gradient(ellipse at 82% 18%, rgba(59, 130, 246, .06), transparent 38%),
    linear-gradient(180deg, var(--bg-primary), var(--bg-secondary));
}

.register-ambient::after {
  content: '';
  position: absolute;
  inset: 0;
  opacity: .35;
  background-image: linear-gradient(rgba(59, 130, 246, .05) 1px, transparent 1px), linear-gradient(90deg, rgba(59, 130, 246, .05) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse at center, #000 20%, transparent 75%);
}

.register-wrapper {
  position: relative;
  z-index: 1;
  width: min(100%, 1200px);
  min-height: calc(100vh - 58px);
  margin: 0 auto;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 560px);
  align-items: center;
  gap: clamp(32px, 6vw, 88px);
  padding: 32px;
}

.register-intro { max-width: 440px; }
.intro-status { display: inline-flex; align-items: center; gap: 8px; color: var(--accent); font-size: .7rem; font-weight: 800; letter-spacing: .1em; }
.intro-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--status-active); box-shadow: 0 0 8px rgba(16,185,129,.35); }
.register-intro h2 { color: var(--text-primary); font-size: clamp(2rem, 3vw, 3rem); line-height: 1.12; letter-spacing: -.035em; margin: 22px 0 14px; }
.register-intro > p { color: var(--text-secondary); font-size: .96rem; line-height: 1.65; max-width: 390px; }
.intro-features { display: grid; gap: 10px; margin-top: 30px; }
.intro-features > div { display: flex; align-items: center; gap: 13px; padding: 15px; background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 11px; }
.feature-icon { flex: 0 0 34px; width: 34px; height: 34px; display: grid; place-items: center; color: var(--accent); background: var(--accent-soft); border-radius: 8px; font-size: 1.15rem; }
.intro-features strong, .intro-features small { display: block; }
.intro-features strong { color: var(--text-primary); font-size: .85rem; margin-bottom: 3px; }
.intro-features small { color: var(--text-muted); font-size: .76rem; line-height: 1.35; }

.register-card {
  position: relative;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 16px;
  width: 100%;
  max-width: 560px;
  overflow: hidden;
  box-shadow: var(--shadow-xl);
  animation: fadeInUp .45s ease-out;
}

.register-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: var(--accent-gradient); }
.register-brand-row { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 16px 28px; border-bottom: 1px solid var(--border-light); }
.register-brand { display: flex; align-items: center; gap: 11px; min-width: 0; }
.register-brand-icon { display: grid; place-items: center; width: 38px; height: 38px; flex: 0 0 38px; border-radius: 10px; color: #fff; background: var(--accent-gradient); }
.register-brand-text { display: flex; flex-direction: column; gap: 1px; min-width: 0; }
.register-brand-text strong { color: var(--text-primary); font-size: 1rem; line-height: 1.2; }
.register-brand-text small { color: var(--accent); font-size: .58rem; font-weight: 700; letter-spacing: .13em; }
.register-badge { color: var(--text-muted); background: var(--bg-secondary); border: 1px solid var(--border-light); border-radius: 99px; padding: 4px 10px; font-size: .62rem; font-weight: 700; letter-spacing: .06em; }

.register-header {
  padding: 20px 28px 0;
}

.register-eyebrow { color: var(--accent); opacity: .8; font-size: .62rem; font-weight: 800; letter-spacing: .16em; }

.register-header h1 {
  font-size: 1.45rem;
  font-weight: 750;
  color: var(--text-primary);
  margin: 4px 0 5px;
}

.register-header p {
  color: var(--text-secondary);
  font-size: .83rem;
  line-height: 1.45;
  margin: 0;
}

/* Form Styles */
.register-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 20px 28px 24px;
}

.form-row {
  display: flex;
  gap: 14px;
}

.form-row .form-group {
  flex: 1;
  min-width: 0;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-group label {
  font-size: .66rem;
  font-weight: 700;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: .08em;
  margin-left: 2px;
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
  min-height: 44px;
  padding: 11px 44px 11px 42px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: .9rem;
  font-family: inherit;
  transition: border-color .2s ease, background .2s ease, box-shadow .2s ease;
}

.input-wrapper input:focus {
  outline: none;
  border-color: var(--accent);
  background: var(--bg-tertiary);
  box-shadow: 0 0 0 3px rgba(6, 182, 212, .08);
}

.input-wrapper input::placeholder {
  color: var(--text-secondary);
  opacity: .72;
}

/* Password Toggle Button */
.btn-toggle-pw {
  position: absolute;
  right: 5px;
  top: 0;
  bottom: 0;
  margin-block: auto;
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: color 0.2s;
}
.btn-toggle-pw:hover {
  color: var(--text-primary);
}
.btn-toggle-pw:hover:not(:disabled),
.btn-toggle-pw:active:not(:disabled) { transform: none; }
.btn-toggle-pw:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }

/* Password Strength */
.pw-strength {
  display: flex;
  align-items: center;
  gap: 10px;
}

.pw-bar {
  flex: 1;
  height: 4px;
  background: var(--border);
  border-radius: 2px;
  overflow: hidden;
}

.pw-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s ease, background-color 0.3s ease;
}

.pw-fill.pw-weak { background-color: var(--risk-high); }
.pw-fill.pw-medium { background-color: var(--risk-medium); }
.pw-fill.pw-strong { background-color: var(--risk-low); }

.pw-label-text {
  font-size: 0.72rem;
  font-weight: 700;
  white-space: nowrap;
}

.pw-label-text.pw-weak { color: var(--risk-high); }
.pw-label-text.pw-medium { color: var(--risk-medium); }
.pw-label-text.pw-strong { color: var(--risk-low); }

/* Password Requirements */
.pw-requirements {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.pw-requirements li {
  font-size: 0.75rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 6px;
  transition: color 0.2s ease;
}

.pw-requirements li svg {
  color: var(--text-muted);
  opacity: 0.6;
  flex-shrink: 0;
}

.pw-requirements li.met {
  color: var(--risk-low);
}

.pw-requirements li.met svg {
  color: var(--risk-low);
  opacity: 1;
}

/* Button */
.btn-register {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px;
  background: var(--accent-gradient);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
  margin-top: 4px;
}
.btn-register:focus-visible { outline: 3px solid var(--accent); outline-offset: 3px; }

.btn-register:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(14, 165, 233, 0.35);
  filter: brightness(1.1);
}

.btn-register:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Messages */
.error-msg, .success-msg {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  font-weight: 600;
  animation: fadeIn 0.3s ease;
}

.error-msg {
  background: rgba(239, 68, 68, 0.08);
  color: var(--risk-high);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.success-msg {
  background: rgba(16, 185, 129, 0.08);
  color: var(--risk-low);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

/* Footer */
.register-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 15px 28px;
  border-top: 1px solid var(--border-light);
}

.register-footer p {
  font-size: .82rem;
  color: var(--text-muted);
  margin: 0;
}

.register-footer a {
  color: var(--accent);
  font-weight: 700;
  text-decoration: none;
  margin-left: 4px;
}

.register-footer a:hover {
  text-decoration: underline;
}
.register-footer a:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; border-radius: 2px; }
.register-footer-note { display: inline-flex; align-items: center; gap: 6px; color: var(--text-secondary); font-size: .68rem; white-space: nowrap; }
.register-footer-note span { width: 6px; height: 6px; border-radius: 50%; background: var(--status-active); }

/* Animations */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 1024px) {
  .register-intro { display: none; }
  .register-wrapper { display: flex; justify-content: center; padding: 30px 20px; }
}

@media (max-width: 600px) {
  .register-wrapper { padding: 18px 12px; }
  .register-brand-row { padding: 14px 18px; }
  .register-header { padding: 18px 18px 0; }
  .register-form { padding: 18px; gap: 13px; }
  .register-footer { padding: 15px 18px; flex-wrap: wrap; }
  .form-row { flex-direction: column; gap: 13px; }
  .pw-requirements { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 380px) {
  .register-badge, .register-footer-note { display: none; }
  .pw-requirements { grid-template-columns: 1fr; }
}

@media (prefers-reduced-motion: reduce) {
  .register-card, .error-msg, .success-msg { animation: none; }
  .btn-register, .input-wrapper input { transition: none; }
}
</style>
