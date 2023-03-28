#!/usr/bin/env python
# Should be put in root
import os

LOG_FILE = "f1.txt"
OBJECTS_FILE = "f2.txt"

os.system(f"git log --name-only | grep commit > {LOG_FILE}")
os.system(f"git cat-file --batch-check --batch-all-objects  | grep commit > {OBJECTS_FILE}")

log_list = []
obj_list = []

with open(LOG_FILE, "r") as file:
  for line in file:
    log_list.append(line.split(' ')[1].strip())

with open(OBJECTS_FILE, "r") as file:
  for line in file:
    obj_list.append(line.split(' ')[0].strip())

for obj in obj_list:
  if obj not in log_list:
    os.system(f"git show {obj} | grep vrnctf")
