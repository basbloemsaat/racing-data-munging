#!/usr/bin/env python

import json
import os

from pprint import pprint
from dumper import dump

fname = os.path.join(os.path.dirname(__file__), "../data/state.json")

pprint(fname);

with open(fname) as f:
    state = json.load(f)

pprint(state)
dump(state)

print()
pprint(state['test'])

state['test'] = state['test']+1

print()
pprint(state['test'])

with open(fname, 'w') as outfile:
    json.dump(state, outfile)



