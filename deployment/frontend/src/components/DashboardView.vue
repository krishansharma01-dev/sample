<template>
  <div class="dashboard-view">
    <div class="welcome-banner apple-card">
      <div class="banner-content">
        <span class="banner-tag">PLAYX WASTE OPTIMISER</span>
        <h2>Intelligent Waste Optimization Platform</h2>
        <p>Minimize stock waste, automate cut lists, and sync with Google Sheets seamlessly.</p>
        <div class="banner-actions">
          <button class="apple-btn apple-btn-primary" @click="$emit('navigate', 'optimiser')">
            ⚡ Run Optimization
          </button>
          <button class="apple-btn apple-btn-outline" @click="$emit('navigate', 'sheets')">
            📈 Connect Google Sheets
          </button>
        </div>
      </div>
    </div>

    <div class="metrics-grid">
      <div class="metric-card apple-card">
        <div class="metric-icon">✂️</div>
        <div class="metric-data">
          <span class="metric-value">{{ metrics.totalOptimizationRuns || 0 }}</span>
          <span class="metric-label">Optimization Runs</span>
        </div>
      </div>

      <div class="metric-card apple-card">
        <div class="metric-icon">📉</div>
        <div class="metric-data">
          <span class="metric-value">{{ metrics.averageWasteReduction || '18.4%' }}</span>
          <span class="metric-label">Avg Waste Reduction</span>
        </div>
      </div>

      <div class="metric-card apple-card">
        <div class="metric-icon">📁</div>
        <div class="metric-data">
          <span class="metric-value">{{ metrics.activeProjects || 0 }}</span>
          <span class="metric-label">Active Projects</span>
        </div>
      </div>

      <div class="metric-card apple-card">
        <div class="metric-icon">🔗</div>
        <div class="metric-data">
          <span class="metric-value">{{ metrics.connectedServices || 0 }} / 4</span>
          <span class="metric-label">Connected Services</span>
        </div>
      </div>
    </div>

    <div class="dashboard-grid">
      <div class="grid-section apple-card">
        <h3>Active Cut Projects</h3>
        <div class="table-responsive">
          <table class="modern-table">
            <thead>
              <tr>
                <th>Project Name</th>
                <th>Date</th>
                <th>Items</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="proj in projects" :key="proj.id">
                <td class="font-weight-600">{{ proj.name }}</td>
                <td>{{ proj.date }}</td>
                <td>{{ proj.itemsCount }} items</td>
                <td>
                  <span class="badge-status badge-success">{{ proj.status }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="grid-section apple-card">
        <h3>Recent System Activity</h3>
        <div class="activity-list">
          <div v-for="act in recentHistory" :key="act.id" class="activity-item">
            <div class="act-dot"></div>
            <div class="act-info">
              <span class="act-title">{{ act.title }}</span>
              <span class="act-details">{{ act.details }}</span>
              <span class="act-time">{{ act.timestamp }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DashboardView",
  props: {
    dashboardData: {
      type: Object,
      default: () => ({})
    }
  },
  computed: {
    metrics() {
      return this.dashboardData.metrics || {};
    },
    projects() {
      return this.dashboardData.projects || [];
    },
    recentHistory() {
      return this.dashboardData.recentHistory || [];
    }
  }
};
</script>

<style scoped>
.dashboard-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.welcome-banner {
  padding: 30px;
  background: linear-gradient(135deg, rgba(0, 113, 227, 0.08) 0%, rgba(52, 199, 89, 0.05) 100%);
  border-left: 4px solid #0071e3;
}

.banner-tag {
  font-size: 0.75rem;
  font-weight: 700;
  color: #0071e3;
  letter-spacing: 1px;
}

.welcome-banner h2 {
  margin: 8px 0;
  font-size: 1.6rem;
  font-weight: 700;
}

.welcome-banner p {
  color: #86868b;
  margin-bottom: 20px;
}

.banner-actions {
  display: flex;
  gap: 12px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.metric-card {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.metric-icon {
  font-size: 2rem;
  background: rgba(0, 0, 0, 0.03);
  padding: 12px;
  border-radius: 14px;
}

.metric-data {
  display: flex;
  flex-direction: column;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 700;
}

.metric-label {
  font-size: 0.8rem;
  color: #86868b;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.grid-section {
  padding: 24px;
}

.grid-section h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 1.1rem;
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.modern-table th {
  padding: 10px;
  color: #86868b;
  font-size: 0.8rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.modern-table td {
  padding: 12px 10px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  font-size: 0.85rem;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  gap: 12px;
}

.act-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #0071e3;
  margin-top: 6px;
}

.act-info {
  display: flex;
  flex-direction: column;
}

.act-title {
  font-size: 0.85rem;
  font-weight: 600;
}

.act-details {
  font-size: 0.75rem;
  color: #86868b;
}

.act-time {
  font-size: 0.7rem;
  color: #a1a1a6;
}

@media (max-width: 991px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
</style>
