# -*- coding: utf-8 -*-

import json
import os
import sys
from functools import wraps

import typer
from dotenv import load_dotenv

from openapi_client import ApiClient, Configuration
from openapi_client.api import DevicesApi
from openapi_client.exceptions import ApiException
from openapi_client.models import (
    DateRangeFilter,
    DeviceSearchFilter,
    ErrorModel,
    ImeiFilter,
    JobQueueFilter,
    LastSeenAtFilter,
    PostDevicesRequest,
    PostDevicesSearchRequest
)


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

devices_api = DevicesApi(
    api_client=api_client
)

app = typer.Typer(help="IoT Jobs CLI")

devices_app = typer.Typer(help="Manage IoT Devices.")

app.add_typer(devices_app, name="devices")


def handle_api_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ApiException as e:
            print_error(e)

            sys.exit(1)

        except Exception as e:
            typer.secho(
                f"Unexpected error: {e}",
                fg=typer.colors.RED,
                bold=True,
                err=True
            )

            sys.exit(1)

    return wrapper


def print_success(message: str, model=None) -> None:
    typer.secho(
        message,
        fg=typer.colors.GREEN,
        bold=True
    )

    if model is not None:
        typer.secho(
            model.model_dump_json(indent=4, exclude_none=False),
            bold=True
        )


def print_error(e: ApiException) -> None:
    typer.secho(
        f"Error: {e.status} {e.reason}",
        fg=typer.colors.RED,
        bold=True
    )

    if e.body is not None:
        error = ErrorModel(**json.loads(e.body).get("error", {}))

        typer.secho(
            json.dumps({"error": error.model_dump()}, indent=4),
            bold=True,
            err=True
        )


def parse_json_str(json_str: str):
    try:
        return json.loads(json_str)

    except json.JSONDecodeError:
        typer.echo(
            f"Error: Invalid JSON string: {json_str}",
            err=True
        )

        sys.exit(1)


@devices_app.command("create")
@handle_api_call
def create_device(
    imei: str = typer.Argument(
        default=...,
        help="15-digit IMEI."
    )
) -> None:
    typer.echo(f"Attempting to create device with IMEI: {imei}")

    post_devices_request = PostDevicesRequest(
        imei=imei
    )

    response = devices_api.post_devices_v1_devices_post(
        post_devices_request=post_devices_request
    )

    print_success(f"Device '{imei}' created successfully.", response)


@devices_app.command("get")
@handle_api_call
def get_device(
    imei: str = typer.Argument(
        default=...,
        help="15-digit IMEI."
    )
) -> None:
    typer.echo(f"Getting details for device with IMEI: {imei}")

    response = devices_api.get_devices_v1_devices_imei_get(
        imei=imei
    )

    print_success(f"Device '{imei}':", response)


@devices_app.command("delete")
@handle_api_call
def delete_device(
    imei: str = typer.Argument(
        default=...,
        help="15-digit IMEI."
    )
) -> None:
    typer.echo(f"Attempting to delete device with IMEI: {imei}")

    devices_api.delete_devices_v1_devices_imei_delete(
        imei=imei
    )

    print_success(f"Device '{imei}' deleted successfully.")


@devices_app.command("search")
@handle_api_call
def search_devices(
    filter: str | None = typer.Option(
        None,
        "--filter",
        "-f",
        help="Search filter JSON string.",
        callback=lambda x: parse_json_str(x) if x else None
    )
) -> None:
    typer.echo("Searching for devices...")

    post_devices_search_request = PostDevicesSearchRequest()

    if filter is not None:
        device_search_filter_obj = DeviceSearchFilter()

        if "imei" in filter:
            device_search_filter_obj.imei = ImeiFilter(
                var_in=filter["imei"].get("in")
            )

        if "created_at" in filter:
            device_search_filter_obj.created_at = DateRangeFilter(
                gte=filter["created_at"].get("gte"),
                lte=filter["created_at"].get("lte")
            )

        if "updated_at" in filter:
            device_search_filter_obj.updated_at = DateRangeFilter(
                gte=filter["updated_at"].get("gte"),
                lte=filter["updated_at"].get("lte")
            )

        if "last_seen_at" in filter:
            device_search_filter_obj.last_seen_at = LastSeenAtFilter(
                is_empty=filter["last_seen_at"].get("is_empty"),
                gte=filter["last_seen_at"].get("gte"),
                lte=filter["last_seen_at"].get("lte")
            )

        if "job_queue" in filter:
            device_search_filter_obj.job_queue = JobQueueFilter(
                is_empty=filter["job_queue"].get("is_empty"),
                contains_any=filter["job_queue"].get("contains_any")
            )

        post_devices_search_request.filter = device_search_filter_obj

    response = devices_api.post_devices_search_v1_devices_search_post(
        post_devices_search_request=post_devices_search_request
    )

    if response.devices:
        print_success(f"Found {len(response.devices)} devices:")

        for device in response.devices:
            typer.secho(
                device.model_dump_json(indent=4, exclude_none=False),
                bold=True
            )

    else:
        typer.secho(
            "No devices found.",
            fg=typer.colors.YELLOW
        )


if __name__ == "__main__":
    app()
