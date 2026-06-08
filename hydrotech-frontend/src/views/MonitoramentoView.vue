<template>
  <div class="mon-page">
    <!-- Static Gradient Background -->
    <div class="mesh-bg"></div>
    <header class="mon-topbar">
      <div class="mon-inner">
        <div class="mon-brand">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-linecap="round">
  <path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>
  <path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>
  <path d="M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>
</svg>
          <span>HydroTech <b>Monitoramento Público</b></span>
        </div>
        <div class="mon-meta">
          <span class="live-pill"><span class="live-dot"></span>AO VIVO · 10s</span>
          <span v-if="lastUpdate" class="upd-time">{{ lastUpdate }}</span>
          <router-link to="/" class="back-lnk">← Início</router-link>
        </div>
      </div>
    </header>

    <div class="mon-filter-bar">
      <div class="mon-inner row">
        <div class="frow">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
          <select v-model="filtroEstado" class="f-sel">
            <option value="">Todos os estados</option>
            <option v-for="e in estados" :key="e" :value="e">{{ e }}</option>
          </select>
          <button class="fav-filter-btn" :class="{ active: favFilter }" @click="favFilter = !favFilter">
            <svg width="13" height="13" viewBox="0 0 24 24" :fill="favFilter ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            Favoritos
          </button>
        </div>
        <div class="fstats">
          <span class="fs fs-t">{{ totalRios }} rios</span>
        </div>
      </div>
    </div>

    <!-- Loading Skeletons -->
    <div v-if="loading" class="charts-grid" style="padding: 24px;">
      <div v-for="i in 3" :key="'skel'+i" class="skeleton-card" style="margin-bottom: 24px;">
        <div class="skeleton-hdr">
          <div class="skeleton-title skeleton" style="height: 24px;"></div>
          <div class="skeleton-sub skeleton"></div>
        </div>
        <div class="skeleton-body skeleton"></div>
      </div>
    </div>

    <main v-else class="mon-main">
      <!-- Agrupado por Estado -->
      <div v-for="estado in estadosFiltrados" :key="estado" class="estado-section">
        <div class="estado-header">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          {{ estado }}
          <span class="estado-count">{{ riosPorEstado[estado].length }} rios</span>
        </div>

        <!-- Rios do Estado -->
        <div v-for="rio in riosPorEstado[estado]" :key="rio.id" class="rio-block">
          <div class="rio-hdr" :class="rc(rio.risco_inundacao)">
            <div class="rio-hdr-l">
              <div class="rio-icon" :class="rc(rio.risco_inundacao)">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/></svg>
              </div>
              <div>
                <div class="rio-nome-container">
                  <h2 class="rio-name">{{ rio.nome }}</h2>
                  <div 
                    class="gemini-hover-trigger"
                    @mouseenter="showGemini(rio.id)"
                    @mouseleave="hideGemini"
                  >
                    ✨ Conheça este rio
                    
                    <transition name="gemini-fade">
                      <div v-if="expandedGemini === rio.id" class="gemini-panel-wrapper" @click.stop>
                        <div v-if="loadingGemini" class="gemini-skeleton">
                          <div class="skeleton-header">
                            <div class="skeleton-pill"></div>
                            <div class="skeleton-pill"></div>
                            <div class="skeleton-pill"></div>
                          </div>
                          <div class="skeleton-body">
                            <div class="skeleton-line skeleton-line-title"></div>
                            <div class="skeleton-line"></div>
                            <div class="skeleton-line"></div>
                            <div class="skeleton-line skeleton-line-short"></div>
                          </div>
                        </div>

                        <div v-else-if="geminiData" class="gemini-card">
                          <div class="gemini-card-header">
                            <div class="gemini-brand">
                              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" class="gemini-icon">
                                <path d="M12 2a1 1 0 0 1 .993.883L13 3v2.858c3.21.364 5.778 2.932 6.142 6.142L19.284 13h2.858a1 1 0 0 1 .117 1.993L22 15h-2.858c-.364 3.21-2.932 5.778-6.142 6.142L13 21.284v2.858a1 1 0 0 1-1.993.117L11 24v-2.858c-3.21-.364-5.778-2.932-6.142-6.142L4.716 15H1.858a1 1 0 0 1-.117-1.993L2 13h2.858c.364-3.21 2.932-5.778 6.142-6.142L11 5.716V2.858A1 1 0 0 1 12 2z"/>
                              </svg>
                              <span>Ficha Técnica (Gemini AI)</span>
                            </div>
                            <div v-if="geminiData.using_fallback" class="fallback-tag">
                              💡 Simulação
                            </div>
                          </div>
                          
                          <div class="gemini-metrics">
                            <div class="metric-item">
                              <div class="metric-icon">📏</div>
                              <div class="metric-content">
                                <span class="metric-lbl">Comprimento</span>
                                <span class="metric-val">{{ geminiData.comprimento }}</span>
                              </div>
                            </div>
                            <div class="metric-item">
                              <div class="metric-icon">📍</div>
                              <div class="metric-content">
                                <span class="metric-lbl">Áreas de Maior Risco</span>
                                <span class="metric-val">{{ geminiData.areas_risco }}</span>
                              </div>
                            </div>
                            <div class="metric-item">
                              <div class="metric-icon">🌊</div>
                              <div class="metric-content">
                                <span class="metric-lbl">Foz</span>
                                <span class="metric-val">{{ geminiData.foz }}</span>
                              </div>
                            </div>
                          </div>

                          <div class="gemini-info">
                            <div class="gemini-desc">
                              <h3>Descrição e Histórico de Enchentes</h3>
                              <p>{{ geminiData.descricao_historico_enchentes }}</p>
                            </div>
                            <div class="gemini-curiosidade">
                              <h3>⚠️ Período Crítico</h3>
                              <p>{{ geminiData.periodo_critico }}</p>
                            </div>
                          </div>
                        </div>
                        
                        <div v-else class="gemini-error">
                          ❌ Falha ao carregar informações.
                        </div>
                      </div>
                    </transition>
                  </div>
                </div>
                <p class="rio-loc">{{ rio.cidade }} · {{ rio.estado }}</p>
              </div>
            </div>
            <div class="rio-hdr-r">
              <span v-if="rio.risco_inundacao" class="risk-chip" :class="rc(rio.risco_inundacao)">{{ rl(rio.risco_inundacao) }}</span>
            </div>
          </div>

          <!-- Gráficos por Ponto de Risco (igual ao Dashboard Admin) -->
          <div class="charts-wrap">
            <div v-if="!pontos[rio.id]" class="charts-loading">Carregando pontos...</div>
            <div v-else-if="pontos[rio.id].length === 0" class="charts-empty">Nenhum ponto de risco cadastrado neste rio.</div>
            <div v-else class="charts-grid">
              <div v-for="p in sortedPontos(rio.id)" :key="p.id" class="chart-card" :id="'ponto-' + p.id">
                <div class="chart-card-hdr">
                  <div>
                    <h3 class="chart-card-title">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
                      {{ p.descricao.length > 40 ? p.descricao.substring(0,40)+'…' : p.descricao }}
                    </h3>
                    <p class="chart-card-sub">
                      <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z"/><circle cx="12" cy="10" r="3"/></svg>
                      {{ rio.nome }} · {{ p.descricao.length > 45 ? p.descricao.substring(0,45)+'…' : p.descricao }}
                    </p>
                  </div>
                  <div style="display: flex; gap: 8px; align-items: center;">
                    <template v-if="!isDefesaCivil">
                      <div class="unauth-wrap" v-if="!isLoggedIn">
                        <button class="abtn abtn-sm abtn--disabled" style="padding: 4px 8px; font-size: 0.7rem;">
                          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                          Favoritar
                        </button>
                        <button class="abtn abtn-sm abtn--disabled" style="padding: 4px 8px; font-size: 0.7rem;">
                          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                          Alertas
                        </button>
                        <div class="unauth-tooltip">
                          <p>Funcionalidade liberada para cadastrados</p>
                          <router-link to="/registro" class="unauth-btn">Registre-se</router-link>
                        </div>
                      </div>
                      <template v-else>
                        <button class="abtn abtn-sm" :class="{ 'abtn--fav': isFav(p.id) }" @click="toggleFav(p.id)" style="padding: 4px 8px; font-size: 0.7rem;">
                          <svg width="12" height="12" viewBox="0 0 24 24" :fill="isFav(p.id)?'currentColor':'none'" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                          {{ isFav(p.id) ? 'Favorito' : 'Favoritar' }}
                        </button>
                        <button class="abtn abtn-sm" :class="{ 'abtn--alr': isAlert(p.id) }" @click="toggleAlert(p.id)" style="padding: 4px 8px; font-size: 0.7rem;">
                          <svg width="12" height="12" viewBox="0 0 24 24" :fill="isAlert(p.id)?'currentColor':'none'" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                          {{ isAlert(p.id) ? 'Alertas On' : 'Alertas' }}
                        </button>
                      </template>
                    </template>
                    <button class="live-badge" :class="{ 'live--flood': floodMap[p.id] }" @click="toggleFlood(p.id)" :title="floodMap[p.id] ? 'Parar simulação de enchente' : 'Simular enchente'">
                      <span class="live-dot" :class="{ 'live-dot--flood': floodMap[p.id] }"></span>
                      {{ floodMap[p.id] ? 'EXTRAVASANDO' : 'AO VIVO' }}
                    </button>
                  </div>
                </div>
                <div class="chart-canvas-wrap">
                  <div :ref="el => setObserverRef(el, p.id)" class="chart-observer">
                    <canvas v-if="visibleCharts.has(p.id)" :ref="el => setChartRef(el, p)"></canvas>
                    <div v-else class="chart-placeholder">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
                      <span>Rolar para carregar gráfico</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="estadosFiltrados.length === 0 && !loading" class="mon-state">Nenhum rio encontrado.</div>
    </main>

    <footer class="mon-footer">HydroTech · Sistema de Monitoramento Hidrológico · Gráficos atualizados a cada 10 segundos</footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/api'
