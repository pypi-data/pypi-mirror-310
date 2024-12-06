from enum import Enum
from pathlib import Path
import tomli
import tomli_w
from typing import Optional


class VersionPart(str, Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"


def bump_version(version: str, part: VersionPart) -> str:
    major, minor, patch = map(int, version.split('.'))
    
    if part == VersionPart.MAJOR:
        return f"{major + 1}.0.0"
    elif part == VersionPart.MINOR:
        return f"{major}.{minor + 1}.0"
    else:  # PATCH
        return f"{major}.{minor}.{patch + 1}"


def update_project_version(part: VersionPart, project_dir: Optional[Path] = None) -> str:
    """Update the version in pyproject.toml according to semver rules."""
    project_dir = project_dir or Path.cwd()
    pyproject_path = project_dir / "pyproject.toml"
    
    if not pyproject_path.exists():
        raise FileNotFoundError(f"Could not find pyproject.toml in {project_dir}")
    
    # Read the current pyproject.toml
    with open(pyproject_path, "rb") as f:
        pyproject = tomli.load(f)
    
    current_version = pyproject["project"]["version"]
    new_version = bump_version(current_version, part)
    
    # Update the version
    pyproject["project"]["version"] = new_version
    
    # Write back to pyproject.toml
    with open(pyproject_path, "wb") as f:
        tomli_w.dump(pyproject, f)
    
    return new_version
