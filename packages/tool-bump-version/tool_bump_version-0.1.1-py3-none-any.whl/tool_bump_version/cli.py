from pathlib import Path
import typer
from typing import Optional

from tool_bump_version.main import update_project_version, VersionPart


app = typer.Typer()


@app.command()
def bump(
    part: VersionPart = typer.Argument(
        ...,
        help="Version part to bump (major, minor, or patch)",
    ),
    project_dir: Optional[Path] = typer.Option(
        None,
        "--project-dir", "-d",
        help="Project directory containing pyproject.toml (defaults to current directory)",
    ),
):
    """Bump the version in pyproject.toml according to semver rules."""
    try:
        new_version = update_project_version(part, project_dir)
        typer.echo(f"Version bumped to {new_version}")
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()