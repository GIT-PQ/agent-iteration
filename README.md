# agent-iteration 项目

本仓库同时承载 skill 产物与它的设计文档，两层分开管理、各有职责。

## 1. 目录宏观图

```mermaid
flowchart LR
    subgraph repo["本仓库"]
        direction TB
        subgraph prod["agent-iteration/ —— skill 产物（纯净，交付单元）"]
            P1["SKILL.md<br/>references/（六状态行为规约）<br/>assets/templates/（9 份填写模板）<br/>scripts/state_check.py"]
        end
        subgraph design["docs/ —— 设计文档层（不随 skill 分发）"]
            D1["guide/《Agent迭代指南》v2<br/>+ 设计层模板副本"]
            D2["plan.md 演进计划"]
            D3["requirements-analysis/ 需求分析"]
        end
        M["README.md · CHANGELOG.md<br/>仓库级管理文件"]
    end
    subgraph target["工件仓库（被迭代的 agent/skill）"]
        T1["iterations/T-xxx/（01-05 留痕）"]
        T2["evals/ · results/{eval_id}/{version}/"]
        T3["工件自己的 CHANGELOG.md"]
    end
    prod ==|"skill 按状态机迭代工件<br/>运行时产物全部写入工件仓库"| target
```

## 2. 归属规则

| 文件类别 | 归属 | 规则 |
|---|---|---|
| skill 运行所需（SKILL.md、references/、assets/、scripts/） | `agent-iteration/` | 唯一交付单元，保持纯净，不写入管理类内容 |
| 方法论、需求分析、演进计划 | `docs/` | 设计层，不进入 skill 运行时 |
| 仓库级说明与版本索引 | 仓库根 | README.md、CHANGELOG.md |
| 迭代留痕、eval、基线、工件 changelog | 工件仓库 | `iterations/`、`evals/`、`results/`、工件自己的 `CHANGELOG.md`——工件自含全部迭代历史 |
| vault（Obsidian 知识库） | 不参与 | 只是文档阅读场所，不是存储层，任何迭代产物不写入 |

## 3. 结构规则

- **`agent-iteration/` 是 skill 产物，保持纯净**：只写入 skill 运行所需的文件；项目管理类内容（仓库级目录说明、维护约定、跨层指针）一律不写入，放 `docs/` 或仓库根。
- **`docs/` 是设计文档层**：方法论、需求分析、演进计划在此维护。
- **模板双份同步**：`agent-iteration/assets/templates/` 为运行时**权威版本**，`docs/guide/templates/` 为设计层副本；模板变更落在 assets 后同步复制到 docs 侧，以 assets 为准。
- **交付单元是 `agent-iteration/` 目录**：发布或安装 skill 时只取该目录，仓库根与 `docs/` 不随 skill 分发。

## 4. 版本管理（自举）

本仓库按 agent-iteration skill 自身教的方法迭代：

- **tag 是权威版本源**；`agent-iteration/SKILL.md` frontmatter 的 `version` 字段是 tag 的对外投影——skill 被安装或复制后脱离 git 也能自报版本。发布时原子化动作四件：打 tag、追加 `CHANGELOG.md` 条目、归档检查、同步 frontmatter `version`。
- `CHANGELOG.md`：迭代任务条目用 `agent-iteration/assets/templates/06-changelog模板.md` 的完整字段；不开任务编号的文档类改动在当前版本条目下追加带日期的一行。
- 待办与讨论项：`docs/plan.md`；条目符合失败驱动迭代定义时转出为 `iterations/T-xxx` 按状态机执行。