import Chart from 'chart.js/auto'

const route = useRoute()
const userData = JSON.parse(localStorage.getItem('user_data') || '{}')
const isDefesaCivil = computed(() => !!userData.is_defesa_civil)
const isLoggedIn = computed(() => !!localStorage.getItem('user_token'))

const loading = ref(true)
const rios = ref([])
const pontos = ref({})
const filtroEstado = ref('')
const lastUpdate = ref('')
const canvasMap = ref({})
let charts = {}
let chartLevels = {}
let ticker = null
const floodMap = ref({})

const toggleFlood = (pontoId) => {
  floodMap.value = { ...floodMap.value, [pontoId]: !floodMap.value[pontoId] }
}

const expandedGemini = ref(null)
const geminiData = ref(null)
const loadingGemini = ref(false)
let geminiHoverTimer = null

const showGemini = async (rioId) => {
  if (geminiHoverTimer) clearTimeout(geminiHoverTimer)
  
  geminiHoverTimer = setTimeout(async () => {
    if (expandedGemini.value === rioId) return
    
    expandedGemini.value = rioId
    geminiData.value = null
    loadingGemini.value = true
    try {
      // Como agora liberamos o backend pra rotas públicas, batemos no endpoint
      const res = await api.getRioDescricaoGemini(rioId)
      geminiData.value = res.data
    } catch (err) {
      console.error('Erro ao carregar dados do Gemini:', err)
      geminiData.value = null
    } finally {
      loadingGemini.value = false
    }
  }, 250)
}

