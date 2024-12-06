import typer
from .commands.tune import tune_app
from .commands.files import files_app
from .commands.auth import auth_app
from .commands.model import model_app

# Create typer app
app = typer.Typer(help="Felafax CLI")

# Create sub-commands
app.add_typer(auth_app, name="auth")
app.add_typer(files_app, name="files")
app.add_typer(tune_app, name="tune")
app.add_typer(model_app, name="model")
if __name__ == "__main__":
    app()