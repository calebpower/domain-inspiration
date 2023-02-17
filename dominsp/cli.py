"""This module provides the Domain Inspiration CLI."""
# dominsp/cli.py

from pathlib import Path
from typing import List, Optional

import typer

from dominsp import (
  ERRORS,
  __app_name__,
  __version__,
  config,
  database,
  synonym
)

app = typer.Typer()

@app.command()
def init(
  db_path: str = typer.Option(
    str(database.DEFAULT_DB_FILE_PATH),
    "--db-path",
    "-db",
    prompt="database location?",
  ),
) -> None:
  """Initialize the database."""
  app_init_error = config.init_app(db_path)
  if app_init_error:
    typer.secho(
      f'Config file creation failed with "{ERRORS[app_init_error]}"',
      fg=typer.colors.RED,
    )
    raise typer.Exit(1)
  db_init_error = database.init_database(Path(db_path))
  if db_init_error:
    typer.secho(
      f'Database creation failed with "{ERRORS[db_init_error]}"',
      fg=typer.colors.RED,
    )
    raise typer.Exit(1)
  else:
    typer.secho(
      f'The database is located at {db_path}',
      fg=typer.colors.GREEN,
    )

def _version_callback(value: bool) -> None:
  if value:
    typer.echo(f"{__app_name__} v{__version__}")
    raise typer.Exit()

def get_syn_handler() -> synonym.SynonymHandler:
  if config.CONFIG_FILE_PATH.exists():
    db_path = database.get_database_path(config.CONFIG_FILE_PATH)
  else:
    typer.secho(
      'Config file not found. Please run "dominsp init"',
      fg=typer.colors.RED,
    )
    raise typer.Exit(1)
  if db_path.exists():
    return synonym.SynonymHandler(db_path)
  else:
    typer.secho(
      'Database not found. Please run "dominsp init"',
      fg=typer.colors.RED,
    )
    raise typer.Exit(1)

@app.command()
def add(
  word: List[str] = typer.Argument(...),
) -> None:
  """Add a new word to look up."""
  syn_handler = get_syn_handler()
  syn, error = syn_handler.add(word)
  if error:
    typer.secho(
      f'Tried to add a word but got error "{ERRORS[error]}"',
      fg=typer.colors.RED,
    )
    raise typer.Exit(1)
  else:
    typer.secho(
      f"""New word "{syn['word']}" was queued.""",
      fg=typer.colors.GREEN,
    )

@app.callback()
def main(
  version: Optional[bool] = typer.Option(
    None,
    "--version",
    "-v",
    help="Show the application's version and exit.",
    callback=_version_callback,
    is_eager=True,
  )
) -> None:
  return
