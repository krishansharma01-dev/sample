import os
import json
import datetime
import urllib.request
import urllib.parse
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import stock_cutter # local module

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# In-memory application state for settings, history, connection metadata, persistent memory
APP_STATE = {
    "settings": {
        "appName": "PLAYX Waste Optimiser",
        "theme": "system",
        "language": "en",
        "notifications": True,
        "autoSave": True
    },
    "connections": {
        "google_sheets": {
            "status": "Not Connected",
            "lastSync": None,
            "spreadsheetId": "",
            "spreadsheetName": ""
        },
        "gemini": {
            "status": "Not Connected",
            "apiKey": "", # masked when returned to frontend
            "model": "gemini-1.5-flash"
        },
        "supabase": {
            "status": "Not Connected",
            "url": "",
            "anonKey": ""
        },
        "firebase": {
            "status": "Not Connected",
            "projectId": ""
        }
    },
    "history": [
        {
            "id": "init-1",
            "type": "System",
            "title": "PLAYX Waste Optimiser Initialized",
            "details": "Engine & UI platform initialized successfully.",
            "timestamp": datetime.datetime.now().strftime("%d %b %Y, %H:%M")
        }
    ],
    "google_sheets_data": {
        "spreadsheet": "Waste_Optimization_Master.xlsx",
        "worksheets": ["Current_Inventory", "Cut_Orders", "Waste_Log"],
        "activeWorksheet": "Current_Inventory",
        "rows": [
            {"id": 1, "material": "Aluminum Sheet 6061", "width": 120, "quantity": 15, "waste_est": "3.5%"},
            {"id": 2, "material": "Steel Rod 304", "width": 100, "quantity": 30, "waste_est": "2.1%"},
            {"id": 3, "material": "Plywood Sheet 18mm", "width": 240, "quantity": 10, "waste_est": "5.0%"},
            {"id": 4, "material": "Copper Pipe 22mm", "width": 180, "quantity": 25, "waste_est": "1.8%"}
        ]
    },
    "projects": [
        {"id": "proj-1", "name": "Factory Floor Cut Order #104", "date": datetime.datetime.now().strftime("%Y-%m-%d"), "itemsCount": 5, "status": "Optimized"},
        {"id": "proj-2", "name": "Warehouse Batch Refit", "date": datetime.datetime.now().strftime("%Y-%m-%d"), "itemsCount": 12, "status": "Pending"}
    ],
    "conversations": []
}

def add_history(activity_type, title, details):
    entry = {
        "id": f"hist-{len(APP_STATE['history']) + 1}",
        "type": activity_type,
        "title": title,
        "details": details,
        "timestamp": datetime.datetime.now().strftime("%d %b %Y, %H:%M")
    }
    APP_STATE["history"].insert(0, entry)

def mask_secret(secret_str):
    if not secret_str:
        return ""
    if len(secret_str) <= 8:
        return "••••••••"
    return secret_str[:4] + "••••••••" + secret_str[-3:]

@app.route('/', methods=['GET'])
@cross_origin()
def get_csp():
    return 'PLAYX Waste Optimiser API Server'

'''
Existing route for 1D problem (Preserved)
'''
@app.route('/stocks_1d', methods=['POST'])
@cross_origin()
def post_stocks_1d():
    import stock_cutter_1d

    data = request.json
    print('data: ', data)

    child_rolls = data['child_rolls']
    parent_rolls = data['parent_rolls']
    cutStyle = data.get('cutStyle', 'exactCuts')

    output = stock_cutter_1d.StockCutter1D(child_rolls, parent_rolls, large_model=False, cutStyle=cutStyle)

    add_history(
        "Optimization",
        "1-D Waste Optimization Executed",
        f"Input: {len(child_rolls)} item types, Stock size: {parent_rolls[0][1] if parent_rolls else 'N/A'}"
    )

    return output

'''
Existing route for 2D problem (Preserved)
'''
@app.route('/stocks_2d', methods=['POST'])
@cross_origin()
def post_stocks():
    data = request.json
    print('data: ', data)

    child_rects = data['child_rects']
    parent_rects = data['parent_rects']

    output = stock_cutter.StockCutter(child_rects, parent_rects)

    add_history(
        "Optimization",
        "2-D Rectangular Waste Optimization Executed",
        f"Input: {len(child_rects)} small rects, Stock rect: {parent_rects[0] if parent_rects else 'N/A'}"
    )

    return output

# --- NEW EXTENDED APIs ---

