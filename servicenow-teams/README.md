# ServiceNow -> Teams (with mock ServiceNow)

```
python3 mock_servicenow.py --port 8080 &
python3 notify.py --instance-url http://localhost:8080 --teams-webhook http://localhost:8080/teams-webhook
```
Swap in your real ServiceNow instance URL and Teams incoming webhook URL when ready
(set SERVICENOW_USER / SERVICENOW_PASSWORD for basic auth).
