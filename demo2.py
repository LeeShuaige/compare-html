import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import re


def preprocess_filename(filename):
    """预处理文件名：去除扩展名、转换为小写、提取关键词"""
    # 去除文件扩展名
    name_without_ext = '.'.join(filename.split('.')[:-1]) if '.' in filename else filename
    # 转换为小写
    name_lower = name_lower = name_without_ext.lower()
    # 提取关键词（字母和数字）
    keywords = re.findall(r'[a-zA-Z0-9]+', name_lower)
    return ' '.join(keywords)


def calculate_similarity_matrix(filenames):
    """计算文件名之间的相似度矩阵"""
    # 预处理文件名
    processed_names = [preprocess_filename(name) for name in filenames]

    # 使用TF-IDF向量化
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_names)

    # 计算余弦相似度矩阵
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix


def group_filenames_by_similarity(filenames, threshold=0.5):
    """
    根据相似度阈值对文件名进行分组

    Args:
        filenames: 文件名列表
        threshold: 相似度阈值 (0-1)

    Returns:
        list: 分组结果，每个元素是一个包含相似文件名的列表
    """
    if not filenames:
        return []

    # 计算相似度矩阵
    similarity_matrix = calculate_similarity_matrix(filenames)

    # 初始化分组
    groups = []
    used = set()

    # 遍历所有文件名
    for i in range(len(filenames)):
        if i in used:
            continue

        # 创建新组，包含当前文件名
        current_group = [filenames[i]]
        used.add(i)

        # 查找相似的文件名
        for j in range(i + 1, len(filenames)):
            if j in used:
                continue

            # 如果相似度超过阈值，加入当前组
            if similarity_matrix[i][j] >= threshold:
                current_group.append(filenames[j])
                used.add(j)

        # 如果组中有多于一个文件名，或者允许单文件组，则添加到结果中
        if len(current_group) > 1 or True:  # 允许单文件组
            groups.append(current_group)

    return groups


def display_groups(groups, threshold):
    """显示分组结果"""
    print(f"文件名相似度分组结果 (阈值: {threshold})")
    print("=" * 50)

    for i, group in enumerate(groups, 1):
        print(f"\n组 {i} ({len(group)} 个文件):")
        for filename in group:
            print(f"  - {filename}")

    print(f"\n总共 {len(groups)} 组")


def main():
    # 示例数据：包含各种相似和不相似的文件名
    sample_filenames = [
        "report_2023_final.pdf",
        "report_2023_draft.pdf",
        "report_2023_review.docx",
        "financial_report_q1.xlsx",
        "financial_report_q2.xlsx",
        "financial_report_q3.xlsx",
        "user_manual_v1.txt",
        "user_manual_v2.txt",
        "installation_guide.pdf",
        "readme.md",
        "license.txt",
        "config_backup.json",
        "config_production.json",
        "data_export_2023.csv",
        "data_import_2023.csv",
        "image_photo_001.jpg",
        "image_photo_002.jpg",
        "image_photo_003.jpg",
        "random_file.xyz",
        "unrelated_document.txt"
    ]

    print("原始文件名列表:")
    for i, filename in enumerate(sample_filenames, 1):
        print(f"{i:2d}. {filename}")

    # 测试不同阈值
    thresholds = [0.3, 0.5, 0.7]

    for threshold in thresholds:
        print(f"\n{'=' * 60}")
        groups = group_filenames_by_similarity(sample_filenames, threshold)
        display_groups(groups, threshold)

        # 统计信息
        total_files = len(sample_filenames)
        grouped_files = sum(len(group) for group in groups)
        single_files = total_files - grouped_files + len([g for g in groups if len(g) == 1])

        print(f"\n统计信息:")
        print(f"  总文件数: {total_files}")
        print(f"  分组数: {len(groups)}")
        print(f"  平均每组文件数: {grouped_files / len(groups):.1f}" if groups else "  平均每组文件数: 0")



'''
1. 在一个数组中，每个元素是一个文件名，这些文件名之间有的具有高的相似度，有的具有低的相似度，有的完全没有关系。
   设置一个阈值调节相似度，文件名之间相似度大于这个值的时候放到一起展示。彼此不相关的文件名，分别独立展示。

'''

if __name__ == "__main__":
    main()
