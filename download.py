#模型下载
# 模型下载（指定保存到 D:\models 目录）
from modelscope import snapshot_download

# 下载模型并指定保存路径
model_dir = snapshot_download(
    'BAAI/bge-m3',
    cache_dir='D:\\models'   # 关键: 指定下载目录
)

# 打印最终保存路径，方便你查看
print("模型已下载到: ", model_dir)