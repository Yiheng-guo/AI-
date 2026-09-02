---
name: class-notes-assistant
version: 1.0.0
description: "课堂笔记整理助手：将录音转写文本整理成带颜色高亮的结构化笔记，支持问答格式标准化、噪音去除、重点标记。适用于学生、培训参与者、知识工作者整理课堂/会议/讲座录音。"
---

# 课堂笔记整理助手 (Class Notes Assistant)

将海量的课堂录音转写文本，整理成结构化、带颜色高亮、重点分明的学习笔记。

## 核心能力

1. **录音文本清理**：去除说话人标签、语气词、课堂闲聊、识别错误
2. **结构化笔记生成**：自动生成章节、重点概览、对比表格
3. **四色高亮体系**：黄色重点、绿色问题、蓝色答案、紫色答题要点
4. **问答格式标准化**：面试/课堂问答统一为"答题要点→问题→答案"结构
5. **多说话人统计**：统计各说话人发言次数和字数

## 颜色规范（核心）

| 颜色 | 用途 | 样式 | 使用频率 |
|------|------|------|---------|
| 🟡 黄色 | 特别重点/核心理念/面试话术 | 加粗 | 每篇5-6条，只标真正核心的 |
| 🟢 绿色 | 重点问题 | 加粗 | 极少用，只标真正关键的问题 |
| 🔵 蓝色 | 重点问题的回答 | 常规 | 配合绿色问题使用 |
| 🟣 紫色 | 面试答题要点/tips | 加粗 | 面试问答章节使用 |

**高亮原则：克制，重点才标，不泛滥。**

## 标准问答结构

面试/课堂问答统一使用以下结构：

```
🟣 💡 答题要点：（简短说明回答侧重点和小技巧）
🟢 面试官问：（问题文本）
🔵 （完整标准答案，自然流畅的段落，不用引号包裹）
```

**为什么这样设计？**
- 紫色要点：快速抓住回答侧重点，复习时一眼看到核心
- 绿色问题：明确问题边界
- 蓝色答案：完整自然的回答，不像"念稿子"

## 快速开始

### 安装依赖

```bash
pip install python-docx
```

### 1. 清理录音文本

```python
from scripts.transcript_cleaner import TranscriptCleaner

cleaner = TranscriptCleaner()
with open('raw_transcript.txt', 'r', encoding='utf-8') as f:
    text = f.read()

cleaned = cleaner.clean(text)
print(cleaned)
```

命令行使用：
```bash
python scripts/transcript_cleaner.py raw_transcript.txt cleaned.txt
```

### 2. 生成带高亮的笔记

```python
from scripts.highlight_utils import HighlightWriter

writer = HighlightWriter()

# 标题
writer.doc.add_heading('09-02 课堂笔记：RAG检索增强生成', level=0)

# 黄色重点
writer.yellow('① RAG = 让大模型有一本专业领域的书')

# 标准问答块
writer.qa_block(
    question='RAG和关键词检索的区别？',
    answer='RAG能把文字变成向量，计算语义相似度...',
    tips='关键词：语义理解、向量计算'
)

# 表格
writer.add_table(
    ['架构', '优势', '劣势'],
    [['Naive', '快', '不准'], ['Advanced', '准', '慢']]
)

writer.save('notes.docx')
```

### 3. 运行完整示例

```bash
python scripts/generate_notes.py
```

## 笔记结构模板

推荐的课堂笔记结构：

```
1. 📌 今日核心知识点概览
   - 黄色：5-6条特别重点
   - 普通：4-5条次要知识点

2. 🔍 第二章：[主题1]
   - 概念解释（黄色高亮核心定义）
   - 原理说明
   - 示例

3. ⚖️ 第三章：[对比主题]
   - 标准问答块（紫色要点→绿色问题→蓝色答案）
   - 对比表格

4. 🏗️ 第四章：[核心重点]
   - 详细说明
   - 表格总结
   - 黄色高亮核心结论

5. 💡 第五章：产品思维/延伸思考
   - 从课程内容提炼的思维方法

6. 📝 第六章：课后任务
   - 作业和练习

7. 🤔 第七章：补充思考（面试问答）
   - 标准问答块格式
   - 老师提出但没回答的问题，补充答案
```

## 文件结构

```
class-notes-assistant/
├── SKILL.md                    # 本文件
├── README.md                   # GitHub 项目说明
├── requirements.txt            # Python 依赖
├── scripts/
│   ├── highlight_utils.py      # 高亮颜色工具（核心）
│   ├── transcript_cleaner.py   # 录音文本清理工具
│   └── generate_notes.py       # 完整示例脚本
├── templates/
│   └── notes_template.py       # 笔记模板（可扩展）
└── examples/
    └── sample_input.txt        # 示例输入
```

## 自定义配置

### 修改语气词列表

编辑 `scripts/transcript_cleaner.py` 中的 `FILLER_WORDS`：

```python
FILLER_WORDS = [
    '嗯', '啊', '呃',  # 你的语气词
]
```

### 修改识别错误纠正

编辑 `scripts/transcript_cleaner.py` 中的 `corrections`：

```python
corrections = {
    '错误词': '正确词',
}
```

### 修改颜色

编辑 `scripts/highlight_utils.py` 中的颜色常量：

```python
YELLOW = 7   # 改成你想要的颜色编号
GREEN = 4
BLUE = 2
PURPLE = 12
```

## 使用技巧

1. **先清理再整理**：先用 TranscriptCleaner 清理录音文本，再人工或用 LLM 整理知识点
2. **高亮要克制**：黄色重点每篇不超过6条，绿色问题只标真正关键的
3. **问答要自然**：答案用自然流畅的段落，不要用引号包裹，不要"念稿子"
4. **对比用表格**：凡是对比类内容（A vs B、四种架构对比）都用表格呈现
5. **老师没回答的问题要补充**：课堂上老师提出但没给答案的问题，在补充思考章节给出完整回答

## 适用场景

- 🎓 学生课堂笔记整理
- 💼 培训/讲座录音整理
- 📚 在线课程笔记整理
- 🎤 会议纪要整理
- 💼 面试准备问答整理

## 许可证

MIT License
