<template>
  <div>
    <h2>🚨 安全告警列表</h2>
    <button @click="$emit('refresh')" style="margin-bottom: 20px; padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">🔄 刷新告警</button>
    
    <div v-if="alerts.length === 0" style="text-align: center; padding: 40px; color: #999;">
      <div style="font-size: 48px; margin-bottom: 10px;">✨</div>
      <p>暂无告警，系统运行正常</p>
    </div>

    <div v-else>
      <table style="width: 100%; border-collapse: collapse;">
        <thead>
          <tr style="background: #f5f5f5; border-bottom: 2px solid #ddd;">
            <th style="padding: 12px; text-align: left;">🆔 ID</th>
            <th style="padding: 12px; text-align: left;">📌 类型</th>
            <th style="padding: 12px; text-align: left;">🎯 IOC</th>
            <th style="padding: 12px; text-align: left;">👤 用户/主机</th>
            <th style="padding: 12px; text-align: left;">⚠️ 严重级别</th>
            <th style="padding: 12px; text-align: left;">📊 状态</th>
            <th style="padding: 12px; text-align: left;">🕐 时间</th>
            <th style="padding: 12px; text-align: center;">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="alert in alerts" :key="alert.id" style="border-bottom: 1px solid #eee; hover: { background: '#f9f9f9' }">
            <td style="padding: 12px;">{{ alert.id }}</td>
            <td style="padding: 12px;">{{ formatType(alert.type) }}</td>
            <td style="padding: 12px; font-family: monospace; font-size: 12px; word-break: break-all;">{{ alert.ioc }}</td>
            <td style="padding: 12px;">{{ alert.user || alert.host || '-' }}</td>
            <td style="padding: 12px;">
              <span :style="getSeverityStyle(alert.severity)">{{ formatSeverity(alert.severity) }}</span>
            </td>
            <td style="padding: 12px;">
              <span :style="getStatusStyle(alert.status)">{{ formatStatus(alert.status) }}</span>
            </td>
            <td style="padding: 12px; font-size: 12px;">{{ formatTime(alert.created_at) }}</td>
            <td style="padding: 12px; text-align: center;">
              <button @click="$emit('create-ticket', alert.id)" style="padding: 4px 8px; background: #667eea; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 12px;">创建工单</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AlertList',
  props: {
    alerts: Array
  },
  methods: {
    formatType(type) {
      const typeMap = {
        'phishing': '🎣 钓鱼',
        'ransomware': '🔒 勒索',
        'malware': '🦠 恶意软件',
        'suspicious_ip': '❌ 可疑IP'
      }
      return typeMap[type] || type
    },
    formatSeverity(severity) {
      const severityMap = {
        'low': '🟢 低',
        'medium': '🟡 中',
        'high': '🟠 高',
        'critical': '🔴 严重'
      }
      return severityMap[severity] || severity
    },
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
    getSeverityStyle(severity) {
      const styles = {
        'low': { background: '#d4edda', color: '#155724', padding: '4px 8px', borderRadius: '3px', fontSize: '12px' },
        'medium': { background: '#fff3cd', color: '#856404', padding: '4px 8px', borderRadius: '3px', fontSize: '12px' },
        'high': { background: '#ffe5cc', color: '#cc5200', padding: '4px 8px', borderRadius: '3px', fontSize: '12px' },
        'critical': { background: '#f8d7da', color: '#721c24', padding: '4px 8px', borderRadius: '3px', fontSize: '12px', fontWeight: 'bold' }
      }
      return styles[severity] || {}
    },
    getStatusStyle(status) {
      const styles = {
        'open': { background: '#ff6b6b', color: 'white', padding: '4px 8px', borderRadius: '3px', fontSize: '12px' },
        'in_progress': { background: '#4ecdc4', color: 'white', padding: '4px 8px', borderRadius: '3px', fontSize: '12px' },
        'resolved': { background: '#51cf66', color: 'white', padding: '4px 8px', borderRadius: '3px', fontSize: '12px' },
        'closed': { background: '#a9a9a9', color: 'white', padding: '4px 8px', borderRadius: '3px', fontSize: '12px' }
      }
      return styles[status] || {}
    }
  }
}
</script>
