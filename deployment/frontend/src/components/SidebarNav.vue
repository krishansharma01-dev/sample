<template>
  <aside class="sidebar-container" :class="{ 'mobile-open': isMobileOpen }">
    <div class="sidebar-header">
      <div class="brand-logo">
        <span class="logo-icon">⚡</span>
        <div class="brand-info">
          <span class="brand-title">PLAYX</span>
          <span class="brand-sub">Waste Optimiser</span>
        </div>
      </div>
      <button class="mobile-close-btn" @click="$emit('close-mobile')">✕</button>
    </div>

    <nav class="sidebar-nav">
      <div class="nav-section-title">PLATFORM</div>

      <button
        v-for="item in navItems"
        :key="item.id"
        class="nav-item"
        :class="{ active: currentTab === item.id }"
        @click="selectTab(item.id)"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        <span class="nav-label">{{ item.label }}</span>
        <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
      </button>
    </nav>

    <div class="sidebar-footer">
      <div class="user-pill">
        <div class="user-avatar">PX</div>
        <div class="user-details">
          <span class="user-name">PLAYXCODE Pro</span>
          <span class="user-role">Waste Engine v2.4</span>
        </div>
      </div>
    </div>
  </aside>
</template>

<script>
export default {
  name: "SidebarNav",
  props: {
    currentTab: {
      type: String,
      default: "dashboard"
    },
    isMobileOpen: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      navItems: [
        { id: "dashboard", label: "Dashboard", icon: "📊" },
        { id: "optimiser", label: "Waste Optimiser", icon: "✂️" },
        { id: "projects", label: "Projects / Operations", icon: "📁" },
        { id: "data", label: "Data Center", icon: "💾" },
        { id: "sheets", label: "Google Sheets", icon: "📈", badge: "Sync" },
        { id: "ai-assistant", label: "AI Assistant", icon: "🤖", badge: "AI" },
        { id: "reports", label: "Reports", icon: "📄" },
        { id: "history", label: "History", icon: "🕒" },
        { id: "settings", label: "Settings", icon: "⚙️" }
      ]
    };
  },
  methods: {
    selectTab(tabId) {
      this.$emit("change-tab", tabId);
      this.$emit("close-mobile");
    }
  }
};
</script>

<style scoped>
.sidebar-container {
  width: 260px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border-right: 1px solid rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.sidebar-header {
  padding: 24px 20px 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 1.6rem;
  background: #0071e3;
  color: #fff;
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-info {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-weight: 800;
  font-size: 1.1rem;
  letter-spacing: 0.5px;
  color: #1d1d1f;
}

.brand-sub {
  font-size: 0.75rem;
  color: #86868b;
  font-weight: 500;
}

.mobile-close-btn {
  display: none;
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #86868b;
}

.sidebar-nav {
  flex: 1;
  padding: 12px;
  overflow-y: auto;
}

.nav-section-title {
  font-size: 0.7rem;
  font-weight: 700;
  color: #a1a1a6;
  padding: 8px 12px;
  letter-spacing: 0.8px;
}

.nav-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  margin-bottom: 4px;
  border: none;
  background: transparent;
  border-radius: 10px;
  cursor: pointer;
  color: #1d1d1f;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s ease;
  text-align: left;
}

.nav-item:hover {
  background: rgba(0, 0, 0, 0.04);
}

.nav-item.active {
  background: #0071e3;
  color: #ffffff;
}

.nav-icon {
  font-size: 1.1rem;
}

.nav-label {
  flex: 1;
}

.nav-badge {
  font-size: 0.65rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 99px;
  background: rgba(0, 113, 227, 0.15);
  color: #0071e3;
}

.nav-item.active .nav-badge {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.user-pill {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  background: rgba(0, 0, 0, 0.03);
  border-radius: 12px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #1d1d1f;
  color: #fff;
  font-size: 0.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 0.8rem;
  font-weight: 600;
}

.user-role {
  font-size: 0.7rem;
  color: #86868b;
}

@media (max-width: 991px) {
  .sidebar-container {
    transform: translateX(-100%);
  }

  .sidebar-container.mobile-open {
    transform: translateX(0);
  }

  .mobile-close-btn {
    display: block;
  }
}
</style>
