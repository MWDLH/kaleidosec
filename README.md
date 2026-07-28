# Pentest Field Operator

[English Documentation](README.en.md) | 简体中文

**让 AI Agent 像高级渗透测试工程师一样思考和工作——基于证据决策，而不是机械执行工具清单。**

<br>

AI Agent 不缺漏洞知识。你问它 SQL 注入分类、Kerberos 认证流程、AWS 提权路径，它能答得比大多数工程师都好。

但它缺一件事：在真实的、动态的、信息不完整的现场，持续做出正确决策的能力。

Pentest Field Operator 就是为此而生的。它不教 Agent 工具怎么用，它教 Agent 怎么思考：

- 我有什么证据？缺什么信息？
- 哪条路价值最大？
- 失败了改哪个变量，而不是换哪个工具？
- 拿到新权限后，怎么继续原来的攻击链？

本质上，它给 Agent 装上了一套渗透测试的实战操作系统。

---

## 解决了什么问题

| 通用 Agent 的常见问题 | Pentest Field Operator 如何解决 |
|---|---|
| :repeat: **工具循环** — 失败就换工具，不诊断原因 | 8 维失败分类（执行/环境/访问/可达性/方法/前置条件/假设/路径价值），每次只改一个变量 |
| :newspaper: **告警即漏洞** — 把扫描器输出当结论 | 证据分级（事实/推断/假设/未知/已否定），指纹和 CVE 匹配不等于漏洞 |
| :dizzy_face: **跨域失忆** — 换个攻击面就从头开始 | 模块调用栈 + 父路径回传协议，跨域携带身份、网络位置、证据和目标 |
| :tunnel: **隧道视野** — 在一条路径上无限深入 | 路径四态管理（活跃/深入/搁置/关闭），搁置必带重激活条件 |
| :shrug: **决策黑盒** — 说不出为什么选这一步 | 每一步必须输出：当前判断、关键证据、未知项、为什么这一步优先、失败后怎么办 |

---

## 30 秒搞懂它是怎么工作的

Skill 把渗透测试变成了一个**永远不会丢失上下文的决策循环**：

```
我在哪？ → 我知道什么？ → 最好的路径是什么？
→ 执行一个有边界的动作 → 结果意味着什么？
→ 什么能力发生了变化？ → 回到第一步
```

靠的是四个其他 Skill 没有的核心机制：

:compass: **证据驱动决策** — 每一步行动都必须绑定已确认的事实。"我准备做 X，因为观察到了 Y，而未知项 Z 可能改变路线。"不会因为"有这个工具"就动手。

:fork_and_knife: **攻击路径管理** — 路径被持续跟踪、排序、深入、搁置或关闭。既不会浅尝辄止，也不会钻牛角尖。每条被搁置的路径都有重激活条件，不会丢失。

:link: **跨域上下文保持** — 当你从 Web 打到内网再打到云 IAM 时，Agent 带着身份、网络位置、证据和父层目标一起走。不会换个攻击面就从头开始扫描。

:shield: **实战安全分级** — 动作按实际影响（L0-L3）分类，不按工具名称分类。常规操作流畅执行不打断；持久化、信任修改、控制面变更必须有明确的真人批准。

---

## 实战案例

```
运维人员："我有一个普通域用户账号，能打到域控吗？"

Agent [加载 Skill 后]：
  1. 确认位置：whoami、组、网卡、域控制器
  2. 收集信息：枚举 SPN → 发现 MSSQLSvc 服务账户
  3. 决策：Kerberoast 这个账户（低噪声、高信息收益）
  4. 执行：GetUserSPNs → 离线破解 → 拿到明文密码
  5. 验证：crackmapexec → SQL-01 本地管理员
  6. 横移：WMIExec 到 SQL-01 → 发现指向 DC 的链接服务器
  7. 证明影响：通过链接服务器在 DC 上执行命令 → 域管理员确认
  8. 清理：删除测试账户、记录攻击链、保存现场状态
```

每一步都是因为证据支撑才选的，不是清单驱动的。每次如果失败，诊断会精准落位——凭据问题、网络可达性问题、还是 EDR 拦截——而不是换个工具再来一遍。

---

## 覆盖范围

