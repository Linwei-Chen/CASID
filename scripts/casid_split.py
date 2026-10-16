#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CASID 图块裁切脚本（参考 DOTA 数据集的大图滑窗裁切方式，面向语义分割）。

DOTA（arXiv:1711.10398）将大图按滑动窗口切成 1024×1024 图块（论文默认步距 512），
DOTA_devkit 的 ImgSplit 工具把图块尺寸(subsize)与重叠(gap)做成参数，并支持多尺度
（先把原图按 rate 缩放，再用同样的窗口切）。本脚本沿用这套约定，并针对语义分割
做了适配：图像与标注逐像素同步裁切，标注按类别 id 处理（缩放一律用最近邻插值），
窗口越界部分用 0（background）填充或按边缘对齐截取。

默认参数与 CASID 论文实验完全一致：1024×1024、步距 994（重叠 30），
每张 5000×5000 原图恰好切出 5×5=25 块，无填充、无浪费。

依赖：Python >= 3.7，Pillow，numpy

用法示例：
  # 论文同款（默认，25 块/张）
  python casid_split.py --root CASID/ --out TILES_1024/

  # DOTA 论文设置：重叠 512，边缘补零
  python casid_split.py --root CASID/ --out TILES_DOTA/ --gap 512 --pad

  # mmrotate 社区常用：重叠 200
  python casid_split.py --root CASID/ --out TILES_gap200/ --gap 200 --pad

  # 多尺度（DOTA 多尺度惯例 0.5/1.0/1.5）
  python casid_split.py --root CASID/ --out TILES_MS/ --rates 0.5 1.0 1.5

  # 只切训练集 / 指定区域
  python casid_split.py --root CASID/ --out TILES/ --split train
  python casid_split.py --root CASID/ --out TILES/ --regions 20,21

