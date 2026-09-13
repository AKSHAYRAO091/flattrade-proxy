from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# Render ke "Environment" tab mein RELAY_SECRET naam ki env variable add kar dena
# (koi bhi lamba random string) — taaki koi aur is public URL ko misuse na kar sake.
RELAY_SECRET = os.environ.get("RELAY_SECRET", "")


@app.get("/")
def check_ip():
    current_ip = requests.get("https://api.ipify.org").text
    return {
        "status": "Proxy Server Active",
        "render_fixed_ip": current_ip,
    }


@app.post("/forward_order")
async def forward_order(request: Request):
    try:
        body = await request.json()

        if RELAY_SECRET and body.get("secret") != RELAY_SECRET:
            return {"error": "unauthorized"}

        broker_url = body.get("broker_url")
        payload    = body.get("payload")
        mode       = body.get("mode", "form")
        headers    = body.get("headers") or {}
        timeout    = body.get("timeout", 15)

        if not broker_url:
            return {"error": "broker_url missing"}

        if mode == "json":
            res = requests.post(broker_url, json=payload, headers=headers, timeout=timeout)
        else:
            res = requests.post(broker_url, data=payload, headers=headers, timeout=timeout)

        return {
            "status_code": res.status_code,
            "text": res.text,
        }
    except Exception as e:
        return {"error": str(e)}
