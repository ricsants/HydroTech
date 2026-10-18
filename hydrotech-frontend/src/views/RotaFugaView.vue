<template>
  <div class="escape-page">
    <div class="escape-heading">
      <div>
        <p class="eyebrow">HydroTech · demonstração acadêmica</p>
        <h1>Rota de fuga simulada</h1>
        <p>Os círculos representam pontos de risco fictícios cadastrados no HydroTech.</p>
      </div>
      <router-link to="/monitoramento" class="return-link">← Monitoramento</router-link>
    </div>

    <div class="escape-layout">
      <section class="map-panel" aria-label="Mapa de riscos e rota">
        <div ref="mapElement" class="escape-map" :class="{ 'escape-map--choosing': choosingOnMap }" aria-label="Mapa para escolher a partida da rota simulada"></div>
        <div v-if="choosingOnMap" class="map-pick-hint" role="status">Toque no mapa para marcar a partida, inclusive dentro do círculo vermelho.</div>
        <div v-if="autoRoutePending" class="auto-route-progress" role="status" aria-live="polite">
          <span class="auto-route-spinner" aria-hidden="true"></span>
          <span><strong>{{ autoRouteMessage }}</strong><small>Aguarde enquanto os dados da simulação são consultados.</small></span>
        </div>
        <div class="map-legend"><span class="legend-risk"></span> Área simulada de risco · raio de 300 m</div>
      </section>

      <aside class="route-panel">
        <div v-if="alertaId" class="alert-banner">Simulação de alerta para o ponto {{ alertaId }}</div>
        <div class="simulation-warning" role="note"><strong>Simulação acadêmica</strong><span>Alertas e riscos são fictícios. Esta rota não foi validada para emergências reais. Siga as orientações da Defesa Civil.</span></div>
        <div v-if="serviceError" class="service-error" role="alert">
          <p class="message error">{{ serviceError }}</p>
          <button type="button" class="retry-button" :disabled="zonesLoading" @click="loadZones(true)">Tentar carregar os pontos novamente</button>
        </div>
        <p v-else-if="zonesLoading" class="message">Carregando pontos de risco...</p>
        <p v-else-if="zones.length === 0" class="message">Nenhum ponto de risco cadastrado. Cadastre um ponto no HydroTech para demonstrar o cálculo.</p>

        <div class="field-row">
          <label for="travel-mode">Deslocamento</label>
          <select id="travel-mode" v-model="mode" :disabled="busy" @change="clearRoute">
            <option value="pe">A pé</option>
            <option value="carro">De carro</option>
          </select>
        </div>

        <div class="origin-section">
          <strong>1. Escolha a partida</strong>
          <p v-if="origin" class="origin-help" role="status">Partida definida pelo {{ originSource }} · {{ origin.lat.toFixed(5) }}, {{ origin.lng.toFixed(5) }}</p>
          <p v-else class="origin-help">Use sua localização, marque qualquer lugar no mapa ou escolha um ponto para a demonstração.</p>
          <div class="origin-actions">
            <button type="button" class="secondary-button" :disabled="busy || zonesLoading || !!serviceError || !zones.length" @click="useGps">Usar minha localização</button>
            <button type="button" class="secondary-button" :class="{ 'secondary-button--active': choosingOnMap }" :disabled="busy || zonesLoading || !!serviceError || !zones.length" @click="chooseOnMap">{{ choosingOnMap ? 'Toque no mapa acima' : 'Escolher no mapa' }}</button>
          </div>
          <button type="button" class="demo-button" :disabled="busy || zonesLoading || !!serviceError || !zones.length" @click="simulateOrigin">Simular perto do ponto de risco</button>
        </div>
        <button type="button" class="primary-button calculate-button" :disabled="busy || zonesLoading || !!serviceError || !zones.length || !origin" @click="findRoute">
          {{ busy ? 'Calculando...' : result ? 'Recalcular rota simulada' : '2. Calcular rota simulada' }}
        </button>
        <p v-if="routingStatus && !result" class="service-note">{{ routingStatus }}</p>
        <p v-if="error" class="message error" role="alert">{{ error }}</p>

        <template v-if="result">
          <p v-if="result.dentro_de_zona_risco" class="message danger">A partida está dentro de uma zona de risco simulada.</p>
          <div v-if="!result.rota" class="route-assessment route-assessment--warning" role="status"><strong>Sem trajeto pelas ruas</strong><span>O destino é apenas uma referência no mapa. Não há caminho calculado até ele.</span></div>
          <div v-else-if="result.rota.zonas_cruzadas?.length" class="route-assessment route-assessment--danger" role="alert"><strong>Atenção: o trajeto cruza uma área de risco simulada</strong><span>O cálculo não conseguiu contornar todos os círculos vermelhos. Esta rota é somente uma demonstração.</span></div>
          <div v-else-if="!result.rota.desvia_zonas" class="route-assessment route-assessment--warning" role="status"><strong>Desvio das áreas de risco não garantido</strong><span>O OSRM escolheu uma alternativa entre as ruas disponíveis, mas não impede automaticamente a passagem por zonas simuladas.</span></div>
          <div v-if="result.destino" class="destination-card">
            <span class="card-label">Destino potencialmente menos exposto</span>
            <strong>{{ result.destino.endereco || 'Ponto escolhido pelo algoritmo' }}</strong>
            <span>Ponto estimado para demonstração; não é um abrigo cadastrado.</span>
          </div>
          <div v-if="result.rota" class="metrics">
            <span><strong>{{ formatDistance(result.rota.distancia_m) }}</strong> Distância</span>
            <span><strong>{{ formatDuration(result.rota.duracao_s) }}</strong> Tempo estimado</span>
          </div>
          <details v-if="result.rota?.passos?.length" class="steps" open>
            <summary>Orientações do trajeto ({{ result.rota.passos.length }})</summary>
            <ol><li v-for="(step, index) in result.rota.passos" :key="index">{{ step.instrucao }} <span v-if="step.distancia_m">({{ formatDistance(step.distancia_m) }})</span></li></ol>
          </details>
          <div v-if="result.rota?.desvia_zonas && !result.rota.zonas_cruzadas?.length" class="route-assessment route-assessment--info" role="status"><strong>Desvio solicitado ao OpenRouteService</strong><span>O trajeto foi calculado considerando os círculos vermelhos simulados; ele não foi verificado para uma emergência real.</span></div>
          <div v-if="result.destino" class="route-extra"><span v-if="result.destino.acima_do_risco_m != null">Altitude estimada: {{ formatNumber(result.destino.acima_do_risco_m) }} m acima do ponto de referência</span><span v-else>Altitude não disponível para comparação.</span></div>
          <ul v-if="result.avisos?.length" class="warnings">
            <li v-for="(notice, index) in result.avisos" :key="index">{{ notice }}</li>
          </ul>
          <div class="external-links">
            <a v-if="result.links?.google_maps" :href="result.links.google_maps" target="_blank" rel="noopener noreferrer">Abrir Google Maps</a>
            <a v-if="result.modo === 'carro' && result.links?.waze" :href="result.links.waze" target="_blank" rel="noopener noreferrer">Abrir Waze</a>
          </div>
          <p v-if="result.links?.google_maps || result.links?.waze" class="external-note">Google Maps e Waze não consideram as zonas simuladas do HydroTech. Não use esses links como orientação de evacuação.</p>
        </template>
        <div v-if="zones.length && !serviceError" class="route-tools">
          <span>{{ zones.length }} ponto{{ zones.length === 1 ? '' : 's' }} de risco no mapa</span>
          <button type="button" class="refresh-button" :disabled="zonesLoading" @click="loadZones(true)">Atualizar pontos do HydroTech</button>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const route = useRoute()
