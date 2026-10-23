from fastapi import FastAPI, Query
from network_check import check_port

app = FastAPI(title="Network Security Tool")


@app.get("/")
def home():
    return {"application": "network-security-tool", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/check")
def check(port: int = Query(..., ge=1, le=65535)):
    return {
        "host": "127.0.0.1",
        "port": port,
        "open": check_port("127.0.0.1", port),
    }
