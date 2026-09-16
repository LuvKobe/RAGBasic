import os
from dotenv import load_dotenv
from pathlib import Path

# 父级目录
base_path = Path(__file__).parent

# 嵌入模型的路径
model_path = r"D:\models\BAAI--bge-m3\snapshots\master"

# 文档所在的目录
document_path = base_path / "文档"

# 结构分块目录
structure_path = document_path / "结构分块"

# 加载项目根目录下的.env文件
# 解析通义千问大模型秘钥
load_dotenv(base_path/".env")
dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")