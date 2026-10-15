#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
asset_hash.py — 一致性库资产哈希登记 / 比对工具

用途：给锚点图 / 空景图 / 道具图登记 sha256 指纹，垫图前自动比对，
防止参考图被偷偷替换、损坏或丢失（内容变了指纹必变，见哈希雪崩效应）。

命令：
  python asset_hash.py init  <asset_dir> [--manifest manifest.json]
      扫描目录下所有图片，生成指纹清单 manifest.json
  python asset_hash.py check <asset_dir> [--manifest manifest.json]
      重新扫描并对比清单，报告 MISSING(丢失)/CHANGED(被改)/ADDED(新增)/OK(一致)
      有 CHANGED 或 MISSING 时退出码为 1，否则 0（方便脚本判断）
  python asset_hash.py file  <image_path>
      只输出单个文件的 sha256，方便手动填进资产登记表

依赖：Python 3 标准库（hashlib/os/json/argparse），无需安装任何包。
跨平台：Windows(Git Bash/PowerShell) / macOS / Linux 均可。
"""

import argparse
import hashlib
import json
import os
import sys

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff"}


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_images(root):
    """返回 {相对路径(正斜杠): 绝对路径} 按相对路径排序"""
    found = {}
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext in IMAGE_EXTS:
                abs_path = os.path.join(dirpath, name)
                rel = os.path.relpath(abs_path, root).replace(os.sep, "/")
                found[rel] = abs_path
    return dict(sorted(found.items()))


def cmd_init(args):
    root = args.dir
    if not os.path.isdir(root):
        print("[错误] 目录不存在: " + root)
        return 2
    manifest_path = args.manifest
    images = collect_images(root)
    manifest = {
        "tool": "asset_hash.py",
        "algorithm": "sha256",
        "root": os.path.abspath(root),
        "files": {rel: sha256_of(ap) for rel, ap in images.items()},
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print("[init] 已登记 " + str(len(images)) + " 张图片 -> " + manifest_path)
    print("       根目录: " + manifest["root"])
    return 0


def cmd_check(args):
    root = args.dir
    manifest_path = args.manifest
    if not os.path.isfile(manifest_path):
        print("[错误] 清单不存在: " + manifest_path + "，请先跑 init")
        return 2
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    old = manifest.get("files", {})
    if not os.path.isdir(root):
        print("[错误] 目录不存在: " + root)
        return 2
    current = collect_images(root)

    old_keys = set(old)
    cur_keys = set(current)
    missing = sorted(old_keys - cur_keys)
    added = sorted(cur_keys - old_keys)
    changed = []
    ok = []
    for rel in sorted(old_keys & cur_keys):
        if old[rel] != sha256_of(current[rel]):
            changed.append(rel)
        else:
            ok.append(rel)

    print("[check] 对比 " + str(len(old)) + " 登记项 vs " + str(len(current)) + " 当前文件")
    for rel in ok:
        print("  OK      " + rel)
    for rel in changed:
        print("  CHANGED " + rel + "   <- 内容变了，可能被替换/损坏，垫图前务必重出！")
    for rel in missing:
        print("  MISSING " + rel + "   <- 文件不见了")
    for rel in added:
        print("  ADDED   " + rel + "   <- 新文件，未登记（可跑 init 更新清单）")

    problems = len(changed) + len(missing)
    print("[check] 一致 " + str(len(ok)) + " / 变更 " + str(len(changed)) +
          " / 丢失 " + str(len(missing)) + " / 新增 " + str(len(added)))
    if problems:
        print("[check] 存在 CHANGED 或 MISSING，退出码 1（垫图前先处理）")
        return 1
    print("[check] 全部一致，退出码 0")
    return 0


def cmd_file(args):
    p = args.path
    if not os.path.isfile(p):
        print("[错误] 文件不存在: " + p)
        return 2
    print(sha256_of(p))
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="一致性库资产哈希登记/比对工具（防参考图被偷换/损坏）"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="扫描目录生成指纹清单 manifest.json")
    p_init.add_argument("dir", help="资产目录（含图片）")
    p_init.add_argument("--manifest", default="asset-hash-manifest.json",
                        help="清单输出路径（默认 asset-hash-manifest.json）")
    p_init.set_defaults(func=cmd_init)

    p_check = sub.add_parser("check", help="对比清单，报告变更/丢失/新增")
    p_check.add_argument("dir", help="资产目录（含图片）")
    p_check.add_argument("--manifest", default="asset-hash-manifest.json",
                         help="清单路径（默认 asset-hash-manifest.json）")
    p_check.set_defaults(func=cmd_check)

    p_file = sub.add_parser("file", help="输出单个文件的 sha256")
    p_file.add_argument("path", help="图片文件路径")
    p_file.set_defaults(func=cmd_file)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
