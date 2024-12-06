import mimetypes

from abc import ABC
from typing import Optional
from pathlib import Path

from dkdc_util import now


# TODO TODO TODO
# TODO: this is largely AI-generated and unchecked but fine for now
# TODO TODO TODO
# need to split out the "Document" types: PDF, doc, spreadsheet, etc.
# !!!mainly, need to standardize __str__ and __repr__ methods!!!
# need to add code document type


class File(ABC):
    """Base class for all files."""

    def __init__(self, filename: str, data: bytes, mime_type: Optional[str] = None):
        self.filename = Path(filename)
        self._data = data
        self.size = len(data)
        self.created_at = now()
        self._mime_type = mime_type or mimetypes.guess_type(filename)[0]

    @property
    def mime_type(self) -> Optional[str]:
        return self._mime_type

    @property
    def extension(self) -> str:
        return self.filename.suffix.lower()

    @property
    def data(self) -> bytes:
        return self._data

    def to_file(self, path: Optional[str] = None) -> Path:
        """Save file to file on disk."""
        save_path = Path(path) / self.filename if path else self.filename
        save_path.write_bytes(self._data)
        return save_path

    @classmethod
    def from_file(cls, filepath: str) -> "File":
        """Create file from a file."""
        path = Path(filepath)
        data = path.read_bytes()
        return cls(path.name, data)

    @classmethod
    def from_bytes(cls, data: bytes, filename: str) -> "File":
        """Create file directly from bytes."""
        return cls(filename, data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(filename='{self.filename}', size={self.size} bytes)"


class ImageFile(File):
    """Base class for image files."""

    VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"}

    def __init__(self, filename: str, data: bytes, mime_type: Optional[str] = None):
        super().__init__(filename, data, mime_type)
        if self.extension not in self.VALID_EXTENSIONS:
            raise ValueError(
                f"Invalid image format. Must be one of: {', '.join(self.VALID_EXTENSIONS)}"
            )


class TextFile(File):
    """Base class for text files."""

    VALID_EXTENSIONS = {".txt", ".md", ".rst", ".json", ".xml", ".yml", ".yaml", ".csv"}

    def __init__(
        self,
        filename: str,
        data: bytes,
        encoding: str = "utf-8",
        mime_type: Optional[str] = None,
    ):
        super().__init__(filename, data, mime_type)
        if self.extension not in self.VALID_EXTENSIONS:
            raise ValueError(
                f"Invalid text format. Must be one of: {', '.join(self.VALID_EXTENSIONS)}"
            )
        self.encoding = encoding

    @property
    def text(self) -> str:
        """Get the text content of the file."""
        return self._data.decode(self.encoding)


class VideoFile(File):
    """Base class for video files."""

    VALID_EXTENSIONS = {".mp4", ".avi", ".mov", ".wmv", ".webm"}

    def __init__(self, filename: str, data: bytes, mime_type: Optional[str] = None):
        super().__init__(filename, data, mime_type)
        if self.extension not in self.VALID_EXTENSIONS:
            raise ValueError(
                f"Invalid video format. Must be one of: {', '.join(self.VALID_EXTENSIONS)}"
            )


class AudioFile(File):
    """Base class for audio files."""

    VALID_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".flac"}

    def __init__(self, filename: str, data: bytes, mime_type: Optional[str] = None):
        super().__init__(filename, data, mime_type)
        if self.extension not in self.VALID_EXTENSIONS:
            raise ValueError(
                f"Invalid audio format. Must be one of: {', '.join(self.VALID_EXTENSIONS)}"
            )


class DocumentFile(File):
    """Base class for document files."""

    VALID_EXTENSIONS = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"}

    def __init__(self, filename: str, data: bytes, mime_type: Optional[str] = None):
        super().__init__(filename, data, mime_type)
        if self.extension not in self.VALID_EXTENSIONS:
            raise ValueError(
                f"Invalid document format. Must be one of: {', '.join(self.VALID_EXTENSIONS)}"
            )
