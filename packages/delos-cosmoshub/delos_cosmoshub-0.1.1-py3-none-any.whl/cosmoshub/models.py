"""CismosHub data for API Requests."""

from enum import Enum
from typing import Any

from fastapi import UploadFile
from pydantic import BaseModel


class EndpointData(BaseModel):
    """Data structure for ComosHub API endpoints."""

    def as_dict(self) -> dict[str, Any]:
        """Return the data as a dictionary."""
        return self.model_dump()


class FileTranslationReturnType(str, Enum):
    """Enumeration for type of possible request when translating a file."""

    RAW_TEXT = "raw_text"
    URL = "url"
    FILE = "file"


class TranslateTextData(EndpointData):
    """Data structure for text translation."""

    text: str
    output_language: str
    input_language: str | None = None


class TranslateFileData(EndpointData):
    """Data structure for file translation."""

    file: UploadFile
    return_type: FileTranslationReturnType = FileTranslationReturnType.RAW_TEXT
    output_language: str
    input_language: str | None = None


class SearchData(EndpointData):
    """Data structure for search."""

    text: str
    output_language: str


class ChunkerExtractType(str, Enum):
    """Enum for extract types in chunking operations."""

    SUBCHUNKS = "subchunks"
    CHUNKS = "chunks"
    PAGES = "pages"
    FILE = "file"


class ChunkerData(EndpointData):
    """Data structure for chunker."""

    file: UploadFile

    extract_type: ChunkerExtractType = ChunkerExtractType.SUBCHUNKS
    filter_pages: str | None = "[]"
    k_min: int | None = None
    k_max: int | None = None
    overlap: int | None = None


class IndexOperationData(EndpointData):
    """Data structure for index operations."""

    index_uuid: str
    files: list[UploadFile] | None = None
    files_hashes: list[str] | None = None


class LlmData(EndpointData):
    """Data structure for LLM operations."""

    text: str
    model: str | None = None