const serviceUrl = (import.meta.env.VITE_ROTA_API_URL || 'http://127.0.0.1:8100').replace(/\/$/, '')
const alertaId = computed(() => {
  const value = String(route.query.alerta || '')
  return /^\d+(,\d+)*$/.test(value) ? value : ''
})
const mapElement = ref(null)
const zones = ref([])
const zonesLoading = ref(true)
const serviceError = ref('')
const routingStatus = ref('')
const error = ref('')
const busy = ref(false)
const autoRoutePending = ref(route.query.auto === '1' || (route.query.lat != null && route.query.lng != null))
const autoRouteMessage = computed(() => zonesLoading.value ? 'Preparando rota simulada...' : 'Calculando rota simulada...')
const mode = ref(route.query.modo === 'carro' ? 'carro' : 'pe')
const origin = ref(null)
const originSource = ref('')
const choosingOnMap = ref(false)
const result = ref(null)
let map
let zonesLayer
let routeLayer
let originMarker
let destinationMarker
let requestController
let poller
let disposed = false
let gpsRequestId = 0
let zonesRequestId = 0
let focusCorrected = false

function validCoords(lat, lng) {
  return Number.isFinite(lat) && Number.isFinite(lng) && lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180
}

const focusLat = Number(route.query.foco_lat)
const focusLng = Number(route.query.foco_lng)
const alertFocus = route.query.foco_lat != null && route.query.foco_lng != null && validCoords(focusLat, focusLng)
  ? { lat: focusLat, lng: focusLng }
  : null

