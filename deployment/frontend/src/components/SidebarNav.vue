<template>
  <aside class="sidebar-container" :class="{ 'mobile-open': isMobileOpen }">
    <div class="sidebar-header">
      <PlayxLogo variant="full" />
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
        <span class="nav-icon" v-html="item.svg"></span>
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
import PlayxLogo from "./PlayxLogo.vue";

export default {
  components: {
    PlayxLogo
  },
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
        {
          id: "dashboard",
          label: "Dashboard",
          svg: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>`
        },
        {
          id: "optimiser",
          label: "Waste Optimiser",
          svg: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"></circle><circle cx="6" cy="18" r="3"></circle><line x1="20" y1="4" x2="8.12" y2="15.88"></line><line x1="14.47" y1="14.48" x2="20" y2="20"></line><line x1="8.12" y1="8.12" x2="12" y2="12"></line></svg>`
        },
        {
          id: "data-sources",
          label: "Data Sources",
          badge: "Multi",
          svg: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path></svg>`
        },
        {
          id: "projects",
          label: "Projects / Operations",
          svg: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>`
        },
        {
          id: "sheets",
          label: "Google Sheets",
          badge: "Sync",
          svg: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>`
        },
        {
          id: "ai-assistant",
          label: "PLAYX-AI",
          badge: "AI",
          svg: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path><line x1="8" y1="16" x2="8.01" y2="16"></line><line x1="16" y1="16" x2="16.01" y2="16"></line></svg>`
        },
        {
          id: "reports",
          label: "Reports",
          svg: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>`
        },
        {
          id: "history",
          label: "History",
          svg: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>`
        },
        {
          id: "settings",
          label: "Settings",
          svg: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>`
        }
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
  background: linear-gradient(135deg, #0071e3 0%, #34c759 100%);
  color: #fff;
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.25);
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
  display: flex;
  align-items: center;
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
