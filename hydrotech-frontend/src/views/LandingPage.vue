<template>
  <div class="landing">

    <!-- ═══ HERO ═══ -->
    <section class="hero">
      <div class="hero-inner">
        <span class="hero-badge">MONITORAMENTO EM TEMPO REAL &amp; ANÁLISES</span>
        <h1 class="hero-title">HydroTech: Proteção e<br>Resiliência em sua cidade</h1>
        <p class="hero-subtitle">
          Monitoramento contínuo em tempo real e sistema avançado de
          alertas para a segurança e bem-estar, a segurança da população e a
          preservação da infraestrutura urbana contra riscos hidrológicos.
        </p>
        <div class="hero-actions">
          <router-link to="/monitoramento" class="btn-hero-primary">
            ACESSAR MONITORAMENTO PÚBLICO
          </router-link>
          <a href="#servicos" class="btn-hero-secondary">SAIBA MAIS</a>
        </div>
      </div>
    </section>

    <!-- ═══ SERVIÇOS INSTITUCIONAIS ═══ -->
    <section id="servicos" class="services-section">
      <div class="services-inner">
        <div class="services-header">
          <h2>Serviços Institucionais</h2>
          <p>Acesse rapidamente os canais de atendimento, infraestrutura de segurança e documentação oficial para gestores e cidadãos.</p>
        </div>
        <div class="services-grid">
          <div class="service-card" v-for="(s, i) in services" :key="i">
            <div class="service-icon" v-html="s.icon"></div>
            <h3>{{ s.title }}</h3>
            <p>{{ s.desc }}</p>
            <a v-if="s.linkText" :href="s.link || '#'" class="service-link">{{ s.linkText }} <span class="arrow">→</span></a>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ FEATURES (BENTO GRID) ═══ -->
    <section class="features-section" @mousemove="handleMouseMove" :style="{ '--mouse-x': mouseX + 'px', '--mouse-y': mouseY + 'px' }">
      <div class="features-inner">
        <div class="features-header">
          <h2>Como o sistema protege sua região?</h2>
          <p>Tecnologia de ponta integrada a protocolos práticos para o sistema de hidrológicas</p>
        </div>
        <div class="bento-grid">
          <div class="bento-card bento-sm" v-for="(f, i) in features.slice(0,2)" :key="'a'+i">
            <div class="bento-icon" v-html="f.icon"></div>
            <h3>{{ f.title }}</h3>
            <p>{{ f.desc }}</p>
          </div>
          <div class="bento-card bento-sm">
            <div class="bento-icon" v-html="features[2].icon"></div>
            <h3>{{ features[2].title }}</h3>
            <p>{{ features[2].desc }}</p>
          </div>
          <div class="bento-card bento-lg">
            <div class="bento-icon" v-html="features[3].icon"></div>
            <h3>{{ features[3].title }}</h3>
            <p>{{ features[3].desc }}</p>
          </div>
          <div class="bento-card bento-full">
            <div class="bento-icon" v-html="features[4].icon"></div>
            <h3>{{ features[4].title }}</h3>
            <p>{{ features[4].desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ AUDIENCE ═══ -->
    <section id="contingencia" class="audience-section">
      <div class="audience-inner">
        <div class="audience-header">
          <h2>Quem pode usar o HydroTech?</h2>
        </div>
        <div class="audience-grid">
          <div class="audience-card" v-for="(a, i) in audiences" :key="i">
            <div class="audience-icon" v-html="a.icon"></div>
            <h3>{{ a.title }}</h3>
            <ul>
              <li v-for="(item, j) in a.items" :key="j">
                <svg class="check" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                {{ item }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ CTA ═══ -->
    <section class="cta-section">
      <div class="cta-inner">
        <h2>Pronto para proteger sua região?</h2>
        <p>Implemente o HydroTech em seu município e garanta uma gestão de recursos hídricos moderna e eficiente para a comunidade.</p>
        <router-link :to="isLoggedIn ? '/minha-conta' : '/registro'" class="btn-cta">{{ isLoggedIn ? 'Minha Conta' : 'Começar Agora' }}</router-link>
      </div>
    </section>

  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

const isLoggedIn = ref(!!localStorage.getItem('user_token'))
const observer = ref(null)

onMounted(() => {
  observer.value = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('bento-in-view')
      } else {
        entry.target.classList.remove('bento-in-view')
      }
    })
  }, { threshold: 0.15 })

  document.querySelectorAll('.bento-card, .audience-card, .cta-inner').forEach(el => {
    observer.value.observe(el)
  })
})

onUnmounted(() => {
  if (observer.value) {
    observer.value.disconnect()
  }
})

const mouseX = ref(0)
const mouseY = ref(0)