const hideGemini = () => {
  if (geminiHoverTimer) clearTimeout(geminiHoverTimer)
  expandedGemini.value = null
  geminiData.value = null
}

const favs = ref(new Set(JSON.parse(localStorage.getItem('ht_favs') || '[]')))
const alerts = ref(new Set(JSON.parse(localStorage.getItem('ht_alerts') || '[]')))
const isFav = id => favs.value.has(id)
const isAlert = id => alerts.value.has(id)
const favFilter = ref(false)
const toggleFav = async id => {
  const wasFav = favs.value.has(id)
  const next = new Set(favs.value)
  wasFav ? next.delete(id) : next.add(id)
  favs.value = next
  localStorage.setItem('ht_favs', JSON.stringify([...favs.value]))
  if (!wasFav) { favFilter.value = true }
  else if (next.size === 0) { favFilter.value = false }
  if (localStorage.getItem('user_token')) {
    try { await api.toggleFavorite(id) } catch (e) { console.error('Erro ao favoritar na API:', e) }
  }
}
const toggleAlert = async id => {
  isAlert(id) ? alerts.value.delete(id) : alerts.value.add(id);
  localStorage.setItem('ht_alerts', JSON.stringify([...alerts.value]));
  if (localStorage.getItem('user_token')) {
    try { await api.toggleAlert(id) } catch (e) { console.error('Erro ao alterar alerta na API:', e) }
  }
}

const rc = r => r >= 3 ? 'risk--high' : r === 2 ? 'risk--medium' : 'risk--low'
const rl = r => ({ 1: 'Baixo', 2: 'Médio', 3: 'Alto', 4: 'Muito Alto' }[r] || 'N/D')

const estados = computed(() => [...new Set(rios.value.map(r => r.estado))].filter(Boolean).sort())
const estadosFiltrados = computed(() => filtroEstado.value ? [filtroEstado.value] : estados.value)

const riosPorEstado = computed(() => {
  const map = {}
  const filtered = favFilter.value
    ? rios.value.filter(r => (pontos.value[r.id] || []).some(p => favs.value.has(p.id)))
    : rios.value
  filtered.forEach(r => { if (!map[r.estado]) map[r.estado] = []; map[r.estado].push(r) })
  Object.keys(map).forEach(estado => {
    map[estado].sort((a, b) => {
      const fa = (pontos.value[a.id] || []).some(p => favs.value.has(p.id)) ? 0 : 1
      const fb = (pontos.value[b.id] || []).some(p => favs.value.has(p.id)) ? 0 : 1
      return fa - fb
    })
  })
  return map
})
const totalRios = computed(() => rios.value.length)


const sortedPontos = (rioId) => {
  let pts = pontos.value[rioId] || []
  if (favFilter.value) pts = pts.filter(p => favs.value.has(p.id))
  return [...pts].sort((a, b) => {
    const fa = favs.value.has(a.id) ? 0 : 1
    const fb = favs.value.has(b.id) ? 0 : 1
    return fa - fb
  })
}

// Lazy Loading com IntersectionObserver
const visibleCharts = ref(new Set())
let chartObserver = null

