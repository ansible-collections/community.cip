#!/usr/bin/env python3

from pycomm3 import LogixDriver
import sys

# Expected arguements:
# argv[1]: Path to the module to query
# argv[2]: Tag name
# argv[3]: Tag value as a string

# pycomm3 handles datatypes for us? 

rc = 0
module_path = sys.argv[1]
tag_name = sys.argv[2]
tag_value = sys.argv[3]
#create_if_nonexistant = sys.argv[5].lower() in ['True', 'true', 1]

with LogixDriver(module_path) as plc:
  if tag_name in plc.tags_json:
    print(f'Previous tag value: {plc.read(tag_name).value}')
    if str(plc.read(tag_name).value).lower() == tag_value.lower(): # Gross
        # Checking all this is not needed right now, but once implemented as a module(?) we will use this to check idepotence
        print(f"Requested tag value of {tag_value} matches current value in controller")

  # Do some nasty type guessing for common types. It's a demo, we'll live
  plc_data_type = plc.read(tag_name).type
  if plc_data_type == 'BOOL':
    tag_value = tag_value.lower() in ['true', '1', 't', 'y', 'yes']
  elif plc_data_type == 'REAL' or plc_data_type == 'FLOAT':
    tag_value = float(tag_value)
  elif plc_data_type == 'DINT' or plc_data_type == 'DINT':
    tag_value = int(tag_value)


  write_result = plc.write(tag_name, tag_value)
  print(write_result)
  rc = not bool(write_result)

sys.exit(rc)
