<template>
  <div id="app" style="font-family: Arial, sans-serif; background: #f5f5f5; min-height: 100vh; padding: 20px;">
    <header style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
      <h1 style="margin: 0; font-size: 28px; font-weight: bold;">🛡️ SOAR 安全事件自动化响应平台</h1>
      <p style="margin: 10px 0 0 0; font-size: 14px; opacity: 0.9;">为中小企业提供轻量级安全事件自动化处置方案</p>
    </header>

    <nav style="display: flex; gap: 10px; margin-bottom: 30px; flex-wrap: wrap;">
      <button @click="currentTab = 'dashboard'" :style="getButtonStyle('dashboard')">📊 仪表盘</button>
      <button @click="currentTab = 'alerts'" :style="getButtonStyle('alerts')">🚨 告警列表</button>
      <button @click="currentTab = 'tickets'" :style="getButtonStyle('tickets')">📋 工单管理</button>
      <button @click="currentTab = 'playbook'" :style="getButtonStyle('playbook')">⚙️ 剧本执行</button>
    </nav>

    <div style="background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
      <Dashboard v-if="currentTab === 'dashboard'" :stats="stats" @refresh="fetchStats" />
      <AlertList v-if="currentTab === 'alerts'" :alerts="alerts" @refresh="fetchAlerts" @create-ticket="handleCreateTicket" />
      <TicketManagement v-if="currentTab === 'tickets'" :tickets="tickets" @refresh="fetchTickets" />
      <PlaybookRunner v-if="currentTab === 'playbook'" :alerts="alerts" :playbooks="playbooks" @execute="executePlaybook" @refresh="fetchAll" />
    </div>
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
  components: {
    Dashboard,
    AlertList,
    TicketManagement,
    PlaybookRunner
  },
  data() {
    return {
      currentTab: 'dashboard',
      stats: {},
      alerts: [],
      tickets: [],
      playbooks: [],
      baseURL: 'http://localhost:8000/api'
    }
  },
  mounted() {
    this.fetchAll()
    // 每 10 秒自动刷新
    setInterval(() => this.fetchAll(), 10000)
  },
  methods: {
    async fetchAll() {
      await this.fetchStats()
      await this.fetchAlerts()
      await this.fetchTickets()
      await this.fetchPlaybooks()
    },
    async fetchStats() {
      try {
        const response = await axios.get(`${this.baseURL}/alerts/stats`)
        this.stats = response.data
      } catch (e) {
        console.error('获取统计数据失败:', e)
      }
    },
    async fetchAlerts() {
      try {
        const response = await axios.get(`${this.baseURL}/alerts?limit=20`)
        this.alerts = response.data
      } catch (e) {
        console.error('获取告警列表失败:', e)
      }
    },
    async fetchTickets() {
      try {
        const response = await axios.get(`${this.baseURL}/tickets?limit=20`)
        this.tickets = response.data
      } catch (e) {
        console.error('获取工单列表失败:', e)
      }
    },
    async fetchPlaybooks() {
      try {
        const response = await axios.get(`${this.baseURL}/playbooks`)
        this.playbooks = response.data
      } catch (e) {
        console.error('获取剧本列表失败:', e)
      }
    },
    async handleCreateTicket(alertId) {
      try {
        await axios.post(`${this.baseURL}/ticket`, {
          alert_id: alertId,
          title: '手动创建工单',
          description: '通过前端界面手动创建'
        })
        this.fetchTickets()
      } catch (e) {
        alert('创建工单失败: ' + e.message)
      }
    },
    async executePlaybook(payload) {
      try {
        const response = await axios.post(`${this.baseURL}/playbook/run`, payload)
        alert('剧本执行成功！\n' + JSON.stringify(response.data, null, 2))
        this.fetchAll()
      } catch (e) {
        alert('剧本执行失败: ' + e.message)
      }
    },
    getButtonStyle(tab) {
      const baseStyle = {
        padding: '10px 20px',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '14px',
        fontWeight: 'bold',
        transition: 'all 0.3s'
      }
      if (this.currentTab === tab) {
        return { ...baseStyle, background: '#667eea', color: 'white' }
      }
      return { ...baseStyle, background: '#e0e0e0', color: '#333' }
    }
  }
}
</script>

<style scoped>
button:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}
</style>
