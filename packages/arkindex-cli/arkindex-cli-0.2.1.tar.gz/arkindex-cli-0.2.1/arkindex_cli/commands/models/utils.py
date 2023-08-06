# -*- coding: utf-8 -*-
import hashlib
import logging
import os
import tarfile
import tempfile
from contextlib import contextmanager
from typing import NewType, Tuple

import apistar
import requests
import yaml
import zstandard as zstd
from arkindex import ArkindexClient

logger = logging.getLogger(__name__)
CHUNK_SIZE = 1024


FilePath = NewType("FilePath", str)
Hash = NewType("Hash", str)
FileSize = NewType("FileSize", int)
Archive = Tuple[FilePath, Hash, FileSize]


@contextmanager
def create_archive(path: FilePath) -> Archive:
    """First create a tar archive, then compress to a zst archive.
    Finally, get its hash and size
    """
    compressor = zstd.ZstdCompressor(level=3)
    content_hasher = hashlib.md5()
    archive_hasher = hashlib.md5()

    # Remove extension from the model filename
    _, path_to_tar_archive = tempfile.mkstemp(prefix="teklia-", suffix=".tar")

    # Create an uncompressed tar archive with all the needed files
    # Files hierarchy is kept in the archive.
    with tarfile.open(path_to_tar_archive, "w") as tar:
        tar.add(path)
        file_list = [member for member in tar.getnames() if os.path.isfile(member)]

    # Sort by path
    file_list.sort()
    # Compute hash of the files
    for file_path in file_list:
        with open(file_path, "rb") as file_data:
            for chunk in iter(lambda: file_data.read(CHUNK_SIZE), b""):
                content_hasher.update(chunk)

    _, path_to_zst_archive = tempfile.mkstemp(prefix="teklia-", suffix=".tar.zst")

    # Compress the archive
    with open(path_to_zst_archive, "wb") as archive_file:
        with open(path_to_tar_archive, "rb") as model_data:
            for model_chunk in iter(lambda: model_data.read(CHUNK_SIZE), b""):
                compressed_chunk = compressor.compress(model_chunk)
                archive_hasher.update(compressed_chunk)
                archive_file.write(compressed_chunk)

    # Remove the tar archive
    os.remove(path_to_tar_archive)

    # Get content hash, archive size and hash
    hash = content_hasher.hexdigest()
    size = os.path.getsize(path_to_zst_archive)
    archive_hash = archive_hasher.hexdigest()

    yield path_to_zst_archive, hash, size, archive_hash

    # Remove the zstd archive
    os.remove(path_to_zst_archive)


def create_or_retrieve_model(client: ArkindexClient, name: str):
    """Create a new model or retrieve the id of the existing one (with the same name)"""
    status = 200
    try:
        r = client.request("CreateModel", body={"name": name})
        # New model was created
        return r["id"]
    except apistar.exceptions.ErrorResponse as e:
        r = e.content
        status = e.status_code
        if status == 400:
            # Model already exists but user has access to it. The model id was returned in payload
            return r["id"]
        elif status == 403:
            # Model exists but user has no access to it, raise
            raise Exception(f"Permission denied to publish {name}")
        else:
            raise


def parse_yml_config(worker_config_path: str, single_worker: bool = False) -> dict:
    """Parse .arkindex.yml and retrieve each workers data"""
    with open(worker_config_path, "r") as config_file:
        try:
            data = yaml.safe_load(config_file)
        except yaml.YAMLError as exc:
            logger.error(exc)
            return None
    if single_worker:
        return {data["name"]: data.get("configuration", {})}
    workers = data.get("workers", [])
    if len(workers) > 0 and isinstance(workers[0], str):
        parsed_worker_configurations = dict()
        for worker_path in workers:
            parsed_worker_configurations.update(
                parse_yml_config(worker_config_path=worker_path, single_worker=True)
            )
        return parsed_worker_configurations
    else:
        return {worker["name"]: worker.get("configuration", {}) for worker in workers}


def create_model_version(
    client: ArkindexClient, model_id: str, hash: str, size: int, archive_hash: str
) -> dict:
    # Create a new model version with hash and size
    try:
        model_version_details = client.request(
            "CreateModelVersion",
            id=model_id,
            body={"hash": hash, "size": size, "archive_hash": archive_hash},
        )
    except apistar.exceptions.ErrorResponse as e:
        if e.status_code >= 500:
            logger.error(f"Failed to create model version: {e.content}")
        model_version_details = e.content.get("hash")
        # If the existing model is in Created state, this model is returned as a dict.
        # Else an error in a list is returned.
        if model_version_details and isinstance(model_version_details, (list, tuple)):
            logger.error(model_version_details[0])
            return
    return model_version_details


def upload_to_s3(archive_path: str, model_version_details: dict) -> None:
    s3_put_url = model_version_details.get("s3_put_url")
    logger.info("Uploading to s3...")
    # Upload the archive on s3
    with open(archive_path, "rb") as archive:
        r = requests.put(url=s3_put_url, data=archive)
    r.raise_for_status()


def update_model_version(
    client: ArkindexClient, model_version_details: dict, name: str, configuration: dict
) -> None:
    logger.info("Updating the model version...")
    try:
        client.request(
            "UpdateModelVersion",
            id=model_version_details.get("id"),
            body={
                "state": "available",
                "description": name,
                "tag": os.environ.get("CI_COMMIT_TAG"),
                "configuration": configuration,
            },
        )
    except apistar.exceptions.ErrorResponse as e:
        logger.error(f"Failed to update model version: {e.content}")
