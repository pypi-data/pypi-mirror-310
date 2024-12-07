from pathlib import Path
from typing import overload, TypedDict, Unpack

from anyio import open_file
import asyncer
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob.aio import BlobServiceClient, ContainerClient
from azure.storage.blob.aio._blob_client_async import BlobClient

from azaux.storage_resource import StorageResource, StorageResourceType


@overload
async def download_blob(
    client: ContainerClient, blob_name: str, encoding: None = None, **kwargs
) -> bytes: ...


@overload
async def download_blob(
    client: ContainerClient, blob_name: str, encoding: str, **kwargs
) -> str: ...


async def download_blob(
    client: ContainerClient, blob_name: str, encoding: str | None = None, **kwargs
) -> bytes | str:
    """
    Retrieve data from a given blob file within the container.

    :param client: The ContainerClient.
    :param blob_name: The name of the blob file.
    :param encoding: The encoding to use for decoding the blob content.
    :param kwargs: Additional keyword arguments to pass to download_blob.
    :return: The content of the blob.
    """
    downloader = await client.download_blob(blob_name, **kwargs)
    content = await downloader.readall()
    return content.decode(encoding) if encoding else content


async def try_upload_blob(
    client: ContainerClient, filepath: Path, blob_path: Path | None = None
) -> BlobClient:
    """
    Upload a file to a blob, or get the blob client if it already exists.

    :param client: The ContainerClient.
    :param filepath: The path to the file to upload.
    :param blob_path: The path in the blob storage to upload to.
    :return: The BlobClient for the uploaded blob.
    """
    blob_name = (blob_path or filepath).as_posix()
    blob_client = client.get_blob_client(blob_name)
    try:
        async with await open_file(filepath, mode="rb") as f:
            await blob_client.upload_blob(f, overwrite=False)
    except ResourceExistsError:
        # Blob already exists; no action needed.
        pass
    return blob_client


class ServiceKwargs(TypedDict, total=False):
    secondary_hostname: str
    max_block_size: int
    max_single_put_size: int
    min_large_block_upload_threshold: int
    use_byte_buffer: bool
    max_page_size: int
    max_single_get_size: int
    max_chunk_get_size: int
    audience: str


class ContainerManager(StorageResource):
    """
    Class to manage retrieving blob data from a given blob file.

    :param container: The name of the container.
    :param account: The name of the Azure Storage account.
    :param api_key: The API key for the Azure Storage account.
    """

    def __init__(
        self,
        container: str,
        account: str,
        api_key: str,
        **kwargs: Unpack[ServiceKwargs],
    ):
        """
        Initialize the ContainerManager class.

        :param container: The name of the container.
        :param account: The name of the Azure Storage account.
        :param api_key: The API key for the Azure Storage account.
        :param create_if_missing: Whether to create the container if it does not exist.

        """
        self.container = container
        super().__init__(account, api_key)
        self.kwargs = kwargs
        self._client_cache: ContainerClient | None = None

    @property
    def resource_type(self) -> StorageResourceType:
        return StorageResourceType.blob

    @property
    def client(self):
        """Retrieve a client for the container, using a cached client if available"""
        if not self._client_cache:
            service = BlobServiceClient(
                self.endpoint, credential=self.credential, **self.kwargs
            )
            self._client_cache = service.get_container_client(self.container)
        return self._client_cache

    async def download_blob(self, blob_path: Path, encoding: None | str = None):
        """Download a blob from the container"""
        async with self.client as client:
            return await download_blob(client, blob_path.as_posix(), encoding)

    async def try_upload_blob(self, filepath: Path, blob_path: Path | None = None):
        """Upload a file to a blob, or get the blob client if it already exists."""
        async with self.client as client:
            return await try_upload_blob(client, filepath, blob_path)

    async def try_upload_blobs(
        self, filepaths: list[Path], blob_paths: list[Path] | None = None
    ):
        """
        Upload multiple files to blobs with the filepaths as default names.

        :param filepaths: The paths to the files to upload.
        :param blob_paths: The paths in the blob storage to upload to.
        """
        blob_paths_ = blob_paths or [None] * len(filepaths)
        async with self.client as client, asyncer.create_task_group() as tg:
            for pth, blb in zip(filepaths, blob_paths_, strict=True):
                tg.soonify(try_upload_blob)(client, pth, blb)

    async def sync_with_folder(self, folder: Path, pattern: str = "**/*"):
        """Sync the container with a folder"""
        async with self.client as client, asyncer.create_task_group() as tg:
            for pth in folder.glob(pattern):
                if pth.is_file():
                    tg.soonify(try_upload_blob)(client, pth, pth.relative_to(folder))
