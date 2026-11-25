"""Servidor HTTP local y comprobaciones compartidas por las pruebas de servicios."""
import json
import time
from email import message_from_bytes
from email.policy import default as email_policy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from kink import di

import apimarket
from apimarket.api_market_client import ApiMarketClient
from apimarket.cli import main
from apimarket.services import REGISTRY

OK = {"status": 200, "data": {"ok": True}}


class Server(ThreadingHTTPServer):
    def __init__(self):
        super().__init__(("127.0.0.1", 0), Handler)
        self.requests = []
        self.delay = 0  # segundos antes de responder
        self.reply = (200, "application/json", b'{"status":200,"data":{"ok":true}}')

    @property
    def last(self):
        return self.requests[-1]


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _handle(self):
        url = urlsplit(self.path)
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        self.server.requests.append({
            "method": self.command,
            "path": url.path,
            "query": {key: values[0] for key, values in parse_qs(url.query).items()},
            "headers": {key.lower(): value for key, value in self.headers.items()},
            "body": body,
        })
        time.sleep(self.server.delay)
        status, content_type, payload = self.server.reply
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Retry-After", "0")
        self.end_headers()
        self.wfile.write(payload)

    do_GET = do_POST = do_PUT = do_DELETE = _handle

    def log_message(self, *args):
        pass


def connect(server, **options):
    apimarket.assemble(**options)
    # Las llaves vienen fijas para que un .env local no se use en las pruebas.
    di["API_MARKET_API_KEY"] = "llave-de-prueba"
    di["IDSEPRO_BEARER_TOKEN"] = di["IDSEPRO_API_KEY"] = "llave-de-prueba"
    url = f"http://127.0.0.1:{server.server_port}"
    client = di[ApiMarketClient]
    client.request_adapter.base_url = url
    client.path_parameters["idsepro_base_url"] = url  # IDSE Pro usa su propio dominio


def multipart(request):
    header = f"Content-Type: {request['headers']['content-type']}\r\n\r\n".encode()
    message = message_from_bytes(header + request["body"], policy=email_policy)
    return {part.get_param("name", header="content-disposition"): part.get_payload(decode=True)
            for part in message.iter_parts()}


def assert_request(request, expected):
    assert request["method"] == expected.get("method", "POST")
    assert request["path"] == expected["path"]
    assert request["query"] == expected.get("query", {})
    assert request["headers"]["authorization"] == "Bearer llave-de-prueba"
    if "json" in expected:
        assert request["headers"]["content-type"] == "application/json"
        assert json.loads(request["body"]) == expected["json"]
    elif "files" in expected:
        assert multipart(request) == expected["files"]
    else:
        assert request["body"] == b""


def cli_arguments(arguments, directory):
    result = []
    for name, value in arguments.items():
        flag = "--" + name.replace("_", "-").replace("privateKey", "private-key")
        if isinstance(value, bytes):
            path = directory / name
            path.write_bytes(value)
            value = str(path)
        elif name in ("permissions", "complementos"):
            value = ",".join(value)
        elif isinstance(value, (dict, list)):
            value = json.dumps(value)
        result += [flag, str(value)]
    return result


def check_request(server, name, arguments, expected):
    """La función envía la petición esperada y devuelve el JSON de la respuesta."""
    assert getattr(apimarket, name)(**arguments) == OK
    assert len(server.requests) == 1
    assert_request(server.last, expected)


def check_cli(server, directory, capsys, name, arguments, expected):
    """El comando de la CLI envía la misma petición que la función."""
    spec = next(s for s in REGISTRY if s.function.__name__ == name)
    main([spec.group, spec.command, *cli_arguments(arguments, directory)])
    assert json.loads(capsys.readouterr().out) == OK
    assert_request(server.last, expected)
