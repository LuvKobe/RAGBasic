import os
from pathlib import Path

# 父级目录
base_path = Path(__file__).parent

# 嵌入模型的路径
model_path = r"D:\models\BAAI--bge-m3\snapshots\master"

# 文档所在的目录
document_path = base_path / "文档"

# 结构分块目录
structure_path = document_path / "结构分块"