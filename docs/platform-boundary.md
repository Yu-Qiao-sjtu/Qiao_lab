# wisp-drug 与 wisp-science 的边界

结论：在完整的 wisp-science 上做产品分支。魔改限于产品身份、捆绑药物技能和 `drug-discovery` 领域词。Agent、界面和 Run 保持上游实现。具体文件和顺序见 [base-fork.md](base-fork.md)。

## 魔改边界

药物研发要用的项目、会话、技能加载、审批、子代理、远程 Run 仍是上游那套控制平面。拆出 Agent 循环或界面之后，上游修复就进不来。v0 从公开 `9a25a830` 拉产品分支，只保留三类长期差异。

基座版本钉在公开 `main` 的 `9a25a830`（2026-11-11）。私有副本 `Yu-Qiao-sjtu/wisp-science` 不作为魔改起点。程序许可证跟随 AGPL-3.0-only。

## 基座原样调用

这些能力已经在引擎里，药物技能用文档和工具名引用它们。产品分支不复制第二份实现。

| 能力 | 基座位置 | 药物平台里的用法 |
|---|---|---|
| 技能发现与加载 | `search_skills`、`use_skill`；`docs/skills.md`、`docs/skill-authoring.md` | 捆绑进产品分支的 `skills/` 后由 Agent 加载 |
| 技能资源目录 | `references/`、`scripts/`、`assets/`；可选 `wisp:` 元数据 | 深文档按需阅读；脚本由 Agent 显式调用 |
| 适应症档案 | `skills/indication-dossier` | 靶点评估的疾病与试验背景 |
| 公共数据 | `skills/public-data-access` | GEO、SRA、TCGA/GDC、GTEx、DepMap 的获取计划 |
| 可复现分析模块 | `skills/analysis-workflow` | 多步骤计算的目录、参数和版本记录 |
| 远程与集群 | `skills/remote-compute-ssh`；ExecutionContext | 对接、预测、动力学走 SSH / Slurm Run |
| Run 记录 | `run_in_context`；`docs/run-cards.md` | 长计算留在 Run 账本，不拉长 shell 超时 |
| 子代理与工作流 | `docs/agent-delegation.md` | 多证据线并行；依赖写在工作流的 `depends_on` |
| 文献与数据库 | 随基座分发的 MCP | 靶点和变异证据的检索 |

`use_skill` 只载入该技能的入口说明和资源位置。它不会读取自定义的 `dependsOn`，也不会按 frontmatter 把任务送到某台 GPU。前置技能要在 `SKILL.md` 里写成明确的加载步骤。主机选择写执行上下文，例如 `ssh:<alias>`。

产品分支已经在 `crates/wisp-skills/src/manifest.rs` 接受 `drug-discovery`。`target-evaluation` 的 `wisp.domains` 使用 `drug-discovery` 和 `scientific-literature`。

## 本仓负责

1. `skills/target-evaluation` 已落地。它加载基座的 `indication-dossier`，产出带来源的 advance / hold / stop，不搬运外部技能原文。
2. 本仓契约：`SKILL.md` 不超过 300 行；`references/` 有索引；带 `scripts/` 的技能提供 `samples/input.json`；技能之间的前置关系在正文里写清，并由校验器检查目标存在且无环。
3. 校验脚本和 CI。基座的 `quick_validate.py` 仍负责通用包结构，本仓校验器只加药物套件的额外规则。

## 明确留在各自仓库

- DepMap 查询服务留在 `wisp-science-depmap`。靶点评估需要时调用它，不把 DepMap 做成平台本体。
- 单细胞、通用办公和通用生信包装留在基座或社区技能商店。
- 结构预测、对接、分子动力学的程序和权重不进产品分支。技能只写输入、Run 命令、输出文件和校验和。
