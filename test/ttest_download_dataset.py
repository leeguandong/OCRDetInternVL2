#数据集下载
from modelscope.msdatasets import MsDataset
ds =  MsDataset.load('BoyaWu10/Bunny-v1.0-data',cache_dir="/home/lgd/common/Bunny/data/")
#您可按需配置 subset_name、split，参照“快速使用”示例代码