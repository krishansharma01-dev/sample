<template>
  <div class="data-sources-view apple-card">
    <div class="view-header">
      <div>
        <h2>Data Center & Data Sources</h2>
        <p class="subtitle">Manage multi-source datasets (Google Sheets, Excel), switch active data sources safely, and map columns.</p>
      </div>
      <div v-if="activeSource" class="active-badge apple-card">
        <span class="active-dot">🟢</span>
        <div>
          <span class="active-title">Active Source: {{ activeSource.name }}</span>
          <span class="active-type">{{ activeSource.type }} ({{ activeSource.rowsCount }} rows)</span>
        </div>
      </div>
    </div>

    <!-- Data Sources Grid -->
    <div class="sources-sections">
      <div class="section-card apple-card">
        <div class="card-title-bar">
          <h3>Connected & Historical Data Sources</h3>
          <div class="action-btns">
            <button class="apple-btn apple-btn-outline" @click="showExcelModal = true">+ Upload Excel File</button>
            <button class="apple-btn apple-btn-primary" @click="showSheetModal = true">+ Connect Google Sheet</button>
          </div>
        </div>

        <div class="sources-grid">
          <div
            v-for="source in dataSources"
            :key="source.id"
            class="source-card apple-card"
            :class="{ 'is-active': source.id === activeSourceId }"
          >
            <div class="source-head">
              <span class="source-icon">
                <svg v-if="source.type === 'Google Sheets'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
              </span>
              <span class="badge-status" :class="source.id === activeSourceId ? 'badge-success' : 'badge-neutral'">
                {{ source.id === activeSourceId ? 'Active' : 'Previous' }}
              </span>
            </div>

            <div class="source-body">
              <span class="source-name">{{ source.name }}</span>
              <span class="source-meta">Worksheet: {{ source.worksheet }}</span>
              <span class="source-meta">Last Synced: {{ source.lastSynced }}</span>
            </div>

            <div class="source-footer">
              <button
                class="apple-btn btn-sm full-width"
                :class="source.id === activeSourceId ? 'apple-btn-outline' : 'apple-btn-primary'"
                :disabled="source.id === activeSourceId"
                @click="setActiveSource(source.id)"
              >
                {{ source.id === activeSourceId ? 'Active Dataset' : 'Set as Active Source' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Active Dataset Rows Preview -->
      <div v-if="activeSource" class="section-card apple-card">
        <h3>Active Dataset Preview: {{ activeSource.name }}</h3>
        <p class="section-desc">Changes here strictly update the active dataset without altering historical sources.</p>

        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Material Description</th>
                <th>Width / Dimension</th>
                <th>Quantity</th>
                <th>Waste Est.</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in activeSource.rows" :key="row.id">
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

    <!-- Excel Upload & Column Mapping Modal -->
    <div v-if="showExcelModal" class="modal-overlay" @click.self="showExcelModal = false">
      <div class="modal-card apple-card">
        <div class="modal-head">
          <h3>Upload Excel File & Map Columns</h3>
          <button class="close-btn" @click="showExcelModal = false">✕</button>
        </div>

        <div v-if="!excelPreview" class="upload-box" @click="triggerExcelUpload">
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#0071e3" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
          <span class="upload-title">Click to upload Excel spreadsheet (.xlsx)</span>
          <span class="upload-sub">Supports worksheet selection & automatic column mapping.</span>
        </div>

        <div v-else class="mapping-box">
          <div class="form-group">
            <label>Detected Worksheets</label>
            <select class="apple-input" v-model="selectedWorksheet">
              <option v-for="ws in excelPreview.worksheets" :key="ws" :value="ws">{{ ws }}</option>
            </select>
          </div>

          <h4>Column Mapping Layer</h4>
          <div class="mapping-grid">
            <div class="map-item">
              <label>Material Name Column</label>
              <select class="apple-input" v-model="columnMapping.material">
                <option v-for="h in excelPreview.detectedHeaders" :key="h" :value="h">{{ h }}</option>
              </select>
            </div>
            <div class="map-item">
              <label>Stock Width Column</label>
              <select class="apple-input" v-model="columnMapping.width">
                <option v-for="h in excelPreview.detectedHeaders" :key="h" :value="h">{{ h }}</option>
              </select>
            </div>
            <div class="map-item">
              <label>Quantity Column</label>
              <select class="apple-input" v-model="columnMapping.quantity">
                <option v-for="h in excelPreview.detectedHeaders" :key="h" :value="h">{{ h }}</option>
              </select>
            </div>
          </div>

          <div class="modal-actions">
            <button class="apple-btn apple-btn-primary" @click="confirmExcelImport">
              ✓ Confirm Import & Set Active
            </button>
            <button class="apple-btn apple-btn-outline" @click="excelPreview = null">Back</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Google Sheet Modal -->
    <div v-if="showSheetModal" class="modal-overlay" @click.self="showSheetModal = false">
      <div class="modal-card apple-card">
        <div class="modal-head">
          <h3>Connect New Google Sheet</h3>
          <button class="close-btn" @click="showSheetModal = false">✕</button>
        </div>
        <div class="form-group">
          <label>Spreadsheet Name / ID</label>
          <input type="text" class="apple-input" v-model="newSheetName" placeholder="e.g. Production Waste — March" />
        </div>
        <div class="form-group">
          <label>Worksheet Name</label>
          <input type="text" class="apple-input" v-model="newWorksheet" placeholder="e.g. Current_Inventory" />
        </div>
        <div class="modal-actions">
          <button class="apple-btn apple-btn-primary" @click="connectNewSheet">Connect & Set Active</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import { API_BASE } from "../apiConfig";

export default {
  name: "DataSourcesView",
  data() {
    return {
      activeSourceId: "",
      activeSource: null,
      dataSources: [],
      showExcelModal: false,
      showSheetModal: false,
      newSheetName: "",
      newWorksheet: "Sheet1",
      excelPreview: null,
      selectedWorksheet: "Inventory_Master",
      columnMapping: {
        material: "Material Description",
        width: "Stock Width",
        quantity: "Quantity"
      }
    };
  },
  mounted() {
    this.fetchDataSources();
  },
  methods: {
    async fetchDataSources() {
      try {
        const res = await axios.get(`${API_BASE}/api/data-sources`);
        if (res.data) {
          this.activeSourceId = res.data.activeSourceId;
          this.activeSource = res.data.activeSource;
          this.dataSources = res.data.dataSources || [];
        }
      } catch (err) {
        console.error("Error fetching data sources", err);
      }
    },
    async setActiveSource(sourceId) {
      try {
        const res = await axios.post(`${API_BASE}/api/data-sources/active`, {
          sourceId
        });
        if (res.data && res.data.activeSource) {
          this.activeSourceId = res.data.activeSource.id;
          this.activeSource = res.data.activeSource;
          this.dataSources = res.data.dataSources;
        }
      } catch (e) {
        alert("Failed to set active dataset.");
      }
    },
    async triggerExcelUpload() {
      try {
        const res = await axios.post(`${API_BASE}/api/data-sources/upload-excel`, {
          filename: "Uploaded_Factory_Inventory.xlsx"
        });
        if (res.data) {
          this.excelPreview = res.data;
        }
      } catch (e) {
        alert("Excel parse error.");
      }
    },
    async confirmExcelImport() {
      try {
        const res = await axios.post(`${API_BASE}/api/data-sources/map-columns`, {
          filename: this.excelPreview.filename,
          worksheet: this.selectedWorksheet,
          rows: this.excelPreview.previewRows
        });
        if (res.data) {
          this.activeSourceId = res.data.activeSource.id;
          this.activeSource = res.data.activeSource;
          this.dataSources = res.data.dataSources;
          this.showExcelModal = false;
          this.excelPreview = null;
        }
      } catch (e) {
        alert("Failed to map Excel dataset.");
      }
    },
    async connectNewSheet() {
      if (!this.newSheetName.trim()) return;
      try {
        const res = await axios.post(`${API_BASE}/api/data-sources/add-sheet`, {
          name: this.newSheetName,
          worksheet: this.newWorksheet
        });
        if (res.data) {
          this.activeSourceId = res.data.activeSource.id;
          this.activeSource = res.data.activeSource;
          this.dataSources = res.data.dataSources;
          this.showSheetModal = false;
          this.newSheetName = "";
        }
      } catch (e) {
        alert("Failed to connect Google Sheet.");
      }
    }
  }
};
</script>

<style scoped>
.data-sources-view {
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

.active-badge {
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(52, 199, 89, 0.08);
  border-left: 3px solid #34c759;
}

.active-title {
  font-weight: 700;
  font-size: 0.85rem;
  color: #1d1d1f;
  display: block;
}

.active-type {
  font-size: 0.75rem;
  color: #86868b;
}

.sources-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-card {
  padding: 20px;
}

.card-title-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.card-title-bar h3 {
  margin: 0;
  font-size: 1.1rem;
}

.action-btns {
  display: flex;
  gap: 10px;
}

.sources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}

.source-card {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;

  &.is-active {
    border: 2px solid #0071e3;
    background: rgba(0, 113, 227, 0.02);
  }
}

.source-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.source-icon {
  color: #0071e3;
}

.source-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.source-name {
  font-weight: 700;
  font-size: 0.95rem;
}

.source-meta {
  font-size: 0.75rem;
  color: #86868b;
}

.section-desc {
  font-size: 0.8rem;
  color: #86868b;
  margin-bottom: 14px;
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  z-index: 300;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-card {
  width: 460px;
  padding: 24px;
  background: #fff;
}

.modal-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.1rem;
  cursor: pointer;
  color: #86868b;
}

.upload-box {
  padding: 30px;
  border: 2px dashed rgba(0, 113, 227, 0.3);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  background: rgba(0, 113, 227, 0.02);
  transition: all 0.2s ease;
}

.upload-box:hover {
  background: rgba(0, 113, 227, 0.06);
}

.upload-title {
  font-weight: 600;
  font-size: 0.9rem;
}

.upload-sub {
  font-size: 0.75rem;
  color: #86868b;
}

.mapping-box {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label, .map-item label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #86868b;
}

.mapping-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 14px;
}
</style>
