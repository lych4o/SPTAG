import sys
import os
import shutil
import subprocess



def copy_data(ratio, rc):
  if rc == 1:
    return # No need to copy if replica count is 1
  src = f'index/sift100m_{ratio}_1'
  dst = f'index/sift100m_{ratio}_{rc}'

  # 删除目标目录并重新复制
  subprocess.run(f'rm -rf {dst}', shell=True)
  subprocess.run(f'cp -r {src} {dst}', shell=True)
  print(f"Copied from {src} to {dst}")

def build_config(dir, ratio, rc):
  print("dir: {}".format(dir))
  new_config_name = f'{dir}/config_{ratio}_{rc}.ini'
  print("new_config_name: {}".format(new_config_name))

  config_path = f'config/build_sift100m_{ratio}.ini'
  with open(config_path, 'r') as template_file:
    content = template_file.read()
  
  lines = content.splitlines(keepends=True)
  is_execute_count = 2

  for i in range(len(lines)-1, -1, -1):
    if lines[i].startswith('ReplicaCount'):
      lines[i] = f'ReplicaCount={rc}\n'
    elif lines[i].startswith('isExecute'):
      if is_execute_count > 0:
        is_execute_count -= 1
      else:
        lines[i] = 'isExecute=false\n'
    elif lines[i].startswith('IndexDirectory'):
      lines[i] = f'IndexDirectory=index/sift100m_{ratio}_{rc}\n'
    
  with open(new_config_name, 'w') as new_config_file:
    new_config_file.writelines(lines)
  
  return new_config_name

def build_index(dir, ratio, rc):
  config_path = build_config(dir, ratio, rc)
  copy_data(ratio, rc)
  command = f'./../Release/ssdserving {config_path} > {dir}/log_{ratio}_{rc}.c 2>&1'

  print("Running command: {}".format(command))
  
  subprocess.run(command, shell=True)
  print("Finish")

if __name__ == "__main__":
  """
  if len(sys.argv) != 3:
    print("Usage: python build_sift100m.py <ratio> <rc>")
    sys.exit(1)

  ratio = sys.argv[1]
  rc = int(sys.argv[2])
  """

  # dir = 'sift1m_exp_result_6_17'
  # dir = 'sift1m_exp_result'
  dir = 'sift100m_build_7_29'

  os.makedirs(dir, exist_ok=True)

  ratios = ['0.1', '0.05', '0.025', '0.0167']
  replicas = [1, 2, 4, 6, 8]

  for ratio in ratios:
    for replica in replicas:
      print(f"Building index for ratio {ratio} and replica count {replica}")
      build_index(dir, ratio, replica) 

  # to_build = [(0.025, 6), (0.025, 8)]
  # for ratio, replicas in to_build:
  #   print(f"Building index for ratio {ratio} and replicas {replicas}")
  #   build_index(dir, ratio, replicas)

