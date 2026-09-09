from llama_index.core import SimpleDirectoryReader
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.schema import Document
from typing import List, Generator

# 解析input_dir目录下的所有文件
# 返回一个Document对象列表
def parse_all_formats(input_dir):

    reader = SimpleDirectoryReader(
        input_dir = input_dir
    )

    return reader.load_data()

# 把目录下面所有的问文件清洗一下
def clean_all_formats(input_dir) -> List[Document]:
    import dataClean

    docs = parse_all_formats(input_dir)
    # 清洗之后的对象数组
    cleaned_docs = []

    for i, doc in enumerate(docs):
        cleand_doc = dataClean.clean_doc(doc)
        cleaned_docs.append(cleand_doc)

    return cleaned_docs