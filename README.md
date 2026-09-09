# RAGBasic

RAG 初阶实践项目：基于 [LlamaIndex](https://www.llamaindex.ai/) 实现 RAG（检索增强生成）数据预处理链路，涵盖**多格式文档解析 → 文本清洗 → 文本分块**。

本项目是 RAG 学习系列的第一部分，进阶内容见后续的 `RAGAdvance`。

## 功能模块

| 文件 | 说明 |
|------|------|
| `config.py` | 全局配置，定义项目基础路径 |
| `dataParse.py` | 使用 `SimpleDirectoryReader` 解析目录下多种格式文件（PDF / PPTX / CSV / TXT 等） |
| `dataClean.py` | 文本清洗：去除隐形字符、控制字符、PPT 结构噪声、Markdown 标记，Unicode 标准化 |
| `util.py` | 通用工具函数：统一封装解析与清洗流程 |
| `fixedSizeChunk.py` | 分块策略一：按固定字符大小分块（支持重叠 overlap） |
| `sentenceChunk.py` | 分块策略二：按句子分块（支持每块最大句子数） |

## 环境依赖

本项目基于 **Python 3.12 + Miniforge (conda)** 开发。

```bash
# 创建并激活虚拟环境
conda create -n ragbasic python=3.12
conda activate ragbasic

# 安装依赖
pip install llama-index
```

## 使用方法

将待处理文件放入 `文档/` 目录，然后运行对应脚本：

```bash
# 解析文档
python dataParse.py

# 清洗文档
python dataClean.py

# 固定大小分块
python fixedSizeChunk.py

# 按句子分块
python sentenceChunk.py
```

## 项目结构

```
RAGBasic/
├── config.py           # 全局配置
├── dataParse.py        # 文档解析
├── dataClean.py        # 文本清洗
├── util.py             # 工具函数
├── fixedSizeChunk.py   # 固定大小分块
├── sentenceChunk.py    # 按句子分块
└── 文档/               # 待处理的原始文档
```
