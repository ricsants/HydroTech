<template>
  <div class="dashboard">

    <!-- Page Header -->
    <div class="page-header">
      <div>
        <p class="page-label">Painel Operacional</p>
        <h1 class="page-title">Centro de Controle</h1>
        <p class="page-subtitle">Monitoramento em tempo real de todos os pontos de risco hidrológico cadastrados.</p>
      </div>
      <div class="header-right">
        <div class="header-stat">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/></svg>
          <span>Rios</span>
          <strong>{{ rios.length }}</strong>
        </div>
        <div class="header-stat">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z"/><circle cx="12" cy="10" r="3"/></svg>
          <span>Pontos</span>
          <strong>{{ totalPontos }}</strong>
        </div>
        <div class="header-stat header-stat--live">
          <span class="live-dot"></span>
          <span>AO VIVO</span>
          <strong v-if="lastUpdate">{{ lastUpdate }}</strong>
        </div>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="filter-bar">
      <div class="filter-row">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
        <select v-model="filtroEstado" class="filter-select">
          <option value="">Todos os estados</option>
          <option v-for="e in estadosList" :key="e" :value="e">{{ e }}</option>
        </select>
      </div>
    </div>

    <!-- Loading Skeletons -->
    <div v-if="loading" class="skeleton-grid">
      <div v-for="i in 4" :key="'skel'+i" class="skeleton-card">
        <div class="skeleton-hdr">
          <div class="skeleton-title skeleton"></div>
          <div class="skeleton-sub skeleton"></div>
        </div>
        <div class="skeleton-body skeleton"></div>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else-if="todosPontos.length === 0" class="empty-state">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
        <path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>
        <path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>
      </svg>
      <p>Nenhum ponto de risco cadastrado</p>
      <span>Cadastre rios e pontos de levantamento na seção "Gestão de Rios" para começar o monitoramento.</span>
    </div>

    <div v-else class="dashboard-content">
      <!-- Agrupado por Estado -->
      <div v-for="estado in estadosFiltrados" :key="estado" class="estado-section">
        <div class="estado-header">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          {{ estado }}
          <span class="estado-count">{{ riosPorEstado[estado]?.length || 0 }} rios</span>
        </div>

        <!-- Rios do Estado -->
        <div v-for="rio in riosPorEstado[estado]" :key="rio.id" class="rio-block">
          <div class="rio-hdr">
            <div class="rio-hdr-l">
              <div class="rio-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/></svg>
              </div>
              <div>
                <h2 class="rio-name">{{ rio.nome }}</h2>
                <p class="rio-loc">{{ rio.cidade }} · {{ rio.estado }}</p>
              </div>
            </div>
            <span class="rio-pontos-count">{{ (pontosPorRio[rio.id] || []).length }} pontos</span>
          </div>

          <!-- Gráficos por Ponto de Risco -->
          <div class="charts-wrap">
            <div v-if="!pontosPorRio[rio.id] || pontosPorRio[rio.id].length === 0" class="charts-empty">
              Nenhum ponto de risco cadastrado neste rio.
            </div>
            <div v-else class="charts-grid">
              <div v-for="ponto in pontosPorRio[rio.id]" :key="ponto.id" class="chart-card">
                <div class="chart-card-hdr">
                  <div>
                    <h3 class="chart-card-title">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
                      {{ ponto.descricao.length > 40 ? ponto.descricao.substring(0,40)+'…' : ponto.descricao }}
                    </h3>
                    <p class="chart-card-sub">
                      <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z"/><circle cx="12" cy="10" r="3"/></svg>
                      {{ rio.nome }} · {{ ponto.descricao.length > 45 ? ponto.descricao.substring(0,45)+'…' : ponto.descricao }}
                    </p>
                  </div>
                  <div class="live-badge">
                    <span class="live-dot"></span>
                    AO VIVO
                  </div>
                </div>
                <div class="chart-canvas-wrap">
                  <div :ref="el => setObserverRef(el, ponto.id)" class="chart-observer">
                    <canvas v-if="visibleCharts.has(ponto.id)" :ref="el => setChartRef(el, ponto.id)"></canvas>
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
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import api from '../services/api'
import Chart from 'chart.js/auto'

const chartCanvases = ref({})
let chartInstances = {}
let chartLevels = {}
let chartInterval = null

const setChartRef = (el, id) => {
  if (el) chartCanvases.value[id] = el
  else delete chartCanvases.value[id]
}

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
          const todo = todosPontos.value.find(({ ponto }) => ponto.id === id)
          if (todo) buildChart(todo.ponto)
        }
      })
    }, { rootMargin: '100px' })
  }
  el.dataset.pontoId = pontoId
  chartObserver.observe(el)
}

