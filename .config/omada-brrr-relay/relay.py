"""Relay Omada controller webhooks to brrr (https://brrr.now) push notifications.

Omada can only send its own JSON payload (or Google Chat's), while brrr
requires a `message` field. This accepts Omada's webhook POST, reshapes it
and forwards it to brrr. Standard library only.

Only reachable from containers on caddy.network: no published port and no
caddy labels.

Environment:
  BRRR_URL      https://api.brrr.now/v1/<secret>  (required)
  OMADA_SECRET  the webhook's Shared Secret from Omada (optional, recommended)
  PORT          listen port, default 8080
"""

import hmac
import json
import os
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BRRR_URL = os.environ["BRRR_URL"]
OMADA_SECRET = os.environ.get("OMADA_SECRET", "")
PORT = int(os.environ.get("PORT", "8080"))


def log(*args):
    print(*args, file=sys.stderr, flush=True)


def to_brrr(event):
    text = event.get("text") or event.get("description") or ""
    if isinstance(text, list):
        text = "\n".join(str(t) for t in text)
    site = event.get("Site") or event.get("site")
    return {
        "title": f"Omada: {site}" if site else "Omada",
        "message": text or json.dumps(event),
        "thread_id": "omada",
    }


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        try:
            event = json.loads(body)
        except ValueError:
            event = {"text": body.decode("utf-8", "replace")}

        # Omada sends the webhook's Shared Secret in the body (sic: "shardSecret")
        sent = str(event.pop("shardSecret", ""))
        if OMADA_SECRET and not hmac.compare_digest(sent, OMADA_SECRET):
            log("rejected: shared secret mismatch")
            self.send_response(403)
            self.end_headers()
            return

        log("omada:", json.dumps(event))

        req = urllib.request.Request(
            BRRR_URL,
            data=json.dumps(to_brrr(event)).encode(),
            # Cloudflare in front of brrr rejects urllib's default User-Agent
            headers={"Content-Type": "application/json", "User-Agent": "omada-brrr-relay/1.0"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = resp.status
        except urllib.error.HTTPError as e:
            status = e.code
            log("brrr error:", status, e.read().decode("utf-8", "replace"))
        except OSError as e:
            status = 502
            log("brrr unreachable:", e)

        # Tell Omada about failures so its retry policy kicks in.
        self.send_response(200 if status < 300 else 502)
        self.end_headers()

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    log(f"listening on :{PORT}")
    ThreadingHTTPServer(("", PORT), Handler).serve_forever()
