# Stage 0 落地页 · 捕获管道说明（PLUMBING）

> 对象：每日经文会员落地页（Space：`mei-ri-jing-wen-hui-yuan-gospel-wisdom`，挂在 Gospel Wisdom 目标 goal_d01bfe78caf9 下）。
> 原则：零新增支出、不新开任何外部账户；Stage 0 只做到「能登记、能追踪」，不收真实款项。

---

## 今天就能用的（已落地）

| 环节 | 状态 | 说明 |
|---|---|---|
| 落地页 | ✅ 已建 | 全栈 Space（`web_fullstack`）：报价页（简体中文先行＋英文）、免费试读 7 天卷为首要报价、$7.99/月会员说明、状态行「創始會員登記中 — 正式開通時第一時間通知你」 |
| 邮箱捕获 | ✅ 能用 | 页面表单把登记写入 **Space 自身的数据存储**（经页面发布的登记 action 落库），不是 mailto 凑数；因此 **mailto 备用方案不需要** |
| 登记分类 | ✅ 按设计 | 每条登记带类型旗标：**購買意向**（$7.99 购买意向 CTA）、**免費訂閱**、**認領獻詞**（「认领一天 · 献词位」免费意向登记：邮箱＋认领日期＋献给对象＋献词短句）三类分开存、分开计，与台账规则一致；献词模块文案明示：刊出与否取决于篇目编成与项目推进，不承诺出版 |
| 来源追踪 | ✅ 已落地（链接携带式） | 平台支持：每条登记记录都带**来源**——落地链接可用 `?source=` 参数预填（如 `?source=youtube-<视频代号>`），访客也可在表单来源下拉自选。**人工兜底**：没带参数、访客也没选的登记，来源为空——抄录进台账时按投放批次补记，补不出的在台账标「来源未记录」，不猜 |
| 页面形态 | ⚠️ 一处如实注记 | 成品是**一条长页滚动**（品牌头＋试读区＋会员区＋「先说清楚」＋献词区），不是字面「一屏」：双表单＋明示条款塞不进单个视口；内容仍聚焦一页、无分页无外链跳转 |
| 名单读取 | ✅ 能用 | 团队经页面 action 回读：`listSignups`（邮箱/intent/来源/时间）、`listDedications`（邮箱/认领日子/献给谁/献词/来源/时间）、`getSignupStats`（三类分开计数），再人工抄入 `tracking-ledger.md`。生产库经实测为空（purchase 0 / free 0 / dedications 0，2026-11-07 建后核验）——构建期的端到端测试只跑在沙盒库，生产从零开始、无假数据 |
| 追踪台账 | ✅ 已建 | `~/workspace/goals/365/files/stage0-offer/tracking-ledger.md`，基线已填（付款 = 0） |
| 对外公开页 | ✅ 已上线（2026-11-07） | Space 本身没有公开 URL，故另建一页静态公开页作为对外门面（同一报价、同一诚实状态、无付款按钮）：**https://king818.github.io/daddymi-publications/gospel-wisdom/**（`king818/daddymi-publications` 仓 `gospel-wisdom/index.html`，commit `9688d65`，2026-11-07 上线后实测 HTTP 200、双表单链接齐全） |

## 今天还不能的（诚实边界）

- **没有自动同步 Space 登记到表格**：Space 内的登记先落在 Space 存储里，靠团队定期读取抄入台账。公开页的捕获改走 Google Form（见下「选项 A — 已完成」），答复自动汇入绑定 Sheet，与 Space 存储是两路上账，抄台账时两边都读、去重。
- **没有收款**：页面没有任何能成交的付款按钮（有意为之）；Stage 1 须 boss 另行裁示。

## 还差什么才能接通（form → sheet ＋ 对外分发）

两条零支出路线，任选一条即可让陌生人打开页面并自动汇入名单：

### 选项 A — Google Form（iching6 账号）✅ 已完成（2026-11-07）
- 两张表单已建并实测在线（iching6 账号），公开页 CTA 直链表单，答复自动汇入各自绑定的答复 Sheet：
  - **创始登记（购买意向 / 免费试读）**：https://docs.google.com/forms/d/e/1FAIpQLSfwqTcZwqPH-WPPqm6Pa_ZXQui9nSpIOPoYSq72XCWl3XsUKQ/viewform — 答复 Sheet：[Form Responses](https://docs.google.com/spreadsheets/d/1VzbxZzvLDlIEy-XecLdXPjr93ZmjAz-YCzTlEtRSnck/edit?usp=sharing)
  - **认领一天 · 献词**：https://docs.google.com/forms/d/e/1FAIpQLScFT9EpDscbmchwAK7KfE5aZNq5EXdl3floAWtiGYpVPyz__w/viewform — 答复 Sheet：[Form Responses](https://docs.google.com/spreadsheets/d/13HDAPvF2O2_rqxAP7XsYH104ALPUKTNbqGGXykih9Zo/edit?usp=sharing)
- **表单核实档案（2026-11-08 B-1/B-3 浏览器实测后更正）**：先前记录的两张答复 Sheet ID（`16xLYblH…`／`14I1jRsl…`）**不存在**，以上为实测正确 ID。表单编辑 ID：创始登记 `1-xRE3tkbcE7GrwbV-P0rwukxdHaVVZGT5d0cg9Cg4Ok`；认领献词 `1Ky4iuIvbeYriRPvjiUh9hvKT0HVLD9LAEK9renLvuNg`。来源题 entry ID：创始登记 `entry.1134647210`；认领献词 `entry.1559930750`（8 条来源预填链接已逐条载入验证，见 `~/workspace/china-speed-plan-2026-11-07/funnel-source-links.md` §3）。端到端测试（B-1）通过：两张 TEAM TEST 提交均落进各自 Sheet 第 2 行（登记表 11/8/2026 1:36:18；认领表 11/8/2026 1:40:16），已标「TEAM TEST 2026-11-08 — exclude」排除，E0–E4 基线维持 0。
- **表单文案缺口（2026-11-08 实测确认，未改表单）**：创始登记第 1 题选项实测为 ① 購買意向 — 我有興趣以 $7.99/月加入，開放付款時通知我 ② 免費試讀 — 先領取 7 天試讀卷 ③ 兩者都要 Both——**没有「建议篇目（suggest an entry）」选项**（Claude 顾问意见属实）。是否补此选项属战役决策，留待复盘会裁示，不静默修改。
- 公开页：https://king818.github.io/daddymi-publications/gospel-wisdom/（commit [`9688d65`](https://github.com/king818/daddymi-publications/commit/9688d659debdb6239e191dfea4d4e84fa16fa6b0)）。
- 上账口径：公开渠道的登记以这两张 Sheet 为准，抄入台账；Space 内部登记仍走 action 回读。两路并存、去重按邮箱。

### 选项 B — Kit（ConvertKit）免费版
- 机制：团队既定的名单工具（见 GOAL.md 通路定案）；Kit 表单/落地页自带名单管理与后续邮件序列，正好接 Stage 1 的开售通知。
- **只剩一个动作**：boss 本人完成 Kit 免费版账号注册/确认（用 boss 的邮箱；密码走 Secure Vault 捕获页，不经聊天）——账号一开，Amani 即可建表单并把链接/嵌入交给落地页替换 CTA。
- 代价：多一个外部系统要维护；免费版功能上限日后可能撞墙，撞墙再议。

## Stage 1 备注（不在本轮范围）

真实收款（Stripe / Kit Commerce 等）须 boss 单独裁示后另行接线；裁示前本页与台账只记「登记 / 试读下载」，「付款」行只能凭处理商交易记录入账（见台账记账规则）。
