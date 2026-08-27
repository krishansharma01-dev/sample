<template>
  <div class="app-layout">
    <!-- Mobile Hamburger Toggle -->
    <button class="mobile-menu-toggle" @click="isMobileOpen = !isMobileOpen">
      ☰ Menu
    </button>

    <!-- Sidebar Navigation -->
    <SidebarNav
      :currentTab="currentTab"
      :isMobileOpen="isMobileOpen"
      @change-tab="currentTab = $event"
      @close-mobile="isMobileOpen = false"
    />

    <!-- Main Content View -->
    <main class="main-wrapper">
      <header class="top-header">
        <div class="breadcrumb">
          <span class="bc-root">PLAYX</span>
          <span class="bc-sep">/</span>
          <span class="bc-current">{{ currentTabTitle }}</span>
        </div>
        <div class="header-actions">
          <span class="badge-status badge-success">🟢 Engine Operational</span>
        </div>
      </header>

      <div class="view-container">
        <DashboardView
          v-if="currentTab === 'dashboard'"
          :dashboardData="dashboardData"
          @navigate="currentTab = $event"
        />

        <CspTool v-else-if="currentTab === 'optimiser'" />

        <GenericModuleView
          v-else-if="currentTab === 'projects'"
          title="Projects / Operations"
          subtitle="Manage active production batches and cutting operations."
          :items="dashboardData.projects"
        />

        <GenericModuleView
          v-else-if="currentTab === 'data'"
          title="Data Center"
          subtitle="Raw material specifications, master dimensions, and inventory logs."
          :items="[
            { title: 'Aluminum 6061 Stock List', details: '150 items in inventory' },
            { title: 'Steel Pipe Batch #22', details: '95 items in inventory' }
          ]"
        />

        <GoogleSheetsView v-else-if="currentTab === 'sheets'" />

        <AiAssistantView v-else-if="currentTab === 'ai-assistant'" />

        <GenericModuleView
          v-else-if="currentTab === 'reports'"
          title="Reports & Analytics"
          subtitle="Waste summary metrics and yield optimization reports."
          :items="[
            { title: 'Monthly Waste Summary', details: '18.4% total yield improvement achieved.' },
            { title: 'Material Utilization Log', details: 'Generated on ' + new Date().toLocaleDateString() }
          ]"
        />

        <GenericModuleView
          v-else-if="currentTab === 'history'"
          title="Activity History"
          subtitle="System logs, optimization runs, and service sync history."
          :items="dashboardData.recentHistory"
        />

        <SettingsView v-else-if="currentTab === 'settings'" />
      </div>
    </main>
  </div>
</template>

<script>
import axios from "axios";
import SidebarNav from "./components/SidebarNav.vue";
import DashboardView from "./components/DashboardView.vue";
import CspTool from "./components/CspTool.vue";
import GoogleSheetsView from "./components/GoogleSheetsView.vue";
import AiAssistantView from "./components/AiAssistantView.vue";
import SettingsView from "./components/SettingsView.vue";
import GenericModuleView from "./components/GenericModuleView.vue";

export default {
  name: "App",
  components: {
    SidebarNav,
    DashboardView,
    CspTool,
    GoogleSheetsView,
    AiAssistantView,
    SettingsView,
    GenericModuleView
  },
  data() {
    return {
      currentTab: "dashboard",
      isMobileOpen: false,
      dashboardData: {}
    };
  },
  computed: {
    currentTabTitle() {
      const titles = {
        dashboard: "Dashboard",
        optimiser: "Waste Optimiser",
        projects: "Projects / Operations",
        data: "Data Center",
        sheets: "Google Sheets",
        "ai-assistant": "AI Assistant",
        reports: "Reports",
        history: "History",
        settings: "Settings"
      };
      return titles[this.currentTab] || "Dashboard";
    }
  },
  mounted() {
    this.fetchDashboardData();
  },
  methods: {
    async fetchDashboardData() {
      try {
        const res = await axios.get("http://localhost:5000/api/dashboard");
        if (res.data) {
          this.dashboardData = res.data;
        }
      } catch (err) {
        console.error("Failed to load dashboard metrics", err);
      }
    }
  }
};
</script>

<style>
@import "./assets/style.scss";

.app-layout {
  display: flex;
  min-height: 100vh;
}

.mobile-menu-toggle {
  display: none;
  position: fixed;
  top: 14px;
  right: 14px;
  z-index: 200;
  background: #0071e3;
  color: #fff;
  border: none;
  padding: 8px 14px;
  border-radius: 20px;
  font-weight: 600;
  cursor: pointer;
}

.main-wrapper {
  flex: 1;
  margin-left: 260px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.top-header {
  padding: 16px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(15px);
  position: sticky;
  top: 0;
  z-index: 50;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
}

.bc-root {
  font-weight: 700;
  color: #0071e3;
}

.bc-sep {
  color: #a1a1a6;
}

.bc-current {
  font-weight: 600;
  color: #1d1d1f;
}

.view-container {
  padding: 24px 32px;
  flex: 1;
}

@media (max-width: 991px) {
  .mobile-menu-toggle {
    display: block;
  }

  .main-wrapper {
    margin-left: 0;
  }

  .view-container {
    padding: 16px;
  }
}
</style>
