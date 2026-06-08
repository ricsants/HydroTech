const fs = require('fs');
let code = fs.readFileSync('MonitoramentoView.vue', 'utf8');

const styleStart = code.indexOf('<style scoped>');

code = code.replace(
  '<div class="mon-page">',
  '<div class="mon-page">\n    <!-- Animated Gradient Background -->\n    <div class="mesh-bg">\n      <div class="mesh-blob blob-1"></div>\n      <div class="mesh-blob blob-2"></div>\n      <div class="mesh-blob blob-3"></div>\n    </div>'
);

const newStyle = `<style scoped>
.mon-page { min-height: 100vh; background: var(--bg-primary); color: var(--text-primary); display: flex; flex-direction: column; position: relative; overflow-x: hidden; }

/* Animated Gradient Mesh Background */
.mesh-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
  pointer-events: none;
}
.mesh-blob {
  position: absolute;
  filter: blur(120px);
  opacity: 0.25;
  animation: float 20s infinite alternate;
}
.blob-1 {
  top: -10%; left: -10%; width: 50vw; height: 50vw;
  background: radial-gradient(circle, rgba(14,165,233,0.3) 0%, rgba(14,165,233,0) 70%);
}
.blob-2 {
  bottom: -20%; right: -10%; width: 60vw; height: 60vw;
  background: radial-gradient(circle, rgba(56,189,248,0.2) 0%, rgba(56,189,248,0) 70%);
  animation-delay: -5s;
}
.blob-3 {
  top: 40%; left: 40%; width: 40vw; height: 40vw;
  background: radial-gradient(circle, rgba(2,132,199,0.2) 0%, rgba(2,132,199,0) 70%);
  animation-delay: -10s;
}

@keyframes float {
  0% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(5%, 10%) scale(1.1); }
  100% { transform: translate(-5%, -5%) scale(0.9); }
}

/* Topbar */
.mon-topbar { background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.05); padding: 0 24px; position: sticky; top: 0; z-index: 100; }
.mon-inner { max-width: 1300px; margin: 0 auto; position: relative; z-index: 2; }
.mon-inner.row { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
.mon-topbar .mon-inner { display: flex; align-items: center; justify-content: space-between; height: 58px; }
.mon-brand { display: flex; align-items: center; gap: 10px; font-size: 0.95rem; color: var(--text-secondary); }
.mon-brand b { color: var(--accent); }
.mon-meta { display: flex; align-items: center; gap: 14px; }
.live-pill { display: flex; align-items: center; gap: 6px; font-size: 0.7rem; font-weight: 800; color: #EF4444; background: rgba(239,68,68,0.1); padding: 4px 10px; border-radius: 20px; border: 1px solid rgba(239,68,68,0.2); letter-spacing: .5px; }
.live-dot { width: 7px; height: 7px; background: #EF4444; border-radius: 50%; animation: pulse 1.4s infinite; }
.upd-time { font-size: 0.75rem; color: var(--text-muted); }
.back-lnk { font-size: 0.8rem; color: var(--accent); text-decoration: none; font-weight: 600; }
.back-lnk:hover { opacity: .7; }

/* Filter bar */
.mon-filter-bar { background: rgba(15, 23, 42, 0.5); backdrop-filter: blur(10px); border-bottom: 1px solid rgba(255,255,255,0.05); padding: 10px 24px; position: relative; z-index: 2; }
.frow { display: flex; align-items: center; gap: 8px; color: var(--text-secondary); }
.f-sel { padding: 7px 12px; border-radius: var(--radius-md); border: 1px solid rgba(255,255,255,0.1); background: rgba(30, 41, 59, 0.6); color: var(--text-primary); font-size: 0.85rem; }
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
.rio-block { background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: var(--radius-xl); overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
.rio-hdr { display: flex; align-items: center; justify-content: space-between; padding: 16px 22px; flex-wrap: wrap; gap: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); }
.rio-hdr.risk--high { border-left: 4px solid var(--risk-high); }
.rio-hdr.risk--medium { border-left: 4px solid var(--risk-medium); }
.rio-hdr.risk--low { border-left: 4px solid var(--risk-low); }
.rio-hdr-l { display: flex; align-items: center; gap: 12px; }
.rio-icon { width: 42px; height: 42px; border-radius: var(--radius-lg); display: flex; align-items: center; justify-content: center; }
.rio-icon.risk--high { background: rgba(239, 68, 68, 0.1); color: var(--risk-high); }
.rio-icon.risk--medium { background: rgba(245, 158, 11, 0.1); color: var(--risk-medium); }
.rio-icon.risk--low { background: rgba(16,185,129,.12); color: var(--risk-low); }
.rio-name { font-size: 1.1rem; font-weight: 800; color: var(--text-primary); }
.rio-loc { font-size: 0.78rem; color: var(--text-muted); margin-top: 2px; }
.rio-hdr-r { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.risk-chip { font-size: 0.72rem; font-weight: 800; padding: 4px 12px; border-radius: 20px; }
.risk-chip.risk--high { background: rgba(239, 68, 68, 0.15); color: var(--risk-high); border: 1px solid rgba(239, 68, 68, 0.3); }
.risk-chip.risk--medium { background: rgba(245, 158, 11, 0.15); color: var(--risk-medium); border: 1px solid rgba(245, 158, 11, 0.3); }
.risk-chip.risk--low { background: rgba(16,185,129,.15); color: var(--risk-low); border: 1px solid rgba(16, 185, 129, 0.3); }
.abtn { display: flex; align-items: center; gap: 6px; padding: 7px 13px; border-radius: var(--radius-md); border: 1px solid rgba(255,255,255,0.1); background: rgba(30, 41, 59, 0.4); color: var(--text-muted); font-size: 0.78rem; font-weight: 600; cursor: pointer; transition: all .2s; backdrop-filter: blur(4px); }
.abtn:hover { border-color: var(--accent); color: var(--accent); background: rgba(30, 41, 59, 0.8); }
.abtn--fav { color: #F59E0B; border-color: #F59E0B; background: rgba(245,158,11,.08); }
.abtn--alr { color: var(--accent); border-color: var(--accent); background: rgba(56, 189, 248, 0.1); }

/* Charts area */
.charts-wrap { padding: 20px 22px; }
.charts-loading, .charts-empty { color: var(--text-muted); font-size: 0.85rem; text-align: center; padding: 20px; }
.charts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(480px, 1fr)); gap: 20px; }

/* Chart Card — Glassmorphism */
.chart-card { background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255,255,255,0.05); border-radius: var(--radius-xl); overflow: hidden; backdrop-filter: blur(10px); }
.chart-card-hdr { display: flex; align-items: flex-start; justify-content: space-between; padding: 18px 22px; border-bottom: 1px solid rgba(255,255,255,0.05); gap: 10px; }
.chart-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 700; color: var(--text-primary); }
.chart-card-sub { display: flex; align-items: center; flex-wrap: wrap; gap: 4px; font-size: 0.78rem; color: var(--text-muted); margin-top: 5px; }
.nlv--alto { color: #EF4444; font-weight: 700; }
.nlv--medio { color: #F59E0B; font-weight: 700; }
.nlv--baixo { color: #10B981; font-weight: 700; }
.live-badge { display: flex; align-items: center; gap: 5px; font-size: 0.7rem; font-weight: 800; color: #EF4444; background: rgba(239,68,68,.1); padding: 4px 9px; border-radius: 8px; border: 1px solid rgba(239,68,68,.2); flex-shrink: 0; }
.chart-canvas-wrap { height: 300px; padding: 18px 20px; }

.mon-footer { background: rgba(15, 23, 42, 0.5); backdrop-filter: blur(10px); border-top: 1px solid rgba(255,255,255,0.05); padding: 14px 24px; text-align: center; font-size: 0.73rem; color: var(--text-muted); position: relative; z-index: 2; }

@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.4;transform:scale(1.4)} }
.spin { animation: spin .8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 900px) { .charts-grid { grid-template-columns: 1fr; } }
@media (max-width: 600px) { .upd-time { display: none; } .rio-hdr { flex-direction: column; } }
</style>`;

code = code.substring(0, styleStart) + newStyle;
fs.writeFileSync('MonitoramentoView.vue', code);
