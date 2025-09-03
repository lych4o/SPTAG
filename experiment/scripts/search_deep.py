import sys
import os
import shutil
import subprocess

def build_config(dir,template_config_path, ratio, rc, max_check, internal_result_num):
  print("dir: {}".format(dir))
  new_config_name = f'{dir}/config_{ratio}_{rc}_{max_check}_{internal_result_num}.ini'
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
    elif lines[i].startswith('IndexDirectory'):
      lines[i] = f'IndexDirectory=../deep_index/{ratio}_{rc}\n'
    
  with open(new_config_name, 'w') as new_config_file:
    new_config_file.writelines(lines)
  
  return new_config_name

def test_spann(dir, template_config_path, ratio, rc, mc, irn):
  config_path = build_config(dir, template_config_path, ratio, rc, mc, irn)
  command = f'./../../Release/ssdserving {config_path} > {dir}/{ratio}_{rc}_{mc}_{irn}.log 2>&1'

  print("Running command: {}".format(command))
  
  subprocess.run(command, shell=True)
  print("Finish")

if __name__ == "__main__":
  dir = '../deep_exp_result'

  os.makedirs(dir, exist_ok=True)
  template_config_path = "../config/search_deep.ini"

  # ratios = [0.1, 0.05, 0.025, 0.0167]
  # rcs = [1, 2, 4, 8]
  ratios = [0.1]
  rcs = [1]

  # test 1
  mcs = [64]
  irns = [32, 64, 128, 256, 512, 1024, 2048]

  for ratio in ratios:
    for rc in rcs:
      for mc in mcs:
        for irn in irns:
          test_spann(dir, template_config_path, ratio, rc, mc, irn)

  # test 2
  # mcs = [256, 512, 1024, 2048, 4096]
  # irns = [128]
  # test_spann(dir, template_config_path, ratios, rcs, mcs, irns)

  # mc = 64
  # ratio_rc_irns = [
  #   (0.1, 2, 1300),
  #   (0.1, 6, 300),
  #   (0.1, 8, 220),
  #   (0.05, 1, 2800),
  #   (0.05, 2, 850),
  #   (0.05, 6, 190),
  #   (0.05, 8, 150),
  #   (0.025, 1, 1700),
  #   (0.025, 2, 580),
  #   (0.025, 6, 140),
  #   (0.025, 8, 110),
  #   (0.0167, 1, 1250),
  #   (0.0167, 4, 180),
  #   (0.0167, 6, 140),
  # ]

  # for ratio, rc, irn in ratio_rc_irns:
  #   test_spann(dir, template_config_path, ratio, rc, mc, irn)