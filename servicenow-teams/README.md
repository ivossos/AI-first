# ServiceNow -> Teams (with mock ServiceNow)

```
python3 mock_servicenow.py --port 8080 &
python3 notify.py --instance-url http://localhost:8080 --teams-webhook http://localhost:8080/teams-webhook
```
Swap in your real ServiceNow instance URL and Teams incoming webhook URL when ready
(set SERVICENOW_USER / SERVICENOW_PASSWORD for basic auth).

## Host publicly (Docker)
```
docker build -t mock-servicenow .
docker run -p 8080:8080 mock-servicenow
```
The container binds 0.0.0.0 and honors `PORT` (Render, Fly, Cloud Run, etc. set it automatically).
Public URLs: `https://<your-host>` (ServiceNow) and `https://<your-host>/teams-webhook`.
Note: the mock has no auth; anyone with the URL can read the sample data.
