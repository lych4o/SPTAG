import sys
import os
import shutil
import subprocess

def build_config(dir, template_config_path, max_check, internal_result_num):
  print("dir: {}".format(dir))
  new_config_name = '{}/config_{}_{}.ini'.format(dir, max_check, internal_result_num)
  print("new_config_name: {}".format(new_config_name))

  with open(template_config_path, 'r') as template_file:
    content = template_file.read()
  
  lines = content.splitlines(keepends=True)

  max_check_flag = False
  internal_result_num_flag = False

  for i in range(len(lines)-1, -1, -1):
    if lines[i].startswith('MaxCheck') and not max_check_flag:
      max_check_flag = True
      lines[i] = 'MaxCheck={}\n'.format(max_check)
    elif lines[i].startswith('InternalResultNum') and not internal_result_num_flag:
      internal_result_num_flag = True
      lines[i] = 'InternalResultNum={}\n'.format(internal_result_num)
    
  with open(new_config_name, 'w') as new_config_file:
    new_config_file.writelines(lines)
  
  return new_config_name

def test_spann(dir, template_config_path, max_cjeck, internal_result_num):
  config_path = build_config(dir, template_config_path, max_check, internal_result_num)
  command = './../Release/ssdserving  {} > {}/{}_{}.log 2>&1'.format(config_path, dir, max_check, internal_result_num)

  print("Running command: {}".format(command))
  
  subprocess.run(command, shell=True)
  print("Finish")

if __name__ == "__main__":
  if len(sys.argv) != 4:
    print("Usage: python search_sift.py <max_check> <internal_result_num> <template_config_path>")
    sys.exit(1)

  max_check = int(sys.argv[1])
  internal_result_num = int(sys.argv[2])
  template_config_path = sys.argv[3]

  # dir = 'sift1m_exp_result_6_17'
  # dir = 'sift1m_exp_result'
  dir = 'sift100m_7_23_exp_result'

  os.makedirs(dir, exist_ok=True)
  
  test_spann(dir, template_config_path, max_check, internal_result_num)