const setObserverRef = (el, pontoId) => {
  if (!el) return
  if (!chartObserver) {
    chartObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = Number(entry.target.dataset.pontoId)
          visibleCharts.value = new Set([...visibleCharts.value, id])
          chartObserver.unobserve(entry.target)
        }
      })
    }, { rootMargin: '100px' })
  }
  el.dataset.pontoId = pontoId
  chartObserver.observe(el)
}

const setChartRef = (el, ponto) => {
  if (el) {
    const isNew = canvasMap.value[ponto.id] !== el
    canvasMap.value[ponto.id] = el
    if (isNew) {
      nextTick(() => {
        buildChart(ponto)
      })
    }
  }
}

// Igual ao Dashboard Admin
const buildChart = (ponto) => {
  const canvas = canvasMap.value[ponto.id]
  if (!canvas) return
  if (charts[ponto.id]) charts[ponto.id].destroy()
  const ctx = canvas.getContext('2d')
  const styles = getComputedStyle(document.documentElement)
  const nivelColor = '#38bdf8'
  const gradient = ctx.createLinearGradient(0, 0, 0, 300)
  gradient.addColorStop(0, nivelColor + '44')
  gradient.addColorStop(1, nivelColor + '00')
  const baseMap = { 1: 0.8, 2: 1.4, 3: 2.0 }
  const base = (ponto.nivel_base !== null && ponto.nivel_base !== undefined) ? parseFloat(ponto.nivel_base) : (baseMap[ponto.nivel_risco] || 1.0)
  const variance = 0.25
  const labels = Array.from({ length: 15 }, (_, i) => { const d = new Date(); d.setSeconds(d.getSeconds() - (14-i)*10); return d.toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit',second:'2-digit'}) })
  const data = Array.from({ length: 15 }, () => +(base + (Math.random()*variance*2 - variance)).toFixed(2))
  const atencao = (ponto.limite_atencao !== null && ponto.limite_atencao !== undefined) ? parseFloat(ponto.limite_atencao) : +(base + 0.5).toFixed(2)
  const alerta = (ponto.limite_alerta !== null && ponto.limite_alerta !== undefined) ? parseFloat(ponto.limite_alerta) : +(base + 0.85).toFixed(2)
  const emergencia = (ponto.limite_emergencia !== null && ponto.limite_emergencia !== undefined) ? parseFloat(ponto.limite_emergencia) : +(base + 1.2).toFixed(2)
  const txtMuted = styles.getPropertyValue('--text-muted').trim()

  const accentColor = styles.getPropertyValue('--accent').trim()

  chartLevels[ponto.id] = { base, variance, emergencia }
  charts[ponto.id] = new Chart(ctx, {
    type: 'line',
    data: {
      labels: Array.from({ length: 15 }, (_, i) => { const d = new Date(); d.setSeconds(d.getSeconds() - (14-i)*10); return d.toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit',second:'2-digit'}) }),
      datasets: [
        {
          label: 'Altura do Rio',
          data: Array.from({ length: 15 }, () => +(base + (Math.random()*variance*2 - variance)).toFixed(2)),
          borderColor: accentColor,
          backgroundColor: accentColor + '20',
          borderWidth: 2.5,
          pointRadius: 4,
          pointBackgroundColor: accentColor,
          pointBorderColor: styles.getPropertyValue('--bg-card').trim() || '#fff',
          pointBorderWidth: 1.5,
          fill: true,
          tension: 0.4
        },
        { label: 'Alto', data: Array(15).fill(emergencia), borderColor: '#ef4444', borderWidth: 1.5, borderDash: [6,4], pointRadius: 0, fill: false, tension: 0 },
        { label: 'Médio', data: Array(15).fill(alerta), borderColor: '#f59e0b', borderWidth: 1.5, borderDash: [6,4], pointRadius: 0, fill: false, tension: 0 },
        { label: 'Baixo', data: Array(15).fill(atencao), borderColor: '#4ade80', borderWidth: 1.5, borderDash: [6,4], pointRadius: 0, fill: false, tension: 0 }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false, animation: false,
      plugins: {
        legend: { display: true, position: 'top', labels: { usePointStyle: true, color: txtMuted, font: { size: 11 } } },
        tooltip: { backgroundColor: styles.getPropertyValue('--bg-elevated').trim() || '#1e293b', titleColor: styles.getPropertyValue('--text-primary').trim(), bodyColor: accentColor, padding: 10 }
      },
      scales: {
        y: { suggestedMin: 0, grid: { color: 'rgba(100,116,139,0.1)' }, ticks: { color: txtMuted } },
        x: { grid: { display: false }, ticks: { color: txtMuted, maxTicksLimit: 15 } }
      }
    }
  })
}

// Whapi configuration (Sandbox)
const WHAPI_TOKEN = 'YuOAsd5Lgg3bOMZOgueq5KRMB8Zhzlwu';
const CONTATOS = ['5519998534990', '5519997490041'];

const enviarMensagemWhatsApp = async (to, message) => {
  try {
    const response = await fetch('https://gate.whapi.cloud/messages/text', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${WHAPI_TOKEN}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        to: `${to}@s.whatsapp.net`,
        body: message
      })
    });
    if (response.ok) {
      console.log(`✅ Alerta enviado para ${to} com sucesso.`);
    } else {
      console.error(`❌ Falha ao enviar para ${to}. Status: ${response.status}`);
    }
  } catch (error) {
    console.error(`Erro na requisição para ${to}: ${error.message}`);
  }
};

const tick = () => {
  const label = new Date().toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit',second:'2-digit'})
  lastUpdate.value = label
  Object.entries(charts).forEach(([id, chart]) => {
    const lvl = chartLevels[id]; if (!lvl) return
    const ds = chart.data.datasets[0]
    const last = parseFloat(ds.data.at(-1))
    let next
    if (floodMap.value[Number(id)]) {
      next = +(last + (Math.random() * 1.2 + 0.6)).toFixed(2)
    } else {
      next = +(Math.max(Math.max(0,lvl.base-0.6), Math.min(lvl.emergencia+0.2, last+(Math.random()*lvl.variance*2-lvl.variance)))).toFixed(2)
    }
    chart.data.labels.push(label); ds.data.push(next)
    chart.data.datasets[1].data.push(chart.data.datasets[1].data[0])
    chart.data.datasets[2].data.push(chart.data.datasets[2].data[0])
    chart.data.datasets[3].data.push(chart.data.datasets[3].data[0])
    if (chart.data.labels.length > 15) { chart.data.labels.shift(); chart.data.datasets.forEach(d => d.data.shift()) }
    chart.update('none')

    // Integração Whapi: Verifica nível e dispara alerta se necessário
    const numericId = Number(id);
    if (next >= lvl.emergencia && isAlert(numericId)) {
      if (!lvl.alertado) {
        lvl.alertado = true; // Marca como alertado para não disparar a cada 10 segundos
        
        let pontoDesc = "Ponto Desconhecido";
        let rioNome = "";
        
        // Encontra o nome do Rio e a Descrição do Ponto de Risco
        Object.entries(pontos.value).forEach(([rId, pts]) => {
          const pt = pts.find(p => p.id === numericId);
          if (pt) {
            pontoDesc = pt.descricao;
            const r = rios.value.find(rio => rio.id == Number(rId));
            if (r) rioNome = r.nome;
          }
        });
        
        const localNome = rioNome ? `${rioNome} - ${pontoDesc}` : pontoDesc;
        console.log(`⚠️ Nível de emergência atingido em ${localNome}! Disparando alertas via Whapi...`);
        const mensagemAlerta = `⚠️ *ALERTA HYDROTECH*\nO nível em *${localNome}* atingiu ${next}m, nível de EMERGÊNCIA!\nEvite áreas de risco nas proximidades.`;
        
        CONTATOS.forEach(numero => {
          enviarMensagemWhatsApp(numero, mensagemAlerta);
        });
      }
    } else if (next < lvl.emergencia) {
      lvl.alertado = false; // Reseta o estado quando o nível abaixa do ponto de emergência
    }
  })
}

onMounted(async () => {
  try {
    const res = await api.getRiosPublico()
    rios.value = Array.isArray(res.data) ? res.data : res.data.results || []
    await Promise.all(rios.value.map(async rio => {
      try {
        const pr = await api.getPontosRiscoPublico(rio.id)
        pontos.value[rio.id] = Array.isArray(pr.data) ? pr.data : pr.data.results || []
      } catch { pontos.value[rio.id] = [] }
    }))
    lastUpdate.value = new Date().toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit',second:'2-digit'})
  } catch(e) {
    console.error(e)
  } finally {
    loading.value = false   // <-- primeiro renderiza os canvas
  }
  await nextTick()
  ticker = setInterval(tick, 10000)

  // Scroll to ponto if query param exists
  if (route.query.ponto) {
    setTimeout(() => {
      const el = document.getElementById(`ponto-${route.query.ponto}`)
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' })
        // Add a subtle highlight effect
        el.style.transition = 'box-shadow 0.3s ease'
        el.style.boxShadow = '0 0 0 4px rgba(59, 130, 246, 0.5)'
        setTimeout(() => { el.style.boxShadow = 'none' }, 2000)
      }
    }, 500)
  }
})

onUnmounted(() => {
  if (ticker) clearInterval(ticker)
  if (chartObserver) chartObserver.disconnect()
  Object.values(charts).forEach(c => c.destroy())
})
</script>

<style scoped>
.mon-page { min-height: 100vh; background: var(--bg-primary); color: var(--text-primary); display: flex; flex-direction: column; position: relative; overflow-x: hidden; }

/* Static Gradient Background */
.mesh-bg {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  z-index: 0;
  pointer-events: none;
  background:
    radial-gradient(ellipse at 10% 10%, rgba(14,165,233,0.12) 0%, transparent 50%),
    radial-gradient(ellipse at 90% 90%, rgba(56,189,248,0.08) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 50%, rgba(2,132,199,0.05) 0%, transparent 50%);
}

/* Topbar */
.mon-topbar { background: var(--glass-bg); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-bottom: 1px solid var(--glass-border); padding: 0 24px; position: sticky; top: 0; z-index: 100; }
.mon-inner { max-width: 1300px; margin: 0 auto; position: relative; z-index: 2; }
.mon-inner.row { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
.mon-topbar .mon-inner { display: flex; align-items: center; justify-content: space-between; height: 58px; }
.mon-brand { display: flex; align-items: center; gap: 10px; font-size: 0.95rem; color: var(--text-secondary); }
.mon-brand b { color: var(--accent); }
.mon-meta { display: flex; align-items: center; gap: 14px; }
.live-pill { display: flex; align-items: center; gap: 6px; font-size: 0.7rem; font-weight: 800; color: var(--risk-high); background: var(--risk-high-bg); padding: 4px 10px; border-radius: 20px; border: 1px solid var(--risk-high); letter-spacing: .5px; }
.live-dot { width: 7px; height: 7px; background: var(--risk-high); border-radius: 50%; animation: pulse 1.4s infinite; }
.upd-time { font-size: 0.75rem; color: var(--text-muted); }
.back-lnk { font-size: 0.8rem; color: var(--accent); text-decoration: none; font-weight: 600; }
.back-lnk:hover { opacity: .7; }

/* Filter bar */
.mon-filter-bar { background: var(--glass-bg); backdrop-filter: blur(10px); border-bottom: 1px solid var(--glass-border); padding: 10px 24px; position: relative; z-index: 2; }
.frow { display: flex; align-items: center; gap: 8px; color: var(--text-secondary); }
.f-sel { padding: 7px 12px; border-radius: var(--radius-md); border: 1px solid var(--border); background: var(--bg-card); color: var(--text-primary); font-size: 0.85rem; }
.fav-filter-btn { display: inline-flex; align-items: center; gap: 6px; padding: 7px 12px; border-radius: var(--radius-md); border: 1px solid var(--border); background: var(--bg-card); color: var(--text-secondary); font-size: 0.82rem; cursor: pointer; transition: all 0.15s; font-family: inherit; }
.fav-filter-btn:hover { border-color: var(--accent); color: var(--accent); }
.fav-filter-btn.active { background: #f59e0b20; border-color: #f59e0b; color: #f59e0b; }
.fstats { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.fs { font-size: 0.73rem; font-weight: 700; padding: 3px 10px; border-radius: 20px; }
.fs-t { background: rgba(56, 189, 248, 0.1); color: var(--accent); border: 1px solid rgba(56, 189, 248, 0.2); }
.fs-h { background: rgba(239, 68, 68, 0.1); color: var(--risk-high); border: 1px solid rgba(239, 68, 68, 0.2); }
.fs-m { background: rgba(245, 158, 11, 0.1); color: var(--risk-medium); border: 1px solid rgba(245, 158, 11, 0.2); }
.fs-l { background: rgba(16,185,129,.1); color: var(--risk-low); border: 1px solid rgba(16, 185, 129, 0.2); }

/* States */
.mon-state { flex: 1; display: flex; align-items: center; justify-content: center; gap: 12px; padding: 80px; color: var(--text-muted); flex-direction: column; position: relative; z-index: 2; }

/* Main */
.mon-main { flex: 1; max-width: 1300px; margin: 0 auto; width: 100%; padding: 28px 24px; display: flex; flex-direction: column; gap: 36px; position: relative; z-index: 2; }

/* Estado Section */
.estado-section { display: flex; flex-direction: column; gap: 20px; }
.estado-header { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 800; color: var(--text-primary); padding-bottom: 8px; border-bottom: 2px solid rgba(56, 189, 248, 0.4); }
.estado-count { font-size: 0.75rem; font-weight: 600; background: rgba(56, 189, 248, 0.1); color: var(--accent); padding: 2px 8px; border-radius: 20px; margin-left: 4px; border: 1px solid rgba(56, 189, 248, 0.2); }

/* Rio Block */
.rio-block { background: var(--bg-card); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid var(--border); border-radius: var(--radius-xl); overflow: hidden; box-shadow: var(--shadow-lg); }
.rio-hdr { display: flex; align-items: center; justify-content: space-between; padding: 16px 22px; flex-wrap: wrap; gap: 12px; border-bottom: 1px solid var(--border-light); }
.rio-hdr.risk--high { border-left: 4px solid var(--risk-high); }
.rio-hdr.risk--medium { border-left: 4px solid var(--risk-medium); }
.rio-hdr.risk--low { border-left: 4px solid var(--risk-low); }
.rio-hdr-l { display: flex; align-items: center; gap: 12px; }
.rio-icon { width: 42px; height: 42px; border-radius: var(--radius-lg); display: flex; align-items: center; justify-content: center; }
.rio-icon.risk--high { background: var(--risk-high-bg); color: var(--risk-high); }
.rio-icon.risk--medium { background: var(--risk-medium-bg); color: var(--risk-medium); }
.rio-icon.risk--low { background: var(--risk-low-bg); color: var(--risk-low); }
.rio-name { font-size: 1.1rem; font-weight: 800; color: var(--text-primary); }
.rio-loc { font-size: 0.78rem; color: var(--text-muted); margin-top: 2px; }
.rio-hdr-r { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.risk-chip { font-size: 0.72rem; font-weight: 800; padding: 4px 12px; border-radius: 20px; }
.risk-chip.risk--high { background: rgba(239, 68, 68, 0.15); color: var(--risk-high); border: 1px solid rgba(239, 68, 68, 0.3); }
.risk-chip.risk--medium { background: rgba(245, 158, 11, 0.15); color: var(--risk-medium); border: 1px solid rgba(245, 158, 11, 0.3); }
.risk-chip.risk--low { background: rgba(16,185,129,.15); color: var(--risk-low); border: 1px solid rgba(16, 185, 129, 0.3); }
.abtn { display: flex; align-items: center; gap: 6px; padding: 7px 13px; border-radius: var(--radius-md); border: 1px solid var(--border); background: var(--bg-secondary); color: var(--text-muted); font-size: 0.78rem; font-weight: 600; cursor: pointer; transition: all .2s; backdrop-filter: blur(4px); }
.abtn:hover { border-color: var(--accent); color: var(--accent); background: var(--bg-card-hover); }
.abtn--fav { color: #F59E0B; border-color: #F59E0B; background: rgba(245,158,11,.08); }
.abtn--alr { color: var(--accent); border-color: var(--accent); background: rgba(56, 189, 248, 0.1); }
.abtn--disabled { 
  background: var(--bg-card) !important; 
  color: var(--text-muted) !important; 
  border-color: var(--border-light) !important; 
  opacity: 0.6; 
  cursor: not-allowed !important; 
}
.abtn--disabled:hover {
  transform: none !important;
  background: var(--bg-card) !important;
  border-color: var(--border-light) !important;
}

/* Tooltip Balão Não Logado */
.unauth-wrap {
  position: relative;
  display: flex;
  gap: 8px;
}
.unauth-tooltip {
  position: absolute;
  bottom: calc(100% + 12px);
  right: 0;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
  padding: 12px 16px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  gap: 14px;
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transform: translateY(10px);
  transition: all 0.2s ease;
  z-index: 100;
  white-space: nowrap;
}
.unauth-wrap:hover .unauth-tooltip {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
  transform: translateY(0);
}
.unauth-tooltip::before {
  content: '';
  position: absolute;
  bottom: -12px;
  left: 0;
  width: 100%;
  height: 12px;
}
.unauth-tooltip::after {
  content: '';
  position: absolute;
  bottom: -6px;
  right: 25px;
  width: 10px;
  height: 10px;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border-light);
  border-right: 1px solid var(--border-light);
  transform: rotate(45deg);
}
.unauth-tooltip p {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}
.unauth-btn {
  background: var(--accent);
  color: white;
  padding: 7px 16px;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
  font-weight: 800;
  text-decoration: none;
  transition: all 0.2s;
}
.unauth-btn:hover {
  background: var(--accent-hover);
  transform: translateY(-1px);
}

/* Charts area */
.charts-wrap { padding: 20px 22px; }
.charts-loading, .charts-empty { color: var(--text-muted); font-size: 0.85rem; text-align: center; padding: 20px; }
.charts-grid { display: grid; grid-template-columns: 1fr; gap: 20px; position: relative; }

/* Transitions */

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(30px) scale(0.95);
}
.list-leave-active {
  position: absolute;
}

/* Chart Card — Glassmorphism */
.chart-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-xl); backdrop-filter: blur(10px); }
.chart-card-hdr { display: flex; align-items: flex-start; justify-content: space-between; padding: 18px 22px; border-bottom: 1px solid var(--border-light); gap: 10px; }
.chart-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 700; color: var(--text-primary); }
.chart-card-sub { display: flex; align-items: center; flex-wrap: wrap; gap: 4px; font-size: 0.78rem; color: var(--text-muted); margin-top: 5px; }
.nlv--alto { color: var(--risk-high); font-weight: 700; }
.nlv--medio { color: var(--risk-medium); font-weight: 700; }
.nlv--baixo { color: var(--risk-low); font-weight: 700; }
.live-badge { display: flex; align-items: center; gap: 5px; font-size: 0.7rem; font-weight: 800; color: var(--risk-high); background: var(--risk-high-bg); padding: 4px 9px; border-radius: 8px; border: 1px solid var(--risk-high); flex-shrink: 0; cursor: pointer; transition: all 0.2s; font-family: inherit; }
.live-badge:hover { background: var(--risk-high); color: white; }
.live--flood { background: #dc2626; color: white; border-color: #b91c1c; animation: floodPulse 1s infinite; }
.live-dot--flood { background: white; animation: floodPulse 1s infinite; }

@keyframes floodPulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.6;transform:scale(1.3)} }
.chart-canvas-wrap { height: 300px; padding: 18px 20px; }

