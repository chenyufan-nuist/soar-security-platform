<template>
  <div>
    <h2>📊 系统仪表盘</h2>
    <button @click="$emit('refresh')" style="margin-bottom: 20px; padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">🔄 刷新统计</button>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px;">
      <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <div style="font-size: 12px; opacity: 0.9;">📈 告警总数</div>
        <div style="font-size: 32px; font-weight: bold; margin-top: 10px;">{{ stats.total || 0 }}</div>
      </div>
      
      <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <div style="font-size: 12px; opacity: 0.9;">🔴 未处理</div>
        <div style="font-size: 32px; font-weight: bold; margin-top: 10px;">{{ stats.open || 0 }}</div>
      </div>
      
      <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <div style="font-size: 12px; opacity: 0.9;">✅ 已解决</div>
        <div style="font-size: 32px; font-weight: bold; margin-top: 10px;">{{ stats.resolved || 0 }}</div>
      </div>
    </div>

    <h3>按类型统计</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px;">
      <div v-for="(count, type) in stats.by_type" :key="type" style="background: #f0f0f0; padding: 15px; border-radius: 4px; border-left: 4px solid #667eea;">
        <div style="font-size: 12px; color: #666;">{{ formatType(type) }}</div>
        <div style="font-size: 24px; font-weight: bold; color: #667eea; margin-top: 8px;">{{ count }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  props: {
    stats: Object
  },
  methods: {
    formatType(type) {
      const typeMap = {
        'phishing': '🎣 钓鱼邮件',
        'ransomware': '🔒 勒索软件',
        'malware': '🦠 恶意软件',
        'suspicious_ip': '❌ 可疑 IP'
      }
      return typeMap[type] || type
    }
  }
}
</script>
