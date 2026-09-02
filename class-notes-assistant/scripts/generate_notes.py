#!/usr/bin/env python3
"""
课堂笔记生成示例脚本

使用方法：
1. 先清理录音转写文本
2. 人工或使用 LLM 整理笔记结构
3. 使用 HighlightWriter 生成带高亮的 Word 文档

这个脚本展示了完整的笔记生成流程，你可以根据自己的课程内容修改。
"""

import sys
import os

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.highlight_utils import HighlightWriter
from scripts.transcript_cleaner import TranscriptCleaner


def generate_sample_notes(output_path='sample_notes.docx'):
    """
    生成示例笔记

    实际使用时，你需要：
    1. 用 TranscriptCleaner 清理录音文本
    2. 阅读清理后的文本，整理出知识点
    3. 用下面的结构生成笔记
    """
    writer = HighlightWriter()

    # ===== 标题 =====
    title = writer.doc.add_heading('09-02 课堂笔记：RAG检索增强生成', level=0)
    for run in title.runs:
        run.font.name = writer.font_name

    writer.p('📅 2026年9月2日 | AI产品经理课程 · Day6')
    writer.p('🎯 今日核心：RAG检索增强生成原理 + 四种架构对比')

    # ===== 一、核心知识点概览 =====
    writer.h1('📌 今日核心知识点概览')

    # 黄色：特别重点（5-6条）
    writer.yellow('① RAG = 让大模型有一本专业领域的书，需要时去翻书，回答完还能告诉你看了哪本书哪一页')
    writer.yellow('② RAG出现的原因 = 给大模型的信息太多了，需要单独拿出来作为外挂知识库')
    writer.yellow('③ RAG vs 关键词检索的核心区别 = 大模型能把文字变成向量，计算语义相似度')
    writer.yellow('④ 四种RAG架构：Naive → Advanced → Modular → Graph RAG')
    writer.yellow('⑤ 最重要的架构是 Advanced RAG — 学明白了这个，其他的也就懂了')

    writer.p('')  # 空行

    # 普通：次要知识点（6-10条）
    writer.p('⑥ 不用RAG = 完全黑盒，大模型一拍脑门回答')
    writer.p('⑦ 用RAG = 大模型先判断→检索→基于信息源回答')
    writer.p('⑧ Perplexity的核心壁垒 = 信息源质量高')
    writer.p('⑨ 订阅博主功能 = 自动把博主所有笔记拉下来')
    writer.p('⑩ 卡帕西提出大模型VK理念 = 建立个人知识库整体结构')

    # ===== 二、RAG是什么 =====
    writer.h1('🔍 第二章：RAG是什么')

    writer.h2('2.1 RAG的通俗理解')
    writer.yellow('RAG简单理解 = 让大模型有一本某一些专业上的书。比如想做饭，就给一本中餐或西餐的书，让大模型在书里看看别人怎么做的。最后大模型回复完信息，你还知道它是看了哪本书、哪一页给你回答的。')

    writer.h2('2.2 RAG为什么会出现？')
    writer.p('给大模型的信息太多了，需要单独把它拿出来，作为一个外挂的知识库，让大模型在需要的时候去看一看里面有什么用得上的东西，然后再回复最终结果。')
    writer.yellow('核心价值 = 保证信息准确率。大模型不是什么都知道，外挂知识库能让它在需要时查到准确信息。')

    # ===== 三、用RAG和不用RAG的区别 =====
    writer.h1('⚖️ 第三章：用RAG和不用RAG的区别')

    # 标准问答块（紫色要点 → 绿色问题 → 蓝色答案）
    writer.qa_block(
        question='不用RAG时大模型怎么回答？',
        answer='完全黑盒。你不知道它是怎么想的，它就是一拍脑门子回答。要么跟你说它知道，要么给一些正确的废话（因为现在对幻觉限制比较严格，不允许它瞎编乱造，但也给不了什么正确答案）。',
        tips='关键词：黑盒、幻觉、正确的废话'
    )

    writer.qa_block(
        question='用RAG时大模型怎么回答？',
        answer='大模型遇到问题会自己判断：首先这个问题我现有的知识能不能回答？如果不能回答，我要去公开网站上检索一下，看看外部都是怎么说的。再拿着检索到的这几个信息源回答我们的问题。',
        tips='关键词：判断→检索→基于信息源回答'
    )

    # 对比表格
    writer.h2('3.3 对比总结')
    writer.add_table(
        ['维度', '不用RAG', '用RAG'],
        [
            ['回答方式', '黑盒，一拍脑门', '先判断→检索→基于信息源回答'],
            ['准确率', '低，要么废话要么幻觉', '高，基于检索到的真实信息'],
            ['可追溯性', '无，不知道答案哪来的', '有，能告诉你看了哪些信息源'],
            ['适用场景', '闲聊、创意、常识', '专业知识、最新信息、事实查询'],
        ]
    )

    # ===== 四、四种架构对比 =====
    writer.h1('🏗️ 第四章：RAG的四种架构（核心重点）')

    writer.add_table(
        ['架构', '核心特点', '优势', '劣势', '适用场景'],
        [
            ['Naive RAG', '最简单的检索→生成', '成本低、速度快', '准确率低', '简单场景、快速验证'],
            ['Advanced RAG', '查询改写+重排', '准确率高', '速度慢（链路长）', '专业问答、知识库（最重要）'],
            ['Modular RAG', '模块化插件组合', '灵活、可扩展', '开发成本高', '复杂多变的业务场景'],
            ['Graph RAG', '多跳关系寻找', '能处理复杂关联', '技术复杂', '知识图谱、复杂推理'],
        ]
    )

    writer.yellow('所有架构解决的核心问题 = 怎么找、找到多少、回答能不能准。')

    # ===== 五、补充思考（面试问答） =====
    writer.h1('🤔 第五章：补充思考')

    writer.qa_block(
        question='为什么RAG技术2020年就有了，但2023年才火？',
        answer='因为RAG需要配合大模型的语义理解能力才能发挥最大价值。2020年的关键词检索只能匹配关键词，理解不了语义；2023年大模型火了之后，大模型能把文字变成向量、计算语义相似度，RAG才真正变得智能，进入大众视野。技术的成熟需要配套技术的同步发展。',
        tips='答题要点：配套技术同步发展，语义理解是关键'
    )

    writer.qa_block(
        question='Advanced RAG为什么速度慢但还是最重要？',
        answer='因为在专业问答和知识库场景中，准确率比速度更重要。用户问一个专业问题，等20秒得到准确答案，比2秒得到错误答案有价值得多。而且速度可以通过优化（缓存、并行、模型蒸馏）来提升，但准确率的提升需要架构层面的改进。产品经理要根据场景判断：什么场景速度优先，什么场景准确率优先。',
        tips='答题要点：场景决定优先级，准确率在专业场景更重要'
    )

    writer.p('')
    writer.p('— 笔记结束 —')

    # 保存
    writer.save(output_path)
    return output_path


def clean_transcript(input_path, output_path=None):
    """清理录音转写文本"""
    cleaner = TranscriptCleaner()

    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    cleaned = cleaner.clean(text)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f'清理完成，已保存到：{output_path}')

    # 统计说话人
    stats = cleaner.get_speaker_stats(text)
    print('\n说话人统计：')
    for speaker, data in stats.items():
        print(f'  {speaker}: {data["count"]}次发言, {data["chars"]}字')

    return cleaned


if __name__ == '__main__':
    # 生成示例笔记
    print('=== 生成示例笔记 ===')
    generate_sample_notes('sample_notes.docx')

    # 如果有输入文件，也可以清理
    if len(sys.argv) > 1:
        print('\n=== 清理录音文本 ===')
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'cleaned.txt'
        clean_transcript(input_file, output_file)
