<template>
  <div class="playbook-view">
    <div class="header-actions">
      <h2>自动化编排引擎 (AUTOMATION ENGINE)</h2>
      <button class="cyber-btn" @click="$emit('refresh')">LOAD MODULES</button>
    </div>

    <div class="content-grid">
      <!-- Settings Panel -->
      <div class="cyber-panel">
        <h3>执行配置 (EXECUTION CONFIG)</h3>
        <div class="form-group">
          <label>Target Alert ID</label>
          <select v-model="selectedAlert" class="cyber-select">
            <option value="" disabled>Select Target</option>
            <option v-for="a in activeAlerts" :key="a.id" :value="a.id">[{{ a.id }}] {{ a.type }} - {{ a.ioc }}</option>
          </select>
        </div>

        <div class="form-group">
          <label>Playbook Module</label>
          <select v-model="selectedPlaybook" class="cyber-select">
            <option value="" disabled>Select Module</option>
            <option v-for="p in playbooks" :key="p.name" :value="p.name">{{ p.name }}</option>
          </select>
        </div>

        <div class="action-row">
          <button class="cyber-btn danger exec-btn" :disabled="!canExecute || executionState === 'running'" @click="runPlaybook">
            {{ execButtonText }}
          </button>
        </div>
        
        <div v-if="executionState === 'success'" class="alert-msg success-msg">
          [SUCCESS] Playbook executed and log appended.
        </div>
        <div v-if="executionState === 'failed'" class="alert-msg error-msg">
          [ERROR] Execution failed or timed out.
        </div>
      </div>

      <!-- Playbook Library -->
      <div class="cyber-panel library-panel">
        <h3>可用剧本库 (PLAYBOOK LIBRARY)</h3>
        <div class="pb-list">
          <div v-for="p in playbooks" :key="p.name" class="pb-item" :class="{'active-pb': selectedPlaybook === p.name}" @click="selectedPlaybook = p.name">
            <div class="pb-name">{{ p.name }}</div>
            <div class="pb-desc">{{ p.description || 'Automated response module.' }}</div>
            <div class="pb-meta">STATUS: <span class="neon-green">READY</span></div>
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
    alerts: { type: Array, default: () => [] },
    playbooks: { type: Array, default: () => [] },
    executionState: { type: String, default: null }
  },
  data() {
    return {
      selectedAlert: '',
      selectedPlaybook: ''
    }
  },
  computed: {
    activeAlerts() {
      return this.alerts.filter(a => a.status === 'open' || a.status === 'new')
    },
    canExecute() {
      return this.selectedAlert && this.selectedPlaybook
    },
    execButtonText() {
      if (this.executionState === 'running') return 'INITIALIZING SEQUENCE...'
      return 'AUTHORIZE DEPLOYMENT'
    }
  },
  methods: {
    runPlaybook() {
      this.$emit('execute', { alertId: this.selectedAlert, playbookName: this.selectedPlaybook })
    }
  }
}
</script>

<style scoped>
.playbook-view { display: flex; flex-direction: column; gap: 2rem; }
.header-actions { display: flex; justify-content: space-between; align-items: center; }

.content-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }

.form-group { display: flex; flex-direction: column; gap: 0.8rem; margin-bottom: 1.5rem; }
.form-group label { font-family: var(--font-tech); color: var(--neon-cyan); letter-spacing: 1px; font-size: 0.9rem; }

.cyber-select {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid var(--line-light);
  color: var(--text-main);
  padding: 0.8rem;
  border-radius: var(--radius-sm);
  font-family: var(--font-tech);
  font-size: 1rem;
  outline: none;
  transition: var(--transition);
}
.cyber-select:focus { border-color: var(--neon-cyan); box-shadow: var(--neon-cyan-glow); }
.cyber-select option { background: var(--bg-deep); border-bottom: 1px solid var(--line-light); }

.action-row { margin-top: 2rem; }
.exec-btn { width: 100%; padding: 1rem; font-size: 1.1rem; letter-spacing: 2px; }
.exec-btn:disabled { opacity: 0.5; cursor: not-allowed; border-color: gray; color: gray; box-shadow: none; text-shadow: none; background: transparent; }

.alert-msg { margin-top: 1rem; padding: 1rem; border: 1px dashed; font-family: var(--font-tech); letter-spacing: 1px; font-weight: 600; }
.success-msg { color: var(--neon-green); border-color: var(--neon-green); background: rgba(0,166,61,0.1); }
.error-msg { color: var(--neon-pink); border-color: var(--neon-pink); background: rgba(230,0,92,0.1); }

.pb-list { display: flex; flex-direction: column; gap: 1rem; margin-top: 1rem; }
.pb-item {
  border: 1px solid var(--line-light);
  padding: 1rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: var(--transition);
  background: rgba(0, 102, 238, 0.02);
}
.pb-item:hover, .pb-item.active-pb {
  border-color: var(--neon-cyan);
  background: rgba(0, 102, 238, 0.08);
  box-shadow: inset 0 0 10px rgba(0,102,238,0.1);
  transform: translateX(5px);
}

.pb-name { font-family: var(--font-tech); font-size: 1.1rem; color: var(--neon-cyan); margin-bottom: 0.5rem; text-transform: uppercase; }
.pb-desc { font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.8rem; }
.pb-meta { font-family: var(--font-tech); font-size: 0.8rem; letter-spacing: 1px; }
.neon-green { color: var(--neon-green); text-shadow: var(--neon-green-glow); }
</style>