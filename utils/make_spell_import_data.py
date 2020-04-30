#!/usr/bin/python3
import sys
sys.path.insert(0, '..')

import json
from gamerules.spell_effect_kind import SpellEffectKind
from utils.generator_utils import lookup_description


CLASSREC_FILE = "./og_monster_data/classrec.json"
DESC_FILE = './og_monster_data/desc.json'
LINES_FILE = './og_monster_data/lines.json'
SPELLS_FILE = "./og_monster_data/spells.json"


def fill_in(rec, key, descs, lines):
  desc_id = rec[key]
  if desc_id:
    rec[key] = lookup_description(desc_id, descs, lines)
  else:
    rec[key] = ""


def create_spells():
  with open(DESC_FILE) as f:
    descs = json.load(f)
  with open(LINES_FILE) as f:
    lines = json.load(f)
  with open(SPELLS_FILE) as f:
    spells = json.load(f)

  for rec in spells:
    fill_in(rec, "caster_desc", descs, lines)
    fill_in(rec, "victim_desc", descs, lines)
    fill_in(rec, "failure_desc", descs, lines)
    alignment = rec["alignment"]
    if (alignment < 0 or alignment > 99):
      rec["alignment"] = 66  # neutral

  print(json.dumps(spells, indent = 2, sort_keys=False))    


if __name__ == "__main__":
  create_spells()