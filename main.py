# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


import argparse
import os
import shutil
from collections import defaultdict

# -------------------------- 配置规则常量 --------------------------
# 优先匹配homework关键字
HOMEWORK_KEYWORDS = {"作业", "练习", "实验", "任务"}
# 后缀-目录映射
EXT_RULES = {
    (".ppt", ".pptx", ".key"): "slides",
    (".py", ".ipynb", ".c", ".cpp", ".java"): "code",
    (".csv", ".xlsx", ".json"): "data",
    (".pdf", ".doc", ".docx", ".txt", ".md"): "documents",
    (".png", ".jpg", ".jpeg", ".gif"): "images",
}
OTHER_DIR = "others"
# 全局统计
file_record = []
type_count = defaultdict(int)
total_files = 0
operate_mode = "copy"  # 默认复制

# -------------------------- 工具函数 --------------------------
def get_target_subdir(filename: str) -> str:
    """根据文件名判定目标子文件夹，关键字优先级高于后缀"""
    # 第一步：匹配作业关键字
    for kw in HOMEWORK_KEYWORDS:
        if kw in filename:
            return "homework"
    # 第二步：匹配文件后缀
    _, ext = os.path.splitext(filename.lower())
    for ext_tuple, dir_name in EXT_RULES.items():
        if ext in ext_tuple:
            return dir_name
    # 无法识别后缀
    return OTHER_DIR

def get_safe_path(target_dir: str, filename: str) -> str:
    """同名文件自动重命名，避免覆盖"""
    dest_path = os.path.join(target_dir, filename)
    if not os.path.exists(dest_path):
        return dest_path
    # 拆分文件名与后缀
    name_no_ext, ext = os.path.splitext(filename)
    idx = 1
    while True:
        new_name = f"{name_no_ext}_{idx}{ext}"
        new_path = os.path.join(target_dir, new_name)
        if not os.path.exists(new_path):
            return new_path
        idx += 1

def scan_files(source: str, recursive: bool):
    """遍历源目录，递归/非递归扫描文件"""
    all_file_paths = []
    if recursive:
        for root, _, files in os.walk(source):
            for f in files:
                all_file_paths.append(os.path.join(root, f))
    else:
        for item in os.listdir(source):
            full_path = os.path.join(source, item)
            if os.path.isfile(full_path):
                all_file_paths.append(full_path)
    return all_file_paths

def generate_report(target_root: str):
    """生成整理报告.txt"""
    report_path = os.path.join(target_root, "整理报告.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("===== 文件整理报告 =====\n")
        f.write(f"1. 文件操作模式：{operate_mode}\n")
        f.write(f"2. 本次整理总文件数量：{total_files}\n\n")
        f.write("3. 文件迁移明细（源路径 -> 目标路径）\n")
        for src, dst in file_record:
            f.write(f"{src}  -->  {dst}\n")
        f.write("\n4. 各类型文件统计\n")
        for dir_name, cnt in type_count.items():
            f.write(f"{dir_name}：{cnt} 个\n")

def run_organize(source: str, target: str, dry_run: bool, recursive: bool, mode: str):
    global total_files, operate_mode
    operate_mode = mode
    # 校验源目录存在
    if not os.path.isdir(source):
        print(f"错误：源目录 {source} 不存在！")
        return
    all_files = scan_files(source, recursive)
    total_files = len(all_files)
    print(f"共扫描到 {total_files} 个待整理文件\n")
    # dry-run仅打印计划，不创建目录、不复制
    if dry_run:
        print("===== 【预览模式 dry-run】仅输出整理计划，无实际文件操作 =====")
        for file_path in all_files:
            filename = os.path.basename(file_path)
            sub_dir = get_target_subdir(filename)
            target_sub = os.path.join(target, sub_dir)
            safe_dst = get_safe_path(target_sub, filename)
            print(f"计划：{file_path}  ->  {safe_dst}")
        return
    # 真实执行：创建根目录 + 所有分类子目录
    os.makedirs(target, exist_ok=True)
    all_subdirs = ["homework"] + list(EXT_RULES.values()) + [OTHER_DIR]
    for sub in all_subdirs:
        os.makedirs(os.path.join(target, sub), exist_ok=True)
    # 逐个处理文件
    for file_path in all_files:
        filename = os.path.basename(file_path)
        sub_dir = get_target_subdir(filename)
        target_sub = os.path.join(target, sub_dir)
        safe_dst = get_safe_path(target_sub, filename)
        # 执行复制/移动
        if mode == "copy":
            shutil.copy2(file_path, safe_dst)
        elif mode == "move":
            shutil.move(file_path, safe_dst)
        # 记录日志、统计数量
        file_record.append((file_path, safe_dst))
        type_count[sub_dir] += 1
        print(f"已处理：{file_path} --> {safe_dst}")
    # 生成报告
    generate_report(target)
    print(f"\n整理完成！报告已生成：{os.path.join(target, '整理报告.txt')}")

# -------------------------- 命令行参数解析 --------------------------
def main():
    parser = argparse.ArgumentParser(description="课程资料自动分类整理工具")
    # 基础必选参数
    parser.add_argument("--source", required=True, help="原始课程资料目录")
    parser.add_argument("--target", required=True, help="整理后的目标根目录")
    # 可选控制参数
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不执行真实文件操作")
    parser.add_argument("--recursive", action="store_true", help="递归扫描子目录（加分功能）")
    parser.add_argument("--mode", choices=["copy", "move"], default="copy", help="文件操作模式：copy(默认)/move")
    args = parser.parse_args()
    run_organize(args.source, args.target, args.dry_run, args.recursive, args.mode)

if __name__ == "__main__":
    main()

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
