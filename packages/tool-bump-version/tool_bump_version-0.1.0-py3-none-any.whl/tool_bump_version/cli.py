import typer

from tool_bump_version.main import hello


app = typer.Typer()
app.command()(hello)


if __name__ == "__main__":
    app()