import pandas as pd

# 加载 parquet 文件
parquet_file_path = "your_parquet_file_path.parquet"  # parquet 文件路径
df = pd.read_parquet(parquet_file_path)

xlsx_file_path = "output_file.xlsx"  # xlsx 文件路径
df.to_excel(xlsx_file_path, index=False)

print(f"Parquet 文件已成功转换并保存为 {xlsx_file_path}")