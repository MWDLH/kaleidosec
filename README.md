# Kaleidosec

[English](README.en.md) | 简体中文

> **随视角变化，呈现无限安全图景。**
> *Every angle, a different path.*

Kaleidosec 是给 AI Agent 的**渗透测试决策模式**。它不提供扫描器、不编排工具、不生成 payload；
它注入的是一套决策协议——如何评估目标、如何取舍路径、如何用证据支撑每一步、何时收手。

名字取自万花筒：同一个目标，换一个身份、换一个入口、换一个视角，攻击面就是另一幅图景。
有经验的测试者不会只盯着一个角度，而是在多个视角之间切换，挑出最值得走的那条路。

Kaleidosec 以 Claude Code 插件的形式分发：一份常驻决策协议，加上两个生命周期 hook。
装好后，在渗透工作目录或明确信号下自动进入模式；不需要时完全不注入。它也可以作为普通 skill 单独使用。

---

## 为什么需要它

AI Agent 不缺漏洞知识。SQL 注入的分类、Kerberos 的认证流程、云 IAM 的提权路径，
它答得比多数人完整。它缺的是在真实、动态、信息不完整的现场里**持续做对取舍**：

- 现在掌握的证据支持哪条路？
- 哪一条价值最高、成本最低？
- 失败了应该改哪个变量，而不是换哪个工具？
- 拿到新权限之后，原来的攻击链怎么继续？

这些判断很难写进固定流程，因为它们取决于目标的形状、已有的证据和剩余的预算。
Kaleidosec 把这类判断整理成可以注入 Agent 的操作协议。

## 现场问题与对应机制

| 常见问题 | Kaleidosec 的机制 |
|---|---|
| 失败就换工具，不诊断原因 | 8 维失败分类（执行 / 环境 / 访问 / 可达性 / 方法 / 前置条件 / 假设 / 路径价值），每次只改一个变量 |
| 把扫描器输出当成结论 | 证据分级：事实 / 推断 / 假设 / 未知 / 已否定；指纹和 CVE 匹配不等于漏洞 |
| 换个攻击面就从头扫描 | 模块调用栈 + 父路径回传，跨域时携带身份、网络位置、证据和目标 |
| 在一条路径上无限深入 | 路径四态（活跃 / 深入 / 搁置 / 关闭），搁置必须带重激活条件 |
| 说不清为什么走这一步 | 每一步输出：当前判断 / 关键证据 / 未知项 / 为什么优先 / 失败后改什么 |

## 与自动化渗透工具的关系

自动化工具擅长**覆盖**：把已知的攻击面快速扫一遍，把重复劳动交给机器。
现场真正消耗时间的是**取舍**：先打哪、打多深、什么时候该停。

Kaleidosec 处理的是后者。它可以和现有的扫描器、利用框架、代理工具一起使用：
工具负责执行，它负责决定执行什么、以什么顺序执行、什么时候停止。

## 工作方式

Kaleidosec 把一次授权测试建模为一个持续更新的决策循环：

```text
定位当前位置 → 整理已有证据 → 排序候选路径
→ 执行一个有边界的动作 → 判读结果 → 更新状态 → 重新排序
```

循环里的三个关键点：

**分档判断。** 不按固定分类套目标，而是按五个维度评估：暴露面数量、身份与权限边界、
仍会改变路线的未知项、目标价值、可用预算。默认从最轻的一档开始，证据变化时升档，
连续没有收益时收口。

**证据纪律。** 事实、推断、假设、未知、已否定分开记录。每一步动作都绑定已确认的事实，
不因为"手上有这个工具"就动手。

**主动止损。** 每条路径都有成本与收益的权衡。收益不再支撑成本时搁置路径并写明重激活条件，
而不是机械地把工具跑完。

## 设计原则

Kaleidosec 把决策分成三层，各归各管：

