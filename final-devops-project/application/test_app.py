import importlib.util
import pathlib
import unittest
from http.client import HTTPConnection
from threading import Thread

MODULE = pathlib.Path(__file__).with_name("app.py")
spec = importlib.util.spec_from_file_location("homework_app", MODULE)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class ApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = app.ThreadingHTTPServer(("127.0.0.1", 0), app.Handler)
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()
        cls.server.server_close()

    def request(self, path):
        connection = HTTPConnection("127.0.0.1", self.server.server_port, timeout=2)
        try:
            connection.request("GET", path)
            response = connection.getresponse()
            return response.status, response.read()
        finally:
            connection.close()

    def test_root(self):
        status, body = self.request("/")
        self.assertEqual(status, 200)
        self.assertIn("Hello", body.decode())

    def test_health(self):
        status, body = self.request("/health")
        self.assertEqual(status, 200)
        self.assertEqual(body, b'{"status":"healthy"}')

    def test_metrics(self):
        status, body = self.request("/metrics")
        self.assertEqual(status, 200)
        self.assertIn(b"homework_http_requests_total", body)

    def test_not_found(self):
        status, _ = self.request("/missing")
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
