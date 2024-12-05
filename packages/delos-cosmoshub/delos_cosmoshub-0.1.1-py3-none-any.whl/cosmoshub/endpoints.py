"""Definition of CosmosHub endpoints and their request types."""

from enum import Enum


class RequestMethod(str, Enum):
    """Enum representing the type of HTTP requests."""

    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"


class StatusEndpoints(Enum):
    """Enum containing the status service endpoints and their request types."""

    HEALTH = ("/health", RequestMethod.GET)


class WebEndpoints(Enum):
    """Enum containing the web service endpoints and their request types."""

    SEARCH = ("/search", RequestMethod.POST)


class TranslateEndpoints(Enum):
    """Enum containing the translate service endpoints and their request types."""

    TRANSLATE_TEXT = ("/translate-text", RequestMethod.POST)
    TRANSLATE_FILE = ("/translate-file", RequestMethod.POST)


class FileEndpoints(Enum):
    """Enum containing the file service endpoints and their request types."""

    CHUNKER = ("/files/chunker", RequestMethod.POST)
    INDEX_CREATE = ("/files/create_index_and_parse", RequestMethod.POST)
    INDEX_ADD_FILES = ("/files/add_files_to_index", RequestMethod.POST)
    INDEX_DELETE_FILES = ("/files/delete_files_from_index", RequestMethod.DELETE)
    INDEX_DELETE = ("/files/delete_index", RequestMethod.DELETE)
    INDEX_RESTORE = ("/files/restore_index", RequestMethod.POST)

    INDEX_ASK = ("/files/ask_index", RequestMethod.POST)
    INDEX_EMBED = ("/files/embed_index", RequestMethod.POST)
    INDEX_LIST = ("/files/list_index", RequestMethod.GET)
    INDEX_DETAILS = ("/files/index_details", RequestMethod.GET)


class LlmEndpoints(Enum):
    """Enum containing the LLM service endpoints and their request types."""

    CHAT = ("/llm/chat", RequestMethod.POST)
    EMBED = ("/llm/embed", RequestMethod.POST)


class Endpoints:
    """Class grouping all the different types of endpoints."""

    STATUS = StatusEndpoints
    WEB = WebEndpoints
    TRANSLATE = TranslateEndpoints
    FILES = FileEndpoints
    LLM = LlmEndpoints


CosmosHubEndpoints = StatusEndpoints | WebEndpoints | TranslateEndpoints | FileEndpoints | LlmEndpoints
