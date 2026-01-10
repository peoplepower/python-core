# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "click",
#   "requests",
#   "pydantic",
# ]
# ///

import os

import click

from caredaily import (
    Authentication,
    CareDaily,
    CloudConnectivity,
)

from .configure import configure

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--profile", default=os.environ.get("CAREDAILY_PROFILE"), help="The profile to use."
)
@click.pass_context
def app(ctx, profile):
    """caredaily - commandline API client configuration utility.

    caredaily is a commandline utility to configure and interact with the CareDaily API.

    Set the CAREDAILY_PROFILE environment variable to specify a default profile

    Example:

        $ caredaily configure init

    """
    ctx.ensure_object(dict)
    caredaily = CareDaily(profile=profile, raise_errors=False)
    ctx.obj["caredaily"] = caredaily
    ctx.obj["profile"] = profile
    pass


@click.command()
@click.pass_context
def ping(ctx):
    try:
        ctx.obj["caredaily"].app_api(CloudConnectivity).check_availability()
        click.echo("Pong")
    except click.UsageError as e:
        click.echo(e)
    except Exception as e:
        import traceback

        click.echo(f"Ping failed: {e} {traceback.format_exc()}")


@click.command()
@click.option(
    "--check-availability", is_flag=True, help="Check the availability of the server."
)
@click.option("--version", is_flag=True, help="Retrieve the version of the server.")
@click.option(
    "--connection-settings", is_flag=True, help="Retrieve detailed server information."
)
@click.option(
    "--server-url", is_flag=True, help="Retrieve detailed server information."
)
@click.pass_context
def cloud_connectivity(
    ctx, check_availability, version, connection_settings, server_url
):
    try:
        if check_availability:
            result = (
                ctx.obj["caredaily"].app_api(CloudConnectivity).check_availability()
            )
        elif version:
            result = (
                ctx.obj["caredaily"].app_api(CloudConnectivity).get_version(json_format=True)
            )
        elif connection_settings:
            result = (
                ctx.obj["caredaily"].app_api(CloudConnectivity).get_cloud_settings()
            )
        elif server_url:
            result = (
                ctx.obj["caredaily"]
                .app_api(CloudConnectivity)
                .get_server_settings_url()
            )
        else:
            raise click.UsageError("At least one option is required.")
        try:
            import json
            click.echo(json.dumps(result.data, indent=4))
        except Exception:
            click.echo(result.data)
    except click.UsageError as e:
        click.echo(e)
    except Exception as e:
        import traceback

        click.echo(f"Failed to get version: {e} {traceback.format_exc()}")


@click.command()
@click.option("--username", prompt="Username")
@click.option("--password", prompt="Password", hide_input=True)
@click.pass_context
def login(ctx, username, password):
    try:
        result = (
            ctx.obj["caredaily"]
            .app_api(Authentication)
            .login_by_username(username=username, password=password)
        )
        click.echo(result.data)
    except click.UsageError as e:
        click.echo(e)
    except Exception as e:
        import traceback

        click.echo(f"Login failed: {e} {traceback.format_exc()}")


app.add_command(configure)
app.add_command(ping)
app.add_command(cloud_connectivity)
app.add_command(login)
