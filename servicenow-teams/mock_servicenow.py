#!/usr/bin/env python3
"""Mock ServiceNow instance (Table API) plus a mock Teams incoming webhook.

Run:  python3 mock_servicenow.py [--port 8080]
  ServiceNow URL : http://localhost:8080
  Teams webhook  : http://localhost:8080/teams-webhook   (prints payloads, returns 200)
"""
import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

INCIDENTS = [
    {"sys_id": "a1b2c3", "number": "INC0010001", "short_description": "VPN unreachable for Sao Paulo office",
     "priority": "1", "state": "2", "opened_at": "2026-10-06 08:12:00", "assigned_to": "Ana Silva"},
    {"sys_id": "d4e5f6", "number": "INC0010002", "short_description": "Oracle EPM login timeout",
     "priority": "2", "state": "1", "opened_at": "2026-10-06 09:03:00", "assigned_to": ""},
    {"sys_id": "g7h8i9", "number": "INC0010003", "short_description": "Printer offline, floor 3",
     "priority": "4", "state": "1", "opened_at": "2026-10-06 09:45:00", "assigned_to": "Joao Costa"},
]


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = urlparse(self.path)
        qs = parse_qs(url.query)
        if url.path == "/api/now/table/incident":
            rows = INCIDENTS
            # minimal support for sysparm_query=priority=1 and sysparm_limit
            for clause in qs.get("sysparm_query", [""])[0].split("^"):
                if "=" in clause:
                    k, v = clause.split("=", 1)
                    rows = [r for r in rows if str(r.get(k)) == v]
            limit = int(qs.get("sysparm_limit", [len(rows)])[0])
            return self._send(200, {"result": rows[:limit]})
        self._send(404, {"error": {"message": "Not found"}})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        if self.path == "/teams-webhook":
            print("\n--- Teams webhook received ---\n" + body, flush=True)
            return self._send(200, {"ok": True})
        self._send(404, {"error": {"message": "Not found"}})

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8080)))
    ap.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"))
    args = ap.parse_args()
    port = args.port
    print(f"Mock ServiceNow: http://localhost:{port}  |  Teams webhook: http://localhost:{port}/teams-webhook")
    HTTPServer((args.host, port), Handler).serve_forever()