.chart-observer { width: 100%; height: 100%; }

.chart-placeholder {
  width: 100%; height: 100%;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 8px;
  color: var(--text-muted); font-size: 0.82rem; opacity: 0.5;
}

.mon-footer { background: var(--glass-bg); backdrop-filter: blur(10px); border-top: 1px solid var(--glass-border); padding: 14px 24px; text-align: center; font-size: 0.73rem; color: var(--text-muted); position: relative; z-index: 2; }

@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.4;transform:scale(1.4)} }
.spin { animation: spin .8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Gemini Styles */
.rio-nome-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.gemini-hover-trigger {
  position: relative;
  font-size: 0.72rem;
  font-weight: 600;
  color: #818cf8;
  cursor: help;
  padding: 4px 0;
  transition: color 0.2s ease;
}

.gemini-hover-trigger:hover {
  color: #a5b4fc;
}

.gemini-panel-wrapper {
  position: absolute;
  top: calc(100% + 5px);
  left: 0;
  z-index: 100;
  width: 650px;
  max-width: 90vw;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-xl);
  border-radius: var(--radius-lg);
  backdrop-filter: blur(12px);
  padding: 20px;
  cursor: default;
}

.gemini-fade-enter-active,
.gemini-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.gemini-fade-enter-from,
.gemini-fade-leave-to {
  opacity: 0;
  transform: translateY(5px);
}