function formatNumber(value) { return Number(value).toLocaleString('pt-BR', { maximumFractionDigits: 1 }) }
function formatDistance(meters) { return meters >= 1000 ? `${formatNumber(meters / 1000)} km` : `${Math.round(meters)} m` }
function formatDuration(seconds) { return seconds >= 3600 ? `${formatNumber(seconds / 3600)} h` : `${Math.max(1, Math.round(seconds / 60))} min` }

function popupFor(zone) {
  const content = document.createElement('div')
  const title = document.createElement('strong')
  const detail = document.createElement('div')
  title.textContent = zone.descricao || 'Ponto de risco simulado'
  detail.textContent = `${zone.rio || 'Rio não informado'} · raio ${zone.raio_m || 300} m`
  content.append(title, detail)
  return content
}

function showZones() {
  if (!map) return
  zonesLayer.clearLayers()
  const bounds = []
  let selectedPoint = null
  for (const zone of zones.value) {
    const lat = Number(zone.lat), lng = Number(zone.lng)
    if (!validCoords(lat, lng)) continue
    const selected = alertaId.value.split(',').includes(String(zone.id))
    if (selected && !selectedPoint) selectedPoint = [lat, lng]
    L.circle([lat, lng], {
      radius: Number(zone.raio_m) || 300, color: selected ? '#fda4af' : '#ef4444',
      weight: selected ? 3 : 2, fillColor: '#ef4444', fillOpacity: selected ? 0.34 : 0.2,
      bubblingMouseEvents: false,
    }).bindTooltip(popupFor(zone), { sticky: true })
      .on('click', event => setOrigin(event.latlng.lat, event.latlng.lng, 'mapa (área de risco)'))
      .addTo(zonesLayer)
    bounds.push([lat, lng])
  }
  if (!focusCorrected && selectedPoint && alertFocus && map.distance(selectedPoint, [alertFocus.lat, alertFocus.lng]) > 100) {
    focusCorrected = true
    if (originSource.value === 'simulação próxima ao risco') setOrigin(selectedPoint[0] + 0.0008, selectedPoint[1] + 0.0008, 'simulação próxima ao risco')
    else if (!origin.value) map.setView(selectedPoint, 15)
  }
  if (origin.value || alertFocus) return
  if (selectedPoint) map.setView(selectedPoint, 15)
  else if (bounds.length) map.fitBounds(bounds, { padding: [35, 35], maxZoom: 14 })
}

async function loadZones(force = false) {
  const requestId = ++zonesRequestId
  zonesLoading.value = true
  try {
    const response = await fetch(`${serviceUrl}/zonas-risco${force ? '?atualizar=1' : ''}`)
    if (!response.ok) {
      if (response.status === 502) throw new Error('O HydroTech não respondeu ao serviço de rotas. Confira se o backend está ativo e tente novamente.')
      throw new Error(`Não foi possível carregar os pontos de risco (erro ${response.status}). Tente novamente.`)
    }
    const data = await response.json()
    if (!Array.isArray(data)) throw new Error('Resposta inválida do serviço de rotas.')
    if (disposed || requestId !== zonesRequestId) return
    if (JSON.stringify(data) !== JSON.stringify(zones.value)) {
      const hadRoute = !!result.value
      if (requestController) autoRoutePending.value = false
      requestController?.abort()
      requestController = null
      busy.value = false
      clearRoute()
      if (hadRoute) error.value = 'Os pontos de risco mudaram. Recalcule a rota para considerar as áreas atualizadas.'
      zones.value = data
      showZones()
    }
    serviceError.value = ''
  } catch (cause) {
    if (disposed || requestId !== zonesRequestId) return
    serviceError.value = cause instanceof TypeError
      ? 'Serviço de rotas indisponível. Inicie o FastAPI na porta 8100 ou configure VITE_ROTA_API_URL.'
      : cause.message
  } finally { if (!disposed && requestId === zonesRequestId) zonesLoading.value = false }
}

