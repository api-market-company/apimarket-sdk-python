"""Muestra qué produce el SDK para cada código de error. No usa la red ni su llave.

    python tests/ver_errores.py              # en pantalla
    python tests/ver_errores.py reporte.md   # además, guarda un reporte
"""
import sys
import threading

import apimarket
from apimarket.errors import CATALOG

from error_scenarios import SCENARIOS
from support import Server, connect


def run(scenario):
    server = Server()
    threading.Thread(target=server.serve_forever, args=(0.01,), daemon=True).start()
    connect(server)
    scenario.setup(server)
    try:
        scenario.call()
        return None, server
    except Exception as error:
        return error, server
    finally:
        server.shutdown()
        server.server_close()


def main(report=None):
    results = {}
    for scenario in SCENARIOS:
        error, server = run(scenario)
        results[scenario.code] = (scenario, error, bool(server.requests))
    apimarket.assemble()

    lines = ["# Códigos de error del SDK, producidos con casos reales", "",
             "Las respuestas de la API son simuladas en un servidor local."]
    ok = 0
    for title, exception, codes in CATALOG:
        print(f"\n=== {title} ===")
        lines += ["", f"## {title}", "",
                  "| Código | Caso | Excepción | Mensaje | status | success | codigoValidacion | ¿Llamó a la API? |",
                  "|---|---|---|---|---|---|---|---|"]
        for code, _ in codes:
            scenario, error, sent = results[code]
            correct = getattr(error, "code", None) is code
            ok += correct
            message = getattr(error, "message", None) or str(error) or type(error).__name__
            extra = [getattr(error, name, None) for name in ("status", "success", "codigo_validacion")]
            print(f"{'OK   ' if correct else 'FALLA'} {code.value:28} {scenario.description}")
            print(f"      {type(error).__name__}: {message}")
            if extra[2]:
                print(f"      status={extra[0]} success={extra[1]} codigo_validacion={extra[2]}")
            cells = [f"`{code.value}`", scenario.description, f"`{type(error).__name__}`", message,
                     *("" if value is None else value for value in extra), "sí" if sent else "no"]
            lines.append("| " + " | ".join(str(c).replace("|", "/") for c in cells) + " |")
    summary = f"{ok} de {len(SCENARIOS)} códigos se produjeron como se esperaba."
    print(f"\n{summary}")
    lines += ["", f"**{summary}**"]
    if report:
        with open(report, "w", encoding="utf-8") as output:
            output.write("\n".join(lines) + "\n")
    return 0 if ok == len(SCENARIOS) else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:2]))
