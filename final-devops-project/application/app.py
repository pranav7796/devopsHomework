"""Small dependency-free HTTP service with optional PostgreSQL persistence."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock

request_count = 0
request_lock = Lock()


def record_visit():
    """Persist one visit if DATABASE_URL is configured."""
    url = os.getenv("DATABASE_URL")
    if not url:
        return None
    import psycopg
    with psycopg.connect(url, connect_timeout=2) as connection:
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS visits (id BIGSERIAL PRIMARY KEY)")
            cursor.execute("INSERT INTO visits DEFAULT VALUES RETURNING id")
            return cursor.fetchone()[0]


class Handler(BaseHTTPRequestHandler):
    def respond(self, status, body, content_type="application/json"):
        data = body if isinstance(body, bytes) else body.encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        global request_count
        with request_lock:
            request_count += 1
            current_count = request_count
        if self.path in ("/", "/api"):
            try:
                visit_id = record_visit()
            except Exception as exc:
                print(json.dumps({"event": "database_error", "error_type": type(exc).__name__}), flush=True)
                self.respond(503, '{"error":"database unavailable"}')
                return
            self.respond(200, json.dumps({"message": "Hello from the DevOps homework API", "visit_id": visit_id}))
        elif self.path == "/health":
            self.respond(200, '{"status":"healthy"}')
        elif self.path == "/metrics":
            self.respond(200, f"# HELP homework_http_requests_total Requests served by this process\n# TYPE homework_http_requests_total counter\nhomework_http_requests_total {current_count}\n", "text/plain; version=0.0.4")
        else:
            self.respond(404, '{"error":"not found"}')

    def log_message(self, fmt, *args):
        print(json.dumps({"event": "http", "message": fmt % args}), flush=True)


if __name__ == "__main__":
    ThreadingHTTPServer((os.getenv("BIND_HOST", "127.0.0.1"), int(os.getenv("PORT", "8000"))), Handler).serve_forever()
