import pandas as pd

def compare_excel_columns(file1_path, file2_path, column_name, output_path):
    """
    比对两个Excel文件中指定列的内容，找出不同的内容并输出到txt文件
    
    参数:
    file1_path: 第一个Excel文件路径
    file2_path: 第二个Excel文件路径
    column_name: 要比对的列名
    output_path: 输出结果的txt文件路径
    """

    df1 = pd.read_excel(file1_path)
    df2 = pd.read_excel(file2_path)
    
    values1 = set(df1[column_name].dropna().astype(str))
    values2 = set(df2[column_name].dropna().astype(str))
    
    only_in_file1 = values1 - values2
    only_in_file2 = values2 - values1
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("比对结果:\n\n")
        
        f.write(f"仅在文件1 ({file1_path}) 中出现的内容:\n")
        for item in sorted(only_in_file1):
            f.write(f"- {item}\n")
        
        f.write(f"\n仅在文件2 ({file2_path}) 中出现的内容:\n")
        for item in sorted(only_in_file2):
            f.write(f"- {item}\n")
        
        f.write(f"\n统计信息:\n")
        f.write(f"文件1中独有内容数量: {len(only_in_file1)}\n")
        f.write(f"文件2中独有内容数量: {len(only_in_file2)}\n")
        f.write(f"文件1总行数: {len(df1)}\n")
        f.write(f"文件2总行数: {len(df2)}\n")

if __name__ == "__main__":
    file1_path = r"C:\Users\42419\Desktop\Text-to-sql\合并结果\DeepSeek-R1-Distill-Qwen-32B-Text-to-sql.xlsx"
    file2_path = r"C:\Users\42419\Desktop\Text-to-sql\合并结果\Qwen-32B-Text-to-sql.xlsx"
    column_name = "问题"
    output_path = r"C:\Users\42419\Desktop\Text-to-sql\合并结果\comparison_result.txt"
    
    compare_excel_columns(file1_path, file2_path, column_name, output_path)