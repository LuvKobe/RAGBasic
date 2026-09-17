from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pymilvus import MilvusClient
import config
from typing import List, Dict, Any, Optional

client : MilvusClient = None

# 1. 连接milvus
def connect(dbpath : str) -> MilvusClient:
    global client
    client = MilvusClient(str(dbpath))
    return client

# 2. 获取client
def get_client() -> MilvusClient:
    return client

# 3. 创建db
def create_db(dbname : str) -> MilvusClient:
    return connect(config.base_path / f"{dbname}.db")

# 4. 切换db  use db
def use_db(dbname : str) -> MilvusClient:
    return connect(config.base_path / f"{dbname}.db")

# 5. 列出所有的db
def list_dbs() -> List[str]:
    return [p.stem for p in config.base_path.glob("*.db")]

# 6. 创建collection
def create_collection(name: str, dimension: int) -> None:
    client = get_client()
    if client.has_collection(name):
        client.drop_collection(collection_name=name)
    client.create_collection(collection_name=name, dimension=dimension)

# 7. 删除collection
def drop_collection(name:str) -> None:
    get_client().drop_collection(collection_name=name)

# 8. 插入数据
def insert(collection_name : str, rows: List[Dict[str, Any]]) -> Dict:
    return get_client().insert(collection_name=collection_name, data=rows)

# 9. 查询数据
def get_by_ids(collection_name: str, ids: List[int], fields: Optional[List[str]] = None) -> List[Dict]:
    return get_client().get(collection_name=collection_name, ids=ids, output_fields=fields)

# 声明向量模型
embed_model = HuggingFaceEmbedding(model_name=config.model_path)

# 10. 向量查询
def search_by_text(
        collection_name:str,
        limit: int=5,
        text: str="",
        fields: Optional[List[str]] = None,
) -> List[List[dict]]:
    vectors = [embed_model.get_text_embedding(text)]
    return get_client().search(
        collection_name=collection_name,
        data=vectors,
        limit=limit,
        output_fields=fields,
    )


# ============ 测试函数 ============

# 测试1：基础增删查（建库 -> 建集合 -> 插入 -> 按ID查询）
def test_crud():
    print("========== 测试1：基础CRUD ==========")
    # 1. 连接/创建数据库
    use_db("edison")
    # 2. 建集合，维度 1024（bge-m3 的向量维度）
    create_collection("01", 1024)

    # 3. 生成向量并插入
    text = "我是一个帅哥，我今年18岁了！"
    vec = embed_model.get_text_embedding(text)
    print("插入结果:", insert("01", [{"id": 1, "vector": vec, "text": text}]))

    # 4. 加载集合后按ID查询
    get_client().load_collection(collection_name="01")
    result = get_by_ids(collection_name="01", ids=[1], fields=["id", "text"])
    print("查询结果:", result)

    # 5. 简单断言，验证查到的内容和插入的一致
    assert result and result[0]["text"] == text, "❌ CRUD测试失败：查询结果与插入不一致"
    print("✅ CRUD测试通过\n")


# 测试2：向量语义搜索（插入多条 -> 用一句话去搜最相近的）
def test_search():
    print("========== 测试2：向量语义搜索 ==========")
    # 1. 建库建集合
    use_db("edison")
    create_collection("02", 1024)

    # 2. 批量插入若干句子
    datas = ["小明是一个大帅哥", "小明长得很好看", "今天中午吃点什么呢？", "我们正在学习RAG的课程"]
    for i, data in enumerate(datas, start=1):
        vector = embed_model.get_text_embedding(data)
        insert("02", [{"id": i, "vector": vector, "text": data}])

    # 3. 加载集合后按文本语义搜索
    get_client().load_collection(collection_name="02")
    query = "有很多女孩喜欢小明"
    results = search_by_text("02", text=query, limit=2, fields=["text"])

    print(f"搜索『{query}』的最相近结果：")
    for hit in results[0]:
        print(f"  相似度距离={hit['distance']:.4f}  文本={hit['entity']['text']}")
    print("✅ 搜索测试完成（观察上面返回的是否是与小明相关的句子）\n")


if __name__ == "__main__":
    test_crud()
    test_search()