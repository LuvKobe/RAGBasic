from llama_index.core import SimpleDirectoryReader
from pathlib import Path
base_path = Path(__file__).parent

# 定义方法：加载并解析一个目录下面的所有文件
def pare_all_formats(input_dir):

    reader = SimpleDirectoryReader(
        input_dir = input_dir
    )

    documents =  reader.load_data()

    for i, doc in enumerate(documents):
        file_name = doc.metadata.get("file_path")
        print(f"\n 第 {i+1} 个对象 | 文件路径：{file_name}")
        print(doc.text[:200])

    return documents

if __name__ == "__main__":
    pare_all_formats(base_path/"文档")