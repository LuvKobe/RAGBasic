# 正则表达式库，用于匹配并替换各类文本噪声
import re
# Unicode标准化库，统一全角/半角、特殊字符格式
import unicodedata
# 路径处理工具，安全获取文件后缀、拼接路径
from pathlib import Path

# LlamaIndex 文档核心对象，承载单份文件文本+元数据
from llama_index.core import Document
# 项目全局配置，包含基础根目录路径
from config import base_path
# 自定义工具函数：自动解析目录下所有格式文件，输出Document列表
from util import parse_all_formats


# ------------------------------ 预编译正则：PPT解析产生的结构噪声匹配规则 ------------------------------

# 匹配PPT解析生成的标题行：Title: xxx
_PPTX_TITLE_LINE = re.compile(r"^Title:\s*.+\s*$", re.MULTILINE)
# 匹配PPT内容分割线：连续三个及以上短横线
_PPTX_SEPARATOR = re.compile(r"^-{3,}\s*$", re.MULTILINE)
# 匹配PPT备注前缀：[Speaker Notes]:
_PPTX_SPEAKER_NOTES = re.compile(r"^\[Speaker Notes\]:\s*", re.MULTILINE)


# ------------------------------ 预编译正则：Markdown标记清理规则 ------------------------------
# 匹配加粗一级标题 # **标题**
_MD_HEADING_BOLD = re.compile(r"^#\s*\*\*(.+?)\*\*\s*$", re.MULTILINE)
# 匹配行内加粗标记 **内容**
_MD_BOLD = re.compile(r"\*\*(.+?)\*\*")
# 匹配行首标题符号 #
_LEADING_HASH = re.compile(r"^#\s+", re.MULTILINE)
# 匹配首尾包裹#的文本 # 内容 #
_INLINE_HASH_WRAP = re.compile(r"#\s*(.+?)\s*#")
# 匹配行尾多余#符号
_TRAILING_HASH = re.compile(r"#\s*$")


# ------------------------------ 预编译正则：通用脏字符匹配规则 ------------------------------
# 匹配不可见ASCII控制字符（换行、制表符除外）
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
# 匹配零宽空白、字节序标记等肉眼不可见隐形字符
_ZERO_WIDTH = re.compile(r"[\ufeff\u200b\u200c\u200d\ufeff]")
# 匹配连续3行及以上空行，统一压缩为两段换行
_MULTI_BLANK_LINES = re.compile(r"\n{3,}")


# ------------------------------ 核心方法：文本清洗逻辑 ------------------------------
# 对单端文本执行清洗逻辑
def clean_text(text, source_suffix):
    text = _ZERO_WIDTH.sub("", text)
    text = text.replace("\ufeff", "")
    text = unicodedata.normalize("NFKC", text)
    text = _CONTROL_CHARS.sub("", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    if source_suffix.lower() in {".pptx", "ppt", "pptm"}:
        text = clean_ppt(text)

    lines = [line.strip() for line in text.split("\n")  if line.strip()]
    text = _MULTI_BLANK_LINES.sub("\n\n", "\n".join(lines))
    return text.strip();

# 单独处理ppt文件
def clean_ppt(text):
    text = _PPTX_TITLE_LINE.sub("", text)
    text = _PPTX_SEPARATOR.sub("", text)
    text = _PPTX_SPEAKER_NOTES.sub("", text)
    text = _MD_HEADING_BOLD.sub(r"\1", text)
    text = _MD_BOLD.sub(r"\1", text)

    while True:
        cleand = _INLINE_HASH_WRAP.sub(r"\1", text)
        if cleand == text:
            break;
        text = cleand

    text = _LEADING_HASH.sub("", text)
    text = _TRAILING_HASH.sub("", text)
    text = re.sub(r"\s+#\s+", "", text)
    return text.replace("#", "")

# 构建清洗后新的Document对象
def clean_doc(doc):
    suffix = Path(doc.metadata.get("file_path", "")).suffix
    return Document(text=clean_text(doc.text, suffix), metadata=doc.metadata)

# 构建清洗后的Document对象
def clean_all_formats(input_dir):
    # 原始解析出来的对象
    docs = parse_all_formats(input_dir)
    # 清洗之后的对象数组
    cleaned_docs = []

    for i, doc in enumerate(docs):
        cleand_doc = clean_doc(doc)
        cleaned_docs.append(cleand_doc)
        file_path = cleand_doc.metadata.get("file_path")
        print(f"\n第{i+1} 个对象|文件路径:{file_path}")
        print(cleand_doc.text[:200])

    return cleaned_docs


if __name__ == "__main__":
    clean_all_formats(base_path/"文档")