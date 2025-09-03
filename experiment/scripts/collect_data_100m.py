import os
import re

def collect_log_data(log_dir):
    pattern = re.compile(r"([0-9.]+)_(\d+)_(\d+)_(\d+)\.log$")
    recall_pat = re.compile(r"Recall@100:\s*([0-9.]+)")
    dcc_pat = re.compile(r"Total Distance Calculation Count:\s*([0-9]+)")

    results = []

    for fname in os.listdir(log_dir):
        m = pattern.match(fname)
        if not m:
            continue
        RATIO, RC, MC, IRN = float(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
        recall, dcc = None, None
        with open(os.path.join(log_dir, fname), "r") as f:
            for line in f:
                if recall is None:
                    m1 = recall_pat.search(line)
                    if m1:
                        recall = float(m1.group(1))
                if dcc is None:
                    m2 = dcc_pat.search(line)
                    if m2:
                        dcc = float(m2.group(1)) / 10000
                if recall is not None and dcc is not None:
                    break
        if recall is not None and dcc is not None:
            results.append((RATIO, RC, MC, IRN, recall, dcc))

    results.sort(key=lambda x: (x[0], x[1]))
    for RATIO, RC, MC, IRN, recall, dcc in results:
        print(f"RATIO: {RATIO}, RC: {RC}, MaxCheck: {MC}, IRN: {IRN}, Recall: {recall}, DCC: {dcc}")
    return results

def format_results1(results):
    MC64 = [[],[]]
    IRN128 = [[],[]]

    for RATIO, RC, MC, IRN, recall, dcc in results:
        bs = int(1 / RATIO)

        if bs == 10 and RC == 1:
            if MC == 64:
                MC64[0].append(recall)
                MC64[1].append(dcc)
            elif IRN == 128:
                IRN128[0].append(recall)
                IRN128[1].append(dcc)

    print(f"SPANN_MC64[0]={MC64[0]}")
    print(f"SPANN_MC64[1]={MC64[1]}")
    print(f"SPANN_IRN128[0]={IRN128[0]}")
    print(f"SPANN_IRN128[1]={IRN128[1]}")

def format_results2(results):
    result_dict = {}
    for RATIO, RC, MC, IRN, recall, dcc in results:
        bs = int(1 / RATIO)
        key = f"{bs}_{RC}"
        # if MC != 256:
        #     continue
        if bs not in result_dict:
            result_dict[bs] = {}
        if RC not in result_dict[bs]:
            result_dict[bs][RC] = [[], []]
        result_dict[bs][RC][0].append(recall)
        result_dict[bs][RC][1].append(dcc)
    
    for bs, rc_dict in result_dict.items():
        for rc, (recalls, dccs) in rc_dict.items():
            sort_arr = []
            for i in range(len(recalls)):
                sort_arr.append((recalls[i], dccs[i]))
            sort_arr.sort(key=lambda x: x[1])
            # print(f"SPANN[{bs}][{rc}][0]={[x[0] for x in sort_arr]}")
            # print(f"SPANN[{bs}][{rc}][1]={[x[1] for x in sort_arr]}")

def format_recall95(results):
    result_dict = {}
    for RATIO, RC, MC, IRN, recall, dcc in results:
        bs = int(1 / RATIO + 0.5)
        if RC not in result_dict:
            result_dict[RC] = {}
        if bs not in result_dict[RC]:
            result_dict[RC][bs] = (1, -1) # (cur_diff, cur_dcc)
        diff = abs(recall - 0.95)
        if diff < result_dict[RC][bs][0]:
            result_dict[RC][bs] = (diff, dcc)
    
    for rc, bs_dict in result_dict.items():
        print_list = []
        for bs, value in bs_dict.items():
            diff, dcc = value
            print_list.append((bs, value[1]))
        print_list.sort(key=lambda x: x[0])
        # print(f"Recall95_rc[{bs}]={[x[0] for x in print_list]}")
        # print(f"Recall95_dcc[{bs}]={[x[1] for x in print_list]}")
    
        dcc_list = [8184] + [x[1] for x in print_list]
        ratio_list = [x / 8184 for x in dcc_list]
        print(f"Recall95_dcc[{rc}]={dcc_list}")
        print(f"Recall95_ratio[{rc}]={ratio_list}")

    


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("用法: python collect_data.py <log目录>")
        exit(-1)

    
    results = collect_log_data(sys.argv[1])
    #format_results2(results)
    format_recall95(results)