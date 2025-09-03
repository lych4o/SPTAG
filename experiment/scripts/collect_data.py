import os
import re

def collect_log_data(log_dir):
    pattern = re.compile(r"(\d+)_(\d+)\.log$")
    recall_pat = re.compile(r"Recall@100:\s*([0-9.]+)")
    dcc_pat = re.compile(r"Total Distance Calculation Count:\s*([0-9]+)")

    results = []

    for fname in os.listdir(log_dir):
        m = pattern.match(fname)
        if not m:
            continue
        MC, IRN = int(m.group(1)), int(m.group(2))
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
            results.append((MC, IRN, recall, dcc))

    results.sort(key=lambda x: (x[0], x[1]))
    for MC, IRN, recall, dcc in results:
        print(f"MaxCheck: {MC}, IRN: {IRN}, Recall: {recall}, DCC: {dcc}")
    return results

def format_results(results):
    MC64 = [[],[]]
    IRN128 = [[],[]]

    for MC, IRN, recall, dcc in results:
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

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("用法: python collect_data.py <log目录>")
    else:
        results = collect_log_data(sys.argv[1])
        format_results(results)