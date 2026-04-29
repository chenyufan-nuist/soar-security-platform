<template>
  <div class="ticket-view">
    <div class="header-actions">
      <h2>工单调度中心 (TICKET DISPATCH)</h2>
      <button class="cyber-btn" @click="('refresh')">FETCH TICKETS</button>
    </div>

    <div class="cyber-panel">
      <div class="table-container">
        <table class="cyber-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>PRIORITY</th>
              <th>TITLE/DESC</th>
              <th>STATUS</th>
              <th>TIME</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in tickets" :key="t.id">
              <td class="mono neon-cyan-text">T-{{ t.id }}</td>
              <td><span class="cyber-badge" :class="t.priority">{{ t.priority || 'medium' }}</span></td>
              <td>{{ t.title }}</td>
              <td><span class="cyber-badge" :class="getStatusClass(t.status)">{{ t.status.replace('_', ' ') }}</span></td>
              <td class="mono text-muted">{{ formatTime(t.created_at) }}</td>
            </tr>
            <tr v-if="!tickets.length">
              <td colspan="5" class="empty-row">NO TICKETS FOUND</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TicketManagement',
  props: { tickets: { type: Array, default: () => [] } },
  methods: {
    formatTime(str) {
      const d = new Date(str)
      return d.toLocaleTimeString('en-US', { hour12: false })
    },
    getStatusClass(s) {
      if (s === 'resolved' || s === 'closed') return 'safe'
      if (s === 'in_progress') return 'medium'
      return 'high'
    }
  }
}
</script>

<style scoped>
.ticket-view { display: flex; flex-direction: column; gap: 2rem; }
.header-actions { display: flex; justify-content: space-between; align-items: center; }

.table-container { overflow-x: auto; }
.cyber-table { width: 100%; border-collapse: collapse; text-align: left; }
.cyber-table th { font-family: var(--font-tech); font-size: 0.9rem; color: var(--neon-cyan); letter-spacing: 1px; padding: 1rem; border-bottom: 2px solid var(--line-glow); }
.cyber-table td { padding: 1rem; border-bottom: 1px solid var(--line-light); font-size: 0.95rem; }
.cyber-table tr:hover td { background: rgba(0, 102, 238, 0.05); }

.mono { font-family: monospace; }
.neon-cyan-text { color: var(--neon-cyan); }
.text-muted { color: var(--text-muted); }
.empty-row { text-align: center; padding: 3rem !important; font-family: var(--font-tech); letter-spacing: 2px; color: var(--text-muted); }
</style>

