# eval 模板 v1

> **使用方式**：测试准备阶段（3.3）为每个失败案例/回归项在 `evals/` 下新建一个 JSON 文件，文件名即 `{eval-id}.json`，测试输入放 `evals/files/`。
>
> **业务无关性**：eval 是跨任务资产，不含任何真实业务信息（公司名、批号、项目名、业务结论）——脱敏对照存于任务目录的 03-测试准备.md。
>
> **溯源**：`task` 与 `criteria` 字段建立双向索引——02-验收标准的「对应 eval」列回填本文件的 id，本文件用 `criteria` 指回标准编号。

## 落盘骨架（复制为 evals/{eval-id}.json 后填写）

```json
{
  "id": "stable-test-id",
  "task": "T-001",
  "criteria": ["S1"],
  "prompt": "真实但去业务化的用户请求",
  "expected_output": "人可理解的成功标准",
  "files": ["evals/files/input.ext"],
  "assertions": [
    "输出文件可打开",
    "关键字段仅出现一次",
    "禁止内容不存在"
  ]
}
```
