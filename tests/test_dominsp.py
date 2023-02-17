# tests/test_dominsp.py

import json
import pytest

from typer.testing import CliRunner
from dominsp import (
  DB_READ_ERROR,
  SUCCESS,
  __app_name__,
  __version__,
  cli,
  synonym,
)

runner = CliRunner()

def test_version():
  result = runner.invoke(cli.app, ["--version"])
  assert result.exit_code == 0
  assert f"{__app_name__} v{__version__}\n" in result.stdout

@pytest.fixture
def mock_json_file(tmp_path):
  syn = [{"word": "apple", "status": 0}]
  db_file = tmp_path / "dominsp.json"
  with db_file.open("w") as db:
    json.dump(syn, db, indent=2)
  return db_file

test_data_1 = {
  "word": ["bad"],
  "syn": {
    "word": "bad",
    "status": 0
  },
}

test_data_2 = {
  "word": ["beef"],
  "syn": {
    "word": "beef",
    "status": 0
  }
}

@pytest.mark.parametrize(
  "word, expected",
  [
    pytest.param(
      test_data_1["word"],
      (test_data_1["syn"], SUCCESS),
    ),
    pytest.param(
      test_data_2["word"],
      (test_data_2["syn"], SUCCESS),
    ),
  ],
)

def test_add(mock_json_file, word, expected):
  syn_handler = synonym.SynonymHandler(mock_json_file)
  assert syn_handler.add(word) == expected
  read = syn_handler._db_handler.read_synonyms()
  assert len(read.synonym_list) == 2
