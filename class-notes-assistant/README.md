# 课堂笔记整理助手 (Class Notes Assistant)

> 将海量的课堂录音转写文本，整理成结构化、带颜色高亮、重点分明的学习笔记。

## ✨ 特性

- 🎙️ **录音文本清理**：自动去除说话人标签、语气词、课堂闲聊、识别错误
- 📝 **结构化笔记**：自动生成章节、重点概览、对比表格
- 🎨 **四色高亮体系**：黄色重点、绿色问题、蓝色答案、紫色答题要点
- ❓ **问答格式标准化**：面试/课堂问答统一为"答题要点→问题→答案"结构
- 📊 **多说话人统计**：统计各说话人发言次数和字数
- 🔧 **高度可定制**：语气词、颜色、识别错误都可以自定义

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/your-username/class-notes-assistant.git
cd class-notes-assistant
pip install -r requirements.txt
```

### 使用

#### 1. 清理录音文本

```bash
python scripts/transcript_cleaner.py raw_transcript.txt cleaned.txt
```

#### 2. 生成示例笔记

```bash
python scripts/generate_notes.py
```

#### 3. 在代码中使用

```python
from scripts.highlight_utils import HighlightWriter

writer = HighlightWriter()

# 黄色重点
writer.yellow('① RAG = 让大模型有一本专业领域的书')

# 标准问答块
writer.qa_block(
    question='RAG和关键词检索的区别？',
    answer='RAG能把文字变成向量，计算语义相似度...',
    tips='关键词：语义理解、向量计算'
)

writer.save('my_notes.docx')
```

## 🎨 颜色规范

| 颜色 | 用途 | 样式 | 使用频率 |
|------|------|------|---------|
| 🟡 黄色 | 特别重点/核心理念 | 加粗 | 每篇5-6条 |
| 🟢 绿色 | 重点问题 | 加粗 | 极少用 |
| 🔵 蓝色 | 问题的回答 | 常规 | 配合绿色问题 |
| 🟣 紫色 | 答题要点/tips | 加粗 | 面试问答使用 |

**高亮原则：克制，重点才标，不泛滥。**

## 📋 标准问答结构

```
🟣 💡 答题要点：（回答侧重点和小技巧）
🟢 问题：（问题文本）
🔵 （完整标准答案，自然流畅，不用引号包裹）
```

## 📁 项目结构

```
class-notes-assistant/
├── SKILL.md                    # Skill 详细文档
├── README.md                   # 本文件
├── requirements.txt            # Python 依赖
├── scripts/
│   ├── highlight_utils.py      # 高亮颜色工具（核心）
│   ├── transcript_cleaner.py   # 录音文本清理工具
│   └── generate_notes.py       # 完整示例脚本
├── templates/
│   └── notes_template.py       # 笔记模板
└── examples/
    └── sample_input.txt        # 示例输入
```

## 🛠️ 自定义

### 修改语气词

编辑 `scripts/transcript_cleaner.py` 中的 `FILLER_WORDS`。

### 修改识别错误纠正

编辑 `scripts/transcript_cleaner.py` 中的 `corrections`。

### 修改颜色

编辑 `scripts/highlight_utils.py` 中的颜色常量。

## 📖 详细文档

见 [SKILL.md](./SKILL.md)

## 📄 许可证

MIT License
