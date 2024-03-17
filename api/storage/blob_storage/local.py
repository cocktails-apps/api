import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from typing_extensions import override
from yarl import URL

from .base import BlobStorage, BlobStorageError


class LocalBlobStorageError(BlobStorageError):
    pass


class LocalBlobStorage(BlobStorage):
    def __init__(self, root_folder: Path) -> None:
        super().__init__()

        if not root_folder.is_dir():
            raise LocalBlobStorageError(
                f"root_folder '{root_folder}' does not exist or is not a directory"
            )

        self._root_folder = root_folder

    @override
    async def upload(self, folder: str, file_name: str, data: bytes) -> URL:
        file_dir = self._root_folder / folder
        if not file_dir.exists():
            try:
                file_dir.mkdir()
            except Exception as exc:
                raise LocalBlobStorageError(
                    f"failed to create folder '{file_dir}'"
                ) from exc

        if not file_dir.is_dir():
            raise LocalBlobStorageError(f"'{file_dir}' is not a directory")

        file_path = file_dir / file_name

        if file_path.exists():
            raise LocalBlobStorageError(f"file '{file_path}' already exists")

        file_path.write_bytes(data)

        return URL.build(scheme="file", host=str(file_path))


@contextmanager
def local_blob_storage(root_folder: Optional[Path]) -> Iterator[LocalBlobStorage]:
    if root_folder is None:
        with tempfile.TemporaryDirectory() as temp_dir:
            yield LocalBlobStorage(root_folder=Path(temp_dir))
    else:
        yield LocalBlobStorage(root_folder=root_folder)
