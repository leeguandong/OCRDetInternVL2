## OCRDetInternVL2

OCR Large Multi-model Model，基于Internvl2微调OCR文字检测的多模态大模型，在4张A800上基于internvl2-8b模型微调。不仅在ocr文字检测任务上，在大多数的目标检测任务也是work的。非常详细的介绍在博客中：https://blog.csdn.net/u012193416/article/details/142740809

 <p align="center">
      <a href='https://github.com/leeguandong/OCRDetInternVL2'>
            <img src='https://img.shields.io/badge/Project-Page-Green'>
      </a>
      </br>
      <a href="https://github.com/leeguandong/OCRDetInternVL2/graphs/contributors">
        <img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/leeguandong/OCRDetInternVL2" />
      </a>
      <a href="https://github.com/leeguandong/OCRDetInternVL2/issues">
        <img alt="Issues" src="https://img.shields.io/github/issues/leeguandong/OCRDetInternVL2?color=0088ff" />
      </a>
      <a href="https://github.com/leeguandong/OCRDetInternVL2/pulls">
        <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/leeguandong/OCRDetInternVL2?color=0088ff" />
      </a>
      <a href=href="https://github.com/leeguandong/OCRDetInternVL2/stargazers">
        <img src="https://img.shields.io/github/stars/leeguandong/OCRDetInternVL2?color=ccf">
      </a>
      <a href=href="https://github.com/leeguandong/OCRDetInternVL2">
        <img src="https://img.shields.io/github/repo-size/leeguandong/OCRDetInternVL2.svg?style=flat-square">
      </a>
      </br>
      <a href=href="https://github.com/leeguandong/OCRDetInternVL2">
        <img src="https://visitor-badge.laobi.icu/badge?page_id=https://github.com/leeguandong/OCRDetInternVL2">
      </a>
      <a href=href="https://github.com/leeguandong/OCRDetInternVL2">
        <img src="https://img.shields.io/github/last-commit/leeguandong/OCRDetInternVL2">
      </a>
      <a href="https://github.com/leeguandong/OCRDetInternVL2/blob/main/LICENSE">
        <img alt="GitHub Contributors" src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg" />
      </a>
  </p>

## 本文贡献

- 借助OCR数据集，基于internvl2训练微调，并开放了用于学术研究的训练lora权重，推理时需要自行加载原始的internvl2-8b权重，可借助tools/swift_infer_merge_lora.sh进行权重合并。
## 数据集

- [自有数据](./data/ocr_det_test_dataset.jsonl)原始数据进行9:1的划分，主要是自有数据，只用了很少一部分的自有数据来跑通链路。其中训练数据有4788张图片，测试数据有533张图片

在上述工作中，报告信息都为非结构化的，不利于科学研究。我们对两个数据集进行了预处理，并最终得到了可以用于训练的数据。
|数据集|数量|下载链接|质量|
|:-|:-|:-|:-|
|OCR-data|4788|[ocr数据](./data/OCR_Det/test/Annotations/)、[ocr图像](./data/OCR_Det/test/Images/)|低|


## 快速上手

### 1.安装环境
```bash
# Full capabilities
pip install 'ms-swift[all]' -U
# LLM only
pip install 'ms-swift[llm]' -U
# AIGC only
pip install 'ms-swift[aigc]' -U
# Adapters only
pip install ms-swift -U
```
### 2.模型推理

|模型权重|下载链接|质量|微调方法|
|:-|:-|:-|:-|
|checkpoints-OCRDetInternVL2-570|results/internvl2_swift_ocrdet/internvl2-8b/v0-20241005-082227/checkpoint-740/|低|LoRA|

#### CLI推理

```python
CUDA_VISIBLE_DEVICES=7 swift export \
  --ckpt_dir "/home/lgd/e_commerce_lmm/results/internvl2_swift_ocrdet/internvl2-8b/v0-20241005-082227/checkpoint-740/" \
  --merge_lora true


CUDA_VISIBLE_DEVICES=7 swift infer \
    --ckpt_dir "/home/lgd/e_commerce_lmm/results/internvl2_swift_ocrdet/internvl2-8b/v0-20241005-082227/checkpoint-740-merged/" \
    --load_dataset_config true
```
### 3.模型训练（复现OCRDetInternVL2）

<details>
  <summary>硬件资源</summary>
  <p>* 实验在A800 (4X, 80GB)上进行</p>
</details>
- （1）准备[ocr数据](./data/OCR_Det/test/Annotations/)和[ocr图像](./data/OCR_Det/test/Images/);
- （2）开始训练：

```bash
swift_finetune_internvl_lora_det.sh
```
这里的复现过程非常简单，主要是很多过程我们都为大家准备好了，大家可以随时复现一个自己的`OCRDetInternVL2`。

## 效果展示

*以下效果来自于**低质量**的数据训练和权重   

具体的结果展示可以参见博客：https://blog.csdn.net/u012193416/article/details/142740809


## 项目致谢

1. [SWIFT](https://github.com/modelscope/swift)为我们提供了训练框架；

## 免责声明

本项目相关资源仅供学术研究之用，严禁用于商业用途。使用涉及第三方代码的部分时，请严格遵循相应的开源协议。

## 使用许可

此存储库遵循[CC BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/) ，请参阅许可条款。

## Star History

<a href="https://star-history.com/#leeguandong/OCRDetInternVL2&Date">

  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=leeguandong/OCRDetInternVL2&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=leeguandong/OCRDetInternVL2&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=leeguandong/OCRDetInternVL2&type=Date" />
  </picture>

</a>
