from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import config
from typing import List
from llama_index.core.schema import Document
import util
from llama_index.core.node_parser import SemanticSplitterNodeParser #语义分块器


# 测试嵌入模型的方法
def test_embedding_similarity(
        sentence1: str,
        sentence2: str,
) -> float:
    # 1. 嵌入模型
    embed_model = HuggingFaceEmbedding(model_name=config.model_path)

    # 2. 计算文本的向量
    vec1 = embed_model.get_text_embedding(sentence1)
    vec2 = embed_model.get_text_embedding(sentence2)

    # 3. 根据向量求相似度
    similarity = embed_model.similarity(vec1, vec2)

    # 4. 打印
    print(f"\n句子1: {sentence1}")
    print(f"向量1: (维度 {len(vec1)}) : {vec1}")
    print(f"\n句子2: {sentence2}")
    print(f"向量2: (维度 {len(vec2)}) : {vec2}")
    print(f"\n句子相似度：{similarity:.4f}")

    return similarity

if __name__ == "__main__":
    test_embedding_similarity("edison长得很帅！！！", "edison长得很好看！！！")
    test_embedding_similarity("edison长得很帅！！！", "今天要下雨吗？？？")