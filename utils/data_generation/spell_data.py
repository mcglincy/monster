#!/usr/bin/python3
import sys
sys.path.insert(0, '../..')

import json
from generator_utils import *


def fill_in(rec, key, descs, lines):
  desc_id = rec[key]
  if desc_id:
    rec[key] = lookup_description(desc_id, descs, lines)
  else:
    rec[key] = ""


def create_spells():
  for rec in SPELLS:
    fill_in(rec, "caster_desc", DESCS, LINES)
    fill_in(rec, "victim_desc", DESCS, LINES)
    fill_in(rec, "failure_desc", DESCS, LINES)
    alignment = rec["alignment"]
    if (alignment < 0 or alignment > 99):
      rec["alignment"] = 66  # neutral
  print(json.dumps(SPELLS, indent=2, sort_keys=False))    


if __name__ == "__main__":
  create_spells()