.gemini-skeleton {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.skeleton-header {
  display: flex;
  gap: 12px;
}
.skeleton-pill {
  width: 120px;
  height: 32px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  position: relative;
  overflow: hidden;
}
.skeleton-pill::after {
  content: "";
  position: absolute;
  top: 0; right: 0; bottom: 0; left: 0;
  background: linear-gradient(90deg, transparent, var(--border-light), transparent);
  transform: translateX(-100%);
  animation: shimmer 1.5s infinite;
}
.skeleton-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.skeleton-line {
  height: 14px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-sm);
  position: relative;
  overflow: hidden;
  width: 100%;
}
.skeleton-line::after {
  content: "";
  position: absolute;
  top: 0; right: 0; bottom: 0; left: 0;
  background: linear-gradient(90deg, transparent, var(--border-light), transparent);
  transform: translateX(-100%);
  animation: shimmer 1.5s infinite;
}
.skeleton-line-title {
  height: 20px;
  width: 250px;
  margin-bottom: 8px;
}
.skeleton-line-short {
  width: 60%;
}

@keyframes shimmer {
  100% { transform: translateX(100%); }
}

.gemini-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.gemini-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-light);
  padding-bottom: 12px;
}
.gemini-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--text-primary);
}
.gemini-icon {
  color: #818cf8;
  animation: rotateGlow 3s linear infinite;
}

