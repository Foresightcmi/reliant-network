import urllib.request
import json

req = urllib.request.Request(
    "http://localhost:3000/api/admin/run-cron",
    data=b"{}",
    headers={"Content-Type": "application/json"}
)
res = json.loads(urllib.request.urlopen(req).read().decode())
print("Autonomous Cron Heartbeat Result:", json.dumps(res, indent=2))