async function loadStatus() {
  try {
    const response = await fetch(`${serviceUrl}/status`)
    if (!response.ok) return
    const data = await response.json()
    if (!disposed) routingStatus.value = data.desvio_de_zonas?.startsWith('openrouteservice')
      ? 'OpenRouteService configurado para tentar desviar das zonas.'
      : 'Sem chave OpenRouteService: o OSRM público pode fornecer rotas, mas não impõe desvio das zonas.'
  } catch { /* loadZones shows the connection error */ }
}

function clearRoute() {
  result.value = null
  routeLayer?.clearLayers()
  if (destinationMarker) { destinationMarker.remove(); destinationMarker = null }
}

function setOrigin(lat, lng, source) {
  if (disposed || !validCoords(lat, lng)) return
  gpsRequestId++
  if (requestController) autoRoutePending.value = false
  requestController?.abort()
  requestController = null
  busy.value = false
  error.value = ''
  origin.value = { lat, lng }
  originSource.value = source
  choosingOnMap.value = false
  clearRoute()
  if (originMarker) originMarker.setLatLng([lat, lng])
  else originMarker = L.circleMarker([lat, lng], { radius: 9, color: '#fff', weight: 2, fillColor: '#3b82f6', fillOpacity: 1, interactive: false }).addTo(map)
  map.setView([lat, lng], Math.max(map.getZoom(), 14))
}

function chooseOnMap() {
  if (!map || busy.value) return
  choosingOnMap.value = true
  mapElement.value?.scrollIntoView({ behavior: 'smooth', block: 'center' })
}

function simulateOrigin() {
  if (!zones.value.length || disposed) return
  const ids = alertaId.value.split(',')
  const zone = zones.value.find(item => ids.includes(String(item.id))) || zones.value[0]
  const lat = Number(zone.lat)
  const lng = Number(zone.lng)
  if (!validCoords(lat, lng)) {
    error.value = 'O ponto de risco não possui coordenadas válidas para a simulação.'
    return
  }
  setOrigin(lat + 0.0008, lng + 0.0008, 'simulação próxima ao risco')
}

function useGps() {
  if (zonesLoading.value || serviceError.value || !zones.value.length || disposed) return
  error.value = ''
  if (!navigator.geolocation) { error.value = 'GPS indisponível. Toque no mapa para simular a partida.'; return }
  const requestId = ++gpsRequestId
  busy.value = true
  navigator.geolocation.getCurrentPosition(
    position => {
      if (disposed || requestId !== gpsRequestId) return
      busy.value = false
      setOrigin(position.coords.latitude, position.coords.longitude, 'GPS')
    },
    () => {
      if (disposed || requestId !== gpsRequestId) return
      busy.value = false
      error.value = 'Não foi possível usar o GPS. Toque no mapa ou simule a partida no ponto de risco.'
    },
    { enableHighAccuracy: true, timeout: 12000, maximumAge: 30000 },
  )
}

function findRoute() {
  if (origin.value) calculateRoute()
}

function showRoute(data) {
  clearRoute()
  result.value = data
  const bounds = []
  if (origin.value) bounds.push([origin.value.lat, origin.value.lng])
  const destination = data.destino
  if (destination && validCoords(Number(destination.lat), Number(destination.lng))) {
    const point = [Number(destination.lat), Number(destination.lng)]
    destinationMarker = L.circleMarker(point, { radius: 10, color: '#fff', weight: 2, fillColor: '#a78bfa', fillOpacity: 1, interactive: false }).addTo(map)
    bounds.push(point)
  }
  const geometry = data.rota?.geometria
  if (geometry?.type === 'LineString' && Array.isArray(geometry.coordinates) && geometry.coordinates.length > 1) {
    L.geoJSON(geometry, { interactive: false, style: { color: data.rota?.zonas_cruzadas?.length ? '#f97316' : '#3b82f6', weight: 6, opacity: 0.9 } }).addTo(routeLayer)
    for (const coord of geometry.coordinates) if (validCoords(Number(coord[1]), Number(coord[0]))) bounds.push([Number(coord[1]), Number(coord[0])])
  }
  if (bounds.length > 1) map.fitBounds(bounds, { padding: [36, 36], maxZoom: 16 })
}

