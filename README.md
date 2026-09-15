# agent-iteration 项目

本仓库同时承载 skill 产物与它的设计文档，两层分开管理、各有职责。

## 1. 目录宏观图

```
本仓库
├── agent-iteration/                 skill 产物（纯净，交付单元）
│   ├── SKILL.md                     入口：状态机、启动流程、横切规范速查
│   ├── references/                  各状态行为规约（01-06 对应六状态）
│   ├── assets/
│   │   └── templates/               9 份填写模板（编号即状态）
│   └── scripts/
│       └── state_check.py           断点判定（中断重入时用）
├── docs/                            设计文档层（不随 skill 分发）
│   ├── guide/                       《Agent迭代指南》v2 + 设计层模板
│   ├── plan.md                      演进计划：上游 backlog
│   └── requirements-analysis/       需求分析报告
├── README.md                        仓库级说明
└── CHANGELOG.md                     版本视角索引

工件仓库（被迭代的 agent/skill 所在——skill 运行时产物全部写入此处）
├── <工件源码>                       （必须）git 管理：commit 检查点 / tag 定稿
├── iterations/                      （必须）
│   └── {任务编号}/                  01-05 按状态编号留痕
├── evals/                           （必须）稳定测试 id
├── results/                         （必须）
│   └── {eval_id}/{version}/         跨版本基线
└── CHANGELOG.md                     （必须）工件自己的版本视角索引
```

> 工件仓库中以上 5 项（工件源码、`iterations/`、`evals/`、`results/`、`CHANGELOG.md`）为必须存在的最小骨架；其余目录（`docs/`、`data/` 等）均为可选——按需再建，不预设空目录。

> **自举特例**：本仓库用 agent-iteration 迭代它自己时，「本仓库」与「工件仓库」是同一个目录——`iterations/`、`evals/`、`results/` 直接落在本仓库根，与 `agent-iteration/`、`docs/` 并列。

## 2. 归属规则

| 文件类别 | 归属 | 规则 |
|---|---|---|
| skill 运行所需（SKILL.md、references/、assets/、scripts/） | `agent-iteration/` | 唯一交付单元，保持纯净，不写入管理类内容 |
| 方法论、需求分析、演进计划 | `docs/` | 设计层，不进入 skill 运行时 |
| 仓库级说明与版本索引 | 仓库根 | README.md、CHANGELOG.md |
| 迭代留痕、eval、基线、工件 changelog | 工件仓库 | `iterations/`、`evals/`、`results/`、工件自己的 `CHANGELOG.md`——工件自含全部迭代历史 |
| vault（Obsidian 知识库） | 不参与 | 只是文档阅读场所，不是存储层，任何迭代产物不写入 |

## 3. 结构规则

1. **指南与 skill 互不引用**：`docs/guide/`（指南）与 `agent-iteration/`（skill 产物）是两个独立体系——指南不指向 `agent-iteration/` 下的文件或路径，SKILL.md 及 references 等 skill 文件也不指向 `docs/` 下的文件或路径。两者各自内部自洽，不互相指认。
2. **skill 产物保持纯净**：`agent-iteration/` 只写入 skill 运行所需的文件；项目管理类内容（仓库说明、维护约定、跨层路径）一律不写入，放 `docs/` 或仓库根。
3. **模板允许差异**：`docs/guide/templates/` 与 `agent-iteration/assets/templates/` 不是主从同步关系——它们各自服务于所在目录的上下文（设计层 / 运行层），开头使用说明存在差异是预期、不做一致性同步，但模版内容应保持一致。
4. **路径分层**：规则文件（如本 README）可使用仓库相对路径；指南与 skill 内的正文及模板必须使用各自上下文的相对路径，不得出现仓库级路径（如 `agent-iteration/…`、`../…`、`/Users/…`），否则在交付或复制场景下会失效。
5. **交付单元是 `agent-iteration/` 目录**：发布或安装 skill 时只取该目录，仓库根与 `docs/` 不随 skill 分发。

## 4. 版本管理（自举）

本仓库按 agent-iteration skill 自身教的方法迭代：

- **tag 是权威版本源**；`agent-iteration/SKILL.md` frontmatter 的 `version` 字段是 tag 的对外投影——skill 被安装或复制后脱离 git 也能自报版本。发布时原子化动作四件：打 tag、追加 `CHANGELOG.md` 条目、归档检查、同步 frontmatter `version`。
- `CHANGELOG.md`：迭代任务条目用 `agent-iteration/assets/templates/06-changelog模板.md` 的完整字段；不开任务编号的文档类改动在当前版本条目下追加带日期的一行。
- 待办与讨论项：`docs/plan.md`；条目符合失败驱动迭代定义时转出为 `iterations/T-xxx` 按状态机执行。
