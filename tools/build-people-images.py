#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 assets/image/ 里的原始人员照片压缩为网页可用版本，输出到 assets/img/people/。

用法（在 lab-site 目录下执行）：
    python tools/build-people-images.py

依赖：Pillow（pip install Pillow）
原图不会被修改；输出为 .jpg，长边限制 640px，质量 82。
新增成员时：把照片放进 assets/image/，在下面的 NAME_MAP 加一行（英文文件名 -> 拼音），重跑脚本。
"""

import os
import sys
from PIL import Image, ImageOps

SRC_DIR = os.path.join("assets", "image")
OUT_DIR = os.path.join("assets", "img", "people")
MAX_EDGE = 640
QUALITY = 82

# 原始文件名（不含扩展名也算） -> 输出的 ASCII 文件名
NAME_MAP = {
    "王勇": "wangyong",
    "张品蕊": "zhangpinrui",
    "陆进": "lujin",
    "林远硕": "linyuanshuo",
    "薛宇阳": "xueyuyang",
    "田昊鑫": "tianhaoxin",
    "李骏逸": "lijunyi",
    "伊美谕": "yimeiyu",
    "温小雨": "wenxiaoyu",
    "杨丽静": "yanglijing",
    "陈宾": "chenbin",
    "金宏楷": "jinhongkai",
    "张旭": "zhangxu",
    "白卓娜": "baizhuona",
    "王乐威": "wanglewei",
    "唐博文": "tangbowen",
}


def main():
    if not os.path.isdir(SRC_DIR):
        sys.exit("找不到源目录：%s" % SRC_DIR)
    os.makedirs(OUT_DIR, exist_ok=True)

    total_in = total_out = 0
    done, skipped = [], []

    for fn in sorted(os.listdir(SRC_DIR)):
        stem, ext = os.path.splitext(fn)
        if ext.lower() not in (".jpg", ".jpeg", ".png", ".webp", ".bmp"):
            continue
        slug = NAME_MAP.get(stem)
        if not slug:
            skipped.append(fn)
            continue

        src_path = os.path.join(SRC_DIR, fn)
        out_path = os.path.join(OUT_DIR, slug + ".jpg")

        with Image.open(src_path) as im:
            im = ImageOps.exif_transpose(im)          # 修正手机拍摄的方向
            if im.mode in ("RGBA", "LA", "P"):        # 透明通道合成到白底
                im = im.convert("RGBA")
                bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
                im = Image.alpha_composite(bg, im).convert("RGB")
            else:
                im = im.convert("RGB")
            im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
            im.save(out_path, "JPEG", quality=QUALITY, optimize=True, progressive=True)

        size_in = os.path.getsize(src_path)
        size_out = os.path.getsize(out_path)
        total_in += size_in
        total_out += size_out
        done.append((stem, slug, size_in / 1024, size_out / 1024))

    for stem, slug, kb_in, kb_out in done:
        print("  %-6s -> %-14s %8.0f KB  ->  %6.0f KB" % (stem, slug + ".jpg", kb_in, kb_out))
    if skipped:
        print("  未匹配（请在 NAME_MAP 中补充）：" + ", ".join(skipped))
    print("  合计 %.1f MB -> %.1f MB" % (total_in / 1048576, total_out / 1048576))


if __name__ == "__main__":
    main()
