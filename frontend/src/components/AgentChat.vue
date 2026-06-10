<template>
  <div class="agent-chat-wrapper">
    <!-- 悬浮按钮 -->
    <button
      class="agent-fab"
      :class="{ active: isOpen, pulse: hasNewMessage }"
      @click="toggleChat"
      :title="isOpen ? '关闭智能助手' : '打开智能助手'"
    >
      <span class="fab-icon" v-if="!isOpen">◈</span>
      <span class="fab-icon" v-else>✕</span>
      <span class="fab-ripple" v-if="!isOpen"></span>
    </button>

    <!-- 聊天窗口 -->
    <transition name="chat-slide">
      <div class="agent-chat-panel cyber-panel" v-if="isOpen">
        <!-- 头部 -->
        <div class="chat-header">
          <div class="chat-header-left">
            <span class="chat-avatar">◈</span>
            <div class="chat-header-info">
              <span class="chat-title">SOAR AI 智能助手</span>
              <span class="chat-subtitle">DeepSeek · 安全运营顾问</span>
            </div>
          </div>
          <div class="chat-header-actions">
            <button class="chat-action-btn" @click="clearChat" title="清空对话">⌫</button>
            <button class="chat-action-btn" @click="toggleChat" title="最小化">─</button>
          </div>
        </div>

        <!-- 消息列表 -->
        <div class="chat-messages" ref="messagesContainer">
          <!-- 欢迎消息 -->
          <div class="chat-message bot" v-if="messages.length === 0 && !loading">
            <div class="message-avatar">◈</div>
            <div class="message-bubble">
              <div class="message-text">
                <p>👋 你好！我是 <strong>SOAR 安全运营智能助手</strong>。</p>
                <p>我可以帮助你：</p>
                <ul>
                  <li>🔍 分析安全告警与威胁情报</li>
                  <li>📋 解释自动化响应剧本的执行逻辑</li>
                  <li>🛡️ 提供安全处置建议与最佳实践</li>
                  <li>📊 解读平台统计数据与运营指标</li>
                </ul>
                <p>请随时向我提问！</p>
              </div>
            </div>
          </div>

          <!-- 对话消息 -->
          <div
            v-for="(msg, idx) in messages"
            :key="idx"
            class="chat-message"
            :class="msg.role"
          >
            <div class="message-avatar">
              <span v-if="msg.role === 'user'">👤</span>
              <span v-else>◈</span>
            </div>
            <div class="message-bubble">
              <div class="message-text" v-html="renderMarkdown(msg.content)"></div>
              <div class="message-time">{{ msg.time }}</div>
            </div>
          </div>

          <!-- 加载动画 -->
          <div class="chat-message bot" v-if="loading">
            <div class="message-avatar">◈</div>
            <div class="message-bubble thinking">
              <div class="thinking-dots">
                <span></span><span></span><span></span>
              </div>
              <span class="thinking-text">正在分析中...</span>
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="chat-input-area">
          <div class="quick-actions" v-if="messages.length === 0">
            <button
              v-for="qa in quickActions"
              :key="qa"
              class="quick-action-btn"
              @click="sendMessage(qa)"
            >{{ qa }}</button>
          </div>
          <div class="chat-input-row">
            <textarea
              v-model="inputMessage"
              class="chat-input"
              placeholder="输入你的安全问题..."
              rows="1"
              @keydown.enter.exact.prevent="sendMessage()"
              @input="autoResize"
              ref="inputEl"
              :disabled="loading"
            ></textarea>
            <button
              class="chat-send-btn"
              @click="sendMessage()"
              :disabled="!inputMessage.trim() || loading"
              title="发送消息"
            >▶</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AgentChat',
  data() {
    return {
      isOpen: false,
      hasNewMessage: false,
      messages: [],
      inputMessage: '',
      loading: false,
      // DeepSeek API 配置
      apiKey: 'sk-25fa8c22eccc4400861180c0cc81235a',
      apiURL: 'https://api.deepseek.com/v1/chat/completions',
      systemPrompt: `你是内嵌在 SOAR 安全运营平台中的 AI 智能助手，帮助安全分析师处理日常运维工作。

你的职责：
- 用中文回答问题，语气专业、简洁
- 帮助用户理解安全告警的含义和处置思路
- 提供安全运营的通用最佳实践建议
- 遇到不懂的问题诚实说明，不要编造`,

      quickActions: [
        '📊 这个平台有哪些主要功能？',
        '🛡️ 收到安全告警后应该怎么处理？',
        '💡 如何判断一个告警的紧急程度？',
        '📋 SOAR 平台相比传统 SIEM 有什么优势？'
      ]
    }
  },
  methods: {
    toggleChat() {
      this.isOpen = !this.isOpen
      if (this.isOpen) {
        this.hasNewMessage = false
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      }
    },
    clearChat() {
      this.messages = []
      this.hasNewMessage = false
    },
    autoResize() {
      const el = this.$refs.inputEl
      if (el) {
        el.style.height = 'auto'
        el.style.height = Math.min(el.scrollHeight, 120) + 'px'
      }
    },
    scrollToBottom() {
      const container = this.$refs.messagesContainer
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    },
    getTime() {
      const now = new Date()
      return now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
    },
    async sendMessage(quickAction) {
      const text = quickAction || this.inputMessage.trim()
      if (!text || this.loading) return

      // 添加用户消息
      this.messages.push({
        role: 'user',
        content: text,
        time: this.getTime()
      })

      if (!quickAction) {
        this.inputMessage = ''
        // 重置 textarea 高度
        this.$nextTick(() => {
          const el = this.$refs.inputEl
          if (el) el.style.height = 'auto'
        })
      }

      this.scrollToBottom()

      // 调用 DeepSeek API
      this.loading = true
      try {
        const response = await axios.post(
          this.apiURL,
          {
            model: 'deepseek-chat',
            messages: [
              { role: 'system', content: this.systemPrompt },
              ...this.messages.map(m => ({ role: m.role, content: m.content }))
            ],
            temperature: 0.7,
            max_tokens: 2000
          },
          {
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${this.apiKey}`
            },
            timeout: 30000
          }
        )

        const reply = response.data.choices[0].message.content

        this.messages.push({
          role: 'assistant',
          content: reply,
          time: this.getTime()
        })
      } catch (err) {
        console.error('AI API 调用失败:', err)
        let errorMsg = '抱歉，AI 服务暂时不可用，请稍后重试。'
        if (err.response) {
          const status = err.response.status
          if (status === 401) {
            errorMsg = '⚠️ API Key 无效，请联系管理员检查密钥配置。'
          } else if (status === 429) {
            errorMsg = '⏳ 请求过于频繁，请稍等片刻再试。'
          } else if (status === 503) {
            errorMsg = '🔧 AI 服务正在维护中，请稍后重试。'
          }
        } else if (err.code === 'ECONNABORTED') {
          errorMsg = '⏱️ 请求超时，AI 服务响应较慢，请重试。'
        }

        this.messages.push({
          role: 'assistant',
          content: errorMsg,
          time: this.getTime()
        })
      } finally {
        this.loading = false
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      }
    },
    // 简易 Markdown 渲染
    renderMarkdown(text) {
      if (!text) return ''
      let html = text
        // 转义 HTML
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        // 粗体
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        // 行内代码
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        // 换行转 <br>，然后处理段落
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
      return '<p>' + html + '</p>'
    }
  }
}
</script>

<style scoped>
.agent-chat-wrapper {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 10000;
  font-family: var(--font-body);
}

/* ===== 悬浮按钮 ===== */
.agent-fab {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0066ee, #0044aa);
  border: 2px solid var(--neon-cyan);
  color: #fff;
  font-size: 1.4rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--neon-cyan-glow), 0 4px 20px rgba(0, 102, 238, 0.4);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  z-index: 2;
}
.agent-fab:hover {
  transform: scale(1.08);
  box-shadow: 0 0 25px rgba(0, 102, 238, 0.6), 0 6px 24px rgba(0, 102, 238, 0.5);
}
.agent-fab:active {
  transform: scale(0.95);
}
.agent-fab.active {
  background: linear-gradient(135deg, #555, #333);
  border-color: #888;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
}
.fab-icon {
  position: relative;
  z-index: 1;
  line-height: 1;
}

/* 脉冲波纹 */
.fab-ripple {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid var(--neon-cyan);
  animation: ripple 2s ease-out infinite;
}
@keyframes ripple {
  0% { transform: scale(1); opacity: 0.6; }
  100% { transform: scale(1.8); opacity: 0; }
}

.agent-fab.pulse .fab-ripple {
  animation-duration: 1.2s;
}

/* ===== 聊天面板 ===== */
.agent-chat-panel {
  position: absolute;
  bottom: 72px;
  right: 0;
  width: 400px;
  height: 560px;
  padding: 0 !important;
  display: flex;
  flex-direction: column;
  border-radius: var(--radius-lg) !important;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2), var(--neon-cyan-glow);
  overflow: hidden;
}

/* 头部 */
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 1rem;
  background: linear-gradient(135deg, rgba(0, 102, 238, 0.1), rgba(0, 68, 170, 0.1));
  border-bottom: 1px solid var(--line-light);
}
.chat-header-left {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.chat-avatar {
  font-size: 1.4rem;
  color: var(--neon-cyan);
  text-shadow: var(--neon-cyan-glow);
}
.chat-header-info {
  display: flex;
  flex-direction: column;
}
.chat-title {
  font-family: var(--font-tech);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-main);
  letter-spacing: 0.5px;
}
.chat-subtitle {
  font-size: 0.7rem;
  color: var(--text-muted);
}
.chat-header-actions {
  display: flex;
  gap: 0.3rem;
}
.chat-action-btn {
  background: none;
  border: 1px solid transparent;
  color: var(--text-muted);
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}
.chat-action-btn:hover {
  border-color: var(--line-light);
  color: var(--text-main);
  background: rgba(255, 255, 255, 0.5);
}

/* 消息区域 */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chat-message {
  display: flex;
  gap: 0.5rem;
  max-width: 100%;
  animation: msgIn 0.3s ease-out;
}
@keyframes msgIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.chat-message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  background: rgba(0, 102, 238, 0.08);
  border: 1px solid var(--line-light);
}

.message-bubble {
  max-width: 80%;
  padding: 0.7rem 1rem;
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  line-height: 1.6;
}

.chat-message.bot .message-bubble {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid var(--line-light);
  border-top-left-radius: 2px;
}
.chat-message.user .message-bubble {
  background: linear-gradient(135deg, rgba(0, 102, 238, 0.1), rgba(0, 68, 170, 0.1));
  border: 1px solid rgba(0, 102, 238, 0.3);
  border-top-right-radius: 2px;
  color: var(--text-main);
}

.message-bubble.thinking {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 1rem;
}

.thinking-dots {
  display: flex;
  gap: 4px;
}
.thinking-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--neon-cyan);
  animation: dotPulse 1.4s ease-in-out infinite;
}
.thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
.thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes dotPulse {
  0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
  40% { opacity: 1; transform: scale(1.2); }
}

.thinking-text {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.message-text p {
  margin: 0.3rem 0;
}
.message-text p:first-child {
  margin-top: 0;
}
.message-text p:last-child {
  margin-bottom: 0;
}
.message-text ul {
  margin: 0.4rem 0;
  padding-left: 1.2rem;
}
.message-text li {
  margin: 0.2rem 0;
}
.message-text code {
  background: rgba(0, 102, 238, 0.08);
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  color: var(--neon-cyan);
}

.message-time {
  font-size: 0.65rem;
  color: var(--text-muted);
  text-align: right;
  margin-top: 0.3rem;
}

/* 输入区域 */
.chat-input-area {
  padding: 0.8rem 1rem;
  border-top: 1px solid var(--line-light);
  background: rgba(255, 255, 255, 0.5);
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-bottom: 0.6rem;
}
.quick-action-btn {
  font-size: 0.7rem;
  padding: 0.3rem 0.6rem;
  border-radius: 12px;
  border: 1px solid var(--line-light);
  background: rgba(0, 102, 238, 0.04);
  color: var(--neon-cyan);
  cursor: pointer;
  transition: var(--transition);
  white-space: nowrap;
  font-family: var(--font-body);
}
.quick-action-btn:hover {
  background: rgba(0, 102, 238, 0.12);
  border-color: var(--neon-cyan);
  box-shadow: var(--neon-cyan-glow);
}

.chat-input-row {
  display: flex;
  gap: 0.5rem;
  align-items: flex-end;
}
.chat-input {
  flex: 1;
  border: 1px solid var(--line-light);
  border-radius: var(--radius-md);
  padding: 0.6rem 0.8rem;
  font-family: var(--font-body);
  font-size: 0.85rem;
  color: var(--text-main);
  background: rgba(255, 255, 255, 0.7);
  resize: none;
  outline: none;
  transition: var(--transition);
  max-height: 120px;
}
.chat-input:focus {
  border-color: var(--neon-cyan);
  box-shadow: 0 0 8px rgba(0, 102, 238, 0.15);
}
.chat-input::placeholder {
  color: var(--text-muted);
}
.chat-input:disabled {
  opacity: 0.5;
}
.chat-send-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--neon-cyan);
  background: linear-gradient(135deg, #0066ee, #0044aa);
  color: #fff;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  flex-shrink: 0;
}
.chat-send-btn:hover:not(:disabled) {
  box-shadow: var(--neon-cyan-glow);
  transform: scale(1.05);
}
.chat-send-btn:active:not(:disabled) {
  transform: scale(0.95);
}
.chat-send-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* ===== 过渡动画 ===== */
.chat-slide-enter-active {
  animation: slideUp 0.35s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.chat-slide-leave-active {
  animation: slideDown 0.25s cubic-bezier(0.55, 0, 1, 0.45);
}
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
@keyframes slideDown {
  from {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  to {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
}

/* 响应式：小屏幕适配 */
@media (max-width: 480px) {
  .agent-chat-panel {
    width: calc(100vw - 32px);
    right: -8px;
    height: 480px;
  }
  .agent-fab {
    width: 48px;
    height: 48px;
    font-size: 1.2rem;
  }
}
</style>
