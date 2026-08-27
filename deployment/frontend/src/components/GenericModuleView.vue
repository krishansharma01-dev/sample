<template>
  <div class="generic-view apple-card">
    <div class="view-header">
      <h2>{{ title }}</h2>
      <p class="subtitle">{{ subtitle }}</p>
    </div>

    <div class="view-content">
      <div v-if="items && items.length > 0" class="items-grid">
        <div v-for="(item, index) in items" :key="index" class="item-card apple-card">
          <div class="item-top">
            <span class="item-title">{{ item.title || item.name }}</span>
            <span v-if="item.type || item.status" class="badge-status badge-neutral">
              {{ item.type || item.status }}
            </span>
          </div>
          <p class="item-desc">{{ item.details || item.date || 'Active record in PLAYX Optimiser.' }}</p>
        </div>
      </div>
      <div v-else class="empty-state">
        <span>📦</span>
        <p>No records found in this section.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "GenericModuleView",
  props: {
    title: { type: String, required: true },
    subtitle: { type: String, default: "" },
    items: { type: Array, default: () => [] }
  }
};
</script>

<style scoped>
.generic-view {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.view-header h2 {
  margin: 0;
  font-size: 1.4rem;
}

.subtitle {
  color: #86868b;
  font-size: 0.85rem;
  margin-top: 4px;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}

.item-card {
  padding: 16px;
}

.item-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.item-title {
  font-weight: 600;
  font-size: 0.95rem;
}

.item-desc {
  font-size: 0.8rem;
  color: #86868b;
  margin: 0;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #86868b;
}

.empty-state span {
  font-size: 2.5rem;
}
</style>
