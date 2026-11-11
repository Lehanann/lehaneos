import typer

from lehaneos.cli.user import app as app_user

app = typer.Typer()

app.add_typer(app_user, name="user")