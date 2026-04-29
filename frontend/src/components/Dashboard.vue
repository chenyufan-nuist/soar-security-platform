<template>
  <div class="dashboard-view">
    <div class="header-actions">
      <h2>GLOBAL态势感知 (GLOBAL VIEW)</h2>
      <button class="cyber-btn" @click="('refresh')">SCAN / REFRESH</button>
    </div>

    <!-- Top Stats Row -->
    <div class="stats-grid">
      <div class="cyber-panel stat-card">
        <div class="stat-title">总事件监控 (TOTAL EVENTS)</div>
        <div class="stat-value neon-cyan">{{ stats.total || 0 }}</div>
      </div>
      <div class="cyber-panel stat-card">
        <div class="stat-title">待处理告警 (OPEN ALERTS)</div>
        <div class="stat-value neon-pink">{{ stats.open || 0 }}</div>
      </div>
      <div class="cyber-panel stat-card">
        <div class="stat-title">已闭环事件 (RESOLVED)</div>
        <div class="stat-value neon-green">{{ stats.resolved || 0 }}</div>
      </div>
      <div class="cyber-panel stat-card">
        <div class="stat-title">系统负载 (Sys LOAD)</div>
        <div class="stat-value neon-yellow">24%</div>
      </div>
    </div>

    <!-- Main Dashboard Grid -->
    <div class="main-grid">
      <!-- Left Column: Attack Types -->
      <div class="cyber-panel chart-panel">
        <h3>威胁聚类分析 (THREAT CLUSTERS)</h3>
        <div v-if="typeEntries.length" class="bar-chart">
          <div v-for="entry in typeEntries" :key="entry.type" class="bar-row">
            <div class="bar-label">{{ entry.type.toUpperCase() }}</div>
            <div class="bar-track">
              <div class="bar-fill" :style="{ width: entry.percent + '%' }"></div>
            </div>
            <div class="bar-val">{{ entry.count }}</div>
          </div>
        </div>
        <div v-else class="empty-box">NO DATA FOUND</div>
      </div>

      <!-- Right Column: Live Feed -->
      <div class="cyber-panel feed-panel">
        <h3>实时情报串流 (LIVE TICKET FEED)</h3>
        <div v-if="recentTickets.length" class="feed-list">
          <div v-for="ticket in recentTickets" :key="ticket.id" class="feed-item">
            <div class="feed-time">{{ formatTime(ticket.created_at) }}</div>
            <div class="feed-main">
              <div class="feed-id neon-cyan-text">[TICKET-{{ ticket.id }}]</div>
              <div class="feed-desc">{{ ticket.title }}</div>
            </div>
            <div class="feed-status">
              <span class="cyber-badge" :class="getStatusClass(ticket.status)">{{ ticket.status }}</span>
            </div>
          </div>
        </div>
        <div v-else class="empty-box">NO LIVE FEED</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  props: {
    stats: { type: Object, default: () => ({}) },
    alerts: { type: Array, default: () => [] },
    tickets: { type: Array, default: () => [] }
  },
  computed: {
    recentTickets() {
      return this.tickets.slice(0, 6)
    },
    typeEntries() {
      const byType = this.stats.by_type || {}
      const total = Object.values(byType).reduce((a, b) => a + b, 0)
      return Object.entries(byType).map(([type, count]) => ({
        type, count, percent: total ? Math.round((count / total) * 100) : 0
      })).sort((a,b) => b.count - a.count)
    }
  },
  methods: {
    formatTime(str) {
      if (!str) return 'UNKNOWN'
      const d = new Date(str)
      return d.toLocaleTimeString('en-US', { hour12: false })
    },
    getStatusClass(status) {
      const s = status ? status.toLowerCase() : ''
      if (s === 'resolved' || s === 'closed') return 'safe'
      if (s === 'in_progress') return 'medium'
      return 'high'
    }
  }
}
</script>

<style scoped>
.dashboard-view {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.stat-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 2rem;
}

.stat-title {
  font-family: var(--font-tech);
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
  letter-spacing: 1px;
}

.stat-value {
  font-family: var(--font-tech);
  font-size: 3.5rem;
  font-weight: 700;
  text-shadow: 0 0 10px currentColor;
}

.neon-cyan { color: var(--neon-cyan); }
.neon-pink { color: var(--neon-pink); }
.neon-green { color: var(--neon-green); }
.neon-yellow { color: var(--neon-yellow); }
.neon-cyan-text { color: var(--neon-cyan); }

.main-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  margin-top: 1.5rem;
}

.bar-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.bar-label {
  width: 120px;
  font-family: var(--font-tech);
  font-size: 0.9rem;
}

.bar-track {
  flex: 1;
  height: 8px;
  background: rgba(0,0,0,0.05);
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: var(--neon-cyan);
  box-shadow: var(--neon-cyan-glow);
  transition: width 1s ease-out;
}

.bar-val {
  width: 40px;
  text-align: right;
  font-family: var(--font-tech);
  font-weight: 700;
  color: var(--neon-cyan);
}

.feed-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.5rem;
}

.feed-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(0, 102, 238, 0.03);
  border-left: 2px solid var(--neon-cyan);
  border-radius: 0 4px 4px 0;
  transition: var(--transition);
}

.feed-item:hover {
  background: rgba(0, 102, 238, 0.08);
  transform: translateX(5px);
}

.feed-time {
  font-family: var(--font-tech);
  color: var(--text-muted);
  font-size: 0.85rem;
}

.feed-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.feed-id {
  font-family: var(--font-tech);
  font-size: 0.9rem;
  letter-spacing: 1px;
}

.feed-desc {
  font-size: 0.95rem;
}

.empty-box {
  padding: 3rem;
  text-align: center;
  font-family: var(--font-tech);
  color: var(--text-muted);
  letter-spacing: 3px;
  border: 1px dashed rgba(0,0,0,0.1);
  margin-top: 1.5rem;
}
</style>