async function calculateRoute() {
  if (!origin.value || !zones.value.length || busy.value) return
  requestController?.abort()
  const controller = new AbortController()
  requestController = controller
  busy.value = true
  error.value = ''
  clearRoute()
  const params = new URLSearchParams({ lat: origin.value.lat, lng: origin.value.lng, modo: mode.value })
  if (alertaId.value) params.set('alerta', alertaId.value)
  try {
    const response = await fetch(`${serviceUrl}/rota-fuga?${params}`, { signal: controller.signal })
    let data
    try { data = await response.json() } catch { throw new Error('O serviço de rotas retornou uma resposta inválida.') }
    if (controller.signal.aborted || disposed) return
    if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Não foi possível calcular a rota.')
    if (!data.destino) throw new Error('O serviço não retornou um destino para a simulação.')
    showRoute(data)
  } catch (cause) {
    if (!disposed && cause.name !== 'AbortError') error.value = cause instanceof TypeError
      ? 'Falha de comunicação com o serviço de rotas. Confira se o FastAPI está ligado.' : cause.message
  } finally { if (requestController === controller) { requestController = null; busy.value = false; autoRoutePending.value = false } }
}

onMounted(async () => {
  await nextTick()
  const originLat = Number(route.query.lat), originLng = Number(route.query.lng)
  const urlOrigin = route.query.lat != null && route.query.lng != null && validCoords(originLat, originLng)
    ? { lat: originLat, lng: originLng }
    : null
  const initialPoint = urlOrigin || alertFocus
  map = L.map(mapElement.value).setView(initialPoint ? [initialPoint.lat, initialPoint.lng] : [-14.235, -51.925], initialPoint ? 15 : 4)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map)
  zonesLayer = L.layerGroup().addTo(map)
  routeLayer = L.layerGroup().addTo(map)
  if (alertFocus) L.circle([alertFocus.lat, alertFocus.lng], {
    radius: 300, color: '#fda4af', weight: 3, fillColor: '#ef4444', fillOpacity: 0.25, interactive: false,
  }).addTo(zonesLayer)
  map.on('click', event => setOrigin(event.latlng.lat, event.latlng.lng, 'mapa'))
  if (urlOrigin) setOrigin(urlOrigin.lat, urlOrigin.lng, 'simulação por URL')
  else if (route.query.auto === '1' && alertFocus) setOrigin(alertFocus.lat + 0.0008, alertFocus.lng + 0.0008, 'simulação próxima ao risco')
  void loadStatus()
  await loadZones(true)
  if (disposed) return
  if (!zones.value.length) autoRoutePending.value = false
  if (origin.value && zones.value.length) calculateRoute()
  else if (route.query.auto === '1' && zones.value.length) {
    simulateOrigin()
    calculateRoute()
  } else autoRoutePending.value = false
  poller = setInterval(() => loadZones(), 60000)
})

onUnmounted(() => {
  disposed = true
  requestController?.abort()
  if (poller) clearInterval(poller)
  map?.remove()
  map = null
})
</script>