| 层 | 内容 | 谁决定 |
|---|---|---|
| **L0 硬边界** | 高危操作的人工确认、协议是否注入、基础盘必须执行、只加锁不放宽 | 规则，不可协商 |
| **L1 判断** | 目标复杂度、走哪条路、升档降档、止损、深挖深度 | 模型，动态判断 |
| **L2 留痕** | 每一步的判断、下一步、失败后改什么；档位写入状态 | 强制记录 |

一句话：规则管"能不能、进不进、做不做"，模型管"走哪、多深、何时停"。

## 覆盖范围

**8 个攻击面、6 个通用能力。** 卡片按证据按需加载，不做目录式的清单遍历。

| 攻击面 | 覆盖内容 |
|---|---|
| **Web/API** | SQL 注入、XSS、CSRF、SSRF、SSTI、反序列化、JWT、OAuth、GraphQL、竞态条件、文件上传、命令注入 |
| **移动端** | Android 组件、iOS 钥匙串与 ATS、WebView 攻击、深度链接、证书固定绕过、后端 API 测试 |
| **内网/AD** | Kerberos 攻击、ACL 滥用、AD CS、横向移动、凭据提取、LOLBin、域信任跳跃 |
| **云/容器** | AWS / Azure / GCP IAM 提权、元数据服务、K8s RBAC、容器逃逸、Serverless、存储暴露 |
| **AI 安全** | Prompt 注入、工具调用滥用、RAG 中毒、文件与 URL 处理、模型供应链 |
| **供应链** | CI/CD 管道攻击、OIDC 滥用、依赖混淆、Runner 劫持、IaC 分析、制品注册表 |
| **小程序** | wx.login 信任链、云函数授权、WebView 攻击、支付逻辑、平台身份 |
| **基础设施** | Redis / MongoDB / ES 未授权、VPN、默认凭据、厚客户端、网络设备 |

| 通用能力 | 覆盖内容 |
|---|---|
| **代码审计** | Java / PHP / Python / JS / Go / C# 六种语言的 Sink 清单，Source-to-Sink 数据流追踪与审计流程 |
| **逆向与协议** | 原生二进制、Java / .NET 反编译、Frida 运行时 Hook、自定义协议格式与状态机分析 |
| **PoC 开发** | 有边界的验证脚本、失败诊断与调试、按漏洞类型提供的模板与工具选择 |
| **身份与网络** | 凭据类型速查、隧道与跳板模式、网络位置建模与凭据优先级评估 |
| **防御规避** | AMSI / AppLocker / LSA Protection 诊断、EDR 行为理解与受控环境适配 |
| **业务逻辑** | 状态机滥用、工作流绕过、语义约束违反、激励滥用、跨平台逻辑漏洞分析 |

## 安装

### 前置条件（hook 方式需要）

插件通过两个 hook 调用本地 Python 脚本，需要 **Python 3.8+**，并以 `python` 这个名字可用
（Windows 安装时勾选 "Add python.exe to PATH"）。

macOS 12.3+ 和多数 Linux 发行版默认只有 `python3`，hook 会报 `python: command not found`。
三选一：创建别名 `sudo ln -sf "$(command -v python3)" /usr/local/bin/python`；
改用手动 hook 并把命令换成 `python3`；或只作为普通 skill 使用（不需要 Python）。

### Claude Code（推荐：插件，自动进入模式）

```
/plugin marketplace add MWDLH/kaleidosec
/plugin install kaleidosec --marketplace MWDLH/kaleidosec
```

旧版 Claude Code（早于 2.1.275）分两步：

```
/plugin marketplace add MWDLH/kaleidosec
/plugin install kaleidosec@kaleidosec
```

装完**新开会话**生效。之后在带有哨兵的目录或命中强信号时自动进入模式；
其他任务不注入协议，仅在会话启动时输出一行约 70 token 的进入提示。

不安装插件时，可用 [`examples/claude-hook/`](examples/claude-hook/) 手动接入 hook。

### 普通 skill 方式（不做自动注入）

```bash
git clone https://github.com/MWDLH/kaleidosec.git \
  ~/.claude/skills/kaleidosec
```

**Codex** — 复制或克隆到 Codex skills 目录（项目级 `.agents/skills/`，用户级 `~/.agents/skills/`）：

