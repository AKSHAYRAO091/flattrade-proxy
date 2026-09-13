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

        # --- Security check ---
        if RELAY_SECRET and body.get("secret") != RELAY_SECRET:
            return {"error": "unauthorized"}

        broker_url = body.get("broker_url")
        payload    = body.get("payload")
        # "form"  -> NorenAPI (Flattrade SDK) ke jData=...&jKey=... calls
        # "json"  -> daily token-exchange call (authapi.flattrade.in)
        mode    = body.get("mode", "form")
