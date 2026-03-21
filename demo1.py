import pandas as pd
from collections import defaultdict
import argparse
import os


def group_filenames_from_excel(file_path, column_index=1, sheet_name=None):
    """
    从Excel文件的指定列读取文件名并按相同文件名分组

    Args:
        file_path (str): Excel文件路径
        column_index (int): 列索引（从0开始，默认为1即第二列）
        sheet_name (str): 工作表名称（可选）

    Returns:
        dict: 以文件名为键，行索引列表为值的字典
    """
    # 读取Excel文件
    if sheet_name:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    else:
        df = pd.read_excel(file_path)

    # 获取指定列的数据
    filenames = df.iloc[:, column_index]

    # 创建分组字典
    groups = defaultdict(list)

    # 遍历文件名并分组
    for index, filename in enumerate(filenames):
        # 处理NaN值
        if pd.notna(filename):
            groups[str(filename)].append(index + 1)  # Excel行号从1开始

    return dict(groups)


def save_groups_to_excel(groups, output_path):
    """
    将分组结果保存到Excel文件

    Args:
        groups (dict): 分组字典
        output_path (str): 输出文件路径
    """
    # 创建结果DataFrame
    result_data = []
    for filename, rows in groups.items():
        result_data.append({
            '文件名': filename,
            '出现次数': len(rows),
            '所在行号': ', '.join(map(str, rows))
        })

    # 按出现次数降序排列
    result_df = pd.DataFrame(result_data).sort_values('出现次数', ascending=False)

    # 保存到Excel
    result_df.to_excel(output_path, index=False)


def print_statistics(groups):
    """
    打印分组统计信息

    Args:
        groups (dict): 分组字典
    """
    total_groups = len(groups)
    duplicate_groups = {k: v for k, v in groups.items() if len(v) > 1}
    unique_groups = {k: v for k, v in groups.items() if len(v) == 1}

    print(f"总共找到 {total_groups} 个不同的文件名组")
    print(f"其中重复文件名组: {len(duplicate_groups)} 个")
    print(f"唯一文件名组: {len(unique_groups)} 个")

    # 显示前10个重复最多的文件名
    print("\n重复次数最多的前10个文件名:")
    sorted_duplicates = sorted(duplicate_groups.items(), key=lambda x: len(x[1]), reverse=True)
    for filename, rows in sorted_duplicates[:10]:
        print(f"  {filename}: {len(rows)} 次重复")


def main():
    parser = argparse.ArgumentParser(description="Excel文件名分组工具")
    parser.add_argument("input_file", help="输入的Excel文件路径")
    parser.add_argument("-o", "--output", default="grouped_files.xlsx", help="输出文件路径（默认: grouped_files.xlsx）")
    parser.add_argument("-c", "--column", type=int, default=1, help="要处理的列索引（从0开始，默认: 1）")
    parser.add_argument("-s", "--sheet", help="工作表名称（可选）")

    args = parser.parse_args()

    # 检查输入文件是否存在
    if not os.path.exists(args.input_file):
        print(f"错误: 文件 '{args.input_file}' 不存在")
        return

    try:
        # 读取并分组文件名
        print(f"正在读取Excel文件 '{args.input_file}' 并分组...")
        groups = group_filenames_from_excel(args.input_file, args.column, args.sheet)

        # 显示统计信息
        print_statistics(groups)

        # 保存结果到新Excel文件
        print(f"\n正在保存分组结果到 '{args.output}'...")
        save_groups_to_excel(groups, args.output)
        print("分组结果已保存!")

        # 显示部分重复文件名详情
        duplicates = {k: v for k, v in groups.items() if len(v) > 1}
        if duplicates:
            print("\n重复文件名详情:")
            for filename, rows in list(duplicates.items())[:5]:  # 显示前5个
                print(f"  {filename}: 行号 {rows}")

    except Exception as e:
        print(f"处理过程中发生错误: {e}")



'''
 -- 有大量不同文件名，其中有很多比较相像，按照完全不同的各自分开为一组，相像的分为一组
 -- 在一个数组中，每个数组元素是一个文件名，这些文件名有的只有微小不同，有的完全不一样，把文件名只有微小不同的放到一组，完全不同的设置为另外一组
 -- 在一个数组中，在一个数组中，每个数组元素是一个文件名，这些文件名有的只有微小不同，有的完全不一样，把文件名只有微小不同的放到一组，完全不同的设置为另外一组。
    文件名之间如果有三个单词或者汉字相同，不到三个单词或者汉字的有一个单词或者汉字的相同分为一组
'''


if __name__ == "__main__":
    print("33")

    main()









