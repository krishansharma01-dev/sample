<template>
  <div class="csp-tool-container apple-card">
    <div class="tool-header">
      <div class="header-titles">
        <div class="active-ds-tag">
          <span class="active-dot">🟢</span>
          <span>Optimizing Active Source: <strong>{{ activeSourceName }}</strong></span>
        </div>
        <h2>Stock Cuts Waste Planner</h2>
        <p class="subtitle">Plan 1-D & 2-D stock cutting to minimize waste with Google OR-Tools engine.</p>
      </div>
      <div class="tab-controls">
        <button
          class="apple-btn"
          :class="mode === '1d' ? 'apple-btn-primary' : 'apple-btn-outline'"
          @click="setMode('1d')"
        >
          Rods & Rolls (1-D)
        </button>
        <button
          class="apple-btn"
          :class="mode === '2d' ? 'apple-btn-primary' : 'apple-btn-outline'"
          @click="setMode('2d')"
        >
          Rectangular Sheets (2-D)
        </button>
      </div>
    </div>

    <div class="tool-body">
      <!-- Input Panel Left -->
      <div class="panel-left">
        <!-- Child Rolls / Sheets -->
        <div class="input-card apple-card">
          <div class="card-head">
            <h4>{{ mode_data.childTitle }}</h4>
            <div class="head-actions">
              <button class="apple-btn apple-btn-outline btn-xs" @click="addRowToChilds">+ Add Row</button>
              <button class="apple-btn apple-btn-outline btn-xs danger-text" @click="clearChildData(true)">Clear</button>
            </div>
          </div>
          <p class="help-text">{{ mode_data.childMessage }}</p>

          <p v-if="mode_data.childErrors" class="error-msg">{{ mode_data.childErrors }}</p>

          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Width</th>
                  <th v-if="mode === '2d'">Height</th>
                  <th>Quantity</th>
                  <th v-if="mode === '1d' && mode_data.result">Color</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(child, index) in mode_data.childs" :key="index">
                  <td class="index-col">{{ index + 1 }}</td>
                  <td><input class="apple-input table-input" type="text" v-model="child.width" placeholder="e.g. 33" /></td>
                  <td v-if="mode === '2d'"><input class="apple-input table-input" type="text" v-model="child.height" placeholder="e.g. 20" /></td>
                  <td><input class="apple-input table-input" type="text" v-model="child.quantity" placeholder="e.g. 5" /></td>
                  <td v-if="mode === '1d' && mode_data.result" :style="getColor(child.width)" class="color-cell"></td>
                  <td>
                    <button class="icon-btn danger" @click="removeRow(index, false)">✕</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Stock / Parent Roll -->
        <div class="input-card apple-card">
          <div class="card-head">
            <h4>{{ mode_data.parentTitle }}</h4>
            <div class="head-actions">
              <button class="apple-btn apple-btn-outline btn-xs danger-text" @click="clearParentData(true)">Clear</button>
            </div>
          </div>
          <p class="help-text">{{ mode_data.parentMessage }}</p>

          <p v-if="mode_data.parentErrors" class="error-msg">{{ mode_data.parentErrors }}</p>

          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Width</th>
                  <th v-if="mode === '2d'">Height</th>
                  <th>Quantity</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(parent, index) in mode_data.parents" :key="index">
                  <td class="index-col">{{ index + 1 }}</td>
                  <td><input class="apple-input table-input" type="text" v-model="parent.width" placeholder="e.g. 120" /></td>
                  <td v-if="mode === '2d'"><input class="apple-input table-input" type="text" v-model="parent.height" placeholder="e.g. 100" /></td>
                  <td><input class="apple-input table-input" disabled type="text" v-model="parent.quantity" /></td>
                  <td>
                    <button class="icon-btn danger" @click="removeRow(index, true)">✕</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Output Panel Right -->
      <div class="panel-right">
        <div class="controls-card apple-card">
          <h4>Optimization Mode</h4>
          <div class="radio-options">
            <label class="radio-label">
              <input type="radio" value="exactCuts" v-model="cutStyle" />
              <span>Exact Cuts</span>
            </label>
            <label class="radio-label">
              <input type="radio" value="minWaste" v-model="cutStyle" />
              <span>Minimize Waste</span>
            </label>
          </div>

          <div class="action-buttons">
            <button class="apple-btn apple-btn-primary full-width" :disabled="cutButtonDisabled" @click="cutSheets()">
              ✂️ Run Optimization Engine
            </button>
            <button class="apple-btn apple-btn-outline" :disabled="cutButtonDisabled" @click="reset()">
              Reset Inputs
            </button>
          </div>
        </div>

        <div class="result-card apple-card">
          <div class="result-header">
            <h4>Visualization & Solution</h4>
            <span v-if="mode_data.result" class="badge-status badge-success">
              {{ mode_data.result.statusName }}
            </span>
          </div>

          <div id="d3_area" class="d3-canvas-area">
            <svg class="d3-svg"></svg>
          </div>

          <div v-if="mode_data.result" class="cut-details">
            <div class="details-head">
              <h5>Cut Details</h5>
              <button class="apple-btn apple-btn-outline btn-xs" @click="downloadCsv()">Download CSV</button>
            </div>
            <p class="summary-line">Stock required: <strong>{{ mode_data.result.solutions.length }}</strong> units</p>

            <table v-if="mode === '1d'" class="data-table">
              <thead>
                <tr>
                  <th>Stock #</th>
                  <th>Usage</th>
                  <th>Cut Widths</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(bigRoll, idx) in mode_data.result.solutions" :key="idx">
                  <td>{{ idx + 1 }}</td>
                  <td>{{ getPercentageUtilization(bigRoll[0]) }}%</td>
                  <td>{{ bigRoll[1].join(", ") }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import axios from "axios";
import { API_BASE } from "../apiConfig";

export default {
  name: "CspTool",
  props: {
    msg: String
  },
  data() {
    return {
      mode: "1d",
      cutStyle: "exactCuts",
      cutButtonDisabled: false,
      activeSourceName: "Default",

      mode1d: {
        childs: [{ width: "33", quantity: "5" }, { width: "18", quantity: "4" }],
        parents: [{ width: "120", quantity: "1" }],
        childErrors: null,
        parentErrors: null,
        result: null,
        childTitle: "Small Rods / Rolls to Cut",
        childMessage: "Specify widths and quantities required.",
        parentTitle: "Stock Rod Size",
        parentMessage: "Specify stock item length available."
      },

      mode2d: {
        childs: [{ width: "30", height: "20", quantity: "4" }],
        parents: [{ width: "100", height: "80", quantity: "1" }],
        childErrors: null,
        parentErrors: null,
        result: null,
        childTitle: "Small Rectangular Sheets",
        childMessage: "Specify width, height, and quantities.",
        parentTitle: "Stock Sheet Rectangles",
        parentMessage: "Specify main stock sheet dimensions."
      },

      mode_data: null,

      colors: [
        "#1abc9c", "#16a085", "#f1c40f", "#f39c12",
        "#2ecc71", "#27ae60", "#e67e22", "#d35400",
        "#3498db", "#2980b9", "#e74c3c", "#c0392b"
      ],
      wasteColor: "#7f8c8d"
    };
  },
  beforeMount() {
    this.setMode("1d");
    this.fetchActiveSource();
  },
  methods: {
    async fetchActiveSource() {
      try {
        const res = await axios.get(`${API_BASE}/api/data-sources`);
        if (res.data && res.data.activeSource) {
          this.activeSourceName = res.data.activeSource.name;
          // Pre-fill inputs from active source rows if available
          if (res.data.activeSource.rows && res.data.activeSource.rows.length > 0) {
            this.mode1d.childs = res.data.activeSource.rows.map(r => ({
              width: String(r.width || 33),
              quantity: String(r.quantity || 5)
            }));
          }
        }
      } catch (e) {
        console.error("Failed to load active dataset for optimizer", e);
      }
    },
    setMode(newMode) {
      this.mode = newMode;
      if (newMode === "1d") {
        if (this.mode_data != null) this.mode2d = this.mode_data;
        this.mode_data = this.mode1d;
        this.draw1d();
      } else {
        if (this.mode_data != null) this.mode1d = this.mode_data;
        this.mode_data = this.mode2d;
        this.draw2d();
      }
    },
    addRowToChilds() {
      if (this.mode === "1d") {
        this.mode_data.childs.push({ width: "", quantity: "" });
      } else {
        this.mode_data.childs.push({ width: "", height: "", quantity: "" });
      }
    },
    clearChildData(askConfirm) {
      if (askConfirm && !confirm("Empty all items in this table?")) return;
      this.mode_data.childs = this.mode === "1d"
        ? [{ width: "", quantity: "" }]
        : [{ width: "", height: "", quantity: "" }];
      this.mode_data.childErrors = null;
      this.mode_data.result = null;
      this.clearTheDrawing();
    },
    clearParentData(askConfirm) {
      if (askConfirm && !confirm("Reset stock table?")) return;
      this.mode_data.parents = this.mode === "1d"
        ? [{ width: "", quantity: "1" }]
        : [{ width: "", height: "", quantity: "1" }];
      this.mode_data.parentErrors = null;
      this.mode_data.result = null;
      this.clearTheDrawing();
    },
    removeRow(idx, is_parent) {
      if (is_parent) {
        this.clearParentData(false);
        return;
      }
      if (this.mode_data.childs.length > 1) {
        this.mode_data.childs.splice(idx, 1);
      } else {
        this.clearChildData(false);
      }
    },
    cutSheets() {
      this.clearTheDrawing();
      this.mode_data.result = null;
      if (!this.validate()) return;
      this.sendReq();
    },
    validate() {
      this.mode_data.childErrors = null;
      this.mode_data.parentErrors = null;

      const labels = this.mode === "2d" ? ["width", "height", "quantity"] : ["width", "quantity"];
      for (let i = 0; i < this.mode_data.childs.length; i++) {
        const child = this.mode_data.childs[i];
        for (let j = 0; j < labels.length; j++) {
          let val = parseInt(child[labels[j]]);
          if (!Number.isInteger(val) || val < 1) {
            this.mode_data.childErrors = `Row #${i + 1}: "${labels[j]}" must be 1 unit or more.`;
            return false;
          }
        }
      }

      for (let i = 0; i < this.mode_data.parents.length; i++) {
        const parent = this.mode_data.parents[i];
        for (let j = 0; j < labels.length - 1; j++) {
          let val = parseInt(parent[labels[j]]);
          if (!Number.isInteger(val) || val < 1) {
            this.mode_data.parentErrors = `Row #${i + 1}: "${labels[j]}" must be 1 unit or more.`;
            return false;
          }
        }
      }

      return true;
    },
    prepareDataToSend1D() {
      let newChilds = [];
      this.mode_data.childs.forEach(c => {
        newChilds.push([parseInt(c.quantity), parseInt(c.width)]);
      });
      let newParents = [];
      this.mode_data.parents.forEach(p => {
        newParents.push([1, parseInt(p.width)]);
      });
      return { child_rolls: newChilds, parent_rolls: newParents, cutStyle: this.cutStyle };
    },
    prepareDataToSend2D() {
      let newChilds = [];
      this.mode_data.childs.forEach(c => {
        const qty = parseInt(c.quantity);
        const item = [parseInt(c.width), parseInt(c.height)];
        for (let q = 0; q < qty; q++) newChilds.push(item);
      });
      let newParents = [];
      this.mode_data.parents.forEach(p => {
        newParents.push([parseInt(p.width), parseInt(p.height)]);
      });
      return { child_rects: newChilds, parent_rects: newParents };
    },
    sendReq() {
      const url = this.mode === "1d" ? `${API_BASE}/stocks_1d` : `${API_BASE}/stocks_2d`;
      this.cutButtonDisabled = true;
      const payload = this.mode === "1d" ? this.prepareDataToSend1D() : this.prepareDataToSend2D();

      axios.post(url, payload)
        .then(res => {
          this.cutButtonDisabled = false;
          this.mode_data.result = res.data;
          if (this.mode_data.result && this.mode_data.result.statusName) {
            this.mode_data.result.statusName = this.mode_data.result.statusName.toLowerCase();
          }
          if (this.mode === "1d") {
            this.draw1d();
          } else {
            this.draw2d();
          }
        })
        .catch(err => {
          this.cutButtonDisabled = false;
          console.error("Server request error", err);
          alert("Error contacting optimization server. Please check backend server.");
        });
    },
    sortBigRolls(bigRolls) {
      bigRolls = bigRolls.sort((a, b) => a[0] - b[0]);
      for (let i = 0; i < bigRolls.length; i++) {
        let smallRolls = bigRolls[i][1].sort((a, b) => a - b);
        bigRolls[i][1] = smallRolls;
      }
      return bigRolls;
    },
    getColorDict() {
      if (!this.mode_data.result) return {};
      const bigRolls = this.mode_data.result.solutions;
      let set = new Set();
      bigRolls.forEach(r => r[1].forEach(s => set.add(s)));
      let unique = Array.from(set);
      let dict = {};
      unique.forEach((u, idx) => {
        dict[u] = this.colors[idx % this.colors.length];
      });
      return dict;
    },
    getColor(w) {
      const dict = this.getColorDict();
      return { backgroundColor: dict[w] || "#ccc" };
    },
    clearTheDrawing() {
      d3.selectAll("#d3_area svg > *").remove();
    },
    draw1d() {
      this.clearTheDrawing();
      if (!this.mode_data.result) return;
      const bigRolls = this.sortBigRolls(this.mode_data.result.solutions);
      this.mode_data.result.solutions = bigRolls;
      const colorDict = this.getColorDict();
      const parentWidth = parseInt(this.mode_data.parents[0].width);

      const graphWidth = document.getElementById("d3_area").clientWidth || 320;
      let xScale = d3.scaleLinear().domain([0, parentWidth]).range([0, graphWidth]);
      let yScale = d3.scaleBand().domain(d3.range(bigRolls.length)).range([0, Math.max(180, 40 * bigRolls.length)]);

      let svg = d3.select("#d3_area svg");
      svg.attr("width", graphWidth).attr("height", Math.max(200, 42 * bigRolls.length));

      for (let i = 0; i < bigRolls.length; i++) {
        const unusedWidth = bigRolls[i][0];
        const smallRolls = bigRolls[i][1];
        let x1 = 0;
        let y1 = yScale(i);

        for (let j = 0; j < smallRolls.length; j++) {
          const smallRoll = smallRolls[j];
          const w = xScale(smallRoll);
          let g = svg.append("g").attr("transform", `translate(${x1},${y1})`);
          g.append("rect")
            .attr("fill", colorDict[smallRoll])
            .attr("width", Math.max(0, w - 1))
            .attr("height", yScale.bandwidth() - 4)
            .attr("rx", 3);
          g.append("text")
            .attr("fill", "white")
            .attr("font-size", "11px")
            .attr("x", 4)
            .attr("y", yScale.bandwidth() / 2)
            .attr("dy", "0.3em")
            .text(smallRoll);
          x1 += w;
        }

        if (unusedWidth > 0) {
          const wUnused = xScale(unusedWidth);
          let g = svg.append("g").attr("transform", `translate(${x1},${y1})`);
          g.append("rect")
            .attr("fill", this.wasteColor)
            .attr("width", Math.max(0, wUnused - 1))
            .attr("height", yScale.bandwidth() - 4)
            .attr("rx", 3);
          g.append("text")
            .attr("fill", "white")
            .attr("font-size", "11px")
            .attr("x", 4)
            .attr("y", yScale.bandwidth() / 2)
            .attr("dy", "0.3em")
            .text(Math.round(unusedWidth));
        }
      }
    },
    draw2d() {
      this.clearTheDrawing();
      if (!this.mode_data.result) return;
      const solutions = this.mode_data.result.solutions;
      const parentWidth = parseInt(this.mode_data.parents[0].width);
      const parentHeight = parseInt(this.mode_data.parents[0].height);
      const graphWidth = document.getElementById("d3_area").clientWidth || 320;
      const graphHeight = 300;

      let xScale = d3.scaleLinear().domain([0, parentWidth]).range([0, graphWidth]);
      let yScale = d3.scaleLinear().domain([0, parentHeight]).range([0, graphHeight]);

      let svg = d3.select("#d3_area svg").attr("width", graphWidth).attr("height", graphHeight);

      if (solutions.length > 0) {
        const sol = solutions[0];
        sol.forEach((rect, idx) => {
          let x1 = rect[0], y1 = rect[1], x2 = rect[2], y2 = rect[3];
          let w = Math.abs(x2 - x1);
          let h = Math.abs(y2 - y1);

          let g = svg.append("g");
          g.append("rect")
            .attr("x", xScale(x1))
            .attr("y", yScale(y1))
            .attr("width", xScale(w))
            .attr("height", yScale(h))
            .attr("fill", this.colors[idx % this.colors.length])
            .attr("stroke", "#fff")
            .attr("rx", 4);

          g.append("text")
            .attr("x", xScale(x1) + 4)
            .attr("y", yScale(y1) + 16)
            .attr("fill", "#fff")
            .attr("font-size", "10px")
            .text(`${w}x${h}`);
        });
      }
    },
    reset() {
      if (confirm("Reset all inputs?")) {
        this.clearChildData(false);
        this.clearParentData(false);
      }
    },
    getPercentageUtilization(unusedWidth) {
      let pWidth = parseInt(this.mode_data.parents[0].width);
      let usedWidth = Math.abs(pWidth - unusedWidth);
      let pct = (usedWidth * 100) / pWidth;
      return Math.round(pct * 100) / 100;
    },
    downloadCsv() {
      if (!this.mode_data.result || !this.mode_data.result.solutions) return;
      let rows = [["Stock", "Usage", "Width of Cuts"]];
      this.mode_data.result.solutions.forEach((r, idx) => {
        rows.push([idx + 1, this.getPercentageUtilization(r[0]) + "%", r[1].join(",")]);
      });
      const csvStr = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\n");
      let link = document.createElement("a");
      link.setAttribute("href", encodeURI(csvStr));
      link.setAttribute("download", `PLAYX_Waste_Optimization_${Date.now()}.csv`);
      document.body.appendChild(link);
      link.click();
    }
  }
};
</script>

<style scoped>
.csp-tool-container {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.active-ds-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  color: #86868b;
  margin-bottom: 4px;
}

.tool-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.tool-header h2 {
  margin: 0;
  font-size: 1.4rem;
}

.subtitle {
  color: #86868b;
  font-size: 0.85rem;
  margin-top: 4px;
}

.tab-controls {
  display: flex;
  gap: 8px;
}

.tool-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.panel-left, .panel-right {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input-card, .controls-card, .result-card {
  padding: 18px;
}

.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-head h4 {
  margin: 0;
  font-size: 1rem;
}

.help-text {
  font-size: 0.8rem;
  color: #86868b;
  margin: 4px 0 12px 0;
}

.error-msg {
  color: #ff3b30;
  font-size: 0.8rem;
  font-weight: 600;
}

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  font-size: 0.75rem;
  color: #86868b;
  text-align: left;
  padding: 6px 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.data-table td {
  padding: 6px 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.table-input {
  padding: 6px 10px;
  font-size: 0.85rem;
}

.color-cell {
  width: 20px;
  border-radius: 4px;
}

.icon-btn {
  background: none;
  border: none;
  font-size: 0.9rem;
  cursor: pointer;
  color: #86868b;
}

.icon-btn.danger:hover {
  color: #ff3b30;
}

.btn-xs {
  padding: 4px 10px;
  font-size: 0.75rem;
}

.danger-text {
  color: #ff3b30;
}

.radio-options {
  display: flex;
  gap: 20px;
  margin: 12px 0 16px 0;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  cursor: pointer;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.full-width {
  flex: 1;
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.result-header h4 {
  margin: 0;
}

.d3-canvas-area {
  width: 100%;
  min-height: 200px;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 12px;
  padding: 10px;
  box-sizing: border-box;
}

.cut-details {
  margin-top: 16px;
}

.details-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.summary-line {
  font-size: 0.85rem;
  margin: 6px 0 10px 0;
}

@media (max-width: 991px) {
  .tool-body {
    grid-template-columns: 1fr;
  }
}
</style>