**8 个攻击面、5 个通用能力。** 卡片按证据按需加载，Agent 不会把目录当清单遍历。

| 攻击面 | 覆盖内容 |
|---|---|
| :globe_with_meridians: **Web/API** | SQL注入、XSS、CSRF、SSRF、SSTI、反序列化、JWT、OAuth、GraphQL、竞态条件、文件上传、命令注入 |
| :iphone: **移动端** | Android 组件、iOS 钥匙串与 ATS、WebView 攻击、深度链接、证书固定绕过、后端 API 测试 |
| :busts_in_silhouette: **内网/AD** | Kerberos 攻击、ACL 滥用、AD CS、横向移动、凭据提取、LOLBin、域信任跳跃 |
| :cloud: **云/容器** | AWS/Azure/GCP IAM 提权、元数据服务、K8s RBAC、容器逃逸、Serverless、存储暴露 |
| :robot: **AI 安全** | Prompt 注入、工具调用滥用、RAG 中毒、文件与 URL 处理、模型供应链 |
| :package: **供应链** | CI/CD 管道攻击、OIDC 滥用、依赖混淆、Runner 劫持、IaC 分析、制品注册表 |
| :satellite: **小程序** | wx.login 信任链、云函数授权、WebView 攻击、支付逻辑、平台身份 |
| :desktop_computer: **基础设施** | Redis/MongoDB/ES 未授权、VPN、默认凭据、厚客户端、网络设备 |

| 通用能力 | 覆盖内容 |
|---|---|
| :microscope: **代码审计** | Java/PHP/Python/JS/Go/C# Sink 清单，Source-to-Sink 数据流分析 |
| :wrench: **逆向与协议** | 原生二进制、Java/.NET 反编译、Frida 运行时 Hook、自定义协议分析 |
| :test_tube: **PoC 开发** | 有边界的漏洞验证、失败调试、工具工程、PoC 代码模板 |
| :bust_in_silhouette: **身份与网络** | 凭据类型速查、隧道与跳板、网络位置建模、凭据优先级评估 |
| :shield: **防御规避** | AMSI/AppLocker/LSA Protection 诊断与绕过、EDR 行为检测理解 |

---

## 安装

**Claude Code** — 复制或克隆到用户 skills 目录：

```bash
git clone https://github.com/MWDLH/pentest-field-operator.git \
  ~/.claude/skills/pentest-field-operator
```

**Codex** — 复制或克隆到 Codex skills 目录：

```bash
git clone https://github.com/MWDLH/pentest-field-operator.git \
  $CODEX_HOME/skills/pentest-field-operator
```

或手动复制到 `~/.codex/skills/pentest-field-operator`。

安装后重启客户端。必须保持目录完整，内部路由依赖相对路径。

## 使用方式

```
使用 $pentest-field-operator。

目标：判断这个低权限域账户能否到达有实际危害的安全结果。
范围：lab.example.internal 及以下 12 台主机。
授权：L0-L2 已预授权；禁止持久化操作。
当前访问：VPN、一个普通域用户。
已有证据：[附上主机信息、服务扫描、身份枚举结果]

从证据最充分、价值最高的路径继续。
```

中断恢复：提供匹配的 `.pentest_session.json`，Agent 会从父路径精确恢复而非重新开始。

---

## 项目结构

```text
pentest-field-operator/
|-- SKILL.md              ← 核心操作规则、安全门控、决策合同
|-- agents/openai.yaml    ← Codex 接口定义
|-- scripts/              ← 状态管理脚本 (Python 3.9+)
|-- references/           ← 13 个领域与能力目录，每个都有路由入口
|-- README.md / README.en.md
|-- CONTRIBUTING.md / SECURITY.md / LICENSE
```

---

## 设计边界

- :white_check_mark: 仅用于合法授权的安全测试
- :white_check_mark: 不假设工具已安装——先检查可用性
- :white_check_mark: 不存储真实密码、令牌或私钥
- :white_check_mark: 未测试的攻击面不会被声称为已完成
- :white_check_mark: 不代替专业工程师判断和法律授权

---

## 贡献

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。禁止提交真实目标数据、凭据或客户证据。

## 许可证

[MIT](LICENSE)
