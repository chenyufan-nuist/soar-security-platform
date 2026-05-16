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

    <!-- Execution Result Modal -->
    <div v-if="executionState === 'success' && executionResult" class="modal-overlay">
      <div class="modal-content cyber-panel">
        <h3>⚡ 执行结果 (EXECUTION REPORT)</h3>
        <div class="result-list">
          <div v-for="(action, index) in executionResult" :key="index" class="result-item" :class="action.status">
            <div class="result-header">
              <span class="step-num">STEP {{ index + 1 }}</span>
              <span class="action-name">{{ action.action }}</span>
              <span class="status-badge">{{ action.status.toUpperCase() }}</span>
            </div>
            <div class="result-msg">> {{ action.message }}</div>
          </div>
        </div>
        <div class="modal-actions">
          <button class="cyber-btn" @click="$emit('close-result')">ACKNOWLEDGE & CLOSE</button>
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
    executionState: { type: String, default: null },
    executionResult: { type: Array, default: () => [] }
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

/* Modal Styles */
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 5, 15, 0.85); backdrop-filter: blur(5px);
  display: flex; justify-content: center; align-items: center; z-index: 1000;
}
.modal-content {
  width: 600px; max-width: 90vw; background: rgba(0, 15, 30, 0.95) !important;
  border: 1px solid var(--neon-cyan); box-shadow: 0 0 20px rgba(0, 204, 255, 0.2);
  display: flex; flex-direction: column; gap: 1.5rem;
}
.modal-content h3 { color: var(--neon-cyan); margin-bottom: 0; }

.result-list { display: flex; flex-direction: column; gap: 1rem; max-height: 50vh; overflow-y: auto; padding-right: 1rem; }
.result-item {
  border: 1px solid var(--line-light); padding: 1rem;
  border-left: 4px solid var(--neon-cyan); background: rgba(255,255,255,0.02);
}
.result-item.success { border-left-color: var(--neon-green); background: rgba(0,255,100,0.05); }
.result-item.failed { border-left-color: var(--neon-pink); background: rgba(255,0,100,0.05); }

.result-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 0.8rem; }
.step-num { font-family: var(--font-tech); font-size: 0.8rem; color: var(--text-muted); }
.action-name { font-weight: bold; flex: 1; text-transform: uppercase; color: var(--text-main); }
.status-badge {
  font-family: var(--font-tech); font-size: 0.8rem; padding: 0.2rem 0.5rem; border-radius: 4px;
}
.success .status-badge { background: var(--neon-green); color: black; }
.failed .status-badge { background: var(--neon-pink); color: white; }

.result-msg { font-family: var(--font-tech); font-size: 0.9rem; color: var(--text-muted); word-break: break-all; }

.modal-actions { display: flex; justify-content: flex-end; margin-top: 1rem; }
</style>