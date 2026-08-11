---
type: project
region: "欧洲"
country: "德国"
customer: "OWP Gennaker / Skyborn Renewables"
project: "Gennaker 海上风电（976.5MW）"
description: "德国波罗的海海上风电，976.5MW，63 台单桩基础。已签 Amazon 600MW 与 Uniper 100MW 两份 PPA，慕尼黑市政 SWM 收购 25% 股权，预计 2026 Q3 融资关闭后开工。Seaway7 承接单桩运输安装。"
capacity_mw: 976.5
turbine_count: 63
turbine_model: ""
unit_mw: 15.5
segment: "海上"
status: "核准"
oem: "Siemens Gamesa"
turbine_model_confirmed: "SG 14-236 DD"
opportunity: "已失单"
cod_year: 
capex: "约 EUR 30 亿"
owner_contact: ""
source_url: "https://www.offshorewind.biz/2026/06/26/skyborn-nets-another-ppa-for-gennaker-offshore-wind-farm/"
manual: false
publish: true
first_logged: 2026-07-28
updated: 2026-08-11
---

## 项目简介

德国少数在招标缩量背景下仍稳步推进的存量项目：PPA 已锁定 700MW（Amazon 600 + Uniper 100），股权已引入 SWM，融资预计 2026 Q3 关闭。

63 台 / 976.5MW ≈ **15.5MW 单机**。

## 整机采购状态

**整机厂尚未公开。** 基础安装承包（Seaway7）已定，整机通常与基础同期或稍后锁定 —— 窗口正在关闭。

## 待办
- [ ] **紧急**：核实整机是否已定标
- [ ] 15.5MW 档位机型对标（若我方有 15–16MW 平台）
- [ ] 通过 Skyborn（前 wpd offshore）渠道接触

---

## 🔴 2026-08-05 更新：过渡段已开工制造，整机窗口按常规节奏应已关闭

**新事实：中国大金重工（Dajin Heavy Industry）已在山东蓬莱基地切第一块钢，为本项目制造 63 件过渡段。**

- offshoreWIND.biz 报道日期 **2026-08-04**，表述为「开始制造」，容量记 **976MW**
- reNEWS 报道日期 **2026-07-31**，表述为「已切第一块钢」，容量记 **977MW**
- 两条应为同一事件的先后报道；容量与本库既有的 976.5MW 属四舍五入差异，**本库容量口径不变**
- 来源：<https://www.offshorewind.biz/2026/08/04/dajin-starts-fabrication-of-transition-pieces-for-976-mw-gennaker-offshore-wind-farm/>

**63 件过渡段 = 63 台机位，与本库既有的 63 台/976.5MW 口径完全吻合，可交叉验证既有数据无误。**

## 判断修正：从「窗口正在关闭」改为「窗口按常规节奏应已关闭，但仍未见公开定标」

本条 2026-07-28 建档时判断「整机通常与基础同期或稍后锁定 —— 窗口正在关闭」。现在基础侧已进入实际制造：

- 单桩安装承包（Seaway7）**已定**
- 过渡段制造**已开工**
- 融资预计 2026 Q3 关闭，PPA 已锁 700MW

**欧洲海上项目走到过渡段开工这一步，整机合同在绝大多数情况下已经签署，只是未必公开。** 本库在 [[哈萨克斯坦-TotalEnergies-Mirny]] 上已经吃过一次亏 —— 整机早在开工前半年定标却从未公开，本库晚了 9 个月才发现。**Gennaker 现在处在完全相同的风险形态。**

**因此 `oem` 字段维持留空、`opportunity` 维持 `高` 是「尚未查实」而不是「确实开放」，两者含义完全不同，不应在汇报中混为一谈。**

**本周必须完成的一件事：** 查 Skyborn Renewables 官网新闻区与 Siemens Gamesa / Vestas 的 2026 上半年订单披露，确认 Gennaker 整机归属。若查实已定标，本条 `opportunity` 应改 `已失单`，并在 `04-竞争对手` 建对应记录；若确认仍未定，则窗口紧迫度进一步上升，应立即启动接触。

详见 [[P0-德国Gennaker整机窗口即将关闭]] 的今日复核。

---

## 🔴 2026-08-11 更新：查实已失单 —— 整机由 Siemens Gamesa 拿下，63 台 SG 14-236 DD

**2026-08-05 提出的「本周必须完成的一件事」已完成，结论是失单。**

| 项 | 内容 |
|---|---|
| 整机商 | **Siemens Gamesa** |
| 机型 / 台数 | **SG 14-236 DD × 63 台**（单机额定最高 15MW，叶轮 236m） |
| 协议 | 整机供货协议（TSA）+ 海上长周期运维协议（LTPSA），**附条件生效**（以 Skyborn 发出 Notice to Proceed 为准） |
| 上位协议 | 基于 Skyborn 与 Siemens Gamesa **2024-06** 签署的框架供货协议（MSA） |
| 公开披露日 | **2025-07-18** |
| 海上安装 | 计划 2028 年初开始 |
| 来源 | <https://www.offshorewind.biz/2025/07/18/siemens-gamesa-secures-conditional-turbine-order-for-skyborns-german-offshore-wind-farm/> |

**字段变更：`oem` 由留空改为 `Siemens Gamesa`；`opportunity` 由 `高` 改为 `已失单`。以上机会分析全部保留，不删。**

### 与既有记录的口径关系

- 本库既有的 **63 台 / 976.5MW / 15.5MW 单机** 口径与 SGRE 官方的「63 台 SG 14-236 DD、单机额定最高 15MW」**基本吻合**。单机容量两个口径并列：本库既有推算值 **15.5MW**（976.5÷63），厂商机型标称 **最高 15MW**。**不取平均，两者并存** —— 差异可能来自机型的功率提升版本（power-uprate）。
- 2026-08-05 记录的「过渡段已开工制造」与本次结论完全自洽：**过渡段开工时整机合同已签署一年有余。**

### 判断复盘：方向对，动作缺

2026-08-05 的判断原文是「窗口按常规节奏应已关闭，但仍未见公开定标」，并明确写了「`opportunity` 维持 `高` 是『尚未查实』而不是『确实开放』」。**这个判断是准确的 —— 缺的只是一次检索动作。** 定标信息在 2025-07-18 就已公开，检索 "Skyborn Gennaker turbine supply agreement" 即可命中。

这是本库第二次同类漏检（第一次是 [[哈萨克斯坦-TotalEnergies-Mirny]]，晚 9 个月）。**两次共同特征：项目走到基础/过渡段实际制造这一步时，整机合同事实上早已签署。**

### 更重要的一条：项目级竞争在 MSA 阶段就已结束

Gennaker 的 TSA 派生自 2024 年 6 月的 **框架供货协议（MSA）**。这意味着 —— **我方在 2026 年才开始跟踪这个项目时，竞争其实在 2024 年中就已经结束了。** 同类结构本库另有一例：[[Nordex-EDF英国最高900MW独家供货框架]]。

**结论：对欧洲成熟开发商，逐项目投标已基本无效，必须争取进入其框架供货协议。** 这一条应上升为欧洲市场的通用打法，不只针对德国。

## 关联
- 竞对记录：[[SiemensGamesa-德国Gennaker 976.5MW整机供货与长协]]
- [[2026-08-04-大金重工开工建造Gennaker过渡段]]
- [[Seaway7-Gennaker单桩安装]]
- [[Gennaker项目融资与PPA结构]]
- [[P0-德国Gennaker整机窗口即将关闭]]
