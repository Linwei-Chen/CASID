# CASID

CASID: A Large-scale Climate-Aware Satellite Image Dataset for Domain Adaptive Land-Cover Semantic Segmentation



**Abstract**

A few well-annotated datasets for land-cover semantic segmentation have recently been introduced to benefit advancements in earth observation technologies.
However, these datasets ignore the huge diversity among geographic areas with different climates, which can profoundly affect and diversify the land cover. 
This leads to the domain gap of remote sensing images and severe performance degradation of the segmentation models.
To advance land-cover semantic segmentation with higher generalization ability,  we investigate the impact of climate on land-cover semantic segmentation for the first time.
In this paper, we introduce a unique large-scale Climate-Aware Satellite Images Dataset (CASID) for domain adaptive land-cover semantic segmentation.
It is collected from four typical climate zones, i.e., temperate monsoon, subtropical monsoon climate, tropical monsoon, and tropical rainforest.
Specifically, it consists of 980 satellite images in 5000 $\times$ 5000 resolution collected from 30 different areas around Asia, covering more than 24,500 square kilometers.
Samples from four typical climate zones form four sub-datasets/domains regarding their climate types, which makes our CASID the first climate-aware land-cover semantic segmentation dataset with multiple domains.
In addition, we provide a detailed analysis of the samples from the four climate zones, highlighting the differences in global image feature, image texture, category distribution, spectral value, and object shape, which all contribute to the climate domain gap. These analyses can provide valuable insights for subsequent research in this field.
Furthermore, we conduct extensive experiments to evaluate the latest semantic segmentation and unsupervised domain adaptation methods on the CASID dataset, which can serve as a strong baseline for future research.



## Dataset Overview

<img src="https://github.com/Linwei-Chen/CASID/blob/main/static/dataset_overview.png" width="1024px">

The distribution of the geographical locations of images in CASID. 
The box indicates the sampling areas.
The blue, green, yellow, and red in the climate map indicate four typical climates, i.e., temperate monsoon, subtropical monsoon, tropical monsoon, and tropical rainforest.
We illustrate some representative image samples from four climate zones and corresponding pixel-wise land-cover labels.



## Dataset Comparison

Comparison between our CASIDand themain land-cover datasets for semantic segmentation (SS) and unsupervised domain adaptation (UDA).

<img src="https://github.com/Linwei-Chen/CASID/blob/main/static/dataset_comparison.png" width="1024px">



## Dataset  Download

Some dataset samples are available at [link](https://pan.baidu.com/s/1Y8XgLWDEomH7Z16i3r3Ufw) (code: casi).

The whole dataset: 

Temperate Monsoon Climate: [Link](https://pan.baidu.com/s/1dyaWq63osAJbgwPbPDIX6Q) 
Extraction Code: casi 

Subtropical Monsoon Climate: [Link](https://pan.baidu.com/s/1aSEy_xZP3pxzxglia1J0xw) 
Extraction Code: casi 

Tropical Monsoon Climate: [Link](https://pan.baidu.com/s/1WEZ4daJKPwbvUa0preofAg) 
Extraction Code: casi 

Tropical Rainforest Climate: [Link](https://pan.baidu.com/s/1OJTeQRKd9NOjUGJZMMzHfQ) 
Extraction Code: casi

## Citation

Please cite the following:

```
@article{LIU202398,
	title = {A large-scale climate-aware satellite image dataset for domain adaptive land-cover semantic segmentation},
	journal = {ISPRS Journal of Photogrammetry and Remote Sensing},
	volume = {205},
	pages = {98-114},
	year = {2023},
	issn = {0924-2716},
	doi = {https://doi.org/10.1016/j.isprsjprs.2023.09.007},
	url = {https://www.sciencedirect.com/science/article/pii/S0924271623002484},
author = {Songlin Liu and Linwei Chen and Li Zhang and Jun Hu and Ying Fu},
}
```