const buildChart = (ponto) => {
  const canvas = chartCanvases.value[ponto.id]
  if (!canvas || chartInstances[ponto.id]) return
  const ctx = canvas.getContext('2d')
  const nivelColor = '#38bdf8'
  const gradient = ctx.createLinearGradient(0, 0, 0, 220)
  gradient.addColorStop(0, nivelColor + '40')
  gradient.addColorStop(1, nivelColor + '05')
  const baseMap = { 1: 0.8, 2: 1.4, 3: 2.0 }
  const base = (ponto.nivel_base !== null && ponto.nivel_base !== undefined)
    ? parseFloat(ponto.nivel_base)
    : (baseMap[ponto.nivel_risco] || 1.0)
  const variance = 0.25
  const data = Array.from({ length: 15 }, () =>
    (base + (Math.random() * variance * 2 - variance)).toFixed(2)
  )
  const labels = Array.from({ length: 15 }, (_, i) => {
    const d = new Date()
    d.setSeconds(d.getSeconds() - (15 - i) * 10)
    return d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  })
  const atencao = (ponto.limite_atencao !== null && ponto.limite_atencao !== undefined)
    ? parseFloat(ponto.limite_atencao) : +(base + 0.5).toFixed(2)
  const alerta = (ponto.limite_alerta !== null && ponto.limite_alerta !== undefined)
    ? parseFloat(ponto.limite_alerta) : +(base + 0.85).toFixed(2)
  const emergencia = (ponto.limite_emergencia !== null && ponto.limite_emergencia !== undefined)
    ? parseFloat(ponto.limite_emergencia) : +(base + 1.2).toFixed(2)
  chartLevels[ponto.id] = { base, variance, emergenciaLevel: parseFloat(emergencia) }

  chartInstances[ponto.id] = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        { label: 'Altura do Rio', data, borderColor: nivelColor, backgroundColor: gradient, borderWidth: 2, pointRadius: 3, pointHoverRadius: 5, pointBackgroundColor: nivelColor, pointBorderColor: 'transparent', fill: true, tension: 0.4 },
        { label: 'Alto', data: Array(15).fill(emergencia), borderColor: '#ef4444', borderWidth: 1, borderDash: [5, 4], pointRadius: 0, fill: false },
        { label: 'Médio', data: Array(15).fill(alerta), borderColor: '#f59e0b', borderWidth: 1, borderDash: [5, 4], pointRadius: 0, fill: false },
        { label: 'Baixo', data: Array(15).fill(atencao), borderColor: '#4ade80', borderWidth: 1, borderDash: [5, 4], pointRadius: 0, fill: false }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false, animation: false,
      plugins: {
        legend: { display: true, position: 'top', labels: { usePointStyle: true, color: getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim(), font: { size: 10 }, boxWidth: 8 } },
        tooltip: { backgroundColor: getComputedStyle(document.documentElement).getPropertyValue('--bg-elevated').trim() || '#0D1B2E', titleColor: getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim(), bodyColor: getComputedStyle(document.documentElement).getPropertyValue('--accent').trim(), borderColor: 'rgba(0,0,0,0.08)', borderWidth: 1, padding: 10 }
      },
      scales: {
        y: { suggestedMin: 0, grid: { color: 'rgba(100,116,139,0.1)' }, ticks: { color: getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim(), font: { size: 10 } } },
        x: { grid: { display: false }, ticks: { color: getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim(), maxTicksLimit: 15, font: { size: 10 } } }
      }
    }
  })
}

const rios = ref([])
const loading = ref(true)
const lastUpdate = ref('')
const pontosPorRio = ref({})
const todosPontos = ref([])
const totalPontos = computed(() => todosPontos.value.length)

const filtroEstado = ref('')
watch(filtroEstado, () => {
  Object.values(chartInstances).forEach(c => c.destroy())
  chartInstances = {}
  chartLevels = {}
  visibleCharts.value = new Set()
})

const estadosList = computed(() =>
  [...new Set(rios.value.map(r => r.estado))].filter(Boolean).sort()
)
const estadosFiltrados = computed(() => {
  if (filtroEstado.value) return [filtroEstado.value]
  return estadosList.value
})
const riosPorEstado = computed(() => {
  const map = {}
  rios.value.forEach(r => {
    if (!map[r.estado]) map[r.estado] = []
    map[r.estado].push(r)
  })
  return map
})

const tick = () => {
  const newLabel = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  Object.entries(chartInstances).forEach(([pontoId, chart]) => {
    const levels = chartLevels[pontoId]
    if (!levels) return
    const ds = chart.data.datasets[0]
    let v = parseFloat(ds.data.slice(-1)[0]) + (Math.random() * levels.variance * 2 - levels.variance)
    v = Math.max(Math.max(0, levels.base - 0.6), Math.min(levels.emergenciaLevel + 0.2, v))
    chart.data.labels.push(newLabel)
    ds.data.push(v.toFixed(2))
    chart.data.datasets[1].data.push(chart.data.datasets[1].data[0])
    chart.data.datasets[2].data.push(chart.data.datasets[2].data[0])
    chart.data.datasets[3].data.push(chart.data.datasets[3].data[0])
    if (chart.data.labels.length > 15) {
      chart.data.labels.shift()
      chart.data.datasets.forEach(d => d.data.shift())
    }
    chart.update('none')
  })
  lastUpdate.value = newLabel
}

