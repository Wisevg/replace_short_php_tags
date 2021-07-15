import os,sys
import re
from typing import Any, Callable

# temporary list for different purposes
tmp = {}


def process_dir(dir_path: str, root_dir: str = None, processed_dir: str = None) -> None:
  # if root_dir is not define, define it as current dir
  if not root_dir: root_dir = os.path.abspath(dir_path)
  # if dir for processed files is not defined, define it as root_dir's subfolder 'processed'
  if not processed_dir:
    processed_dir = os.path.join(root_dir, 'processed')
    if not os.path.exists(processed_dir): os.mkdir(processed_dir) 
  
  
  for file in os.listdir(dir_path):
    file_path: str = os.path.join(dir_path, file)

    # if file is directory for processed files, then skip iteration
    if (file_path == processed_dir): continue
    
    processed_file_path: str = os.path.join(processed_dir, os.path.relpath(file_path, root_dir))
    
    if (os.path.isdir(file_path)):
      process_dir(file_path, root_dir)
    else:
      # make all subfolders if they doesnt exist
      if not os.path.exists(os.path.split(processed_file_path)[0]):
        os.makedirs(os.path.split(processed_file_path)[0])

      replace_short_php(file_path, processed_file_path)


def apply_line_by_line(abs_path, func: Callable[[str, int, str], Any]) -> None:
  with open(abs_path, 'r') as f:
    line_number: int = 1
    while True:
      line: str = f.readline()
      if not line: break
      func(line, line_number, abs_path)
      line_number += 1

def replace_short_php(inp_path: str, out_path: str) -> None:
  if not os.path.splitext(inp_path)[1] == '.php': return # return if not a php file
  with open(out_path, 'w') as out:
    apply_line_by_line(inp_path, lambda line, _, __: out.write(process_php_line(line)))

# replace '<?=' with '<?php echo ' and '<?' with '<?php '
def process_php_line(line: str) -> str:
  line = re.sub(r'<\?=', '<?php echo ', line)
  line = re.sub(r'<\?(?!=)(?!php)', '<?php ', line)
  return line


def check_dir_for_short_php(dir_path):
  for file in os.listdir(dir_path):
    file_path = os.path.join(dir_path, file)
    if os.path.isdir(file_path):
      check_dir_for_short_php(file_path)
    else:
      check_for_short_php(file_path)

# print all lines that contains '<?' or '<?='
def check_for_short_php(abs_path: str):
  if not os.path.splitext(abs_path)[1] == '.php': return # return if not a php file

  apply_line_by_line(abs_path, print_line_if_contains_short_php)

# True: if contains '<?' or '<?='
def contains_short_php(line: str) -> bool:
  contains: bool = False
  contains = contains | bool(re.findall(r'<\?=', line))
  contains = contains | bool(re.findall(r'<\?(?!=)(?!php)', line))
  return contains

# print line in format '1: ...code...'
def print_line_if_contains_short_php(line: str, num: int, file_path: str) -> None:
  if contains_short_php(line):
    
    try:
      if not file_path in tmp['printed']:
        add_file_to_printed(file_path)
    except:
      tmp['printed'] = []
      add_file_to_printed(file_path)
      
    print('{}| {}'.format(num, line.strip()))

def add_file_to_printed(file_path):
  print('\n>>> ' + file_path + '\n')
  tmp['printed'].append(file_path)


for arg in sys.argv:
  if not arg in ['-c']:
    arg = os.path.abspath(arg)
    if not os.path.exists(arg): 
      print('"{}" is not a valid file/dir name')
      sys.exit()
    if os.path.isdir(arg):
      if '-c' in sys.argv:
        check_dir_for_short_php(arg)
      else:
        process_dir(arg)
    else:
      if '-c' in sys.argv:
        check_for_short_php(arg)
      else:
        split = os.path.split(arg)
        replace_short_php(arg, os.path.join(split[0], 'processed-'+split[1]))
