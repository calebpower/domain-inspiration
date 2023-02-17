"""This module provides the synonym model controller."""
# dominsp/synonym.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from dominsp import DB_READ_ERROR
from dominsp.database import DatabaseHandler

class CurrentSynonym(NamedTuple):
  synonym: Dict[str, Any]
  error: int

class SynonymHandler:
  def __init__(self, db_path: Path) -> None:
    self._db_handler = DatabaseHandler(db_path)

  def add(self, word: List[str]) -> CurrentSynonym:
    """Add a new synonym to the database."""
    word_text = " ".join(word)
    syn = {
      "word": word_text,
      "status": 0,
    }
    read = self._db_handler.read_synonyms()
    if read.error == DB_READ_ERROR:
      return CurrentSynonym(syn, read.error)
    read.synonym_list.append(syn)
    write = self._db_handler.write_synonyms(read.synonym_list)
    return CurrentSynonym(syn, write.error)

  def get_syn_list(self) -> List[Dict[str, Any]]:
    """Return the current list of synonyms."""
    read = self._db_handler.read_synonyms()
    return read.synonym_list
