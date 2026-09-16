from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import config
from typing import List
from llama_index.core.schema import Document
import util
from llama_index.core.node_parser import SemanticSplitterNodeParser #语义分块器

# 通过嵌入模型实现语义分块
def semantic_chunk_documents(
        input_str :str,
) -> List[Document]:
    # 1. 获取清洗之后的目录下所有的文档
    documents = util.clean_all_formats(input_str)

    # 2. 加载嵌入模型
    embed_model = HuggingFaceEmbedding(model_name=config.model_path)

    # 3. 语义分块器
    splitter = SemanticSplitterNodeParser(
        embed_model=embed_model
    )

    # 4. 执行语义分块操作
    chunks = []
    for d in documents:
        text = d.text
        if not text:
            continue

        path = d.metadata.get("file_path")
        # 对单篇的文档执行语义切分
        nodes = splitter.get_nodes_from_documents(
            [
                Document(text=text, metadata=d.metadata)
            ]
        )

        # 拼装合并生成语义分块
        for idx, n in enumerate(nodes):
            m = dict(n.metadata)
            m.update(
                {
                    "source_file_path" : path,
                    "chunk_index": idx, # 一个Document可能会语义分块成多个node
                }
            )
            chunks.append(Document(text=n.text, metadata=m))

    for i, chunk in enumerate(chunks):
        print(f"第{i+1}个分块")
        print(chunk.metadata)
        print(chunk.text)

    return chunks

if __name__ == "__main__":
    semantic_chunk_documents(config.document_path)