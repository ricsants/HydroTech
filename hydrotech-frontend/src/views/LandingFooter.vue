<template>
  <footer class="footer">
    <div class="footer-container">

      <div class="footer-top">
        <div class="footer-brand">
          <div class="footer-logo">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
            </svg>
          </div>
          <span class="footer-brand-text">HydroTech</span>
        </div>
        <p class="footer-desc">
          © {{ currentYear }} HydroTech Standardised Monitoring Authority Official
          Government Portal.
        </p>
      </div>

      <div class="footer-divider"></div>

      <div class="footer-bottom">
        <div class="footer-links">
        </div>
      </div>

    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
.footer {
  margin-top: auto;
  background: var(--nav-bg);
  border-top: 1px solid var(--border);
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px 24px;
}

.footer-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.footer-logo {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: var(--accent-gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.footer-brand-text {
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--text-primary);
}

.footer-desc {
  font-size: 0.78rem;
  color: var(--text-muted);
}

.footer-divider {
  height: 1px;
  background: var(--border);
  margin: 20px 0 16px;
}

.footer-bottom {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}

.footer-links a {
  font-size: 0.78rem;
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.2s;
}
.footer-links a:hover { color: var(--text-secondary); }

@media (max-width: 768px) {
  .footer-top { flex-direction: column; align-items: flex-start; }
  .footer-bottom { justify-content: flex-start; }
  .footer-links { flex-direction: column; gap: 10px; }
}
</style>