const handleMouseMove = (e) => {
  mouseX.value = (e.clientX - window.innerWidth / 2) * -0.05
  mouseY.value = (e.clientY - window.innerHeight / 2) * -0.05
}

const services = ref([
  {
    title: 'Atendimento e Consulta',
    desc: 'Solicite vistorias, consulte processos e tire dúvidas sobre áreas de risco.',
    link: '#',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
  },
  {
    title: 'Abrigos',
    desc: 'Localização em tempo real e capacidade dos abrigos públicos disponíveis.',
    link: '#',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
  },
  {
    title: 'Histórico',
    desc: 'Repositório de dados históricos de ocorrências e níveis dos rios.',
    link: '#',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
  },
  {
    title: 'Plano de Contingência',
    desc: 'Documentação técnica e protocolos de ação para cenários de risco.',
    link: '#',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'
  }
])

const features = ref([
  {
    title: 'Sensores',
    desc: 'Rede de sensores alimentados a painéis solares, monitorando o nível do rio em tempo real via batimetria.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6 8-2-2"/><path d="m18 8 2-2"/><path d="m6 16-2 2"/><path d="m18 16 2 2"/><path d="M12 2v2"/><path d="M12 20v2"/><circle cx="12" cy="12" r="4"/></svg>'
  },
  {
    title: 'Dados Meteorológicos',
    desc: 'Integração direta com sistemas meteorológicos e satélites para previsão de precipitação e clima em tempo real.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>'
  },
  {
    title: 'Análise de Risco',
    desc: 'IA e ML de alta precisão, combinando variáveis e modelos para detecção e probabilidade de transbordamentos.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>'
  },
  {
    title: 'Dashboard Interativo',
    desc: 'Interface rica para gerenciamento e acompanhamento completo das monitorações e da região em tempo real.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>'
  },
  {
    title: 'Alertas no Painel',
    desc: 'Sistema automático de lançamento para alertas oficiais ao público em caso de alertas e emergências.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
  }
])

const audiences = ref([
  {
    title: 'Gestores Públicos',
    icon: '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    items: [
      'Somando ao controle máximo com métricas poderosas',
      'Gestão de equipes de fiscalização e defesa civil',
      'Relatórios automatizados para tomada de decisões',
      'Configuração de gatilhos oficiais SMS e e-mail'
    ]
  },
  {
    title: 'Cidadãos',
    icon: '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    items: [
      'Mapa público de monitoramento dos rios',
      'Cadastro prático e informativo de alertas locais',
      'Com interface simplificada para acesso rápido',
      'Contatos de serviços sociais e emergências'
    ]
  }
])
</script>

<style scoped>
/* ═══ LANDING BASE ═══ */
.landing {
  width: 100%;
  display: flex;
  flex-direction: column;
  font-family: 'Inter', sans-serif;
}

/* ═══ HERO ═══ */
.hero {
  background: var(--bg-primary);
  padding: 100px 24px 80px;
  position: relative;
  overflow: hidden;
}
.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: url('/hero_bg.png') no-repeat center center;
  background-size: cover;
  opacity: 0.7;
  mix-blend-mode: overlay;
  pointer-events: none;
}
[data-theme='light'] .hero::after {
  opacity: 0.15;
}


.hero-inner {
  max-width: 720px;
  position: relative;
  z-index: 1;
  margin-left: 8%;
}

.hero-badge {
  display: inline-block;
  background: rgba(59,130,246,0.15);
  color: var(--accent);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  padding: 6px 16px;
  border-radius: 4px;
  margin-bottom: 28px;
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.1s forwards;
}

.hero-title {
  font-size: 3.2rem;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.12;
  letter-spacing: -0.03em;
  margin-bottom: 20px;
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.2s forwards;
}

.hero-subtitle {
  font-size: 1rem;
  color: var(--text-secondary);
  line-height: 1.7;
  max-width: 540px;
  margin-bottom: 0;
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.3s forwards;
}

.hero-actions {
  margin-top: 32px;
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.4s forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.btn-hero-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  background: var(--accent);
  color: #fff;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  border-radius: 6px;
  text-decoration: none;
  transition: background 0.2s;
}
.btn-hero-primary:hover { background: var(--accent-hover); }

.btn-hero-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  background: transparent;
  color: var(--text-secondary);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  border-radius: 6px;
  border: 1px solid var(--border);
  text-decoration: none;
  transition: border-color 0.2s, color 0.2s;
}
.btn-hero-secondary:hover { border-color: var(--accent); color: var(--text-primary); }

/* ═══ SERVICES ═══ */
.services-section {
  background: var(--bg-secondary);
  padding: 80px 24px;
}

.services-inner {
  max-width: 1100px;
  margin: 0 auto;
}

