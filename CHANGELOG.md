# CHANGELOG

本文件自举《Agent迭代指南》3.6 的 changelog 机制：**tag 是权威版本源，本文件是版本视角索引**。

- 迭代任务条目：用 `agent-iteration/assets/templates/06-changelog模板.md` 的完整字段（任务编号、根因编号、影响调用方、回滚点、门禁八条对照）。
- 不开任务编号的文档类改动：在当前版本条目下追加带日期的一行。
- 本文件自 v2.0 起建立，此前无 tag 的历史 commit 不回补——changelog 只记录定稿事实。

## v2.0 — 2026-09-15

基线版本：《Agent迭代指南》v2 状态机模型（六状态、守卫三层、P1/P2/P3 分级分诊、模板库）与 `state_check.py` 现状即 v2.0。自此起 tag、CHANGELOG、frontmatter `version` 三者对齐。

- 2026-09-15 SKILL.md frontmatter 增加 `version` 字段；新增「版本与自举维护」一节
- 2026-09-15 建立 `docs/plan.md` 演进计划（APO-P 覆盖判断、git 管理范围与时机、工作目录宏观图三项待裁决）
- 2026-09-15 P-3 完成：目录宏观图（README §1-2 归属规则 / 指南 2.3 存储布局图）、vault 退出存储体系、模板双份同步（assets 为权威）、指南模板路径更新
