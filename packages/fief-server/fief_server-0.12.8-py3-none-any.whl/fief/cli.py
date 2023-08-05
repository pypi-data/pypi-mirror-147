import asyncio
import secrets

import typer
import uvicorn
from alembic import command
from alembic.config import Config
from dramatiq import cli as dramatiq_cli
from pydantic import ValidationError
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from fief import __version__
from fief.crypto.encryption import generate_key
from fief.paths import ALEMBIC_CONFIG_FILE
from fief.services.workspace_db import WorkspaceDatabase

app = typer.Typer()


def get_settings():
    from fief.settings import settings

    return settings


@app.command()
def quickstart(
    docker: bool = typer.Option(
        False,
        help="Show the Docker command to run the Fief server with required environment variables.",
    )
):
    """Generate secrets and keys to help users getting started quickly."""
    typer.secho(
        "⚠️  Be sure to save the generated secrets somewhere safe for subsequent runs. Otherwise, you may lose access to the data.",
        bold=True,
        fg="red",
        err=True,
    )
    generated_secrets = {
        "SECRET": secrets.token_urlsafe(64),
        "FIEF_CLIENT_ID": secrets.token_urlsafe(),
        "FIEF_CLIENT_SECRET": secrets.token_urlsafe(),
        "ENCRYPTION_KEY": generate_key().decode("utf-8"),
    }
    if docker:
        parts = [
            "docker run",
            "--name fief-server",
            "-p 8000:8000",
            "-d",
            *[f'-e "{name}={value}"' for (name, value) in generated_secrets.items()],
            "ghcr.io/fief-dev/fief:latest",
        ]
        typer.echo(" \\\n  ".join(parts))
    else:
        for (name, value) in generated_secrets.items():
            typer.echo(f"{typer.style(name, bold=True)}: {value}")


@app.command()
def info():
    """Show current Fief version and settings."""
    try:
        settings = get_settings()

        typer.secho(f"Fief version: {__version__}", bold=True)
        typer.secho(f"Settings", bold=True)
        for key, value in settings.dict().items():
            typer.echo(f"{key}: {value}")
    except ValidationError as e:
        typer.secho(
            "❌ Some environment variables are missing or invalid.", bold=True, fg="red"
        )
        typer.secho(
            "Run 'fief quickstart' to help you generate the secrets.", bold=True
        )
        for error in e.errors():
            typer.secho(error)
        raise typer.Exit(code=1) from e


@app.command("migrate-main")
def migrate_main():
    """Apply database migrations to the main database."""
    settings = get_settings()

    engine = create_engine(settings.get_database_url(False))
    with engine.begin() as connection:
        alembic_config = Config(ALEMBIC_CONFIG_FILE, ini_section="main")
        alembic_config.attributes["connection"] = connection
        command.upgrade(alembic_config, "head")


@app.command("migrate-workspaces")
def migrate_workspaces():
    """Apply database migrations to each workspace database."""
    from fief.models import Workspace

    settings = get_settings()

    engine = create_engine(settings.get_database_url(False))
    Session = sessionmaker(engine)
    with Session() as session:
        workspace_db = WorkspaceDatabase()
        workspaces = select(Workspace)
        for [workspace] in session.execute(workspaces):
            assert isinstance(workspace, Workspace)
            typer.secho(f"Migrating {workspace.name}", bold=True)
            workspace_db.migrate(
                workspace.get_database_url(False), workspace.get_schema_name()
            )


@app.command("create-main-workspace")
def create_main_workspace():
    """Create a main Fief workspace following the environment settings."""
    from fief.services.main_workspace import (
        MainWorkspaceAlreadyExists,
        create_main_fief_workspace,
    )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(create_main_fief_workspace())
        typer.echo("Main Fief workspace created")
    except MainWorkspaceAlreadyExists as e:
        typer.echo("Main Fief workspace already exists")
        raise typer.Exit(code=1) from e


@app.command("create-main-user")
def create_main_user(
    user_email: str = typer.Option(..., help="The admin user email"),
    user_password: str = typer.Option(
        ...,
        prompt=True,
        confirmation_prompt=True,
        hide_input=True,
        help="The admin user password",
    ),
):
    """Create a main Fief workspace user."""
    from fief.services.main_workspace import (
        CreateMainFiefUserError,
        create_main_fief_user,
    )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(create_main_fief_user(user_email, user_password))
        typer.echo("Main Fief user created")
    except CreateMainFiefUserError as e:
        typer.echo("An error occured")
        raise typer.Exit(code=1) from e


@app.command("run-server")
def run_server(
    host: str = "0.0.0.0",
    port: int = 8000,
    migrate: bool = typer.Option(
        True,
        help="Run the migrations on main and workspaces databases before starting.",
    ),
):
    """Run the Fief backend server."""
    if migrate:
        migrate_main()
        migrate_workspaces()
    uvicorn.run("fief.app:app", host=host, port=port)


@app.command(
    "run-worker",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    add_help_option=False,
)
def run_worker(ctx: typer.Context):
    """
    Run the Fief worker.

    Just forwards the options to the Dramatiq CLI.
    """
    parser = dramatiq_cli.make_argument_parser()
    args = parser.parse_args(ctx.args + ["fief.worker"])
    dramatiq_cli.main(args)


if __name__ == "__main__":
    app()
