# wisp-drug 技能契约 v0.1

本契约只约束本仓库的 `skills/`。基座的 `quick_validate.py` 仍检查通用技能包。校验命令：

```text
python tools/validate_skills.py
```

## 目录

```text
skills/<skill-name>/
├── SKILL.md
├── references/
├── scripts/          # 可省略；一旦存在就必须有 samples/input.json
└── samples/
    └── input.json
```

## 入口

`SKILL.md` 使用 YAML frontmatter。`name` 与目录名一致，并包含 `description` 和 `license`。全文不超过 300 行。

`loads` 列出要先调用 `use_skill` 的基座技能。这些名字不必出现在本仓库。正文必须写出同样的加载步骤，因为基座不会自动预加载 `loads`。

`requires` 只指向本仓库里的其他技能。校验器确认目标存在，并拒绝循环。空列表表示没有本仓前置技能。

可选的 `wisp:` 块只使用基座已经接受的词表。

## 资源

`SKILL.md` 用相对链接指向 `references/` 下的文件，并在索引表里说明何时阅读。链接指向的文件必须存在。`references/` 里未被链接的文件产生警告。

带 `scripts/` 的技能提交 `samples/input.json`，且内容是 JSON 对象。样例不访问网络。

## 级别

| 检查 | 级别 |
|---|---|
| `SKILL.md` 存在，frontmatter 可解析，`name` 与目录一致 | error |
| `description`、`license` 非空 | error |
| `requires` 指向本仓技能且无环 | error |
| `loads` 中的每个名字出现在正文里 | error |
| `SKILL.md` 不超过 300 行 | error |
| `references/` 链接存在 | error |
| 未被链接的 reference | warning |
| 有脚本时 `samples/input.json` 是 JSON 对象 | error |
