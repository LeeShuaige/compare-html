import re
import html
import string
from typing import List, Dict, Any
import json


class LoRADatasetCleaner:
    def __init__(self):
        # 常见的停用词列表（可根据需要扩展）
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }

    def remove_html_tags(self, text: str) -> str:
        """移除HTML标签"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def remove_special_characters(self, text: str) -> str:
        """移除特殊字符，保留字母、数字、基本标点和空格"""
        # 保留字母、数字、空格和基本标点符号
        allowed_chars = string.ascii_letters + string.digits + string.punctuation + ' '
        return ''.join(char for char in text if char in allowed_chars)

    def normalize_whitespace(self, text: str) -> str:
        """标准化空格，将多个空格替换为单个空格"""
        return re.sub(r'\s+', ' ', text).strip()

    def remove_extra_punctuation(self, text: str) -> str:
        """移除多余的标点符号"""
        # 将连续的标点符号替换为单个
        text = re.sub(r'([^\w\s])\1+', r'\1', text)
        return text

    def decode_html_entities(self, text: str) -> str:
        """解码HTML实体"""
        return html.unescape(text)

    def remove_stopwords(self, text: str) -> str:
        """移除停用词（可选）"""
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in self.stop_words]
        return ' '.join(filtered_words)

    def standardize_encoding(self, text: str) -> str:
        """标准化编码格式"""
        # 确保文本是UTF-8编码
        if isinstance(text, bytes):
            text = text.decode('utf-8', errors='ignore')
        else:
            text = text.encode('utf-8', errors='ignore').decode('utf-8')
        return text

    def remove_repeated_phrases(self, text: str, min_length=5) -> str:
        """移除重复的短语"""
        # 查找并移除重复的子字符串
        for i in range(min_length, len(text) // 2):
            pattern = re.escape(text[:i])
            if len(re.findall(pattern, text)) > 1:
                text = re.sub(pattern + '+', pattern, text)
        return text

    def clean_text(self, text: str, remove_stopwords=False) -> str:
        """综合文本清洗"""
        if not text or not isinstance(text, str):
            return ""

        # 1. 标准化编码
        text = self.standardize_encoding(text)

        # 2. 解码HTML实体
        text = self.decode_html_entities(text)

        # 3. 移除HTML标签
        text = self.remove_html_tags(text)

        # 4. 移除特殊字符
        text = self.remove_special_characters(text)

        # 5. 移除重复短语
        text = self.remove_repeated_phrases(text)

        # 6. 标准化空格
        text = self.normalize_whitespace(text)

        # 7. 移除多余标点
        text = self.remove_extra_punctuation(text)

        # 8. 移除停用词（可选）
        if remove_stopwords:
            text = self.remove_stopwords(text)

        return text.strip()

    def clean_dataset(self, dataset: List[Dict[str, Any]],
                      remove_stopwords=False) -> List[Dict[str, Any]]:
        """清洗整个数据集"""
        cleaned_dataset = []

        for item in dataset:
            cleaned_item = {}
            for key, value in item.items():
                if isinstance(value, str):
                    cleaned_item[key] = self.clean_text(value, remove_stopwords)
                else:
                    cleaned_item[key] = value
            # 只添加非空的项
            if any(cleaned_item.get(k) for k in ['instruction', 'input', 'output'] if k in cleaned_item):
                cleaned_dataset.append(cleaned_item)

        return cleaned_dataset


def main():
    # 示例数据集
    sample_dataset = [
        {
            "instruction": "  Translate the following English text to French:  ",
            "input": "<p>Hello World!</p>   &nbsp;  ",
            "output": "Bonjour le monde!!!???"
        },
        {
            "instruction": "Summarize the article@@@@@",
            "input": "The quick brown fox jumps over the lazy dog...                ...The quick brown fox jumps over the lazy dog...",
            "output": "A fox jumps over a dog??????"
        }
    ]

    # 创建清洗器实例
    cleaner = LoRADatasetCleaner()

    # 清洗数据集
    print("原始数据集:")
    for i, item in enumerate(sample_dataset):
        print(f"样本 {i + 1}: {item}")

    cleaned_dataset = cleaner.clean_dataset(sample_dataset)

    print("\n清洗后的数据集:")
    for i, item in enumerate(cleaned_dataset):
        print(f"样本 {i + 1}: {item}")

    # 保存清洗后的数据集
    with open('cleaned_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_dataset, f, ensure_ascii=False, indent=2)

    print("\n清洗后的数据集已保存到 cleaned_dataset.json")


'''
噪声去除是常见的基础清理步骤，旨在剔除文本中表层的、通用的噪声。
具体包括：清除无意义的停用词、标点符号、特殊字符、冗余空格以及重复内容，
同时对编码格式进行标准化处理，消除残留的HTML标记或其他非文本元素。
'''
if __name__ == "__main__":
    main()





