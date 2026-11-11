# wisp-drug 基座：在 wisp-science 上魔改

wisp-drug 的基座是 `wisp-science` 的产品分支。技术栈保持 Rust、Tauri 2 和 Leptos。不换 GPUI，不重写 Agent 循环、SQLite 和 Run。

上游钉在公开仓库 `xuzhougeng/wisp-science` 的 `9a25a830`（2026-11-11）。私有副本 `Yu-Qiao-sjtu/wisp-science` 已经和这条 `main` 分叉，不作为魔改起点。

许可证跟随上游 AGPL-3.0-only。对外发行的 wisp-drug 程序按 AGPL 提供对应源码。`target-evaluation` 正文仍可标 Apache-2.0，打进安装包之后整包以 AGPL 为准。

## 仓库怎么摆

这个仓库就是产品分支。`origin` 是 `Yu-Qiao-sjtu/wisp-drug`，`upstream` 是 `xuzhougeng/wisp-science` 且禁止推送。`skills/target-evaluation` 放在本仓库的 `skills/` 里，和上游技能一起打包。

产品分支只长期保留下面三类差异。其余提交跟上游合并，冲突就说明改出了引擎边界。

| 差异 | 落点 | v0 做什么 |
|---|---|---|
| 产品身份 | `src-tauri/tauri.conf.json` 的 `productName`、`identifier`；窗口标题和关于页 | `wisp-drug`，标识 `science.wisp-drug`。更新源先关掉，避免装到 wisp-science 的发布通道 |
| 捆绑技能 | `skills/`，安装包已通过 `tauri.conf.json` 的 `../skills/` 资源带上 | 加入 `target-evaluation`。基座原有技能保留，包括 `indication-dossier` |
| 技能词表 | `crates/wisp-skills/src/manifest.rs` 的 `DOMAINS` | 增加 `drug-discovery`。解析器现在会拒绝未知领域，所以药物技能要能写进 `wisp.domains` |

这三处是 v0 的全部引擎改动。

## 先不改的部分

这些能力直接沿用上游实现：

- Agent 循环、`use_skill`、子代理和 Workflow Studio
- ExecutionContext、`run_in_context`、SSH / Slurm
- MCP、Python/R 内核、项目库和证据胶囊
- Tauri / Leptos 界面，以及 macOS、Windows 的原生壳

`loads` 仍然不是运行时字段。基座不会因为 frontmatter 自动调用 `use_skill`。v0 继续把加载步骤写在 `SKILL.md` 正文里。等一条真实技能证明手写步骤不够用，再改 `wisp-skills` 的加载逻辑，并单独评审。

对接、结构预测和分子动力学不进基座。它们是以后的 Run 技能，程序和权重留在执行主机上。

## 实施顺序

1. 从 `9a25a830` 建产品分支，加 `upstream` 远程。
2. 改产品名、标识，并关闭对 `xuzhougeng/wisp-science` 的更新检查。
3. 把 `target-evaluation` 放进 `skills/`，给它的 `wisp.domains` 加上 `drug-discovery`。
4. 在 `manifest.rs` 的领域表和对应测试里接受这个新词。
5. 用本仓 `python tools/validate_skills.py` 检查技能包；引擎测试按改动的解析器单独补。

之后每次同步上游，只解决这三类差异上的冲突。Agent、界面和 Run 的上游修复原样进入 wisp-drug。
