#!/bin/bash

# ./../Release/indexbuilder -c config/build_sift.ini -d 128 -v float -f XVEC -i /home/ycli/siftsmall/siftsmall_base.fvecs -o temp_small -a SPANN

# test 1
max_check_values=(64)
internal_result_num_values=(32 64 128 256 512 1024 2048 4096)

for max_check in "${max_check_values[@]}"; do
  for internal_result_num in "${internal_result_num_values[@]}"; do
    python3 search_sift.py $max_check $internal_result_num config/search_sift1m.ini
  done
done

#tese 2
max_check_values=(256 512 1024 2048 4096 8192 16384)
internal_result_num_values=(128)

for max_check in "${max_check_values[@]}"; do
  for internal_result_num in "${internal_result_num_values[@]}"; do
    python3 search_sift.py $max_check $internal_result_num config/search_sift1m.ini
  done
done


# python3 search_sift.py 256 32 config/search_sift1m.ini 
# python3 search_sift.py 256 64 config/search_sift1m.ini 
# python3 search_sift.py 256 128 config/search_sift1m.ini 
# python3 search_sift.py 256 256 config/search_sift1m.ini 
# 
# python3 search_sift.py 512 32 config/search_sift1m.ini 
# python3 search_sift.py 512 64 config/search_sift1m.ini 
# python3 search_sift.py 512 128 config/search_sift1m.ini 
# python3 search_sift.py 512 256 config/search_sift1m.ini 
# python3 search_sift.py 512 512 config/search_sift1m.ini 
# 
# python3 search_sift.py 1024 32 config/search_sift1m.ini 
# python3 search_sift.py 1024 64 config/search_sift1m.ini 
# python3 search_sift.py 1024 128 config/search_sift1m.ini 
# python3 search_sift.py 1024 256 config/search_sift1m.ini 
# python3 search_sift.py 1024 512 config/search_sift1m.ini 
# python3 search_sift.py 1024 1024 config/search_sift1m.ini 
# 
# python3 search_sift.py 2048 32 config/search_sift1m.ini 
# python3 search_sift.py 2048 64 config/search_sift1m.ini 
# python3 search_sift.py 2048 128 config/search_sift1m.ini 
# python3 search_sift.py 2048 256 config/search_sift1m.ini 
# python3 search_sift.py 2048 512 config/search_sift1m.ini 
# python3 search_sift.py 2048 1024 config/search_sift1m.ini 
# python3 search_sift.py 2048 2048 config/search_sift1m.ini 
# 

