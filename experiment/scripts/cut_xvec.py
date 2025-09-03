import sys

def crop_vec(input_file: str, output_file: str, datatype_length: int, crop_length: int):
    """
    直接通过字节流裁剪 .fvecs 文件的第一个向量（不依赖 struct）
    :param input_file: 输入文件路径（.fvecs）
    :param output_file: 输出文件路径（.fvecs）
    """
    with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
        # 读取向量维度（4字节的小端int）
        for _i in range(crop_length):
            dim_bytes = fin.read(4)
            if not dim_bytes:
                print("警告：输入文件为空")
                return
            
            # 计算向量数据长度（dim × 4字节的float）
            dim = int.from_bytes(dim_bytes, byteorder='little')
            vec_data = fin.read(datatype_length * dim)
            
            if len(vec_data) != datatype_length * dim:
                raise ValueError("文件损坏：向量数据不完整")
            
            # 直接写入维度 + 数据（无需解析内容）
            fout.write(dim_bytes)
            fout.write(vec_data)

    print(f"成功裁剪：{input_file} -> {output_file}")

# 使用示例
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(f"用法: python {sys.argv[0]} <input_file> <output_file> <datatype_length> <crop_length>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    datatype_length = int(sys.argv[3])
    crop_length = int(sys.argv[4])
    crop_vec(input_file, output_file, datatype_length, crop_length)