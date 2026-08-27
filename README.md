# PLAYX WASTE OPTIMISER

> Intelligent Waste Management & Waste Optimization Platform by **PLAYXCODE**

## Overview
**PLAYX Waste Optimiser** is an enterprise-grade software application designed to solve 1-Dimensional (1-D) and 2-Dimensional (2-D) Cutting Stock Problems (CSP) while minimizing waste and maximizing material utilization. Powered by **Google OR-Tools**, it features an Apple-inspired SaaS user interface, Google Sheets integration with data-safety validation, Gemini AI Assistant with agentic task execution, and Supabase/Firebase persistent memory capabilities.

---

## Features
- **Apple-Inspired UI/UX**: Minimalist, glassmorphic, responsive design suitable for Desktop, Tablet, and Mobile devices.
- **1-D & 2-D Optimization Engine**: High-performance linear programming and constraint solving (preserves Google OR-Tools algorithms).
- **Google Sheets Integration**: Connect spreadsheets, preview updates, validate operations, and write back results safely (**Preview → Validate → Execute → Verify**).
- **AI Assistant**: Conversational agent (ChatGPT-style) supporting tool orchestration (`get_dashboard_data`, `get_google_sheets`, `propose_sheet_update`, `get_optimization_results`).
- **Connection Manager**: Centralized interface to manage credentials for Google Sheets, Gemini API, Supabase, and Firebase with secret masking (`AIza••••••••XYZ`).
- **Activity & History Audit**: Complete logging of connections, optimizations, and data modifications without exposing credentials.
- **PLAYXCODE Branding & CTA Card**: Floating footer card with animated glowing button pointing to [https://playxcode.netlify.app](https://playxcode.netlify.app).

---

## System Architecture
```text
Frontend (Vue 3 / Apple UI System)
        │
        ▼
Backend API Server (Flask / Python)
        │
   ┌────┴───────────────────────────┬──────────────────────────┐
   ▼                                ▼                          ▼
Google OR-Tools               Google Sheets Service      Gemini AI & Agentic Tools
(1D / 2D Algorithms)          (Data Safety Layer)        (Safe Action Preview)
```

---

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+ / npm

### Environment Setup

1. Copy environment variables template:
   ```sh
   cp .env.example .env
   ```

2. Install Python Dependencies:
   ```sh
   pip install -r deployment/requirements.txt
   ```

3. Run Backend API Server:
   ```sh
   python3 deployment/server.py
   ```
   *The server runs on `http://localhost:5000`.*

4. Build & Run Frontend:
   ```sh
   cd deployment/frontend
   npm install
   NODE_OPTIONS=--openssl-legacy-provider npm run build
   ```
   *To start dev server:*
   ```sh
   NODE_OPTIONS=--openssl-legacy-provider npm run serve
   ```

---

## Testing & Verification
Run Python test suite:
```sh
python3 -m pytest tests/
```

Verify frontend production build:
```sh
cd deployment/frontend && NODE_OPTIONS=--openssl-legacy-provider npm run build
```

---

## Security Guidelines
- **No Secret Exposure**: Passwords, API keys, and OAuth tokens are never logged or stored in unencrypted client states.
- **Data Safety Protocol**: Spreadsheet modifications require explicit user preview & confirmation before execution.

---

## Creator Branding
- **Developed by**: PLAYXCODE
- **Website**: [https://playxcode.netlify.app](https://playxcode.netlify.app)
