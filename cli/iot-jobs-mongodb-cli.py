# -*- coding: utf-8 -*-

import json
import os
import sys

import typer
from dotenv import load_dotenv

from openapi_client import ApiClient, Configuration
from openapi_client.api import MongodbApi
from openapi_client.models import (
    PostCollectionsIndexRequest,
    PostCollectionsRequest,
    PutCollectionsValidatorRequest
)
from openapi_client.exceptions import ApiException


load_dotenv()

API_CLIENT_HOST = os.getenv("API_CLIENT_HOST", None)

if API_CLIENT_HOST is None:
    typer.echo(
        "Error: API_CLIENT_HOST environment variable is not set.",
        err=True
    )

    sys.exit(1)

configuration = Configuration(
    host=API_CLIENT_HOST
)

api_client = ApiClient(
    configuration=configuration
)

mongodb_api = MongodbApi(
    api_client=api_client
)

app = typer.Typer(help="IoT Jobs MongoDB CLI")

collection_app = typer.Typer(help="Manage MongoDB collections.")
index_app = typer.Typer(help="Manage MongoDB collection indexes.")
validator_app = typer.Typer(help="Manage MongoDB collection validators.")

app.add_typer(collection_app, name="collection")
app.add_typer(index_app, name="index")
app.add_typer(validator_app, name="validator")


@collection_app.command("create")
def create_collection(
    collection_name: str = typer.Argument(
        default=...,
        help="Name of the collection to create."
    )
) -> None:
    typer.echo(
        f"Attempting to create collection: {collection_name}"
    )

    try:
        post_collections_request = PostCollectionsRequest(
            collection_name=collection_name
        )

        mongodb_api.post_collections_mongodb_collections_post(
            post_collections_request=post_collections_request
        )

        typer.echo(
            f"Collection '{collection_name}' created successfully."
        )

    except ApiException as e:
        typer.echo(
            f"Error creating collection '{collection_name}': {e}",
            err=True
        )

        sys.exit(1)

    except Exception as e:
        typer.echo(
            f"An unexpected error occurred: {e}",
            err=True
        )

        sys.exit(1)


@collection_app.command("delete")
def delete_collection(
    collection_name: str = typer.Argument(
        default=...,
        help="Name of the collection to delete."
    )
) -> None:
    typer.echo(
        f"Attempting to delete collection: {collection_name}"
    )

    try:
        mongodb_api.delete_collections_mongodb_collections_collection_name_delete(
            collection_name=collection_name
        )

        typer.echo(
            f"Collection '{collection_name}' deleted successfully."
        )

    except ApiException as e:
        typer.echo(
            f"Error deleting collection '{collection_name}': {e}",
            err=True
        )

        sys.exit(1)

    except Exception as e:
        typer.echo(
            f"An unexpected error occurred: {e}",
            err=True
        )

        sys.exit(1)


@index_app.command("get")
def get_collection_indexes(
    collection_name: str = typer.Argument(
        default=...,
        help="Name of the collection to retrieve indexes from."
    )
) -> None:
    typer.echo(
        f"Getting indexes for collection: {collection_name}"
    )

    try:
        indexes = mongodb_api.get_collections_index_mongodb_collections_collection_name_index_get(
            collection_name=collection_name
        )

        if indexes:
            typer.echo(
                f"Indexes for '{collection_name}':"
            )

            for idx in indexes:
                typer.echo(
                    json.dumps(idx, indent=4)
                )

        else:
            typer.echo(
                f"No indexes found for collection '{collection_name}'."
            )

    except ApiException as e:
        typer.echo(
            f"Error getting indexes for collection '{collection_name}': {e}",
            err=True
        )

        sys.exit(1)

    except Exception as e:
        typer.echo(
            f"An unexpected error occurred: {e}",
            err=True
        )

        sys.exit(1)


@index_app.command("create")
def create_collection_index(
    collection_name: str = typer.Argument(
        default=...,
        help="Name of the collection."
    ),
    key: str = typer.Option(
        default=...,
        help="JSON string representing the index key (e.g., '{\"field_name\": \"ASCENDING\"}').",
        callback=lambda x: json.loads(x)
    ),
    unique: bool = typer.Option(
        default=...,
        help="Whether the index should enforce uniqueness."
    )
) -> None:
    typer.echo(
        f"Attempting to create index on collection: {collection_name} with key: {key}, unique: {unique}"
    )

    try:
        post_collections_index_request = PostCollectionsIndexRequest(
            key=key,
            unique=unique
        )

        mongodb_api.post_collections_index_mongodb_collections_collection_name_index_post(
            collection_name=collection_name,
            post_collections_index_request=post_collections_index_request
        )

        typer.echo(
            f"Index created on '{collection_name}' successfully."
        )

    except ApiException as e:
        typer.echo(
            f"Error creating index on collection '{collection_name}': {e}",
            err=True
        )

        sys.exit(1)

    except Exception as e:
        typer.echo(
            f"An unexpected error occurred: {e}",
            err=True
        )

        sys.exit(1)


