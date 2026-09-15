# -*- coding: utf-8 -*-
"""扫描工件仓库的 iterations/ 目录，输出当前任务的状态与下一步。

用法：
    python state_check.py <工件仓库路径> [任务编号]

不指定任务编号时取编号最大的任务目录。
状态判定依据 SKILL.md 的"文件即进度"表：任务目录里按编号落盘的文件本身就是进度。
"""
import re
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    repo = Path(sys.argv[1])
    if not repo.is_dir():
        print(f"错误：{repo} 不是目录")
        sys.exit(2)
    iters = repo / "iterations"
    if not iters.is_dir():
        print("iterations/ 不存在——该工件仓库尚无迭代任务。下一步：3.1 问题归因（确认工件与仓库、提醒人 git init、分配任务编号）。")
        return

    task_dirs = [d for d in iters.iterdir() if d.is_dir() and re.fullmatch(r"T-\d+", d.name)]
    if not task_dirs:
        print("iterations/ 下没有任务目录。下一步：3.1 问题归因（分配 T-001）。")
        return

    if len(sys.argv) > 2:
        task = iters / sys.argv[2]
        if not task.is_dir():
            print(f"错误：iterations/{sys.argv[2]} 不存在")
            sys.exit(2)
    else:
        task = max(task_dirs, key=lambda d: int(d.name.split("-")[1]))
        if len(task_dirs) > 1:
            names = ", ".join(sorted(d.name for d in task_dirs))
            print(f"注意：存在多个任务目录（{names}），以下展示最新的 {task.name}。")

    files = {p.name for p in task.iterdir() if p.is_file()}
    has_01 = any(f.startswith("01-") for f in files)
    has_02_std = any(f.startswith("02-验收标准") for f in files)
    has_02_plan = any(f.startswith("02-变更方案") for f in files)
    has_03 = any(f.startswith("03-") for f in files)
    has_04 = any(f.startswith("04-") for f in files)
    reports_05 = sorted(
        (p for p in task.iterdir() if p.is_file() and p.name.startswith("05-验证报告")),
        key=lambda p: p.stat().st_mtime,
    )

    print(f"任务目录：{task}")

    if not has_01:
        if has_02_std or has_03 or has_04:
            print("异常：01-归因问答缺失但后续文件存在——编号跳跃，人工检查是否有文件被误删或漏提交。")
        print("当前状态：未入流程或 3.1 问题归因中。下一步：完成归因，写 01-归因问答.md。")
        return
    if not (has_02_std and has_02_plan):
        missing = "、".join(n for n, ok in [("02-验收标准", has_02_std), ("02-变更方案", has_02_plan)] if not ok)
        print(f"当前状态：3.2 变更设计。下一步：补写 {missing}。")
        return
    if not has_03:
        print("当前状态：3.3 测试准备。下一步：保存基线、建 eval，写 03-测试准备.md。")
        return
    if not has_04:
        print("当前状态：3.4 修改实现。下一步：按触及清单修改，自检通过后提醒人 commit（人确认提交后进入 3.5），写 04-变更记录.md。")
        return
    if not reports_05:
        print("当前状态：3.5 验证回归。下一步：由非实现者在干净上下文验证候选 commit，写 05-验证报告-{hash}.md。"
              "（若上次验证被中断，直接重入即可——05 缺失即视为未完成）")
        return
    if len(reports_05) > 1:
        print(f"注意：存在 {len(reports_05)} 份验证报告（每个候选版本一份），以最新落盘的为准：{reports_05[-1].name}")
    cl = repo / "CHANGELOG.md"
    published = cl.exists() and task.name in cl.read_text(encoding="utf-8", errors="replace")
    if published:
        print(f"当前状态：3.6 发布（changelog 已含 {task.name}，任务可能已发布完结）。"
              "下一步：核对 tag 与 changelog 是否原子化落盘；若生产恶化，提醒人执行回滚并带新证据重入 3.1。")
    else:
        print("当前状态：3.6 发布。下一步：门禁八条对照 → 提醒人打 tag（指向验证过的候选 commit，与 05 报告 hash 一致）"
              "→ 提醒人提交留痕与 changelog → 归档检查，三者原子化。")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    main()
