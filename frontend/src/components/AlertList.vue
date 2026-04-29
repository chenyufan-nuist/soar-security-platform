<template>
  <div class="alert-view">
    <div class="header-actions">
      <h2>告警流监控 (THREAT ALERTS)</h2>
      <button class="cyber-btn" @click="('refresh')">SYNC STREAM</button>
    </div>

    <div class="cyber-panel">
      <div class="table-container">
        <table class="cyber-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>TYPE</th>
              <th>SEVERITY</th>
              <th>INDICATOR (IOC)</th>
              <th>TIME</th>
              <th>ACTION</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="alert in alerts" :key="alert.id">
              <td class="mono neon-cyan-text">#{{ alert.id }}</td>
              <td>{{ alert.type.toUpperCase() }}</td>
              <td>
                <span class="cyber-badge" :class="getSeverityClass(alert.severity)">{{ alert.severity }}</span>
              </td>
              <td class="mono">{{ alert.ioc }}</td>
              <td class="mono text-muted">{{ formatTime(alert.created_at) }}</td>
              <td>
                <button class="cyber-btn" style="font-size:0.75rem; padding:0.4rem 0.8rem" @click="('create-ticket', alert.id)">DISPATCH TICKET</button>
              </td>
            </tr>
            <tr v-if="!alerts.length">
              <td colspan="6" class="empty-row">SYSTEM CLEAR - NO ACTIVE ALERTS</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AlertList',
  props: { alerts: { type: Array, default: () => [] } },
  methods: {
    formatTime(str) {
      const d = new Date(str)
      return d.toLocaleTimeString('en-US', { hour12: false })
    },
    getSeverityClass(sev) {
      if (sev === 'high' || sev === 'critical') return 'high'
      if (sev === 'medium') return 'medium'
      return 'low'
    }
  }
}
</script>

<style scoped>
.alert-view { display: flex; flex-direction: column; gap: 2rem; }
.header-actions { display: flex; justify-content: space-between; align-items: center; }

.table-container { overflow-x: auto; }
.cyber-table {
  width: 100%; border-collapse: collapse; text-align: left;
}
.cyber-table th {
  font-family: var(--font-tech); font-size: 0.9rem; color: var(--neon-cyan); letter-spacing: 1px;
  padding: 1rem; border-bottom: 2px solid var(--line-glow);
}
.cyber-table td { padding: 1rem; border-bottom: 1px solid var(--line-light); font-size: 0.95rem; }
.cyber-table tr:hover td { background: rgba(0, 102, 238, 0.05); }

.mono { font-family: monospace; }
.neon-cyan-text { color: var(--neon-cyan); }
.text-muted { color: var(--text-muted); }
.empty-row { text-align: center; padding: 3rem !important; font-family: var(--font-tech); letter-spacing: 2px; color: var(--neon-green); }
</style>

