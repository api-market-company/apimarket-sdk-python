"""Servicios de inteligencia artificial: OCR, plantillas, procesamiento y datasets."""
from typing import Any, Dict, List, Optional

from apimarket import rules
from apimarket.services._core import Call, FileInput, service
from apimarket.validations import InvalidParameterError


@service("ai", "ocr-id", "/api/ai/v2/ocr-id")
def ocr_id(anverso: FileInput, reverso: Optional[FileInput] = None):
    """Extrae los datos de una identificación (JPG, PNG o PDF, hasta 20 MB)."""
    front = rules.load_file("anverso", anverso, extensions=rules.DOCUMENTS, max_megabytes=20)
    back = None if reverso is None else rules.load_file("reverso", reverso, extensions=rules.DOCUMENTS,
                                                        max_megabytes=20)
    return Call(files={"anverso": front, "reverso": back})


# ---------------------------------------------------------------------------
# Plantillas PDF
# ---------------------------------------------------------------------------

@service("ai", "plantilla-crear", "/api/ai/v2/templates", retry=False)
def create_template(template: FileInput):
    """Sube una plantilla PDFMe en formato JSON."""
    return Call(files={"template": rules.template_file("template", template)})


# PHP solo interpreta archivos multipart en peticiones POST, así que la
# actualización viaja como POST con ``_method=PUT``.
@service("ai", "plantilla-actualizar", "/api/ai/v2/templates/{template_id}", retry=False)
def update_template(template_id: str, template: FileInput):
    """Reemplaza el contenido de una plantilla."""
    rules.text("template_id", template_id)
    return Call(path_params={"template_id": template_id}, data={"_method": "PUT"},
                files={"template": rules.template_file("template", template)})


@service("ai", "plantilla-generar", "/api/ai/v2/templates/{template_id}", retry=False)
def generate_from_template(template_id: str, inputs: List[Dict[str, Any]],
                           options: Optional[Dict[str, Any]] = None, wait: bool = True):
    """Genera un PDF a partir de una plantilla.

    :param inputs: de 1 a 100 objetos con los valores de la plantilla.
    :param options: ``filename``, ``title``, ``correlation_id`` o ``metadata``.
    :param wait: si es ``False`` responde de inmediato con el código de seguimiento.
    """
    rules.text("template_id", template_id)
    for item in rules.items("inputs", inputs, max_items=100):
        rules.mapping("inputs", item)
    if options is not None:
        rules.mapping("options", options)
        for key in ("filename", "title", "correlation_id"):
            rules.optional_text(f"options.{key}", options.get(key), max_length=255)
        if options.get("metadata") is not None and not isinstance(options["metadata"], (dict, list)):
            rules.mapping("options.metadata", options["metadata"])
    query, headers = {}, {}
    if not rules.boolean("wait", wait):
        # La API espera si cualquiera de los dos vale "true".
        query, headers = {"wait": "false"}, {"x-wait-for-completion": "false"}
    return Call(path_params={"template_id": template_id}, query=query, headers=headers,
                json={"inputs": inputs, "options": options})


# ---------------------------------------------------------------------------
# Procesamiento inteligente
# ---------------------------------------------------------------------------

def _job(transaction_id: Optional[int], webhook: Optional[str]) -> None:
    if transaction_id is not None:
        rules.integer("transaction_id", transaction_id, minimum=0)
    if webhook is not None:
        rules.https_url("webhook", webhook)


@service("ai", "procesar-subir", "/api/ai/v2/smart-processing", retry=False)
def smart_processing_upload(data: FileInput):
    """Sube un archivo CSV para su procesamiento."""
    return Call(files={"data": rules.csv_file("data", data)})


@service("ai", "procesar-planear", "/api/ai/v2/smart-processing/plan", retry=False)
def smart_processing_plan(resources: List[Dict[str, str]]):
    """Define los servicios que enriquecen un dataset.

    :param resources: objetos con ``resource``, ``field``, ``url`` y ``json_path_query``.
    """
    for item in rules.items("resources", resources):
        rules.mapping("resources", item)
        for key in ("resource", "field", "url", "json_path_query"):
            rules.text(f"resources.{key}", item.get(key))
    return Call(json={"resources": resources})


