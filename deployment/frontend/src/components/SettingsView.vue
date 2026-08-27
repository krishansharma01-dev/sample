<template>
  <div class="settings-view apple-card">
    <div class="settings-header">
      <h2>Settings Center</h2>
      <p class="subtitle">Manage system preferences, connections, and platform branding.</p>
    </div>

    <div class="settings-sections">
      <!-- General Preferences -->
      <div class="section-card apple-card">
        <h3>General Preferences</h3>
        <div class="form-group">
          <label>Platform Name</label>
          <input type="text" class="apple-input" value="PLAYX Waste Optimiser" readonly />
        </div>
        <div class="form-group">
          <label>Interface Theme</label>
          <select class="apple-input" v-model="settings.theme">
            <option value="system">System Default</option>
            <option value="light">Light Minimal</option>
            <option value="dark">Dark Glass</option>
          </select>
        </div>
      </div>

      <!-- Connections Manager -->
      <div class="section-card apple-card">
        <h3>Connection Manager</h3>
        <p class="section-desc">Configure external services and data credentials securely.</p>

        <div class="connections-list">
          <div class="connection-item">
            <div class="conn-info">
              <span class="conn-name">📈 Google Sheets</span>
              <span class="badge-status" :class="connections.google_sheets?.status === 'Connected' ? 'badge-success' : 'badge-neutral'">
                {{ connections.google_sheets?.status || 'Not Connected' }}
              </span>
            </div>
            <button class="apple-btn apple-btn-outline" @click="toggleConnection('google_sheets')">
              {{ connections.google_sheets?.status === 'Connected' ? 'Disconnect' : 'Connect' }}
            </button>
          </div>

          <div class="connection-item">
            <div class="conn-info">
              <span class="conn-name">🤖 Gemini API</span>
              <span class="badge-status" :class="connections.gemini?.status === 'Connected' ? 'badge-success' : 'badge-neutral'">
                {{ connections.gemini?.status || 'Not Connected' }}
              </span>
            </div>
            <div class="conn-actions">
              <input type="password" class="apple-input key-input" placeholder="AIza••••••••" v-model="geminiKey" />
              <button class="apple-btn apple-btn-primary" @click="saveKey('gemini', geminiKey)">Save Key</button>
            </div>
          </div>

          <div class="connection-item">
            <div class="conn-info">
              <span class="conn-name">⚡ Supabase Database</span>
              <span class="badge-status" :class="connections.supabase?.status === 'Connected' ? 'badge-success' : 'badge-neutral'">
                {{ connections.supabase?.status || 'Not Connected' }}
              </span>
            </div>
            <button class="apple-btn apple-btn-outline" @click="toggleConnection('supabase')">
              {{ connections.supabase?.status === 'Connected' ? 'Disconnect' : 'Connect' }}
            </button>
          </div>

          <div class="connection-item">
            <div class="conn-info">
              <span class="conn-name">🔥 Firebase</span>
              <span class="badge-status" :class="connections.firebase?.status === 'Connected' ? 'badge-success' : 'badge-neutral'">
                {{ connections.firebase?.status || 'Not Connected' }}
              </span>
            </div>
            <button class="apple-btn apple-btn-outline" @click="toggleConnection('firebase')">
              {{ connections.firebase?.status === 'Connected' ? 'Disconnect' : 'Connect' }}
            </button>
          </div>
        </div>
      </div>

      <!-- FLOATING BRANDING CARD AT BOTTOM OF SETTINGS -->
      <div class="floating-branding-card apple-card">
        <div class="branding-header">
          <span class="by-text">Made by: <strong>PLAYXCODE</strong></span>
        </div>
        <div class="branding-body">
          <h4>About App</h4>
          <p>This is an app about waste-management optimiser.</p>
          <div class="cta-section">
            <span class="cta-text">WANT NEW APP, SOFTWARE? VISIT OUR WEBSITE</span>
            <a
              href="https://playxcode.netlify.app"
              target="_blank"
              rel="noopener noreferrer"
              class="glowing-cta-btn"
            >
              <span>LET'S GO!</span>
              <span class="arrow">🚀</span>
            </a>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { API_BASE } from "../apiConfig";

export default {
  name: "SettingsView",
  data() {
    return {
      settings: {
        theme: "system"
      },
      connections: {},
      geminiKey: ""
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const res = await axios.get(`${API_BASE}/api/connections`);
        if (res.data && res.data.connections) {
          this.connections = res.data.connections;
        }
      } catch (err) {
        console.error("Failed to load connections", err);
      }
    },
    async toggleConnection(service) {
      const isConn = this.connections[service]?.status === 'Connected';
      try {
        const res = await axios.post(`${API_BASE}/api/connections`, {
          service,
          payload: { action: isConn ? 'disconnect' : 'connect' }
        });
        this.connections = res.data.connections;
      } catch (e) {
        alert("Failed to update connection state.");
      }
    },
    async saveKey(service, key) {
      if (!key) return;
      try {
        const res = await axios.post(`${API_BASE}/api/connections`, {
          service,
          payload: { apiKey: key, action: 'connect' }
        });
        this.connections = res.data.connections;
        this.geminiKey = "";
        alert("API Key saved securely!");
      } catch (e) {
        alert("Error saving API Key.");
      }
    }
  }
};
</script>

<style scoped>
.settings-view {
  padding: 30px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.settings-header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.subtitle {
  color: #86868b;
  margin-top: 4px;
}

.settings-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-card {
  padding: 24px;
}

.section-card h3 {
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 1.1rem;
}

.section-desc {
  font-size: 0.85rem;
  color: #86868b;
  margin-bottom: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 14px;
}

.form-group label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #86868b;
}

.connections-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.connection-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 12px;
}

.conn-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.conn-name {
  font-weight: 600;
  font-size: 0.95rem;
}

.conn-actions {
  display: flex;
  gap: 8px;
}

.key-input {
  width: 180px;
}

/* Floating Branding Card */
.floating-branding-card {
  margin-top: 20px;
  padding: 28px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(240, 246, 255, 0.9) 100%);
  border: 2px solid rgba(0, 113, 227, 0.2);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 113, 227, 0.12);
  text-align: center;
}

.branding-header {
  margin-bottom: 12px;
}

.by-text {
  font-size: 0.9rem;
  color: #86868b;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.by-text strong {
  color: #0071e3;
}

.branding-body h4 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
}

.branding-body p {
  color: #86868b;
  font-size: 0.9rem;
  margin: 6px 0 20px 0;
}

.cta-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
}

.cta-text {
  font-weight: 700;
  font-size: 0.85rem;
  color: #1d1d1f;
  letter-spacing: 0.5px;
}

.arrow {
  font-size: 1.1rem;
}
</style>