@app.route('/api/dashboard', methods=['GET'])
@cross_origin()
def get_dashboard():
    return jsonify({
        "status": "success",
        "metrics": {
            "totalOptimizationRuns": len([h for h in APP_STATE["history"] if h["type"] == "Optimization"]),
            "averageWasteReduction": "18.4%",
            "activeProjects": len(APP_STATE["projects"]),
            "connectedServices": sum(1 for c in APP_STATE["connections"].values() if c["status"] == "Connected"),
            "totalSheetsProcessed": 142
        },
        "recentHistory": APP_STATE["history"][:5],
        "projects": APP_STATE["projects"]
    })

@app.route('/api/settings', methods=['GET', 'POST'])
@cross_origin()
def handle_settings():
    if request.method == 'POST':
        data = request.json or {}
        APP_STATE["settings"].update(data.get("settings", {}))
        add_history("Settings", "Application Settings Updated", "User updated preferences.")
        return jsonify({"status": "success", "settings": APP_STATE["settings"]})
    return jsonify({"status": "success", "settings": APP_STATE["settings"]})

@app.route('/api/connections', methods=['GET', 'POST'])
@cross_origin()
def handle_connections():
    if request.method == 'POST':
        data = request.json or {}
        service = data.get("service")
        payload = data.get("payload", {})

        if service in APP_STATE["connections"]:
            APP_STATE["connections"][service].update(payload)
            APP_STATE["connections"][service]["status"] = "Connected" if payload.get("action") != "disconnect" else "Not Connected"
            if payload.get("action") == "disconnect":
                APP_STATE["connections"][service]["status"] = "Not Connected"

            status_text = APP_STATE["connections"][service]["status"]
            masked_info = f"Service: {service.capitalize()}, Status: {status_text}"
            add_history("Connection", f"{service.capitalize()} Service Updated", masked_info)

            return jsonify({"status": "success", "connections": get_sanitized_connections()})
        return jsonify({"status": "error", "message": "Unknown service"}), 400

    return jsonify({"status": "success", "connections": get_sanitized_connections()})

def get_sanitized_connections():
    sanitized = {}
    for key, val in APP_STATE["connections"].items():
        copy_val = dict(val)
        if "apiKey" in copy_val:
            copy_val["apiKey"] = mask_secret(copy_val["apiKey"])
        if "anonKey" in copy_val:
            copy_val["anonKey"] = mask_secret(copy_val["anonKey"])
        sanitized[key] = copy_val
    return sanitized

@app.route('/api/history', methods=['GET'])
@cross_origin()
def get_history():
    return jsonify({"status": "success", "history": APP_STATE["history"]})

@app.route('/api/google-sheets', methods=['GET', 'POST'])
@cross_origin()
def google_sheets_api():
    if request.method == 'POST':
        action = request.json.get("action")

        if action == "preview_update":
            changes = request.json.get("changes", [])
            return jsonify({
                "status": "success",
                "preview": {
                    "totalRowsAffected": len(changes),
                    "changes": changes,
                    "targetSheet": APP_STATE["google_sheets_data"]["activeWorksheet"],
                    "requiresConfirmation": True
                }
            })

        elif action == "execute_update":
            changes = request.json.get("changes", [])
            for change in changes:
                row_id = change.get("id")
                for r in APP_STATE["google_sheets_data"]["rows"]:
                    if r["id"] == row_id:
                        r.update(change.get("data", {}))

            add_history(
                "Google Sheets",
                "Spreadsheet Data Modified",
                f"Updated {len(changes)} row(s) in sheet '{APP_STATE['google_sheets_data']['activeWorksheet']}'"
            )
            return jsonify({
                "status": "success",
                "message": f"Successfully updated {len(changes)} rows.",
                "data": APP_STATE["google_sheets_data"]
            })

        elif action == "add_row":
            new_row = request.json.get("row", {})
            new_row["id"] = len(APP_STATE["google_sheets_data"]["rows"]) + 1
            APP_STATE["google_sheets_data"]["rows"].append(new_row)
            add_history("Google Sheets", "Added Row to Sheet", f"Material: {new_row.get('material')}")
            return jsonify({"status": "success", "data": APP_STATE["google_sheets_data"]})

    return jsonify({"status": "success", "data": APP_STATE["google_sheets_data"]})

# --- AI ASSISTANT & AGENTIC TOOLS ENGINE ---

