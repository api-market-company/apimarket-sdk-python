"""Reglas de los movimientos afiliatorios de IDSE, tomadas de la API."""
import re
from datetime import datetime

from apimarket import rules
from apimarket.validations import validate_curp, validate_nss

BAJA, MODIFICACION, REINGRESO = "2", "7", "8"
MOVEMENT_TYPES = (BAJA, MODIFICACION, REINGRESO)
LEAVE_REASONS = ("-", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A")
SALARY_TYPES = ("0", "1", "2")
WORKDAY_TYPES = ("0", "1", "2", "3", "4", "5", "6")
WORKER_TYPES = ("1", "2", "3", "4")
CREDENTIAL_FIELDS = ("userId", "password", "certificate", "privateKey")


def credentials(value) -> None:
    rules.mapping("credentials", value)
    for key in CREDENTIAL_FIELDS:
        name = f"credentials.{key}"
        if not rules.text(name, value.get(key)).isascii():
            rules.fail(name, "FORMAT", f"El parámetro '{name}' solo admite caracteres ASCII.")


def _choice(name: str, value, choices) -> str:
    if isinstance(value, int) and not isinstance(value, bool):
        value = str(value)
    return rules.option(name, value, choices)


def movements(value) -> None:
    for position, item in enumerate(rules.items("movimientos", value)):
        rules.mapping("movimientos", item)

        def label(key):
            return f"movimientos[{position}].{key}"

        rules.required(**{label("nss"): item.get("nss")})
        validate_nss(item["nss"])
        rules.text(label("nombre"), item.get("nombre"), max_length=27)
        rules.text(label("apellidoPaterno"), item.get("apellidoPaterno"), max_length=27)
        if item.get("apellidoMaterno"):
            rules.text(label("apellidoMaterno"), item["apellidoMaterno"], max_length=27)
        kind = _choice(label("tipoDeMovimiento"), item.get("tipoDeMovimiento"), MOVEMENT_TYPES)

        date_name = label("fechaDeMovimiento")
        date = rules.text(date_name, item.get("fechaDeMovimiento"))
        try:
            valid = bool(re.fullmatch(r"\d{2}-\d{2}-\d{4}", date)) and datetime.strptime(date, "%d-%m-%Y")
        except ValueError:
            valid = False
        if not valid:
            rules.fail(date_name, "FORMAT", f"El parámetro '{date_name}' debe ser una fecha DD-MM-AAAA.")

        employer = rules.text(label("registroPatronal"), item.get("registroPatronal"))
        if len(re.sub(r"[^A-Za-z0-9]", "", employer)) != 11:
            rules.fail(label("registroPatronal"), "FORMAT",
                       "El registro patronal debe tener 11 caracteres.")

        worker_key = item.get("claveDelTrabajador")
        if worker_key:
            if not re.fullmatch(r"[A-Za-z0-9]{1,10}", str(worker_key)):
                rules.fail(label("claveDelTrabajador"), "FORMAT",
                           "La clave del trabajador admite hasta 10 letras o números.")
        if item.get("curp"):
            validate_curp(item["curp"])

        if kind == BAJA:
            _choice(label("causaDeBaja"), item.get("causaDeBaja"), LEAVE_REASONS)
        if kind in (MODIFICACION, REINGRESO):
            salary_name = label("salarioDiarioIntegrado")
            salary = item.get("salarioDiarioIntegrado")
            rules.required(**{salary_name: salary})
            try:
                float(salary)
            except (TypeError, ValueError):
                rules.fail(salary_name, "TYPE", f"El parámetro '{salary_name}' debe ser numérico.")
            _choice(label("tipoDeSalario"), item.get("tipoDeSalario"), SALARY_TYPES)
            _choice(label("jornada"), item.get("jornada"), WORKDAY_TYPES)
        if kind == REINGRESO:
            rules.digits(label("umf"), item.get("umf"), 3, 3)
            _choice(label("tipoDeTrabajador"), item.get("tipoDeTrabajador"), WORKER_TYPES)
