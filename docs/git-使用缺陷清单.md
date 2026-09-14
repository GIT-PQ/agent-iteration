# agent-iteration skill — git 使用缺陷清单

> 2026-09-14 审查结论。skill 框架、流程、输出模板已齐备，但 git 使用存在以下缺陷，按严重程度排列。
> 证据以 `文件:行号` 标注（相对 agent-iteration/ 仓库根）。

## 1. `git archive` 提取副本泄漏 02-变更方案（读者边界被验证机制本身破坏）【严重】

- `references/05-verification.md:13,24` 明确"不给验证方 02-变更方案、偏离记录"；`SKILL.md:111` 规定验证对象是候选 commit 的 `git archive {hash}` 解包副本。
- 但 `iterations/{T-xxx}/` 整个目录（含 02-变更方案、01-归因问答、04-变更记录）就在工件仓库里，且按"文件即进度"在 3.1–3.4 期间写入。候选 commit 一旦包含它们（最自然做法，见缺陷 2），`git archive` 解包出的**完整仓库快照**里验证者可直接读到变更方案——"干净上下文"要求被 skill 自己规定的提取机制破坏。
- 指令说"只给工件 + 02-验收标准"，但文件就躺在副本里，约定形同虚设。

## 2. 迭代日志的提交时机完全未定义（缺陷 1 的根因）【严重】

- 整个 skill 没有一句话规定 01/02/03/05 文件、`evals/`、`results/` 基线**何时 commit**。SKILL.md 的"文件即进度"表只管落盘，不管 git。
- 两难：若 3.4 候选 commit 打包 iterations/ → 缺陷 1 成立；若不打包 → tag 指向的版本不含迭代日志，且 3.6 发布时工作区状态不明。
- 内部不一致证据：`scripts/state_check.py:59` 写"是否有文件被误删或**漏提交**"——脚本暗示这些文件该提交，但流程从未定义提交点。
- `references/03-testing.md:17` 基线只说"Git 提交或快照"，同样含糊。

## 3. 发布序列的 git 操作不闭合【中】

- `references/06-release.md:42` 说 changelog 是"紧随 tag 的独立 commit"，但 05 报告写回后**是否 commit、何时 commit** 未提及——3.5"工件冻结"与"05 是唯一写回仓库的产物"在 git 语义上如何调和，没有答案。
- 结果：3.6 打 tag 时工作区必然是脏的（05 报告 + changelog 修改）。
- `06-release.md:32` 的原子化补救（"tag 已打而 changelog 写入失败时删 tag 重来"）没覆盖 changelog commit 已存在的情况——tag 删了，commit 还在。
- tag 永远落后 HEAD 若干 commit（changelog、下个任务的日志）这个设计可以成立，但流程没有明说，agent 执行时容易自行脑补出错误操作。

## 4. 回滚的 git 语义含糊且有破坏性风险【中】

- `references/06-release.md:56`"切换 tag 指向回滚点"——不是任何标准 git 操作，可被解读为 checkout / `reset --hard` / revert，甚至移动现有 tag（移动已发布 tag 是典型反模式）。
- 若被解读为 `reset --hard`，会连带丢弃 tag 之后的 changelog、05 报告、iterations 留痕的 commit。
- 对一个由 agent 执行的 skill 来说，含糊到这个程度的 git 指令就是事故源。
- 回滚条目追加到 CHANGELOG 后的 commit 落点也未说明。

## 5. 启动时无"工作区干净"前置检查、无入库范围约定【严重】

- `SKILL.md:16` 只说"未 git 化先 git init"。缺少：
  - 初始 commit 作 diff 基准的要求（空仓库上第一个候选 commit 的 diff 基准是什么？）
  - 启动时工作区必须干净的要求。若工件仓库带着用户未提交的无关修改（现实中很常见），3.4 候选 commit 会把它们一并混入——**"改了什么由 git diff 承载"（`references/04-implementation.md:39`）和"触及清单是 diff 边界"（`SKILL.md:91`）两个核心机制直接失效**。
  - .gitignore/入库范围约定：`out/` 生成产物、`results/` 基线是否入库未说明——eval3 fixture 恰好就是"用户手改产物"的场景。
  - 分支约定：`references/04-implementation.md:47` 提到"可用任务分支，发布时合并回主线"，但 merge 是否 fast-forward、changelog commit 落在哪条线、tag 指向的候选 hash 与合并后主线的关系，均未定义。

## 次要

- `scripts/state_check.py` 完全不看 git：不校验 04 里记录的 hash 是否存在、工作区是否干净、tag 是否存在——断点判定与 git 状态脱节，SKILL.md:49 表中"04-变更记录.md（含 commit）"这行脚本层面并未兑现。
- `references/06-release.md` 未指定 annotated vs lightweight tag（建议 annotated，tag 才携带版本元数据）。

## 小结

- 最严重：缺陷 1（验证隔离失效）与缺陷 5（diff 边界失效）；缺陷 2 是根因；缺陷 3、4 是发布阶段没写完。
- 修复涉及：`SKILL.md`、`references/03/04/05/06-*.md`、`scripts/state_check.py`。
