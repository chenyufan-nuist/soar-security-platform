<template>
  <div>
    <h2>📋 工单管理系统</h2>
    <button @click="$emit('refresh')" style="margin-bottom: 20px; padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">🔄 刷新工单</button>
    
    <div v-if="tickets.length === 0" style="text-align: center; padding: 40px; color: #999;">
      <div style="font-size: 48px; margin-bottom: 10px;">📭</div>
      <p>暂无工单</p>
    </div>

    <div v-else>
      <table style="width: 100%; border-collapse: collapse;">
        <thead>
          <tr style="background: #f5f5f5; border-bottom: 2px solid #ddd;">
            <th style="padding: 12px; text-align: left;">🆔 工单ID</th>
            <th style="padding: 12px; text-align: left;">📝 标题</th>
            <th style="padding: 12px; text-align: left;">👤 负责人</th>
            <th style="padding: 12px; text-align: left;">📊 状态</th>
            <th style="padding: 12px; text-align: left;">🕐 创建时间</th>
            <th style="padding: 12px; text-align: center;">📄 详情</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ticket in tickets" :key="ticket.id" style="border-bottom: 1px solid #eee;">
            <td style="padding: 12px;">{{ ticket.id }}</td>
            <td style="padding: 12px;">{{ ticket.title }}</td>
            <td style="padding: 12px;">{{ ticket.assignee || '-' }}</td>
            <td style="padding: 12px;">
              <span :style="getStatusStyle(ticket.status)">{{ formatStatus(ticket.status) }}</span>
            </td>
            <td style="padding: 12px; font-size: 12px;">{{ formatTime(ticket.created_at) }}</td>
            <td style="padding: 12px; text-align: center;">
              <button @click="showDetail(ticket)" style="padding: 4px 8px; background: #4ecdc4; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 12px;">查看</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="selectedTicket" style="margin-top: 30px; background: #f9f9f9; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea;">
        <h3 style="margin-top: 0;">📄 工单详情</h3>
        <p><strong>标题:</strong> {{ selectedTicket.title }}</p>
        <p><strong>描述:</strong> {{ selectedTicket.description }}</p>
        <p><strong>负责人:</strong> {{ selectedTicket.assignee || '-' }}</p>
        <p><strong>状态:</strong> {{ formatStatus(selectedTicket.status) }}</p>
        
        <div v-if="selectedTicket.actions" style="margin-top: 15px;">
          <h4>📋 执行的动作:</h4>
          <pre style="background: white; padding: 10px; border-radius: 4px; border: 1px solid #ddd; overflow-x: auto;">{{ formatJSON(selectedTicket.actions) }}</pre>
        </div>
        
        <div v-if="selectedTicket.report" style="margin-top: 15px;">
          <h4>📄 处置报告:</h4>
          <pre style="background: white; padding: 10px; border-radius: 4px; border: 1px solid #ddd; overflow-x: auto; max-height: 300px; overflow-y: auto;">{{ formatJSON(selectedTicket.report) }}</pre>
        </div>
        
        <button @click="selectedTicket = null" style="margin-top: 15px; padding: 8px 16px; background: #999; color: white; border: none; border-radius: 4px; cursor: pointer;">关闭</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TicketManagement',
  props: {
    tickets: Array
  },
  data() {
    return {
      selectedTicket: null
    }
  },
  methods: {
    formatStatus(status) {
      const statusMap = {
        'open': '❌ 未处理',
        'in_progress': '⏳ 处理中',
        'resolved': '✅ 已解决',
        'closed': '🔒 已关闭'
      }
      return statusMap[status] || status
    },
    formatTime(timestamp) {
      const date = new Date(timestamp)
      return date.toLocaleString('zh-CN')
    },
    getStatusStyle(status) {
      const styles = {
        'open': { background: '#ff6b6b', color: 'white', padding: '4px 8px', borderRadius: '3px', fontSize: '12px' },
        'in_progress': { background: '#4ecdc4', color: 'white', padding: '4px 8px', borderRadius: '3px', fontSize: '12px' },
        'resolved': { background: '#51cf66', color: 'white', padding: '4px 8px', borderRadius: '3px', fontSize: '12px' },
        'closed': { background: '#a9a9a9', color: 'white', padding: '4px 8px', borderRadius: '3px', fontSize: '12px' }
      }
      return styles[status] || {}
    },
    showDetail(ticket) {
      this.selectedTicket = ticket
    },
    formatJSON(jsonString) {
      try {
        return JSON.stringify(JSON.parse(jsonString), null, 2)
      } catch {
        return jsonString
      }
    }
  }
}
</script>