```bash
git clone https://github.com/MWDLH/kaleidosec.git \
  .agents/skills/kaleidosec
```

安装后重启客户端。保持目录完整，内部路由依赖相对路径。

## 进入模式

在 engagement 目录放置哨兵 `.kaleidosec`（旧版 `.pfo_active` 仍被识别）：

```json
{"engagement_id":"acme-01","objective":"判断低权账户能否到域控","tier":"quick"}
```

可选第 4 个字段 `scope_root` 限定作用范围，兄弟目录不会继承：

```json
{"engagement_id":"acme-01","objective":"…","tier":"standard","scope_root":"."}
```

## 使用示例

```
使用 $kaleidosec。

目标：判断这个低权限域账户能否到达有实际危害的安全结果。
范围：lab.example.internal 及以下 12 台主机。
授权：L0-L2 已预授权；禁止持久化操作。
当前访问：VPN、一个普通域用户。
已有证据：[主机信息、服务扫描、身份枚举结果]

从证据最充分、价值最高的路径继续。
```

中断恢复：提供匹配的 `.pentest_session.json`，Agent 从父路径精确恢复，而不是重新开始。

## 宿主支持

| 宿主 | 加载方式 | 确定性 |
|---|---|---|
| Claude Code（插件） | `hooks/` 自动注入 + skill | **高**：哨兵或强关键词自动进入 |
| Claude Code（手动 hook） | `examples/claude-hook/settings.json` | **高**：同上 |
| Claude Code（普通 skill） | 复制到 `~/.claude/skills/` | 低：按 description 语义调用 |
| Codex | `.agents/skills/` | 低：按 description 语义调用 |
| dsh | 待适配 | — |

"确定性"指不依赖模型临场想起；低确定性宿主仍需手动点名或显式调用。

## 项目结构

```text
kaleidosec/
|-- SKILL.md                    ← 唯一常驻协议（注入源，只此一份）
|-- .claude-plugin/             ← 插件清单 + marketplace
|-- hooks/                      ← hooks.json + kaleido_gate.py（确定性注入）
|-- skills/kaleidosec/          ← 插件 skill 薄入口（指向根协议）
|-- modes/                      ← STANDARD / DEEP 按需卡片
|-- references/                 ← 14 个领域与能力目录，每个都有路由入口
|-- scripts/                    ← 状态管理 + 预算/同步校验
|-- examples/claude-hook/       ← 不装插件时的手动 hook 兜底
|-- agents/openai.yaml          ← Codex 接口定义
|-- README.md / README.en.md
|-- CHANGELOG.md / CONTRIBUTING.md / SECURITY.md / LICENSE
```

## 从 v1 升级

Kaleidosec 2.0 由 1.1 的 `pentest-field-operator` skill 升级而来，属于结构性变更：

- 名称统一为 `kaleidosec`，安装方式改为插件（两条命令）
- 常驻协议从约 3.5k token 压缩到约 1.4k
- 分档由静态分类改为判断框架，新增确定性注入与状态动词
- 旧哨兵 `.pfo_active`、旧环境变量 `PFO_FORCE`、旧 `CLAUDE.md` 托管块仍被识别

详见 [CHANGELOG.md](CHANGELOG.md)。

## 授权与免责声明

Kaleidosec 仅用于**获得明确授权的**安全测试、红队演练和攻防评估。

- 使用者必须确保对目标拥有合法授权，并遵守所在地法律法规与授权范围。
- 本项目不授予任何测试权限，也不对使用者的行为或后果承担责任。
- 不得用于未授权的系统、网络、账号或数据。
- 工具本身不执行攻击动作；执行由使用者选择的 Agent 与外部工具完成，责任由使用者承担。
- 不得在报告或提交中保留未经脱敏的客户数据、凭据、证据或目标信息。
- 未测试的攻击面不应被声称为已完成；工具的输出不替代专业工程师的判断与法律授权。

## 贡献

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。禁止提交真实目标数据、凭据或客户证据。

## 许可证

[MIT](LICENSE)