@keyframes rotateGlow {
  0% { transform: rotate(0deg); filter: drop-shadow(0 0 2px rgba(99, 102, 241, 0.4)); }
  50% { filter: drop-shadow(0 0 8px rgba(99, 102, 241, 0.8)); }
  100% { transform: rotate(360deg); filter: drop-shadow(0 0 2px rgba(99, 102, 241, 0.4)); }
}

.fallback-tag {
  background: rgba(217, 119, 6, 0.1);
  border: 1px solid rgba(217, 119, 6, 0.2);
  color: #fbbf24;
  font-size: 0.68rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: var(--radius-full);
}

.gemini-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}
.metric-item {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  padding: 8px 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all var(--transition-fast);
}
.metric-item:hover {
  background: var(--bg-card-hover);
  border-color: var(--accent);
}
.metric-icon {
  font-size: 1.5rem;
}
.metric-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.metric-lbl {
  font-size: 0.60rem;
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: 700;
  letter-spacing: 0.05em;
}
.metric-val {
  font-size: 0.78rem;
  color: var(--text-primary);
  font-weight: 600;
  line-height: 1.2;
}

.gemini-info {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}
.gemini-desc h3, .gemini-curiosidade h3 {
  font-size: 0.82rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #a5b4fc;
  margin-bottom: 8px;
}
.gemini-desc p {
  font-size: 0.875rem;
  line-height: 1.6;
  color: var(--text-secondary);
  white-space: pre-line;
}
.gemini-curiosidade {
  background: rgba(99, 102, 241, 0.04);
  border: 1px solid rgba(99, 102, 241, 0.1);
  padding: 12px 16px;
  border-radius: var(--radius-md);
}
.gemini-curiosidade p {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.5;
}
.gemini-error {
  color: var(--risk-high);
  background: var(--risk-high-bg);
  border: 1px solid var(--risk-high);
  padding: 16px;
  border-radius: var(--radius-md);
  text-align: center;
  font-weight: 600;
  font-size: 0.9rem;
}

@media (max-width: 900px) { .charts-grid { grid-template-columns: 1fr; } }
@media (max-width: 600px) { .upd-time { display: none; } .rio-hdr { flex-direction: column; } }
</style>