const load = async () => {
  loading.value = true
  try {
    const res = await api.getRios()
    rios.value = Array.isArray(res.data) ? res.data : res.data.results || []
    const promises = rios.value.map(async (rio) => {
      try {
        const pr = await api.getPontosRisco(rio.id)
        const pontos = Array.isArray(pr.data) ? pr.data : pr.data.results || []
        pontosPorRio.value[rio.id] = pontos
        return pontos.map(ponto => ({ rio, ponto }))
      } catch {
        pontosPorRio.value[rio.id] = []
        return []
      }
    })
    const resultados = await Promise.all(promises)
    todosPontos.value = resultados.flat()
  } catch (err) {
    console.error('Erro ao carregar:', err)
  } finally {
    loading.value = false
    lastUpdate.value = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    await nextTick()
    if (todosPontos.value.length > 0) {
      chartInterval = setInterval(tick, 10000)
    }
  }
}

onMounted(() => load())
onUnmounted(() => {
  if (chartInterval) clearInterval(chartInterval)
  if (chartObserver) chartObserver.disconnect()
  Object.values(chartInstances).forEach(c => c.destroy())
  chartLevels = {}
})
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
  animation: fadeInUp 0.35s ease-out;
}

/* Page Header */
.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.page-label {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-top: 4px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.header-stat {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-size: 0.78rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.header-stat svg { color: var(--accent); }
.header-stat strong { font-size: 1.1rem; font-weight: 800; color: var(--text-primary); }

.header-stat--live {
  background: var(--risk-high-bg);
  border-color: var(--risk-high);
  color: var(--risk-high);
}
.header-stat--live strong { color: var(--risk-high); font-size: 0.78rem; }

/* Filter Bar */
.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
}

.filter-select {
  padding: 8px 14px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  background: var(--bg-card);
  color: var(--text-primary);
  font-size: 0.85rem;
  font-family: inherit;
}

/* Skeleton Loading */
.skeleton-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 80px 24px;
  color: var(--text-muted);
  text-align: center;
}

.empty-state p {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-secondary);
}

.empty-state span {
  font-size: 0.9rem;
  max-width: 400px;
  line-height: 1.6;
}

/* Dashboard Content */
.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

/* Estado Section */
.estado-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.estado-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  font-weight: 800;
  color: var(--text-primary);
  padding-bottom: 8px;
  border-bottom: 2px solid rgba(56, 189, 248, 0.4);
}

.estado-count {
  font-size: 0.75rem;
  font-weight: 600;
  background: rgba(56, 189, 248, 0.1);
  color: var(--accent);
  padding: 2px 8px;
  border-radius: 20px;
  margin-left: 4px;
  border: 1px solid rgba(56, 189, 248, 0.2);
}

/* Rio Block */
.rio-block {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.rio-hdr {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 22px;
  border-bottom: 1px solid var(--border-light);
  border-left: 4px solid var(--accent);
  flex-wrap: wrap;
  gap: 12px;
}

.rio-hdr-l {
  display: flex;
  align-items: center;
  gap: 12px;
}

.rio-icon {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent-soft);
  color: var(--accent);
}

.rio-name {
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--text-primary);
}

.rio-loc {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-top: 2px;
}

.rio-pontos-count {
  font-size: 0.72rem;
  font-weight: 700;
  background: var(--bg-elevated);
  color: var(--text-secondary);
  padding: 4px 12px;
  border-radius: var(--radius-full);
  border: 1px solid var(--border);
}

/* Charts */
.charts-wrap {
  padding: 20px 22px;
}

.charts-empty {
  color: var(--text-muted);
  font-size: 0.85rem;
  text-align: center;
  padding: 20px;
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

/* Chart Card */
.chart-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
}

.chart-card-hdr {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 18px 22px;
  border-bottom: 1px solid var(--border-light);
  gap: 10px;
}

.chart-card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.chart-card-sub {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-top: 5px;
}

.live-badge {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.7rem;
  font-weight: 800;
  color: var(--risk-high);
  background: var(--risk-high-bg);
  padding: 4px 9px;
  border-radius: 8px;
  border: 1px solid var(--risk-high);
  flex-shrink: 0;
}

.live-dot {
  width: 7px;
  height: 7px;
  background: var(--risk-high);
  border-radius: 50%;
  animation: pulse 1.4s infinite;
}

.chart-canvas-wrap {
  height: 280px;
  padding: 18px 20px;
}

.chart-observer {
  width: 100%;
  height: 100%;
}

.chart-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: var(--text-muted);
  font-size: 0.82rem;
  opacity: 0.5;
}

/* Animations */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(1.4); }
}

/* Responsive */
@media (max-width: 768px) {
  .page-header { flex-direction: column; align-items: flex-start; }
  .header-right { flex-wrap: wrap; }
}
</style>