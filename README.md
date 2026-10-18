# CASID

<p align="center">
  <a href="https://huggingface.co/datasets/Linwei-Chen/CASID"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Dataset-CASID-yellow" alt="Hugging Face Dataset"></a>
  <a href="https://doi.org/10.1016/j.isprsjprs.2023.09.007"><img src="https://img.shields.io/badge/ISPRS_JPRS-205%3A98--114%2C_2023-blue" alt="Paper"></a>
  <a href="https://arxiv.org/abs/2610.21238"><img src="https://img.shields.io/badge/arXiv-2610.21238-b31b1b" alt="arXiv"></a>
</p>

**CASID: A Large-scale Climate-Aware Satellite Image Dataset for Domain Adaptive Land-Cover Semantic Segmentation**

*Songlin Liu*¹·², *Linwei Chen*³ (co-first authors), Li Zhang², Jun Hu⁴, Ying Fu³ (corresponding)

¹ Wuhan University &nbsp; ² State Key Laboratory of Geo-information Engineering, Xi'an &nbsp; ³ Beijing Institute of Technology &nbsp; ⁴ Sun Yat-sen University

Published in **ISPRS Journal of Photogrammetry and Remote Sensing 205 (2023) 98–114** — [doi.org/10.1016/j.isprsjprs.2023.09.007](https://doi.org/10.1016/j.isprsjprs.2023.09.007)

---

**Abstract**

A few well-annotated datasets for land-cover semantic segmentation have recently been introduced to benefit advancements in earth observation technologies. However, these datasets ignore the huge diversity among geographic areas with different climates, which can profoundly affect and diversify the land cover. This leads to the domain gap of remote sensing images and severe performance degradation of the segmentation models. To advance land-cover semantic segmentation with higher generalization ability, we investigate the impact of climate on land-cover semantic segmentation for the first time. In this paper, we introduce a unique large-scale Climate-Aware Satellite Images Dataset (CASID) for domain adaptive land-cover semantic segmentation. It is collected from four typical climate zones, i.e., temperate monsoon, subtropical monsoon, tropical monsoon, and tropical rainforest. Specifically, it consists of 980 satellite images in 5000 × 5000 resolution collected from 30 different areas around Asia, covering more than 24,500 square kilometers. Samples from four typical climate zones form four sub-datasets/domains regarding their climate types, which makes our CASID the first climate-aware land-cover semantic segmentation dataset with multiple domains. In addition, we provide a detailed analysis of the samples from the four climate zones, highlighting the differences in global image feature, image texture, category distribution, spectral value, and object shape, which all contribute to the climate domain gap. These analyses can provide valuable insights for subsequent research in this field. Furthermore, we conduct extensive experiments to evaluate the latest semantic segmentation and unsupervised domain adaptation methods on the CASID dataset, which can serve as a strong baseline for future research.

## Dataset Overview

<img src="https://github.com/Linwei-Chen/CASID/blob/main/static/dataset_overview.png" width="1024px">

The distribution of the geographical locations of images in CASID.
The box indicates the sampling areas.
The blue, green, yellow, and red in the climate map indicate four typical climates, i.e., temperate monsoon, subtropical monsoon, tropical monsoon, and tropical rainforest.
We illustrate some representative image samples from four climate zones and corresponding pixel-wise land-cover labels.

## Dataset Comparison

Comparison between our CASID and the main land-cover datasets for semantic segmentation (SS) and unsupervised domain adaptation (UDA).

<img src="https://github.com/Linwei-Chen/CASID/blob/main/static/dataset_comparison.png" width="1024px">

---

## 🤗 Full Dataset Released

The **complete dataset** is now publicly available on Hugging Face:
### 👉 https://huggingface.co/datasets/Linwei-Chen/CASID

The release (~65 GB) contains **980 image–label pairs at full 5000×5000 resolution** (LZW-compressed GeoTIFF-style TIF), unified 5-class palette-PNG labels, region-level train/test splits, bilingual region metadata, an MD5 manifest for integrity verification, and a DOTA-style tile-cropping script.

### 1. Download

```bash
pip install -U "huggingface_hub[cli]"

# full dataset (~65 GB)
hf download Linwei-Chen/CASID --repo-type dataset --local-dir CASID-dataset

# or in Python
python -c "
from huggingface_hub import snapshot_download
snapshot_download('Linwei-Chen/CASID', repo_type='dataset', local_dir='CASID-dataset')"
```

> In mainland China you can set the mirror endpoint: `export HF_ENDPOINT=https://hf-mirror.com`
>
> The full dataset is also mirrored on Baidu Netdisk (code: `casi`):
> Temperate Monsoon: [Link](https://pan.baidu.com/s/1dyaWq63osAJbgwPbPDIX6Q) ·
> Subtropical Monsoon: [Link](https://pan.baidu.com/s/1aSEy_xZP3pxzxglia1J0xw) ·
> Tropical Monsoon: [Link](https://pan.baidu.com/s/1WEZ4daJKPwbvUa0preofAg) ·
> Tropical Rainforest: [Link](https://pan.baidu.com/s/1OJTeQRKd9NOjUGJZMMzHfQ)
>
> A small sample subset is available at [Baidu Netdisk](https://pan.baidu.com/s/1Y8XgLWDEomH7Z16i3r3Ufw) (code: `casi`).

### 2. Verify integrity (recommended)

Every released file is listed with its size and MD5 in `release_file_hashes.csv`. After downloading, run:

```bash
python scripts/verify_download.py --root CASID-dataset
```

### 3. Dataset structure & naming

```
CASID-dataset
├── images/{climate_zone}/{region_dir}/{region_dir}_{idx:03d}_img.tif   # 980 satellite images, 5000×5000
├── labels/{climate_zone}/{region_dir}/{region_dir}_{idx:03d}_gt.png    # 980 pixel-wise labels (palette PNG)
├── splits/train.txt              # 681 image stems
├── splits/test.txt               # 299 image stems
├── file_mapping.csv              # original (Chinese) filename ↔ released filename ↔ split
├── regions.csv                   # 30 regions, bilingual metadata (zone, counts, country)
├── colormap.json                 # class → color definition
├── release_file_hashes.csv       # size + MD5 of every file
├── verification_report.md        # how the release was validated
└── scripts/casid_split.py        # DOTA-style tile cropping tool
```

- `{climate_zone}` ∈ `temperate_monsoon` (284) / `subtropical_monsoon` (284) / `tropical_monsoon` (202) / `tropical_rainforest` (210)
- `{region_dir}` = `region{NN}_{english_name}`, e.g. `region18_northwest_of_zhangjiakou` — **all filenames are ASCII**; the original Chinese filenames are preserved in `file_mapping.csv` together with `regions.csv` (e.g. `region03_east_of_yilan` ↔ 台湾-宜兰县以东).
- The train/test split follows the paper: **whole regions are never split across sets** (22 train regions → 681 images; 8 test regions → 299 images), so there is no cross-region leakage.

### 4. Labels

Five classes, `0–4`, encoded as a palette PNG — one line of code returns the id map:

| id | class | color | RGB |
|----|--------------|--------|-------------|
| 0 | Background | black | (0, 0, 0) |
| 1 | Building | yellow | (255, 255, 0) |
| 2 | Forest | green | (85, 255, 0) |
| 3 | Road | red | (255, 0, 0) |
| 4 | Water | blue | (0, 112, 255) |

```python
import numpy as np
from PIL import Image

label = np.array(Image.open("labels/tropical_rainforest/region02_kuala_lumpur/region02_kuala_lumpur_000_gt.png"))
print(label.shape, label.dtype, np.unique(label))  # (5000, 5000) uint8 [0..4]

# visualize with the exact released colors
from PIL import Image as I
colormap = {0:(0,0,0), 1:(255,255,0), 2:(85,255,0), 3:(255,0,0), 4:(0,112,255)}
rgb = np.zeros((*label.shape, 3), np.uint8)
for k, v in colormap.items(): rgb[label == k] = v
I.fromarray(rgb).save("vis.png")
```

> **Note on label unification.** The original internal RGB labels contain a few non-canonical color variants (e.g., forest rendered as `(76,230,0)` in 77 images instead of `(85,255,0)`, caused by a legacy palette mismatch in the authors' tile-cutting tool). In the released labels every pixel is deterministically mapped to the canonical 5-class ids — each image passed a strict **zero-mismatch** check against the authors' official training tiles (see `verification_report.md` for the full audit). You can therefore train on the released labels and on `cropped_label` tiles consistently.

### 5. Crop 5000×5000 images into 1024×1024 tiles (DOTA-style)

`scripts/casid_split.py` reproduces the tile grid used in the paper's experiments: **1024×1024 tiles with a 30-px overlap (stride 994), 25 tiles per image**, and also supports DOTA-style gap/padding and multi-scale training.

```bash
# paper-faithful default: subsize 1024, stride 994 → 5×5 = 25 tiles per image
python scripts/casid_split.py --img-dir <images_root> --label-dir <labels_root> --out-dir <output>

# DOTA-style with a 200-px gap between tiles, padding with zeros
python scripts/casid_split.py --gap 200 --pad --img-dir ... --label-dir ... --out-dir ...

# multi-scale training sets (0.5×, 1.0×, 1.5×); images resampled bilinearly, labels nearest
python scripts/casid_split.py --rates 0.5,1.5 --img-dir ... --label-dir ... --out-dir ...

# parallel
python scripts/casid_split.py --num-workers 8 ...
```

Tile filenames follow `{stem}-H{row}-W{col}.png` conventions, and both `--img-ext`/`--label-ext` are configurable. The default grid was verified **pixel-exact** against the authors' original cropped tiles.

### 6. Benchmark snapshot

Training and testing within the same climate zone vs. across climate zones (DeepLabV2, mIoU):

| Train \ Test | TemMs | SubMs | TroMs | TroRf |
|---|---|---|---|---|
| TemMs | **39.9** | 9.4 | 10.9 | 12.2 |
| SubMs | 10.0 | **60.9** | 12.8 | 15.3 |
| TroMs | 12.2 | 12.8 | **56.5** | 9.1 |
| TroRf | 8.5 | 10.2 | 12.8 | **49.0** |

A model trained in one climate zone **collapses** in another (e.g., temperate monsoon → tropical rainforest: only 12.2 mIoU). The paper additionally analyzes the gap via t-SNE global features, GLCM texture statistics, per-class distributions (forest: 76.2% in rainforest vs. 45.4% in temperate zones), spectral values, and object shapes, and benchmarks 12 segmentation methods and 7 UDA methods (up to DAFormer) — see the [paper](https://doi.org/10.1016/j.isprsjprs.2023.09.007) for full results.

### 7. Known quirks

- 978/980 images are exactly 5000×5000; the two Singapore (`region29_linkcuo_port`) images are 5000×4656 — the cropping tool handles them by clipping the last tile row.
- Test regions (8): Hokkaido, Lyuliang, Yilan(Taiwan), Tokyo, Shaoyang, Wanning, Around Laoag, Pharaangkaraya — matching the paper's split.

## Citation

If you find CASID useful for your research, please cite:

```bibtex
@article{LIU202398,
	title = {A large-scale climate-aware satellite image dataset for domain adaptive land-cover semantic segmentation},
	journal = {ISPRS Journal of Photogrammetry and Remote Sensing},
	volume = {205},
	pages = {98-114},
	year = {2023},
	issn = {0924-2716},
	doi = {10.1016/j.isprsjprs.2023.09.007},
	url = {https://www.sciencedirect.com/science/article/pii/S0924271623002484},
	author = {Songlin Liu and Linwei Chen and Li Zhang and Jun Hu and Ying Fu},
}
```

## License

The dataset itself is released under **CC BY 4.0**; the tools/scripts in this repository are released under the **MIT License** (see [LICENSE](LICENSE)).
