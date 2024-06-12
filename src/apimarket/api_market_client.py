from __future__ import annotations

from typing import TYPE_CHECKING

from kiota_abstractions.api_client_builder import register_default_deserializer, register_default_serializer
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_serialization_form.form_parse_node_factory import FormParseNodeFactory
from kiota_serialization_form.form_serialization_writer_factory import FormSerializationWriterFactory
from kiota_serialization_json.json_parse_node_factory import JsonParseNodeFactory
from kiota_serialization_json.json_serialization_writer_factory import JsonSerializationWriterFactory
from kiota_serialization_multipart.multipart_serialization_writer_factory import MultipartSerializationWriterFactory
from kiota_serialization_text.text_parse_node_factory import TextParseNodeFactory
from kiota_serialization_text.text_serialization_writer_factory import TextSerializationWriterFactory

if TYPE_CHECKING:
    from .api.api_request_builder import ApiRequestBuilder
    from .openapi_json.openapi_json_request_builder import OpenapiJsonRequestBuilder


class ApiMarketClient(BaseRequestBuilder):
    """
    The main entry point of the SDK, exposes the configuration and the fluent API.
    """

    def __init__(self, request_adapter: RequestAdapter) -> None:
        """
        Instantiates a new ApiMarketClient and sets the default values.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        if not request_adapter:
            raise TypeError("request_adapter cannot be null.")
        super().__init__(request_adapter, "{+baseurl}", None)
        register_default_serializer(JsonSerializationWriterFactory)
        register_default_serializer(TextSerializationWriterFactory)
        register_default_serializer(FormSerializationWriterFactory)
        register_default_serializer(MultipartSerializationWriterFactory)
        register_default_deserializer(JsonParseNodeFactory)
        register_default_deserializer(TextParseNodeFactory)
        register_default_deserializer(FormParseNodeFactory)
        if not self.request_adapter.base_url:
            self.request_adapter.base_url = "https://apimarket.mx"
        self.path_parameters["base_url"] = self.request_adapter.base_url

    @property
    def api(self) -> ApiRequestBuilder:
        """
        The api property
        """
        from .api.api_request_builder import ApiRequestBuilder

        return ApiRequestBuilder(self.request_adapter, self.path_parameters)

    @property
    def openapi_json(self) -> OpenapiJsonRequestBuilder:
        """
        The openapiJson property
        """
        from .openapi_json.openapi_json_request_builder import OpenapiJsonRequestBuilder

        return OpenapiJsonRequestBuilder(self.request_adapter, self.path_parameters)
