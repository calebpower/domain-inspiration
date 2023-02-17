"""This module provides the synonym model controller."""
# dominsp/synonym.py

import re

from nltk.corpus import wordnet
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

  def add(self, word: List[str], status: int=0) -> CurrentSynonym:
    """Add a new synonym to the database."""
    word_text = " ".join(word).lower()
    syn = {
      "word": word_text,
      "status": status,
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

  def process(self) -> None:
    """Process entries-- generate synonyms and their domain statuses."""
    syn_list = self.get_syn_list()
    synonyms = []
    for id, syndict in enumerate(syn_list, 1):
      word, status = syndict.values()
      if status == 0:
        for syn in wordnet.synsets(word):
          for lemma in syn.lemmas():
            synonyms.append(re.sub(r'[^A-Za-z0-9]', "", lemma.name().lower()))
        syndict["status"] = 1
    synonyms = list(set(synonyms))
    for id, syndict in enumerate(syn_list, 1):
      word, status = syndict.values()
      if word in synonyms:
        synonyms.remove(word)
    self._db_handler.write_synonyms(syn_list)
    for syn in synonyms:
      self.add(syn.split("_"), 1)
