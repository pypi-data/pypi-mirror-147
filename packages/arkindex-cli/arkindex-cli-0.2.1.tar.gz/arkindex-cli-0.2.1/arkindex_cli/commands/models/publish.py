# -*- coding: utf-8 -*-
import logging
import os
from typing import Optional

from arkindex import ArkindexClient
from rich.progress import Progress

from arkindex_cli.auth import Profiles
from arkindex_cli.commands.models.utils import (
    create_archive,
    create_model_version,
    create_or_retrieve_model,
    parse_yml_config,
    update_model_version,
    upload_to_s3,
)

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def add_publish_parser(subcommands) -> None:
    publish_parser = subcommands.add_parser(
        "publish",
        description="Publish every ML models of this git repository.",
        help="Publish ML models to Arkindex.",
    )
    publish_parser.set_defaults(func=run)


def publish_model(client: ArkindexClient, name: str, configuration: dict) -> None:
    """This takes a model associated to a worker and publishes a new version of the model"""
    logger.info(f"Publishing {name}")

    default_models_dir = "/usr/share/teklia/models/"
    # Find the model file associated
    path_to_model = configuration.pop("model")

    # Try to create a model
    # On 201, use the given id
    # On 400, use the given id key='name'
    # On 403 abort and log error
    model_id = create_or_retrieve_model(client=client, name=name)

    # Path to model may have a static prefix from teklia but it's not available
    # on Git repos, so we replace it with ./models
    if not os.path.exists(path_to_model) and path_to_model.startswith(
        default_models_dir
    ):
        path_to_model = path_to_model.replace(default_models_dir, "")

    # Add the prefix the folder where the models are actually stored
    # The path given in the worker configuration may omit this prefix that's why we have to add it
    path_to_model = os.path.join("models", path_to_model)

    assert os.path.exists(path_to_model), f"Missing local model in {path_to_model}"

    # Create the zst archive, get its hash and size
    with create_archive(path=path_to_model) as (
        path_to_archive,
        hash,
        size,
        archive_hash,
    ):

        # Create a new model version with hash and size
        model_version_details = create_model_version(
            client=client,
            model_id=model_id,
            hash=hash,
            size=size,
            archive_hash=archive_hash,
        )

        if model_version_details is None:
            return
        upload_to_s3(
            archive_path=path_to_archive, model_version_details=model_version_details
        )

    # Update the model version with state, configuration parsed, tag, description (defaults to name of the worker)
    update_model_version(
        client=client,
        model_version_details=model_version_details,
        name=name,
        configuration=configuration,
    )


def run(profile_slug: Optional[str] = None) -> None:
    with Progress(transient=True) as progress:
        progress.add_task(start=False, description="Loading API client")
        client = Profiles().get_api_client_or_exit(profile_slug)

    # Parse .arkindex.yml => retrieve worker name, path and configuration
    workers = parse_yml_config(worker_config_path=".arkindex.yml")

    # For each worker, do_publish
    for worker_name, worker_configuration in workers.items():
        try:
            publish_model(client, worker_name, worker_configuration)
        except Exception:
            logger.exception(f"{worker_name} publishing has failed with error")
            logger.error("Skipping this model.")

    logger.info("All done.")
