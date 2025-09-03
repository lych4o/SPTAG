import sys

def xvecs_to_xbin(num, dim, xvecs_path, xbin_path, data_type_length):
    with open(xvecs_path, 'rb') as fin, open(xbin_path, 'wb') as fout:
        fout.write(num.to_bytes(4, 'little'))
        fout.write(dim.to_bytes(4, 'little'))
        while True:
            dim_bytes = fin.read(4)
            if not dim_bytes:
                break
            dim = int.from_bytes(dim_bytes, byteorder='little', signed=True)

            vec_bytes = fin.read(data_type_length * dim)
            if len(vec_bytes) != data_type_length * dim:
                raise ValueError("文件格式错误或数据不完整")
            fout.write(vec_bytes)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("用法: python xvecs_to_xbin.py <input.xvecs> <output.xbin> <data_type_length> <num> <dim>")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    data_type_length = int(sys.argv[3])
    num = int(sys.argv[4])
    dim = int(sys.argv[5])
    xvecs_to_xbin(num, dim, input_path, output_path, data_type_length)

    print(f"将 {input_path} 转换为 {output_path}，数据类型长度为 {data_type_length} 字节")
