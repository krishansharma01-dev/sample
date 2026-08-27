<template>
  <div class="sheets-view apple-card">
    <div class="view-header">
      <div>
        <h2>Google Sheets Integration</h2>
        <p class="subtitle">Direct spreadsheet integration with safety validation layer.</p>
      </div>
      <span class="badge-status" :class="sheetsData ? 'badge-success' : 'badge-neutral'">
        {{ sheetsData ? 'Connected' : 'Not Connected' }}
      </span>
    </div>

    <div v-if="sheetsData" class="sheets-content">
      <div class="sheet-info-bar apple-card">
        <div class="info-item">
          <span class="label">Spreadsheet:</span>
          <span class="val">📊 {{ sheetsData.spreadsheet }}</span>
        </div>
        <div class="info-item">
          <span class="label">Worksheet:</span>
          <select class="apple-input select-sm" v-model="sheetsData.activeWorksheet">
            <option v-for="ws in sheetsData.worksheets" :key="ws" :value="ws">{{ ws }}</option>
          </select>
        </div>
        <button class="apple-btn apple-btn-primary btn-sm" @click="addRow">+ Add Inventory Row</button>
      </div>

      <div class="table-card apple-card">
        <table class="data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Material Description</th>
              <th>Width / Size</th>
              <th>Quantity</th>
              <th>Est. Waste</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in sheetsData.rows" :key="row.id">
              <td>{{ row.id }}</td>
              <td class="font-weight-600">{{ row.material }}</td>
              <td>{{ row.width }} units</td>
              <td>{{ row.quantity }}</td>
              <td><span class="badge-status badge-neutral">{{ row.waste_est }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "GoogleSheetsView",
  data() {
    return {
      sheetsData: null
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const res = await axios.get("http://localhost:5000/api/google-sheets");
        if (res.data && res.data.data) {
          this.sheetsData = res.data.data;
        }
      } catch (e) {
        console.error("Failed to fetch Google Sheets data", e);
      }
    },
    async addRow() {
      const mat = prompt("Enter Material Name:", "Aluminum Sheet 7075");
      if (!mat) return;
      try {
        const res = await axios.post("http://localhost:5000/api/google-sheets", {
          action: "add_row",
          row: { material: mat, width: 150, quantity: 20, waste_est: "2.5%" }
        });
        this.sheetsData = res.data.data;
      } catch (e) {
        alert("Failed to add row.");
      }
    }
  }
};
</script>

<style scoped>
.sheets-view {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.view-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
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

.sheet-info-bar {
  padding: 14px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.label {
  font-size: 0.8rem;
  color: #86868b;
  font-weight: 600;
}

.val {
  font-weight: 600;
  font-size: 0.9rem;
}

.select-sm {
  width: 180px;
  padding: 6px 10px;
}

.table-card {
  padding: 16px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  font-size: 0.8rem;
  color: #86868b;
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.data-table td {
  padding: 12px 10px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  font-size: 0.85rem;
}
</style>
