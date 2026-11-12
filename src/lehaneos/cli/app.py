import typer

from lehaneos.cli.user import app as app_user
from lehaneos.core.logging_config import configure_logging

configure_logging()

app = typer.Typer()

app.add_typer(app_user, name="user")