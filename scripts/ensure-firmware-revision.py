#!/usr/bin/env python3

from pycomm3 import LogixDriver
import sys

# Expects two arguements:
# argv[1]: Path to the module to query
# argv[2]: Expected major firmware revision
rc = 0
module_path = sys.argv[1]
expected_revision = int(sys.argv[2])

with LogixDriver(module_path) as plc:
  module_revision = plc.revision_major

  print(f'Expected revision: {expected_revision} | Module Revision: {module_revision}')
  if module_revision != expected_revision:
    rc = 1
   
sys.exit(rc)
