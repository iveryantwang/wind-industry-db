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
oem: ""
opportunity: "高"
cod_year: 
capex: "约 EUR 30 亿"
owner_contact: ""
source_url: "https://www.offshorewind.biz/2026/06/26/skyborn-nets-another-ppa-for-gennaker-offshore-wind-farm/"
manual: false
publish: true
first_logged: 2026-07-28
updated: 2026-08-05
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

## 关联
- [[2026-08-04-大金重工开工建造Gennaker过渡段]]
- [[Seaway7-Gennaker单桩安装]]
- [[Gennaker项目融资与PPA结构]]
- [[P0-德国Gennaker整机窗口即将关闭]]
