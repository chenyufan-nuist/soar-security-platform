<template>
  <div>
    <h2>⚙️ 剧本执行系统</h2>
    
    <div style="background: #f5f5f5; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
      <h3 style="margin-top: 0;">🎬 选择告警和剧本</h3>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
        <div>
          <label style="display: block; margin-bottom: 8px; font-weight: bold;">📌 选择告警:</label>
          <select v-model="selectedAlertId" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;">
            <option value="">-- 选择告警 --</option>
            <option v-for="alert in alerts" :key="alert.id" :value="alert.id">
              [{{ alert.type }}] {{ alert.ioc }} (ID: {{ alert.id }})
            </option>
          </select>
        </div>
        
        <div>
          <label style="display: block; margin-bottom: 8px; font-weight: bold;">📚 选择剧本:</label>
          <select v-model="selectedPlaybook" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;">
            <option value="">-- 选择剧本 --</option>
            <option v-for="playbook in playbooks" :key="playbook.id" :value="playbook.name">
              {{ playbook.name }} - {{ playbook.description }}
            </option>
          </select>
        </div>
      </div>

      <button @click="executePlaybook" :disabled="!selectedAlertId || !selectedPlaybook" style="padding: 12px 30px; background: selectedAlertId && selectedPlaybook ? '#667eea' : '#ccc'; color: white; border: none; border-radius: 4px; cursor: selectedAlertId && selectedPlaybook ? 'pointer' : 'not-allowed'; font-weight: bold; font-size: 16px;">
        🚀 执行剧本
      </button>
    </div>

    <div v-if="executionResult" style="background: #e8f5e9; border-left: 4px solid #4caf50; padding: 20px; border-radius: 4px; margin-top: 20px;">
      <h3 style="margin-top: 0; color: #2e7d32;">✅ 执行结果</h3>
      <div style="background: white; padding: 15px; border-radius: 4px; margin-top: 15px; max-height: 400px; overflow-y: auto;">
        <pre style="margin: 0;">{{ JSON.stringify(executionResult, null, 2) }}</pre>
      </div>
    </div>

    <div v-if="playbooks.length === 0" style="text-align: center; padding: 40px; color: #999;">
      <div style="font-size: 48px; margin-bottom: 10px;">⚠️</div>
      <p>暂无可用剧本</p>
    </div>

    <div v-if="playbooks.length > 0" style="margin-top: 30px;">
      <h3>📚 可用剧本列表</h3>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
        <div v-for="playbook in playbooks" :key="playbook.id" style="background: white; border: 1px solid #ddd; border-radius: 8px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
          <h4 style="margin-top: 0; color: #667eea;">{{ playbook.name }}</h4>
          <p style="color: #666; font-size: 14px; margin: 8px 0;">{{ playbook.description }}</p>
          <p style="color: #999; font-size: 12px; margin: 8px 0;"><strong>触发类型:</strong> {{ playbook.alert_type }}</p>
          <div style="background: #f5f5f5; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 12px; word-break: break-all; max-height: 150px; overflow-y: auto;">
            {{ formatPlaybookContent(playbook.content) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlaybookRunner',
  props: {
    alerts: Array,
    playbooks: Array
  },
  data() {
    return {
      selectedAlertId: '',
      selectedPlaybook: '',
      executionResult: null
    }
  },
  methods: {
    executePlaybook() {
      if (!this.selectedAlertId || !this.selectedPlaybook) {
        alert('请选择告警和剧本')
        return
      }
      this.$emit('execute', {
        alert_id: parseInt(this.selectedAlertId),
        playbook_name: this.selectedPlaybook
      })
    },
    formatPlaybookContent(content) {
      try {
        const obj = JSON.parse(content)
        return JSON.stringify(obj, null, 2).substring(0, 200) + '...'
      } catch {
        return content.substring(0, 200) + '...'
      }
    }
  }
}
</script>
