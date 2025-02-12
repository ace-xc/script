import json
from datetime import datetime

def compare_sql_fields(input_file, output_file=None):
    """
    比较JSON文件中accuracy为1的记录中SQL和generated字段是否一致
    
    Args:
        input_file (str): 输入JSON文件路径
        output_file (str): 输出文件路径，如果为None则自动生成
    """
    # 如果没有指定输出文件，创建一个带时间戳的文件名
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'sql_differences_{timestamp}.txt'
    
    try:
        # 读取JSON文件
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 确保数据是列表格式
        if not isinstance(data, list):
            data = [data]
        
        # 用于存储不一致的记录
        differences = []
        
        # 遍历所有记录
        for item in data:
            # 检查accuracy是否为1且SQL和generated字段不一致
            if (item.get('accuracy') == 1 and 
                'SQL' in item and 
                'generated' in item and 
                item['SQL'].strip() != item['generated'].strip()):
                
                differences.append({
                    'question_id': item.get('question_id', 'N/A'),
                    'question': item.get('question', 'N/A'),
                    'SQL': item.get('SQL', ''),
                    'generated': item.get('generated', '')
                })
        
        # 将结果写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"发现 {len(differences)} 条不一致记录\n")
            f.write("=" * 80 + "\n\n")
            
            for i, diff in enumerate(differences, 1):
                f.write(f"记录 {i}:\n")
                f.write(f"问题ID: {diff['question_id']}\n")
                f.write(f"问题: {diff['question']}\n")
                f.write("原始SQL:\n{}\n".format(diff['SQL']))
                f.write("生成SQL:\n{}\n".format(diff['generated']))
                f.write("-" * 80 + "\n\n")
        
        return len(differences), output_file
    
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
        return -1, None

# 使用示例
if __name__ == "__main__":
    input_file = r"C:\Users\42419\Desktop\Text-to-sql\合并结果\DeepSeek-R1-Distill-Qwen-32B-predict.json"  # 替换为你的输入文件路径
    count, output_file = compare_sql_fields(input_file)
    
    if count >= 0:
        print(f"处理完成！发现 {count} 条不一致记录")
        print(f"结果已保存到: {output_file}")
    else:
        print("处理失败！")