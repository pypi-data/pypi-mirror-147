# -*- coding: utf-8 -*-
import csv
from pathlib import Path
from typing import Optional
from uuid import UUID

from arkindex_cli.auth import Profiles
from arkindex_cli.commands.elements.utils import retrieve_children

CSV_HEADER = [
    "id",
    "name",
    "type",
    "image_id",
    "image_url",
    "polygon",
    "worker_version_id",
    "created",
]


def add_list_parser(subcommands):
    list_parser = subcommands.add_parser(
        "list",
        description="List all elements in a corpus or under a specified parent and output results in a CSV file.",
        help="",
    )
    root = list_parser.add_mutually_exclusive_group(required=True)
    root.add_argument(
        "--corpus",
        help="UUID of an existing corpus.",
        type=UUID,
    )
    root.add_argument(
        "--parent",
        help="UUID of an existing parent element.",
        type=UUID,
    )
    list_parser.add_argument(
        "--type",
        help="Limit the listing using this slug of an element type.",
        type=str,
    )
    list_parser.add_argument(
        "--recursive",
        help="List elements recursively.",
        action="store_true",
    )
    list_parser.add_argument(
        "--output",
        default=Path.cwd() / "elements.csv",
        type=Path,
        help="Path to a CSV file where results will be outputted. Defaults to '<current_directory>/elements.csv'.",
        dest="output_path",
    )
    list_parser.set_defaults(func=run)


def run(
    corpus: Optional[UUID] = None,
    parent: Optional[UUID] = None,
    type: Optional[str] = None,
    recursive: Optional[bool] = False,
    output_path: Optional[str] = Path.cwd() / "elements.csv",
    profile_slug: Optional[str] = None,
):
    profiles = Profiles()
    client = profiles.get_api_client_or_exit(profile_slug)

    children = retrieve_children(
        client, corpus=corpus, parent=parent, type=type, recursive=recursive
    )

    with open(output_path, "w", encoding="UTF8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=CSV_HEADER)
        writer.writeheader()

        for child in children:
            writer.writerow(
                {
                    "id": child["id"],
                    "name": child["name"],
                    "type": child["type"],
                    "image_id": child["zone"]["image"]["id"]
                    if child.get("zone") and child["zone"].get("image")
                    else None,
                    "image_url": child["zone"]["image"]["url"]
                    if child.get("zone") and child["zone"].get("image")
                    else None,
                    "polygon": child["zone"]["polygon"] if child.get("zone") else None,
                    "worker_version_id": child["worker_version_id"],
                    "created": child["created"],
                }
            )