.services-header {
  margin-bottom: 48px;
}
.services-header h2 {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: 10px;
}
.services-header p {
  font-size: 0.95rem;
  color: var(--text-secondary);
  max-width: 620px;
  line-height: 1.6;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.service-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 28px 24px;
  transition: transform 0.2s, box-shadow 0.2s;
}
.service-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.service-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 10px;
  background: var(--accent-soft);
  color: var(--accent);
  margin-bottom: 18px;
}

.service-card h3 {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.service-card p {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 18px;
}

.service-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--accent);
  text-decoration: none;
  letter-spacing: 0.05em;
  transition: gap 0.2s;
}
.service-link:hover { gap: 10px; }
.service-link .arrow { transition: transform 0.2s; }

/* ═══ FEATURES (BENTO) ═══ */
.features-section {
  background: var(--bg-primary);
  padding: 80px 24px;
  position: relative;
  overflow: hidden;
}
.features-section::after {
  content: '';
  position: absolute;
  width: 110%;
  height: 110%;
  top: -5%;
  left: -5%;
  background: url('/features_bg.png') no-repeat center center;
  background-size: cover;
  opacity: 0.3;
  mix-blend-mode: overlay;
  pointer-events: none;
  z-index: 0;
  transform: translate(var(--mouse-x, 0), var(--mouse-y, 0));
  transition: transform 0.15s ease-out;
  will-change: transform;
}
[data-theme='light'] .features-section::after {
  opacity: 0.1;
}
.features-inner {
  position: relative;
  z-index: 1;
  max-width: 1100px;
  margin: 0 auto;
}

.features-header {
  text-align: center;
  margin-bottom: 48px;
}
.features-header h2 {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: 10px;
}
.features-header p {
  font-size: 0.95rem;
  color: var(--text-muted);
  max-width: 500px;
  margin: 0 auto;
  line-height: 1.6;
}

.bento-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.bento-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 32px 28px;
  opacity: 0;
  transform: translateY(40px) scale(0.95);
  transition: border-color 0.2s, transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.bento-card.bento-in-view {
  opacity: 1;
  transform: translateY(0) scale(1);
}
.bento-card:hover { border-color: rgba(59,130,246,0.3); }

.bento-sm { /* default 1 col */ }

.bento-lg {
  /* takes 1 col but visually bigger */
}

.bento-full {
  grid-column: 1 / -1;
}

.bento-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 10px;
  background: var(--accent-soft);
  color: var(--accent);
  margin-bottom: 18px;
}

.bento-card h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.bento-card p {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

/* ═══ AUDIENCE ═══ */
.audience-section {
  background: var(--bg-secondary);
  padding: 80px 24px;
}

.audience-inner {
  max-width: 900px;
  margin: 0 auto;
}

.audience-header {
  text-align: center;
  margin-bottom: 48px;
}
.audience-header h2 {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.audience-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
}

.audience-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 32px 28px;
  opacity: 0;
  transform: translateY(40px) scale(0.95);
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.audience-card.bento-in-view {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.audience-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 52px;
  height: 52px;
  border-radius: 12px;
  background: var(--accent-soft);
  color: var(--accent);
  margin-bottom: 18px;
}

.audience-card h3 {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.audience-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.audience-card li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

.audience-card li .check {
  color: var(--accent);
  flex-shrink: 0;
  margin-top: 1px;
}

/* ═══ CTA ═══ */
.cta-section {
  background: var(--bg-primary);
  padding: 80px 24px;
}

.cta-inner {
  max-width: 680px;
  margin: 0 auto;
  text-align: center;
  opacity: 0;
  transform: translateY(40px) scale(0.95);
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.cta-inner.bento-in-view {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.cta-inner h2 {
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: 14px;
}

.cta-inner p {
  font-size: 1rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 32px;
}

.btn-cta {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 40px;
  border-radius: 8px;
  background: var(--emergency);
  color: #fff;
  text-decoration: none;
  font-weight: 700;
  font-size: 1rem;
  letter-spacing: 0.02em;
  transition: background 0.2s, transform 0.15s;
}
.btn-cta:hover { background: var(--emergency-hover); transform: translateY(-2px); }

/* ═══ RESPONSIVE ═══ */
@media (max-width: 1024px) {
  .services-grid { grid-template-columns: repeat(2, 1fr); }
  .hero-inner { margin-left: 5%; }
}

@media (max-width: 768px) {
  .hero { padding: 80px 20px 60px; }
  .hero-inner { margin-left: 0; }
  .hero-title { font-size: 2.2rem; }
  .hero-actions { flex-direction: column; }
  .services-grid { grid-template-columns: 1fr; }
  .bento-grid { grid-template-columns: 1fr; }
  .audience-grid { grid-template-columns: 1fr; }
  .cta-inner h2 { font-size: 1.6rem; }
}
</style>