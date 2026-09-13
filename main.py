from fastapi import FastAPI, Request
import requests

app = FastAPI()

@app.get("/")
def check_ip():
    current_ip = requests.get('https://api.ipify.org').text
    return {
        "status": "Proxy Server Active",
        "render_fixed_ip": current_ip
    }

@app.post("/forward_order")
async def forward_order(request: Request):
    try:
        body = await request.json()
        broker_url = body.get("broker_url")
        payload = body.get("payload")
        
        headers = {'Content-Type': 'application/json'}
        res = requests.post(broker_url, json=payload, headers=headers, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}