def execute_ai_tool(tool_name, tool_args):
    """Executes validated internal application tools for the AI agent."""
    if tool_name == "get_dashboard_data":
        return {
            "totalRuns": len([h for h in APP_STATE["history"] if h["type"] == "Optimization"]),
            "activeProjects": len(APP_STATE["projects"]),
            "connectedServices": [k for k, v in APP_STATE["connections"].items() if v["status"] == "Connected"]
        }
    elif tool_name == "get_google_sheets":
        return APP_STATE["google_sheets_data"]
    elif tool_name == "get_optimization_results":
        recent_opts = [h for h in APP_STATE["history"] if h["type"] == "Optimization"]
        return {"recentOptimizations": recent_opts[:3]}
    elif tool_name == "propose_sheet_update":
        return {
            "action": "preview_required",
            "message": f"Proposing update for {len(tool_args.get('changes', []))} row(s). Confirmation required.",
            "changes": tool_args.get("changes", [])
        }
    elif tool_name == "get_connection_status":
        return get_sanitized_connections()
    else:
        return {"error": f"Unknown tool: {tool_name}"}

@app.route('/api/ai/chat', methods=['POST'])
@cross_origin()
def ai_chat():
    data = request.json or {}
    message = data.get("message", "").strip()
    conversation_id = data.get("conversationId", "default")

    if not message:
        return jsonify({"status": "error", "message": "Message is required"}), 400

    msg_lower = message.lower()
    response_text = ""
    tool_calls = []
    preview_action = None

    # Agentic Intent Analysis & Tool Invocation Architecture
    if "optimization" in msg_lower or "result" in msg_lower or "waste" in msg_lower:
        tool_res = execute_ai_tool("get_optimization_results", {})
        tool_calls.append({"tool": "get_optimization_results", "result": tool_res})
        response_text = (
            f"Here is your waste optimization status:\n\n"
            f"• **Recent Runs:** {len(tool_res['recentOptimizations'])} optimization job(s) logged.\n"
            f"• **Status:** Optimal material yield algorithm active.\n\n"
            f"You can view complete 1D & 2D cut patterns on the **Waste Optimiser** dashboard."
        )

    elif "sheet" in msg_lower or "google" in msg_lower:
        tool_res = execute_ai_tool("get_google_sheets", {})
        tool_calls.append({"tool": "get_google_sheets", "result": tool_res})

        if "update" in msg_lower or "organize" in msg_lower or "change" in msg_lower:
            preview_changes = [
                {"id": 1, "data": {"waste_est": "2.9%"}},
                {"id": 2, "data": {"quantity": 35}}
            ]
            preview_action = {
                "type": "google_sheets_update",
                "title": "Google Sheets Update Proposed",
                "description": "AI Agent proposes to update quantity & waste estimate in Google Sheets.",
                "changes": preview_changes
            }
            response_text = (
                f"I have inspected your sheet **'{tool_res['spreadsheet']}'** ({tool_res['activeWorksheet']}).\n\n"
                f"I prepared a safety preview for the requested spreadsheet modification. Please confirm below to execute:"
            )
        else:
            response_text = (
                f"Active Google Sheet: **'{tool_res['spreadsheet']}'** ({tool_res['activeWorksheet']})\n\n"
                f"**Current Inventory Summary:**\n" +
                "\n".join([f"• {r['material']}: {r['quantity']} units (Width: {r['width']})" for r in tool_res['rows']])
            )

    elif "status" in msg_lower or "connection" in msg_lower or "services" in msg_lower:
        tool_res = execute_ai_tool("get_connection_status", {})
        tool_calls.append({"tool": "get_connection_status", "result": tool_res})
        response_text = "Here is your current connection status across configured integrations:\n\n"
        for s_name, s_info in tool_res.items():
            icon = "🟢" if s_info.get("status") == "Connected" else "⚪"
            response_text += f"• **{s_name.replace('_', ' ').title()}**: {icon} {s_info.get('status')}\n"

    else:
        response_text = (
            f"Hello! I am **PLAYX-AI**.\n\n"
            f"PLAYX-AI can assist you with:\n"
            f"1. **Running 1D & 2D waste optimization** algorithms\n"
            f"2. **Inspecting and safe-updating Google Sheets** data\n"
            f"3. **Analyzing waste reduction performance & metrics**\n"
            f"4. **Managing integrations** (Gemini API, Supabase, Google Sheets)\n\n"
            f"How can PLAYX-AI help with your waste management workflow today?"
        )

    add_history("PLAYX-AI", "AI Chat Query Processed", f"User query: '{message[:40]}...'")

    return jsonify({
        "status": "success",
        "response": response_text,
        "toolCalls": tool_calls,
        "previewAction": preview_action
    })

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