<style scoped>
.escape-page { background: var(--bg-primary); color: var(--text-primary); min-height: 100vh; padding: 18px clamp(16px, 3vw, 40px) 28px; }
.escape-heading { display: flex; justify-content: space-between; align-items: flex-start; gap: 14px; max-width: 1380px; margin: 0 auto 16px; }
.escape-heading h1 { font-size: clamp(1.5rem, 2.5vw, 1.85rem); line-height: 1.2; margin: 3px 0 5px; }
.escape-heading p { color: var(--text-secondary); font-size: .86rem; margin: 0; }
.escape-heading .eyebrow { color: var(--accent); font-size: .72rem; font-weight: 800; text-transform: uppercase; letter-spacing: .12em; }
.return-link { display: inline-flex; align-items: center; justify-content: center; min-height: 42px; padding: 9px 16px; border: 1px solid var(--accent); border-radius: 9px; background: var(--accent); color: #fff; text-decoration: none; white-space: nowrap; font-size: .86rem; font-weight: 700; box-shadow: 0 3px 12px rgba(59, 130, 246, .22); transition: background .18s ease, border-color .18s ease, transform .18s ease; }
.return-link:hover { background: var(--accent-hover); border-color: var(--accent-hover); transform: translateY(-1px); }
.return-link:focus-visible { outline: 3px solid var(--accent); outline-offset: 3px; }
.escape-layout { display: grid; grid-template-columns: minmax(0, 1fr) 350px; gap: 16px; max-width: 1380px; margin: auto; }
.map-panel, .route-panel { border: 1px solid var(--border); border-radius: var(--radius-xl); background: var(--bg-card); overflow: hidden; }
.map-panel { position: relative; height: clamp(420px, 48vh, 540px); }
.escape-map { width: 100%; height: 100%; background: #102139; }
.escape-map--choosing { cursor: crosshair; }
.map-pick-hint { position: absolute; z-index: 500; top: 12px; left: 50%; transform: translateX(-50%); width: max-content; max-width: calc(100% - 24px); padding: 9px 12px; border: 1px solid var(--accent); border-radius: 8px; background: var(--bg-primary); color: var(--text-primary); font-size: .8rem; font-weight: 700; text-align: center; pointer-events: none; box-shadow: var(--shadow-md); }
.auto-route-progress { position: absolute; z-index: 510; top: 16px; left: 50%; transform: translateX(-50%); display: flex; align-items: center; gap: 11px; width: max-content; max-width: calc(100% - 32px); padding: 12px 15px; border: 1px solid var(--accent); border-radius: 11px; background: var(--bg-primary); color: var(--text-primary); box-shadow: var(--shadow-lg); pointer-events: none; }
.auto-route-progress > span:last-child { display: flex; flex-direction: column; gap: 3px; }
.auto-route-progress strong { font-size: .88rem; }
.auto-route-progress small { color: var(--text-secondary); font-size: .74rem; line-height: 1.3; }
.auto-route-spinner { width: 20px; height: 20px; flex: 0 0 20px; border: 3px solid var(--border-accent); border-top-color: var(--accent); border-radius: 50%; animation: route-loading-spin .8s linear infinite; }
@keyframes route-loading-spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { .auto-route-spinner { animation: none; border-top-color: var(--accent); } }
.map-legend { position: absolute; z-index: 500; left: 12px; bottom: 12px; background: rgba(9, 19, 31, .9); border: 1px solid var(--border); color: #fff; padding: 7px 10px; border-radius: 6px; font-size: .72rem; }
.legend-risk { display: inline-block; width: 11px; height: 11px; border-radius: 50%; background: #ef4444; margin-right: 5px; }
.route-panel { padding: 15px; align-self: start; display: flex; flex-direction: column; gap: 10px; }
.alert-banner { background: var(--emergency-soft); color: #fca5a5; padding: 8px 10px; border: 1px solid #ef4444; border-radius: 8px; font-weight: 700; }
.simulation-warning { display: flex; flex-direction: column; gap: 4px; padding: 10px 12px; border: 1px solid rgba(245, 158, 11, .55); border-radius: 8px; background: rgba(245, 158, 11, .12); color: #fbbf24; font-size: .8rem; line-height: 1.4; }
.simulation-warning strong { font-size: .84rem; }
[data-theme='light'] .simulation-warning { color: #78350f; }
.origin-help, .service-note, .external-note { color: var(--text-secondary); font-size: .8rem; }
.service-note { margin: 0; padding: 8px 10px; border-left: 3px solid var(--accent); background: var(--bg-elevated); line-height: 1.4; }
.refresh-button { align-self: flex-start; padding: 0; border: 0; background: none; color: #93c5fd; font-size: .78rem; cursor: pointer; }
.route-tools { display: flex; flex-direction: column; align-items: flex-start; gap: 5px; padding-top: 10px; border-top: 1px solid var(--border); color: var(--text-secondary); font-size: .78rem; }
.refresh-button:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }
.field-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; font-size: .83rem; }
.field-row select { background: var(--bg-elevated); color: var(--text-primary); border: 1px solid var(--border); border-radius: 6px; padding: 8px; }
.origin-section { display: flex; flex-direction: column; gap: 8px; padding: 12px; border: 1px solid var(--border); border-radius: 10px; background: var(--bg-secondary); }
.origin-section > strong { font-size: .86rem; }
.origin-help { margin: 0; line-height: 1.4; }
.origin-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.origin-actions button, .demo-button, .calculate-button { min-height: 44px; border-radius: 8px; padding: 9px 10px; font-size: .82rem; font-weight: 700; cursor: pointer; }
.origin-actions button:disabled, .demo-button:disabled, .calculate-button:disabled { opacity: .55; cursor: not-allowed; }
.secondary-button { border: 1px solid var(--border-accent); background: var(--bg-elevated); color: var(--text-primary); }
.secondary-button--active { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-soft); }
.demo-button { border: 1px dashed var(--border-accent); background: transparent; color: var(--text-secondary); }
.calculate-button { width: 100%; border: 0; background: var(--accent); color: #fff; }
.calculate-button:hover:not(:disabled) { background: var(--accent-hover); }
.origin-actions button:focus-visible, .demo-button:focus-visible, .calculate-button:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
.message { padding: 10px; border-radius: 8px; background: var(--bg-elevated); font-size: .8rem; }
.message.error, .message.danger { background: var(--emergency-soft); color: #fecaca; border: 1px solid rgba(239, 68, 68, .4); }
.service-error { display: flex; flex-direction: column; gap: 8px; }
.service-error .message { margin: 0; }
.retry-button { min-height: 44px; padding: 9px 12px; border: 1px solid var(--border-accent); border-radius: 8px; background: var(--bg-elevated); color: var(--text-primary); font-size: .82rem; font-weight: 700; cursor: pointer; }
.retry-button:disabled { opacity: .55; cursor: not-allowed; }
.retry-button:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
.route-assessment { display: flex; flex-direction: column; gap: 5px; padding: 11px 12px; border: 1px solid; border-radius: 8px; font-size: .8rem; line-height: 1.4; }
.route-assessment strong { font-size: .84rem; }
.route-assessment--danger { color: #fecaca; background: rgba(239, 68, 68, .16); border-color: #ef4444; }
.route-assessment--warning { color: #fbbf24; background: rgba(245, 158, 11, .13); border-color: #f59e0b; }
.route-assessment--info { color: var(--text-primary); background: var(--bg-elevated); border-color: var(--border-accent); }
[data-theme='light'] .route-assessment--danger { color: #991b1b; }
[data-theme='light'] .route-assessment--warning { color: #78350f; }
.destination-card { display: flex; flex-direction: column; gap: 5px; padding: 13px; border: 1px solid rgba(16, 185, 129, .45); border-radius: 8px; background: rgba(16, 185, 129, .08); font-size: .8rem; }
.destination-card strong { font-size: 1rem; }.card-label { color: #6ee7b7; font-weight: 700; }
.route-extra { color: var(--text-secondary); font-size: .78rem; line-height: 1.4; }
.metrics { display: flex; gap: 12px; }.metrics span { flex: 1; display: flex; flex-direction: column; padding: 10px; border-radius: 8px; background: var(--bg-elevated); font-size: .74rem; color: var(--text-secondary); }.metrics strong { color: var(--text-primary); font-size: 1rem; }
.warnings { padding-left: 20px; color: #fbbf24; font-size: .78rem; }.warnings li { margin: 4px 0; }
.steps { padding: 11px 12px; border: 1px solid var(--border-accent); border-radius: 8px; background: var(--bg-elevated); color: var(--text-primary); font-size: .82rem; }.steps summary { cursor: pointer; font-weight: 700; }.steps summary:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }.steps ol { padding-left: 20px; margin: 9px 0 0; max-height: 200px; overflow: auto; }.steps li { margin: 5px 0; }.steps span { color: var(--text-secondary); }
.external-links { display: flex; gap: 12px; }.external-links a { color: #93c5fd; font-size: .82rem; }
.external-note { margin: 0; padding: 9px 10px; border: 1px solid rgba(245, 158, 11, .4); border-radius: 8px; background: rgba(245, 158, 11, .08); line-height: 1.4; }
@media (max-width: 900px) { .escape-layout { grid-template-columns: 1fr; }.map-panel { height: min(52vh, 480px); min-height: 360px; }.escape-heading { align-items: flex-start; } }
@media (max-width: 520px) { .escape-heading { flex-direction: column; }.return-link { min-height: 44px; }.escape-page { padding: 14px 12px 24px; }.map-panel { height: min(46vh, 400px); min-height: 300px; }.origin-actions { grid-template-columns: 1fr; } }
</style>
