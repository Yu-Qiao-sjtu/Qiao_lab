# wisp-drug

下一代药物研发平台。本地优先，证据可回溯。

一个药物项目放在同一工作台里：靶点是否值得做、适应症里的患者是谁、证据从哪篇文献来、重计算跑在哪台机器上。界面沿用 wisp-science 的桌面壳（Rust、Tauri、Leptos）。wisp-drug 改的是产品身份和药物技能，不另做一套窗口框架。

引擎上游是 [wisp-science](https://github.com/xuzhougeng/wisp-science)。本仓库是产品分支：[Yu-Qiao-sjtu/Qiao_lab](https://github.com/Yu-Qiao-sjtu/Qiao_lab)。

## 界面

打开应用后是一条项目里的研究对话，旁边可以预览项目文件。药物工作都落在这四个面上。

| 界面 | 药物研发里做什么 |
|---|---|
| 项目 | 一个项目对应一条研发线，例如一个靶点加一个适应症。文件、对话和 Run 都留在这个目录 |
| 对话 | 用自然语言提出问题。`/` 加载技能，`@` 附上结构文件、表格或已有报告。批准卡默认开着 |
| 文件预览 | 打开评估报告、适应症档案和 JSON 证据。Markdown、PDF、表格和图片沿用基座预览 |
| Runs | 对接、预测、动力学走这里。命令、日志和退出状态留在 Run 记录里，不靠把对话超时拉长 |
| 设置 | 自备模型；在 Skills 里确认 `target-evaluation`；在执行上下文里登记本机、WSL 或 SSH 主机 |

密钥留在操作系统钥匙串，不写入项目数据库。

## 第一条工作流：靶点评估

在项目对话里加载 `target-evaluation`。它回答一个问题：这个靶点在这个适应症里应该 **advance**、**hold** 还是 **stop**。

1. 先确认靶点和适应症身份。身份没对齐之前，不展开检索。
2. 疾病背景加载基座技能 `indication-dossier`：患者人群、标准治疗和关键试验。wisp-drug 不重写这份档案。
3. 四条证据线分别写入项目文件：人类遗传与临床、适应症内机制、所述模态是否可做、安全性与临床竞争。
4. 报告里的数字、分期和竞品名称必须带原始链接。没有来源就标成证据不足，不升成支持。
5. 结构预测、对接和分子动力学不在这个技能里。需要时另开 Run，程序和权重留在执行主机上。

技能说明在 `skills/target-evaluation/SKILL.md`。示例输入是 `skills/target-evaluation/samples/input.json`。

## 现在有的，和还没有的

现在可以使用的是基座窗口加上捆绑技能 `target-evaluation`。领域词 `drug-discovery` 已写入技能目录。

下面这些还不是单独的界面，不要在 README 或演示里当成已完成功能：

- 靶点决策卡片（把 advance / hold / stop 固定在对话之外）
- 四条证据线的对照视图
- 分子结构画布、对接姿态和轨迹播放
- wisp-drug 自己的安装包和更新通道

这些要做时，加在现有窗口上：决策进入项目文件和预览，计算进入 Runs。

## 从源码运行

安装包尚未发布。在本仓库按上游开发方式启动桌面壳：

```text
cargo tauri dev
```

模型在 **设置 → 模型** 里配置。技能随仓库的 `skills/` 一起打包，其中包含上游科研技能和 `target-evaluation`。

平台边界和魔改范围见 [docs/platform-boundary.md](docs/platform-boundary.md) 与 [docs/base-fork.md](docs/base-fork.md)。

## 许可证

程序跟随上游 [AGPL-3.0-only](LICENSE)。`target-evaluation` 的技能正文为 Apache-2.0；打进安装包之后，整包以 AGPL 为准。

引用 wisp-science 引擎时使用上游的 Zenodo 记录，不要把该 DOI 写成 wisp-drug 的版本号。
