from pathlib import Path

import pytest

from .local import LocalBlobStorage, LocalBlobStorageError


def test_init_fail_when_not_exists(tmp_path: Path):
    with pytest.raises(LocalBlobStorageError, match="does not exist"):
        LocalBlobStorage(root_folder=tmp_path / "not_exists")


def test_init_fail_when_not_a_directory(tmp_path: Path):
    file_path = tmp_path / "file"
    file_path.touch()

    with pytest.raises(LocalBlobStorageError, match="is not a directory"):
        LocalBlobStorage(root_folder=file_path)


@pytest.fixture
def sut(tmp_path: Path) -> LocalBlobStorage:
    return LocalBlobStorage(root_folder=tmp_path)


async def test_upload_folder_is_not_dir(sut: LocalBlobStorage, tmp_path: Path):
    file_path = tmp_path / "folder"
    file_path.touch()

    with pytest.raises(LocalBlobStorageError, match="is not a directory"):
        await sut.upload(folder="folder", file_name="file", data=b"data")


async def test_upload_file_exists(sut: LocalBlobStorage, tmp_path: Path):
    file_path = tmp_path / "folder" / "file"
    file_path.parent.mkdir()
    file_path.touch()

    with pytest.raises(LocalBlobStorageError, match="already exists"):
        await sut.upload(folder="folder", file_name="file", data=b"data")


async def test_upload(sut: LocalBlobStorage, tmp_path: Path):
    folder = "some_folder"
    file_name = "some_file"
    data = b"some data"

    url = await sut.upload(folder=folder, file_name=file_name, data=data)

    assert url.scheme == "file"

    file_path = tmp_path / folder / file_name
    assert file_path.is_file()
    assert file_path.read_bytes() == data
