"""This module provides the Domain Inspiration database functionality."""
# dominsp/database.py

import configparser
from pathlib import Path

from dominsp import DB_WRITE_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(".dominsp.json")

def get_database_path(config_file: Path) -> Path:
  """Return the current path to the database."""
  config_parser = configparser.ConfigParser()
  config_parser.read(config_file)
  return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
  """Create the database."""
  try:
    db_path.write_text("[]")
    return SUCCESS
  except OSError:
    return DB_WRITE_ERROR
