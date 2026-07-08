# mitmproxy addon for CTF / authorized APK protocol observation.
# Usage: mitmproxy -s protocol_logger.py

from mitmproxy import http
import json
import base64
from pathlib import Path
from datetime import datetime

OUT = Path("network_events.jsonl")

KEYWORDS = [
    "sign", "signature", "token", "timestamp", "nonce", "device",
    "deviceid", "fingerprint", "android_id", "oaid", "imei", "model",
    "brand", "uid", "session", "key", "iv"
]


def maybe_text(content: bytes) -> str:
    try:
        return content.decode("utf-8", errors="replace")
    except Exception:
        return base64.b64encode(content).decode()


def request(flow: http.HTTPFlow):
    body = maybe_text(flow.request.raw_content or b"")
    lower = body.lower() + " " + str(flow.request.headers).lower() + " " + flow.request.pretty_url.lower()
    hits = [k for k in KEYWORDS if k in lower]
    event = {
        "time": datetime.utcnow().isoformat() + "Z",
        "type": "request",
        "method": flow.request.method,
        "url": flow.request.pretty_url,
        "headers": dict(flow.request.headers),
        "content_type": flow.request.headers.get("content-type", ""),
        "body_preview": body[:4096],
        "keyword_hits": hits,
    }
    with OUT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def response(flow: http.HTTPFlow):
    body = maybe_text(flow.response.raw_content or b"")
    event = {
        "time": datetime.utcnow().isoformat() + "Z",
        "type": "response",
        "status_code": flow.response.status_code,
        "url": flow.request.pretty_url,
        "headers": dict(flow.response.headers),
        "body_preview": body[:4096],
    }
    with OUT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