@index_app.command("delete")
def delete_collection_index(
    collection_name: str = typer.Argument(
        default=...,
        help="Name of the collection."
    ),
    index_name: str = typer.Argument(
        default=...,
        help="Name of the index to delete."
    )
) -> None:
    typer.echo(
        f"Attempting to delete index '{index_name}' from collection: {collection_name}"
    )

    try:
        mongodb_api.delete_collections_index_mongodb_collections_collection_name_index_index_name_delete(
            collection_name=collection_name,
            index_name=index_name
        )

        typer.echo(
            f"Index '{index_name}' deleted from '{collection_name}' successfully."
        )

    except ApiException as e:
        typer.echo(
            f"Error deleting index '{index_name}' from collection '{collection_name}': {e}",
            err=True
        )

        sys.exit(1)

    except Exception as e:
        typer.echo(
            f"An unexpected error occurred: {e}",
            err=True
        )

        sys.exit(1)


@validator_app.command("get")
def get_collection_validator(
    collection_name: str = typer.Argument(
        default=...,
        help="Name of the collection to retrieve validator from."
    )
) -> None:
    typer.echo(
        f"Getting validator for collection: {collection_name}"
    )

    try:
        validator = mongodb_api.get_collections_validator_mongodb_collections_collection_name_validator_get(
            collection_name=collection_name
        )

        if validator:
            typer.echo(
                f"Validator for '{collection_name}':"
            )

            typer.echo(
                json.dumps(validator, indent=2)
            )

        else:
            typer.echo(
                f"No validator found for collection '{collection_name}'."
            )

    except ApiException as e:
        typer.echo(
            f"Error getting validator for collection '{collection_name}': {e}",
            err=True
        )

        sys.exit(1)

    except Exception as e:
        typer.echo(
            f"An unexpected error occurred: {e}",
            err=True
        )

        sys.exit(1)


@validator_app.command("update")
def update_collection_validator(
    collection_name: str = typer.Argument(
        default=...,
        help="Name of the collection to update validator for."
    ),
    validator: str = typer.Option(
        default=...,
        help="JSON string representing the validator document (e.g., '{\"fieldA\": {\"$type\": \"string\"}}').",
        callback=lambda x: json.loads(x)
    ),
    validation_level: str | None = typer.Option(
        default="strict",
        help="Validation level: 'off', 'strict', or 'moderate'."
    ),
    validation_action: str | None = typer.Option(
        default="error",
        help="Validation action: 'error' or 'warn'."
    )
) -> None:
    typer.echo(
        f"Updating validator for collection: {collection_name}"
    )

    try:
        put_collections_validator_request = PutCollectionsValidatorRequest(
            validator=validator,
            validation_level=validation_level,
            validation_action=validation_action
        )

        mongodb_api.put_collections_validator_mongodb_collections_collection_name_validator_put(
            collection_name=collection_name,
            put_collections_validator_request=put_collections_validator_request
        )

        typer.echo(
            f"Validator for '{collection_name}' updated successfully."
        )

    except ApiException as e:
        typer.echo(
            f"Error updating validator for collection '{collection_name}': {e}",
            err=True
        )

        sys.exit(1)

    except Exception as e:
        typer.echo(
            f"An unexpected error occurred: {e}",
            err=True
        )

        sys.exit(1)


@validator_app.command("summary")
def get_collection_validator_summary(
    collection_name: str = typer.Argument(
        default=...,
        help="Name of the collection to get validator error summary from."
    )
) -> None:
    typer.echo(
        f"Getting validator error summary for collection: {collection_name}"
    )

    try:
        summary = mongodb_api.get_collections_validator_validation_error_summary_mongodb_collections_collection_name_validator_validation_error_summary_get(
            collection_name=collection_name
        )

        if summary:
            typer.echo(
                f"Validator error summary for '{collection_name}':"
            )

            typer.echo(
                json.dumps(summary, indent=4)
            )

        else:
            typer.echo(
                f"No validator error summary found for collection '{collection_name}'."
            )

    except ApiException as e:
        typer.echo(
            f"Error getting validator error summary for collection '{collection_name}': {e}",
            err=True
        )

        sys.exit(1)

    except Exception as e:
        typer.echo(
            f"An unexpected error occurred: {e}",
            err=True
        )

        sys.exit(1)


if __name__ == "__main__":
    app()
