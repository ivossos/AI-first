#!/usr/bin/env python3
"""Fetch ServiceNow incidents and post them to a Microsoft Teams incoming webhook.

Usage:
  python3 notify.py --instance-url https://dev12345.service-now.com --teams-webhook https://...
Env fallbacks: SERVICENOW_URL, TEAMS_WEBHOOK_URL, SERVICENOW_USER, SERVICENOW_PASSWORD
"""
import argparse
import base64
import json
import os
import urllib.request


def get(url, user, password):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    if user:
        req.add_header("Authorization", "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode())
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def post(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as r:
        return r.status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance-url", default=os.environ.get("SERVICENOW_URL"))
    ap.add_argument("--teams-webhook", default=os.environ.get("TEAMS_WEBHOOK_URL"))
    ap.add_argument("--query", default="priority=1")
    a = ap.parse_args()
    if not a.instance_url or not a.teams_webhook:
        ap.error("--instance-url and --teams-webhook are required")
    base = a.instance_url.rstrip("/")
    data = get(f"{base}/api/now/table/incident?sysparm_query={a.query}&sysparm_limit=10",
               os.environ.get("SERVICENOW_USER"), os.environ.get("SERVICENOW_PASSWORD"))
    for inc in data["result"]:
        text = f"**{inc['number']}** (P{inc['priority']}): {inc['short_description']}"
        status = post(a.teams_webhook, {"text": text})
        print(f"posted {inc['number']} -> HTTP {status}")


if __name__ == "__main__":
    main()
