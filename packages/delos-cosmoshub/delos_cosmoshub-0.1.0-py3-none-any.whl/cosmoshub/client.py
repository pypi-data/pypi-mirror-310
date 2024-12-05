"""Client for interacting with the CosmosHub API."""

import logging
from typing import Any

import requests

from .endpoints import Endpoints, FileEndpoints, RequestMethod
from .models import ChunkerData, IndexOperationData, SearchData, TranslateFileData, TranslateTextData
from .releases import AllReleases

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COSMOS_PLATFORM_BACKEND_URL = "https://platform.cosmos-suite.ai"


class CosmosHubClient:
    """Client for interacting with the CosmosHub API.

    Attributes:
        server_url: The URL of the server.
        apikey: The API key to be used for requests.
    """

    def __init__(self: "CosmosHubClient", apikey: str, server_url: str = COSMOS_PLATFORM_BACKEND_URL, debug_mode: bool = False) -> None:
        """Initialize the client with the server URL and API key."""
        self.server_url = server_url
        self.apikey = apikey

        self._client_version = AllReleases[0]

        self._headers = self._getheaders()
        self._debug_mode = debug_mode

    def _getheaders(self: "CosmosHubClient") -> dict[str, str]:
        """Return the headers to be used for requests."""
        return {"apikey": self.apikey}

    def _make_request(
        self,
        endpoint: tuple[str, RequestMethod],
        data: dict[str, Any] | None = None,
        files: Any = None,
    ) -> dict[str, Any] | None:
        """Make a request to the specified endpoint with the given data and files.

        Args:
            apikey: The CosmosHub key to be used for the request.
            endpoint: A tuple containing the endpoint URL and the request type.
            data: The data to be sent in the request body (default is None).
            files: The files to be sent in the request (default is None).

        Returns:
            The response from the request as a dictionary, or None if an error occurred.
        """
        url = f"{self.server_url}{self._client_version.suffix}{endpoint[0]}"
        request_method = endpoint[1].value
        if self._debug_mode:
            error_message = f"Making request to {url} with method {request_method}"
            logger.debug(error_message)

        try:
            response = requests.request(request_method, url, headers=self._headers, json=data, files=files, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            return response.json()

        except requests.exceptions.RequestException as e:
            if self._debug_mode:
                error_message = f"An error occurred: {e}"
                logger.exception(error_message)
            return None

    def status_health_request(self: "CosmosHubClient") -> dict[str, Any] | None:
        """Make a request to check the health of the server."""
        return self._make_request(Endpoints.STATUS.HEALTH.value)

    def translate_text_request(
        self: "CosmosHubClient",
        translate_data: TranslateTextData,
    ) -> dict[str, Any] | None:
        """Make a request to translate text."""
        data = translate_data.as_dict()
        return self._make_request(Endpoints.TRANSLATE.TRANSLATE_TEXT.value, data)

    def translate_file_request(
        self: "CosmosHubClient",
        translate_data: TranslateFileData,
    ) -> dict[str, Any] | None:
        """Make a request to translate a file."""
        data = translate_data.as_dict()
        files = {"file": (translate_data.file.filename, translate_data.file.file)}
        return self._make_request(Endpoints.TRANSLATE.TRANSLATE_FILE.value, data, files)

    def web_search_request(self: "CosmosHubClient", search_data: SearchData) -> dict[str, Any] | None:
        """Make a request to perform a search."""
        data = search_data.as_dict()
        return self._make_request(Endpoints.WEB.SEARCH.value, data)

    def files_chunker_request(self: "CosmosHubClient", chunker_data: ChunkerData) -> dict[str, Any] | None:
        """Make a request to chunk a file."""
        files = {"file": (chunker_data.file.filename, chunker_data.file.file)}
        return self._make_request(Endpoints.FILES.CHUNKER.value, {}, files)

    def files_index_operation_request(
        self: "CosmosHubClient",
        index_data: IndexOperationData,
        operation: FileEndpoints,
    ) -> dict[str, Any] | None:
        """Make a request for index operations."""
        args: dict[str, Any] = {}
        if index_data.files:
            args["files"] = [("files", (file.filename, file.file)) for file in index_data.files]

        if index_data.files_hashes:
            args["files_hashes"] = index_data.files_hashes

        if index_data.index_uuid:
            args["index_uuid"] = index_data.index_uuid

        return self._make_request(operation.value, **args)
