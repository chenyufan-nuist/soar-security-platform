<template>
  <div class="app-container">
    <div class="scanline"></div>
    <header class="top-bar">
      <div class="brand">
        <div class="brand-icon anim-pulse">⬢</div>
        <div class="brand-text">
          <span class="brand-title">SOAR SYSTEM</span>
          <span class="brand-subtitle">Security Operations & Automated Response</span>
        </div>
      </div>

      <nav class="nav-tabs">
        <button 
          v-for="item in navItems" 
          :key="item.key" 
          class="nav-tab" 
          :class="{ active: currentTab === item.key }"
          @click="currentTab = item.key"
        >
          {{ item.label }}
        </button>
      </nav>

      <div class="system-status">
        <div class="status-indicator">
          <span class="status-dot safe anim-pulse"></span>
          <span class="status-text">SYSTEM ONLINE</span>
        </div>
      </div>
    </header>

    <main class="main-content">
      <Dashboard v-if="currentTab === 'dashboard'" :stats="stats" :alerts="alerts" :tickets="tickets" @refresh="fetchAll" />
      <AlertList v-else-if="currentTab === 'alerts'" :alerts="alerts" @refresh="fetchAlerts" @create-ticket="handleCreateTicket" />
      <TicketManagement v-else-if="currentTab === 'tickets'" :tickets="tickets" @refresh="fetchTickets" />
      <PlaybookRunner v-else :alerts="alerts" :playbooks="playbooks" :execution-state="executionState" @execute="executePlaybook" @refresh="fetchAll" />
    </main>
  </div>
</template>

<script>
import axios from 'axios'
import Dashboard from './components/Dashboard.vue'
import AlertList from './components/AlertList.vue'
import TicketManagement from './components/TicketManagement.vue'
import PlaybookRunner from './components/PlaybookRunner.vue'

export default {
  name: 'App',
  components: { Dashboard, AlertList, TicketManagement, PlaybookRunner },
  data() {
    return {
      currentTab: 'dashboard',
      stats: {},
      alerts: [],
      tickets: [],
      playbooks: [],
      executionState: null,
      baseURL: 'http://localhost:8000/api',
      navItems: [
        { key: 'dashboard', label: 'Global View' },
        { key: 'alerts', label: 'Threat Alerts' },
        { key: 'tickets', label: 'Dispatch Center' },
        { key: 'playbook', label: 'Automation Engine' }
      ]
    }
  },
  methods: {
    async fetchAll() {
      this.fetchStats()
      this.fetchAlerts()
      this.fetchTickets()
      this.fetchPlaybooks()
    },
    async fetchStats() {
      try {
        const res = await axios.get(`${this.baseURL}/alerts/stats`)
        this.stats = res.data
      } catch (err) { console.error('Fetch Stats failed', err) }
    },
    async fetchAlerts() {
      try {
        const res = await axios.get(`${this.baseURL}/alerts`)
        this.alerts = res.data
      } catch (err) { console.error('Fetch Alerts failed', err) }
    },
    async fetchTickets() {
      try {
        const res = await axios.get(`${this.baseURL}/tickets`)
        this.tickets = res.data
      } catch (err) { console.error('Fetch Tickets failed', err) }
    },
    async fetchPlaybooks() {
      try {
        const res = await axios.get(`${this.baseURL}/playbooks`)
        this.playbooks = res.data.playbooks || []
      } catch (err) {
        // Mock if not implemented in backend
        this.playbooks = [
          { name: 'phishing_response', description: 'Analyze URL and block sender' },
          { name: 'ransomware_quarantine', description: 'Isolate host and create ticket' }
        ]
      }
    },
    async handleCreateTicket(alertId) {
      if (!alertId) return
      try {
        await axios.post(`${this.baseURL}/ticket`, { alert_id: alertId })
        this.fetchTickets()
        this.fetchAlerts()
      } catch (err) { console.error('Create Ticket failed', err) }
    },
    async executePlaybook({ alertId, playbookName }) {
      try {
        this.executionState = 'running'
        const res = await axios.post(`${this.baseURL}/playbook/run`, {
          alert_id: alertId,
          playbook_name: playbookName
        })
        setTimeout(() => {
          this.executionState = 'success'
          this.fetchAll()
          setTimeout(() => { this.executionState = null }, 3000)
        }, 1500)
      } catch (err) {
        this.executionState = 'failed'
        setTimeout(() => { this.executionState = null }, 3000)
      }
    }
  },
  mounted() {
    this.fetchAll()
    setInterval(this.fetchAll, 15000)
  }
}
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.85);
  border-bottom: 1px solid var(--line-light);
  backdrop-filter: blur(10px);
  z-index: 100;
}

.brand { display: flex; align-items: center; gap: 1rem; }
.brand-icon { font-family: var(--font-tech); font-size: 2.5rem; font-weight: 700; color: var(--neon-cyan); text-shadow: var(--neon-cyan-glow); }
.brand-text { display: flex; flex-direction: column; }
.brand-title { font-family: var(--font-tech); font-size: 1.5rem; font-weight: 700; color: var(--text-main); letter-spacing: 2px; }
.brand-subtitle { font-size: 0.8rem; color: var(--neon-cyan); text-transform: uppercase; letter-spacing: 1px; }

.nav-tabs { display: flex; gap: 2rem; }
.nav-tab {
  background: none; border: none; color: var(--text-muted);
  font-family: var(--font-tech); font-size: 1.1rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;
  padding: 0.5rem 1rem; cursor: pointer; transition: var(--transition); position: relative;
}
.nav-tab::after {
  content: ''; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
  width: 0; height: 2px; background: var(--neon-cyan); transition: var(--transition);
  box-shadow: var(--neon-cyan-glow);
}
.nav-tab:hover { color: var(--text-main); }
.nav-tab.active { color: var(--neon-cyan); text-shadow: var(--neon-cyan-glow); }
.nav-tab.active::after { width: 100%; }

.system-status { display: flex; align-items: center; }
.status-indicator {
  display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem;
  background: rgba(0, 166, 61, 0.05); border: 1px solid rgba(0, 166, 61, 0.3); border-radius: 20px;
}
.status-dot { width: 8px; height: 8px; border-radius: 50%; }
.status-dot.safe { background: var(--neon-green); box-shadow: var(--neon-green-glow); }
.status-text { font-family: var(--font-tech); font-size: 0.9rem; color: var(--neon-green); font-weight: 600; letter-spacing: 1px; }

.main-content {
  flex: 1; padding: 2rem; overflow-y: auto;
}
</style>

