"""Local-only WildSense server with optional Ollama integration."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
HOST, PORT = "127.0.0.1", 8765
OLLAMA = "http://127.0.0.1:11434"
MODEL = "llama3.2:1b"
SYSTEM = ("You are WildSense, a practical nature-observation guide. Offer concise, safe, low-cost outdoor activities. "
          "Never encourage touching, tasting, collecting, feeding, or disturbing unknown wildlife or plants. "
          "Recommend observing animals from a respectful distance, staying in public/safe places, following local rules, "
          "and involving a trusted adult where appropriate. Be honest about uncertainty and do not claim certain species "
          "identifications from vague descriptions. This is educational guidance, not emergency advice.")

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        print("[WildSense] " + (fmt % args))

    def _json(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/status":
            try:
                req = Request(OLLAMA + "/api/tags", headers={"Accept": "application/json"})
                with urlopen(req, timeout=2) as res:
                    tags = json.loads(res.read().decode("utf-8"))
                names = [m.get("name", "") for m in tags.get("models", [])]
                installed = any(n == MODEL or n.startswith(MODEL + ":") for n in names)
                self._json(200, {"ollama": True, "available": installed, "model": MODEL, "installedModels": names})
            except Exception:
                self._json(200, {"ollama": False, "available": False, "model": MODEL, "installedModels": []})
            return
        if self.path.startswith("/api/"):
            self._json(404, {"error": "Unknown API endpoint"})
            return
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/chat":
            self._json(404, {"error": "Unknown API endpoint"})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size < 1 or size > 12000:
                self._json(400, {"error": "Message size is invalid (maximum 12 KB)."})
                return
            payload = json.loads(self.rfile.read(size).decode("utf-8"))
            prompt = str(payload.get("prompt", "")).strip()
            if not prompt or len(prompt) > 1200:
                self._json(400, {"error": "Enter a message of 1–1200 characters."})
                return
            request_data = json.dumps({
                "model": MODEL,
                "system": SYSTEM,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.65, "num_predict": 350}
            }).encode("utf-8")
            req = Request(OLLAMA + "/api/generate", data=request_data,
                          headers={"Content-Type": "application/json"}, method="POST")
            with urlopen(req, timeout=180) as res:
                result = json.loads(res.read().decode("utf-8"))
            self._json(200, {"response": result.get("response", "").strip(), "model": MODEL})
        except HTTPError as exc:
            self._json(502, {"error": f"Ollama returned HTTP {exc.code}. Check the model and Ollama status."})
        except URLError:
            self._json(503, {"error": "Cannot connect to Ollama at 127.0.0.1:11434."})
        except (ValueError, json.JSONDecodeError):
            self._json(400, {"error": "Invalid JSON request."})
        except Exception as exc:
            self._json(500, {"error": f"Local request failed: {type(exc).__name__}."})

if __name__ == "__main__":
    print(f"WildSense is running at http://{HOST}:{PORT}")
    print("Keep this window open while using the site. Press Ctrl+C to stop.")
    try:
        ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nWildSense stopped.")
