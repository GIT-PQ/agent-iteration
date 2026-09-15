# agent-iteration 项目

本仓库同时承载 skill 产物与它的设计文档，两层分开管理、各有职责。

## 1. 目录结构

```
agent-iteration/          skill 产物（纯净，只含 skill 运行所需文件）
  SKILL.md                入口：状态机、启动流程、横切规范速查
  references/             各状态行为规约（01-06 对应六状态）
  assets/templates/       9 份填写模板（编号即状态）
  scripts/state_check.py  断点判定（中断重入时用）
docs/                     设计文档层（不进入 skill 运行时）
  guide/                  《Agent迭代指南》v2 方法论全文与设计层模板
  plan.md                 演进计划：上游 backlog（待裁决与讨论项）
  requirements-analysis/  需求分析报告
CHANGELOG.md              版本视角索引
```

## 2. 结构规则

- **`agent-iteration/` 是 skill 产物，保持纯净**：只写入 skill 运行所需的文件；项目管理类内容（仓库级目录说明、维护约定、跨层指针）一律不写入，放 `docs/` 或仓库根。
- **`docs/` 是设计文档层**：方法论、需求分析、演进计划在此维护。`docs/guide/templates/`（设计层模板）与 `agent-iteration/assets/templates/`（实现层模板）的双份关系待裁决，见 `docs/plan.md` P-3。
- **交付单元是 `agent-iteration/` 目录**：发布或安装 skill 时只取该目录，仓库根与 `docs/` 不随 skill 分发。

## 3. 版本管理（自举）

本仓库按 agent-iteration skill 自身教的方法迭代：

- **tag 是权威版本源**；`agent-iteration/SKILL.md` frontmatter 的 `version` 字段是 tag 的对外投影——skill 被安装或复制后脱离 git 也能自报版本。发布时原子化动作四件：打 tag、追加 `CHANGELOG.md` 条目、归档检查、同步 frontmatter `version`。
- `CHANGELOG.md`：迭代任务条目用 `agent-iteration/assets/templates/06-changelog模板.md` 的完整字段；不开任务编号的文档类改动在当前版本条目下追加带日期的一行。
- 待办与讨论项：`docs/plan.md`；条目符合失败驱动迭代定义时转出为 `iterations/T-xxx` 按状态机执行。
