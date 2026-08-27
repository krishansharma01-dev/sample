<template>
  <div class="ai-assistant-view apple-card">
    <div class="chat-header">
      <div class="header-info">
        <div class="ai-icon-bg">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="11" width="18" height="10" rx="2"></rect>
            <circle cx="12" cy="5" r="2"></circle>
            <path d="M12 7v4"></path>
            <line x1="8" y1="16" x2="8.01" y2="16"></line>
            <line x1="16" y1="16" x2="16.01" y2="16"></line>
          </svg>
        </div>
        <div>
          <h2>PLAYX-AI</h2>
          <span class="status-indicator">🟢 Agentic Engine Operational</span>
        </div>
      </div>
      <button class="apple-btn apple-btn-outline" @click="clearChat">Clear Chat</button>
    </div>

    <div class="messages-container" ref="msgContainer">
      <div v-for="(msg, index) in messages" :key="index" :class="['message-row', msg.sender]">
        <div class="avatar">
          <svg v-if="msg.sender === 'user'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
          <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path></svg>
        </div>
        <div class="bubble apple-card">
          <div class="sender-name">{{ msg.sender === 'user' ? 'You' : 'PLAYX-AI' }}</div>
          <div class="message-text" v-html="formatMarkdown(msg.text)"></div>

          <div v-if="msg.previewAction" class="action-preview-box">
            <div class="preview-header">⚠️ Safe Confirmation Required</div>
            <div class="preview-title">{{ msg.previewAction.title }}</div>
            <p class="preview-desc">{{ msg.previewAction.description }}</p>
            <div class="preview-buttons">
              <button class="apple-btn apple-btn-primary" @click="confirmAction(msg.previewAction)">
                ✓ Confirm & Execute
              </button>
              <button class="apple-btn apple-btn-outline" @click="cancelAction(msg)">
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="loading" class="message-row ai">
        <div class="avatar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle></svg>
        </div>
        <div class="bubble apple-card">
          <span class="typing-indicator">PLAYX-AI is processing query & tools...</span>
        </div>
      </div>
    </div>

    <div class="chat-input-container">
      <input
        v-model="inputMsg"
        type="text"
        placeholder="Ask PLAYX-AI to optimize waste, check Google Sheets, or run tasks..."
        class="apple-input"
        @keyup.enter="sendMessage"
      />
      <button class="apple-btn apple-btn-primary" :disabled="loading" @click="sendMessage">
        Send
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { API_BASE } from "../apiConfig";

export default {
  name: "AiAssistantView",
  data() {
    return {
      inputMsg: "",
      loading: false,
      messages: [
        {
          sender: "ai",
          text: "Hello! I am **PLAYX-AI**.\n\nAsk PLAYX-AI to summarize waste results, inspect your Google Sheet, or execute optimizations safely."
        }
      ]
    };
  },
  methods: {
    formatMarkdown(text) {
      if (!text) return "";
      let html = text
        .replace(/\n/g, '<br/>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/• (.*?)(<br\/>|$)/g, '<li>$1</li>');
      return html;
    },
    async sendMessage() {
      if (!this.inputMsg.trim()) return;
      const userText = this.inputMsg.trim();
      this.messages.push({ sender: "user", text: userText });
      this.inputMsg = "";
      this.loading = true;

      try {
        const res = await axios.post(`${API_BASE}/api/ai/chat`, {
          message: userText
        });
        if (res.data && res.data.response) {
          this.messages.push({
            sender: "ai",
            text: res.data.response,
            previewAction: res.data.previewAction
          });
        }
      } catch (err) {
        this.messages.push({
          sender: "ai",
          text: "⚠️ Backend connection error. Ensure server is active."
        });
      } finally {
        this.loading = false;
        this.scrollToBottom();
      }
    },
    async confirmAction(action) {
      this.loading = true;
      try {
        const res = await axios.post(`${API_BASE}/api/google-sheets`, {
          action: "execute_update",
          changes: action.changes
        });
        this.messages.push({
          sender: "ai",
          text: `✅ **Action Confirmed & Executed by PLAYX-AI!**\n\n${res.data.message}`
        });
      } catch (e) {
        this.messages.push({ sender: "ai", text: "❌ Failed to execute action." });
      } finally {
        this.loading = false;
        this.scrollToBottom();
      }
    },
    cancelAction(msg) {
      msg.previewAction = null;
      this.messages.push({ sender: "ai", text: "Operation canceled by user." });
    },
    clearChat() {
      this.messages = [
        {
          sender: "ai",
          text: "Chat history cleared. How can PLAYX-AI assist you?"
        }
      ];
    },
    scrollToBottom() {
      this.$nextTick(() => {
        if (this.$refs.msgContainer) {
          this.$refs.msgContainer.scrollTop = this.$refs.msgContainer.scrollHeight;
        }
      });
    }
  }
};
</script>

<style scoped>
.ai-assistant-view {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
  padding: 20px;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ai-icon-bg {
  background: #0071e3;
  color: #fff;
  padding: 8px;
  border-radius: 10px;
  display: flex;
  align-items: center;
}

.header-info h2 {
  margin: 0;
  font-size: 1.2rem;
}

.status-indicator {
  font-size: 0.75rem;
  color: #34c759;
  font-weight: 600;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-row {
  display: flex;
  gap: 12px;
  max-width: 80%;
}

.message-row.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.avatar {
  background: rgba(0, 0, 0, 0.05);
  padding: 8px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 36px;
  width: 36px;
}

.message-row.user .avatar {
  background: #0071e3;
  color: #ffffff;
}

.bubble {
  padding: 14px 18px;
  border-radius: 16px;
}

.message-row.user .bubble {
  background: #0071e3;
  color: #ffffff;
}

.sender-name {
  font-size: 0.75rem;
  font-weight: 700;
  margin-bottom: 4px;
  opacity: 0.7;
}

.message-text {
  font-size: 0.9rem;
  line-height: 1.5;
}

.action-preview-box {
  margin-top: 12px;
  padding: 12px;
  background: rgba(255, 149, 0, 0.1);
  border-left: 3px solid #ff9500;
  border-radius: 8px;
}

.preview-header {
  font-size: 0.75rem;
  font-weight: 700;
  color: #c67300;
}

.preview-title {
  font-weight: 600;
  margin-top: 4px;
}

.preview-desc {
  font-size: 0.8rem;
  color: #86868b;
  margin: 4px 0 10px 0;
}

.preview-buttons {
  display: flex;
  gap: 8px;
}

.chat-input-container {
  display: flex;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}
</style>
