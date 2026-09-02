"""
录音转写文本清理工具
用于处理语音转文字的原始文本，去除噪音，提取有效内容

常见噪音类型：
- 说话人标签（说话人1 00:11:13）
- 语气词（嗯、啊、那个、就是）
- 重复内容
- 课堂闲聊（和课程无关的对话）
- 识别错误（同音字、断句错误）
"""

import re
from typing import List, Dict, Tuple


class TranscriptCleaner:
    """录音转写文本清理器"""

    # 常见语气词（可根据需要扩展）
    FILLER_WORDS = [
        '嗯', '啊', '呃', '哦', '唉', '哎',
        '那个', '这个', '就是', '然后', '所以说',
        '怎么说呢', '你知道吧', '对吧', '是吧',
        '怎么讲', '怎么说', '也就是说',
    ]

    # 课堂闲聊模式（和课程内容无关的对话）
    CHAT_PATTERNS = [
        r'声太大了',
        r'压到我心脏了',
        r'吃饭',
        r'下课',
        r'休息一下',
        r'温度.*电',
        r'QQ号',
        r'小说',
    ]

    def __init__(self, remove_fillers=True, remove_chat=True):
        self.remove_fillers = remove_fillers
        self.remove_chat = remove_chat

    def clean(self, text: str) -> str:
        """
        完整清理流程

        Args:
            text: 原始转写文本

        Returns:
            清理后的文本
        """
        # 1. 分离说话人
        segments = self._split_speakers(text)

        # 2. 清理每个片段
        cleaned_segments = []
        for speaker, time_str, content in segments:
            # 跳过闲聊
            if self.remove_chat and self._is_chat(content):
                continue

            # 清理内容
            content = self._clean_content(content)

            # 跳过空内容
            if content.strip():
                cleaned_segments.append((speaker, time_str, content))

        # 3. 合并输出
        result = []
        for speaker, time_str, content in cleaned_segments:
            result.append(f'[{speaker} {time_str}] {content}')

        return '\n\n'.join(result)

    def _split_speakers(self, text: str) -> List[Tuple[str, str, str]]:
        """
        分离说话人标签

        格式：说话人1 00:11:13\n内容
        """
        # 匹配说话人标签
        pattern = r'(说话人\d+)\s+(\d{2}:\d{2}:\d{2})\s*\n(.*?)(?=\n说话人\d+\s+\d{2}:\d{2}:\d{2}|$)'
        matches = re.findall(pattern, text, re.DOTALL)

        if not matches:
            # 如果没有说话人标签，返回整个文本作为一个片段
            return [('未知', '00:00:00', text)]

        return [(speaker, time_str, content.strip()) for speaker, time_str, content in matches]

    def _clean_content(self, text: str) -> str:
        """清理单段内容"""
        # 去除多余空白
        text = re.sub(r'\s+', ' ', text).strip()

        # 去除语气词
        if self.remove_fillers:
            text = self._remove_fillers(text)

        # 修复常见识别错误
        text = self._fix_recognition_errors(text)

        return text

    def _remove_fillers(self, text: str) -> str:
        """去除语气词"""
        for word in self.FILLER_WORDS:
            # 去除句首的语气词
            text = re.sub(rf'^{word}[，,。.\s]*', '', text)
            # 去除句中的语气词（保留标点）
            text = re.sub(rf'[，,]{word}[，,]', '，', text)
            text = re.sub(rf'\s{word}\s', ' ', text)

        # 去除连续的标点
        text = re.sub(r'[，,]{2,}', '，', text)
        text = re.sub(r'[。.]{2,}', '。', text)

        return text.strip()

    def _fix_recognition_errors(self, text: str) -> str:
        """修复常见识别错误（可根据课程领域扩展）"""
        # AI 领域常见识别错误
        corrections = {
            '大模形': '大模型',
            '提示词': '提示词',
            '只能体': '智能体',
            '检索曾强': '检索增强',
            '向量数据哭': '向量数据库',
            '瑞个': 'RAG',
            '瑞一个': 'RAG',
            '水球泡': '水球泡',  # 人名保留
        }

        for wrong, right in corrections.items():
            text = text.replace(wrong, right)

        return text

    def _is_chat(self, text: str) -> bool:
        """判断是否是课堂闲聊"""
        for pattern in self.CHAT_PATTERNS:
            if re.search(pattern, text):
                return True
        return False

    def extract_key_points(self, text: str) -> List[str]:
        """
        从清理后的文本中提取关键点（简单版）

        基于标点和关键词提取，更复杂的提取建议使用 LLM
        """
        # 按句号分割
        sentences = re.split(r'[。！？]', text)

        key_points = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue

            # 包含关键词的句子可能是重点
            keywords = ['核心', '关键', '重要', '本质', '区别', '优势', '劣势',
                       '解决', '定义', '原理', '流程', '方法', '注意']
            if any(kw in sentence for kw in keywords):
                key_points.append(sentence)

        return key_points

    def get_speaker_stats(self, text: str) -> Dict[str, int]:
        """统计各说话人的发言次数和字数"""
        segments = self._split_speakers(text)
        stats = {}

        for speaker, _, content in segments:
            if speaker not in stats:
                stats[speaker] = {'count': 0, 'chars': 0}
            stats[speaker]['count'] += 1
            stats[speaker]['chars'] += len(content)

        return stats


def clean_file(input_path: str, output_path: str = None) -> str:
    """
    清理文件的便捷函数

    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径（可选）

    Returns:
        清理后的文本
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    cleaner = TranscriptCleaner()
    cleaned = cleaner.clean(text)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f'清理完成，已保存到：{output_path}')

    return cleaned


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        clean_file(input_file, output_file)
    else:
        print('用法：python transcript_cleaner.py <输入文件> [输出文件]')