@service("ai", "procesar-estimar", "/api/ai/v2/smart-processing/estimate")
def smart_processing_estimate(dataset: str):
    """Estima el costo de procesar un dataset."""
    rules.text("dataset", dataset)
    return Call(json={"dataset": dataset})


@service("ai", "procesar-ejecutar", "/api/ai/v2/smart-processing/execute", retry=False)
def smart_processing_execute(dataset: str, transaction_id: Optional[int] = None, webhook: Optional[str] = None):
    """Ejecuta el procesamiento de un dataset. Consume saldo."""
    rules.text("dataset", dataset)
    _job(transaction_id, webhook)
    return Call(json={"dataset": dataset, "transaction_id": transaction_id, "webhook": webhook})


@service("ai", "procesar-exportar", "/api/ai/v2/smart-processing/export", retry=False)
def smart_processing_export(transaction_id: Optional[int] = None, webhook: Optional[str] = None):
    """Exporta los resultados del procesamiento."""
    _job(transaction_id, webhook)
    return Call(json={"transaction_id": transaction_id, "webhook": webhook})


@service("ai", "procesar-estado", "/api/ai/v2/smart-processing/status", method="GET")
def smart_processing_status(transaction_id: Optional[int] = None):
    """Consulta el estado de las transacciones de procesamiento."""
    if transaction_id is not None:
        rules.integer("transaction_id", transaction_id, minimum=0)
    return Call(query={"transaction_id": transaction_id})


@service("ai", "procesar-eliminar", "/api/ai/v2/smart-processing/{resource}", method="DELETE", retry=False)
def smart_processing_delete(resource: str):
    """Elimina un dataset y sus transacciones. No se puede deshacer."""
    rules.text("resource", resource)
    return Call(path_params={"resource": resource})


# ---------------------------------------------------------------------------
# Datasets
# ---------------------------------------------------------------------------

@service("ai", "datasets", "/api/ai/v2/dataset", method="GET")
def list_datasets():
    """Lista los datasets del token."""
    return Call()


@service("ai", "dataset-filas", "/api/ai/v2/dataset/{resource}", method="GET")
def get_dataset_rows(resource: str, filter: Optional[Dict[str, Any]] = None, sort: Optional[str] = None,
                     select: Optional[str] = None, page: Optional[int] = None, per_page: Optional[int] = None):
    """Consulta las filas de un dataset.

    :param filter: ``{"columna": "valor"}`` o ``{"columna": {"like": "texto"}}``.
    :param sort: columna; con prefijo ``-`` el orden es descendente.
    :param select: columnas separadas por comas.
    :param per_page: máximo 100.
    """
    rules.text("resource", resource)
    rules.optional_text("sort", sort)
    rules.optional_text("select", select)
    if page is not None:
        rules.integer("page", page, minimum=1)
    if per_page is not None:
        rules.integer("per_page", per_page, minimum=1, maximum=100)
    if filter is not None:
        for column, value in rules.mapping("filter", filter).items():
            rules.text("filter", column)
            if isinstance(value, dict) and set(value) != {"like"}:
                raise InvalidParameterError.of("filter", "OPTION",
                                               "El único operador de filtro admitido es 'like'.")
            operand = value["like"] if isinstance(value, dict) else value
            if not isinstance(operand, (str, int, float)):
                rules.text("filter", operand)
    query = {"sort": sort, "select": select, "page": page, "per_page": per_page}
    for column, value in (filter or {}).items():
        if isinstance(value, dict):
            for operator, operand in value.items():
                query[f"filter[{column}][{operator}]"] = operand
        else:
            query[f"filter[{column}]"] = value
    return Call(path_params={"resource": resource}, query=query)


@service("ai", "dataset-fila", "/api/ai/v2/dataset/{resource}/{row_id}", method="GET")
def get_dataset_row(resource: str, row_id: int):
    """Consulta una fila de un dataset."""
    rules.text("resource", resource)
    rules.integer("row_id", row_id, minimum=0)
    return Call(path_params={"resource": resource, "row_id": row_id})
