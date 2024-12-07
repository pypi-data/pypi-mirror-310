from __future__ import annotations

import logging
import os
from datetime import datetime
from datetime import timezone
from pathlib import Path
from typing import Any

import click
import yaml
from yaml.parser import ParserError


@click.group()
def init_config() -> None:
    """
    Initialize configuration for modeling environment.

    Returns
    -------
    None
    """


def setup_logging() -> None:
    """
    Configure logging for the application.

    Returns
    -------
    None
    """
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def load_config(config_path: Path) -> dict[str, Any]:
    """
    Load configuration from YAML file.

    Parameters
    ----------
    config_path : Path
        The path to the configuration YAML file.

    Returns
    -------
    dict[str, Any]
        The loaded configuration as a dictionary.

    Raises
    ------
    click.Abort
        If there is an error parsing or reading the config file.
    """
    try:
        if config_path.exists():
            with config_path.open("r") as f:
                return yaml.safe_load(f) or {}
        else:
            return {}
    except ParserError as e:
        click.secho(f"Error parsing config file: {e}", fg="red")
        raise click.Abort from e
    except OSError as e:
        click.secho(f"Error reading config file: {e}", fg="red")
        raise click.Abort from e


def save_config(config: dict[str, Any], config_path: Path) -> None:
    """
    Save configuration to YAML file.

    Parameters
    ----------
    config : dict[str, Any]
        The configuration dictionary to save.
    config_path : Path
        The path to the configuration YAML file.

    Returns
    -------
    None

    Raises
    ------
    click.Abort
        If there is an error writing the config file.
    """
    try:
        with config_path.open("w") as f:
            yaml.dump(config, f, default_flow_style=False)
    except OSError as e:
        click.secho(f"Error writing config file: {e}", fg="red")
        raise click.Abort from e


def update_shell_config(project_root: Path, shell_config: Path, env_name: str) -> None:
    """
    Update shell configuration file with environment variables.

    Parameters
    ----------
    project_root : Path
        The root path of the project.
    shell_config : Path
        The path to the shell configuration file.
    env_name : str
        The name of the environment variable to set.

    Returns
    -------
    None

    Raises
    ------
    click.Abort
        If there is an error writing to the shell configuration file.
    """
    try:
        with shell_config.open("a") as f:
            f.write(
                f"\n# Set {env_name} for the ML project\nexport {env_name}={project_root}\n"
            )
        click.secho(f"Environment variable {env_name} set to: {project_root}", fg="green")
        click.secho(
            f"Please run 'source {shell_config}' or restart your terminal", fg="yellow"
        )
    except OSError as e:
        click.secho(f"Failed to write to {shell_config}: {e}", fg="red")
        raise click.Abort from e


@init_config.command()
@click.option("-n", "--project_name", type=str, help="Name of the project initialized")
def init(project_name: str) -> None:
    """
    Initialize project structure and environment variables.

    Parameters
    ----------
    project_name : str
        The name of the project to initialize.

    Returns
    -------
    None

    Raises
    ------
    click.Abort
        If the required project structure is missing and cannot be created.
    """
    setup_logging()
    logger = logging.getLogger(__name__)

    expected_folders = [
        "download_data",
        "notebooks",
        "models",
        "config",  # "src"
    ]

    # Check if the current directory has the required structure
    missing_folders = [folder for folder in expected_folders if not Path(folder).is_dir()]

    if missing_folders:
        click.secho(f"Missing folders: {', '.join(missing_folders)}", fg="red")
        click.secho(
            "Please ensure you are in the root directory of the project.", fg="yellow"
        )
        click.secho("Use --force to create missing folders automatically.", fg="yellow")
        raise click.Abort

    # TODO(Isaias Gutierrez): Evaluate if the path is empty, it it is maybe is the first time that is executed
    # Create missing folders if force flag is used
    force = True
    if force:
        for folder in missing_folders:
            Path(folder).mkdir(exist_ok=True)
            click.secho(f"Created folder: {folder}", fg="green")

    env_var_name = f"PROJECT_{project_name.upper()}_ROOT"

    # Get project root and config paths
    project_root = Path.cwd()
    config_path = project_root / "config" / "main.yml"
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Load and update configuration
    config = load_config(config_path)
    config.setdefault("project", {}).update(
        {
            "name": project_name,
            "created_at": datetime.now(tz=timezone.utc),
        }
    )

    # Save updated configuration
    save_config(config, config_path)
    logger.info("Configuration updated in %s", config_path)

    # Update shell configuration
    shell = Path(os.environ.get("SHELL", ""))
    shell_config = Path.home() / (".zshrc" if "zsh" in shell.name else ".bashrc")
    update_shell_config(project_root, shell_config, env_name=env_var_name)

    click.secho("Project initialization complete!", fg="green")
