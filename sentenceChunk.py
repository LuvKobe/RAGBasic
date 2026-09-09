import re
from typing import List
from llama_index.core.schema import Document
import util
import config


# 实现按照句子去分块的功能
def sentence_chunk_documents(
        input_str : str,
        max_sentences: int = 5,
) -> List[Document]:
    chunks = []
    documents = util.clean_all_formats(input_str)

    for d in documents:
        text = d.text
        if not text:
            continue

        path = d.metadata.get("file_path")

        sents = [
            s.strip()
            for s in re.split(r"(?<=[。！？！？\.])\s+", text)
            if s.strip()
        ]

        if len(sents) == 1:
            sents = [
                s.strip()
                for s in re.split(r"(?<=[。！？！？\.])", text)
                if s.strip()
            ]

        # 每次遍历max_sentences这么多的句子，合并一个块
        for i in range(0, len(sents), max_sentences):
            part = " ".join(sents[i : i+max_sentences]).strip()
            if not part:
                continue

            m = dict(d.metadata)
            m.update({
                "source_file_path": path,
                "chunk_index": i // max_sentences,
                "chunk_start": i,
                "chunk_end": min(i+max_sentences, len(sents)),
            })

            chunks.append(Document(text=part, metadata=m))

    # for i, chunk in enumerate(chunks):
    #     print(f"第{i+1}个分块")
    #     print(chunk.metadata)
    #     print(chunk.text)
    return chunks

if __name__ == "__main__":
    sentence_chunk_documents(config.base_path/"文档")