输入目录结构（即 Hugging Face 上 CASID 仓库的结构）：
  CASID/
    images/{zone}/{region_dir}/*_img.tif
    labels/{zone}/{region_dir}/*_gt.png
    splits/train.txt, test.txt      # 每行一个样本 stem（相对路径不含扩展名）
    regions.csv

输出：
  out/images/{zone}/{region_dir}/{stem}_H{y}_W{x}.png
  out/labels/{zone}/{region_dir}/{stem}_H{y}_W{x}_gt.png
  多尺度时外层多一级 out/rate{r}/...
"""
import argparse
import csv
import os
import sys
from multiprocessing import Pool

import numpy as np
from PIL import Image

# 5 类地物 + 调色板（与数据集 colormap.json 一致；沿用原始标注配色：黄=建筑、红=道路）
CLASS_NAMES = ["background", "building", "forest", "road", "water"]
PALETTE_RGB = {
    0: (0, 0, 0),
    1: (255, 255, 0),
    2: (85, 255, 0),
    3: (255, 0, 0),
    4: (0, 112, 255),
}
N_CLASSES = 5
PAL_SIZE = 16


def build_palette():
    pal = []
    for i in range(PAL_SIZE):
        pal.extend(PALETTE_RGB.get(i, (i, i, i)))
    return pal


PALETTE = build_palette()


def tile_starts(size, subsize, stride, pad):
    """一个轴上的窗口起点序列。

    pad=False：固定步距网格（与 CASID 原始图块一致，所有图像共用同一网格；
    上一窗未到达边缘才继续开窗，末窗越界时按图像边缘裁齐——如 4656 高的图
    网格仍为 {0,994,1988,2982,3976}，末行高度裁到 680）。
    pad=True：DOTA 风格，按 stride 铺满、末窗越界补零。
    """
    if size <= subsize:
        return [0]
    if pad:
        return list(range(0, size, stride))
    starts = [0]
    while starts[-1] + subsize < size:
        starts.append(starts[-1] + stride)
    return starts


def load_pairs(root, args):
    """返回 [(img_path, lbl_path, stem, zone, region_dir), ...]"""
    pairs = []
    zones = args.zones.split(",") if args.zones else None
    regions = set(args.regions.split(",")) if args.regions else None
    allow = None
    if args.split and args.split != "all":
        sf = os.path.join(root, "splits", "%s.txt" % args.split)
        with open(sf, encoding="utf-8") as f:
            allow = set(l.strip() for l in f if l.strip())
    with open(os.path.join(root, "regions.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if zones and row["zone_en"] not in zones:
                continue
            if regions and row["region_id"] not in regions:
                continue
            zone, rdir = row["zone_en"], row["region_dir"]
            idir = os.path.join(root, "images", zone, rdir)
            ldir = os.path.join(root, "labels", zone, rdir)
            if not os.path.isdir(idir):
                print("WARNING: 找不到 %s，跳过区域 %s（本地未下载该区？）" % (idir, rdir))
                continue
            for fn in sorted(os.listdir(idir)):
                if not fn.endswith(args.img_ext):
                    continue
                stem = fn[: -len(args.img_ext)]
                if stem.endswith("_img"):   # 发布版图像名为 {stem}_img.tif
                    stem = stem[: -len("_img")]
                ipath = os.path.join(idir, fn)
                lpath = os.path.join(ldir, stem + args.lbl_suf + ".png")
                if not os.path.isfile(lpath):
                    raise FileNotFoundError("label missing for %s" % ipath)
                if allow is not None:
                    rel = "%s/%s/%s" % (zone, rdir, stem)
                    if rel not in allow:
                        continue
                pairs.append((ipath, lpath, stem, zone, rdir))
    return pairs


def cut_one(task):
    ipath, lpath, stem, zone, rdir, out_root, subsize, stride, pad, rate = task
    img = Image.open(ipath); img.load()
    lbl = Image.open(lpath); lbl.load()
    # 标签统一到"像素值=类别id"的 uint8 数组域，避免调色板/插值重映射
    la = np.array(lbl)
    if la.ndim == 3:
        la = la[:, :, 0]
    la = la.astype(np.uint8, copy=False)
    if rate != 1.0:
        w, h = img.size
        nw, nh = round(w * rate), round(h * rate)
        img = img.resize((nw, nh), Image.BILINEAR)
        la_img = Image.fromarray(la, "L").resize((nw, nh), Image.NEAREST)
        la = np.array(la_img)
    W, H = img.size
    assert la.shape == (H, W), "label/image size mismatch: %s" % ipath
    ia = np.asarray(img)
    xs = tile_starts(W, subsize, stride, pad)
    ys = tile_starts(H, subsize, stride, pad)
    od_i = os.path.join(out_root, "images", zone, rdir)
    od_l = os.path.join(out_root, "labels", zone, rdir)
    n = 0
    for y in ys:
        for x in xs:
            if pad:
                ch = min(subsize, H - y); cw = min(subsize, W - x)
                iarr = np.zeros((subsize, subsize, 3), dtype=np.uint8)
                iarr[:ch, :cw] = ia[y:y + ch, x:x + cw]
                larr = np.zeros((subsize, subsize), dtype=np.uint8)
                larr[:ch, :cw] = la[y:y + ch, x:x + cw]
            else:
                iarr = np.ascontiguousarray(ia[y:y + subsize, x:x + subsize])
                larr = np.ascontiguousarray(la[y:y + subsize, x:x + subsize])
            itile = Image.fromarray(iarr)
            ltile = Image.fromarray(larr)
            ltile.putpalette(PALETTE)
            os.makedirs(od_i, exist_ok=True)
            os.makedirs(od_l, exist_ok=True)
            base = "%s_H%d_W%d" % (stem, y, x)
            itile.save(os.path.join(od_i, base + ".png"))
            ltile.save(os.path.join(od_l, base + "_gt.png"))
            n += 1
    return (stem, n)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True, help="CASID 数据集根目录")
    ap.add_argument("--out", required=True, help="输出根目录")
    ap.add_argument("--subsize", type=int, default=1024, help="图块边长（默认 1024）")
    ap.add_argument("--stride", type=int, default=994, help="滑动步距（默认 994，即重叠 30，论文同款）")
    ap.add_argument("--gap", type=int, default=None,
                    help="DOTA 习惯：用重叠量代替步距，stride = subsize - gap（如 --gap 512 为 DOTA 论文设置）")
    ap.add_argument("--pad", action="store_true", help="越界补零（DOTA 风格）；默认关闭：末窗锚定图像边缘，不补零")
    ap.add_argument("--rates", type=float, nargs="+", default=[1.0], help="多尺度缩放系数（DOTA 惯例 0.5 1.0 1.5）")
    ap.add_argument("--split", default="all", choices=["train", "test", "all"])
    ap.add_argument("--zones", default=None, help="逗号分隔的气候带英文名过滤")
    ap.add_argument("--regions", default=None, help="逗号分隔的区域编号过滤，如 20,21")
    ap.add_argument("--img-ext", default=".tif")
    ap.add_argument("--lbl-suf", default="_gt")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    if args.gap is not None:
        args.stride = args.subsize - args.gap
        if args.stride <= 0:
            sys.exit("--gap 必须小于 --subsize")
    if args.stride > args.subsize:
        sys.exit("--stride 不能大于 --subsize（会产生漏切空隙）")

    pairs = load_pairs(args.root, args)
    print("待处理样本：%d" % len(pairs))

    for rate in args.rates:
        if rate <= 0:
            sys.exit("--rates 必须为正数")
        out_root = args.out if len(args.rates) == 1 else os.path.join(args.out, "rate%s" % rate)
        tasks = [(ip, lp, st, z, r, out_root, args.subsize, args.stride, args.pad, rate)
                 for ip, lp, st, z, r in pairs]
        total = 0
        with Pool(args.workers) as pool:
            for stem, n in pool.imap_unordered(cut_one, tasks):
                total += n
        print("rate=%s：完成 %d 样本，共 %d 图块 → %s" % (rate, len(tasks), total, out_root))


if __name__ == "__main__":
    main()
