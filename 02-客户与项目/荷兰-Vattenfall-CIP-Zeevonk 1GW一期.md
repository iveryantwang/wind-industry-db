---
type: project
region: "欧洲"
country: "荷兰"
customer: "Vattenfall + Copenhagen Infrastructure Partners（合资）"
project: "Zeevonk 海上风电 一期 1GW"
description: "荷兰北海 Zeevonk 海上风电项目，由 Vattenfall 与 CIP 合资开发。2026-09-16 选定 EEW Special Pipe Constructions 制造一期 1GW 的 69 根单桩基础，采用无过渡段（transition-piece-less）设计——塔筒直接安装于单桩之上，省去传统过渡段，节约钢材、简化物流并降低制造与安装环节碳排；其中 1 根采用高再生比例钢材。"
capacity_mw: 1000
turbine_count: 69
turbine_model: ""
unit_mw:
segment: "海上"
status: "在建"
oem: ""
opportunity: "低"
cod_year:
capex: ""
owner_contact: ""
source_url: "https://www.renews.biz/uncategorized/eew-wins-zeevonk-foundations-contract/"
manual: false
publish: true
first_logged: 2026-09-17
updated: 2026-10-16
---

**2026-10-16 更新（信息日 2026-10-15）：风机运输安装合同授予 DEME；项目仍待 FID。** 以下既有内容全部保留。

- DEME 将为一期 **69 台风机**做运输与安装，船为 Norse Energi（3200 吨起重机，水深至 70 米），2028 年起动员，一期 2029 年投运。
- **来源仍未披露风机供应商与机型**，`oem` 继续留空。
- **口径并列：** 既有笔记依据基础已定标，推断"整机大概率已锁但未公开"；本条来源则称项目**仍需最终投资决定**。两者不矛盾（整机可在 FID 前签优先供货），但"FID 前整机可能仍有变数"的可能性不能排除。`opportunity` 暂维持「低」，不据此上调。
- **待办补充：** 本周内查 DEME 新闻稿原文（是否点名风机商）；若点名则补 `oem`，若明说整机未定则上调为「高」并建 P0。
- 来源：<https://www.offshorewind.biz/2026/10/15/deme-to-install-wind-turbines-at-vattenfall-and-cips-1-gw-dutch-offshore-wind-farm>

## 项目简介

| 项 | 内容 |
|---|---|
| 位置 | **荷兰北海** |
| 业主 | **Vattenfall + CIP** 合资 |
| 一期容量 | **1GW** |
| 基础 | **69 根单桩**，供应商 **EEW Special Pipe Constructions**（2026-09-16 定标） |
| 基础设计 | **无过渡段（transition-piece-less）—— 塔筒直接装于单桩** |
| 特别项 | 1 根基础采用高再生比例钢材 |

**69 根对应 1GW → 单机约 14.5MW 级**（本库推算，非来源口径，不作为定论）。

## 整机采购状态

**来源未披露整机商，本库 `oem` 字段留空。但机会等级定为「低」，不是「高」，理由有三：**

1. **项目已进入基础采购阶段。** 基础定标通常晚于或同期于整机定标 —— 1GW 项目走到 69 根单桩签约，整机大概率已锁，只是未公开。本库在 [[哈萨克斯坦-TotalEnergies-Mirny]] 上吃过一次亏：整机早在开工前半年定标却从未公开，本库晚了 9 个月才发现。**「检索不到定标消息」不等于「未定标」。**
2. **无过渡段设计对整机接口有专门要求。** 塔筒底段必须为单桩顶法兰定制，打桩垂直度公差直接传导到塔筒接口 —— **这类设计通常是整机商与基础商同期敲定的，不会等到基础签完再选整机。**
3. **业主组合是 Vattenfall + CIP。** 两家均为成熟买方，整机偏好成型。Vattenfall 在本库已出现于 [[丹麦-Vattenfall-Nordsoen Midt与Hesseloe 1.8GW]]、[[德国-Vattenfall-ABO 43MW陆上风电]]；CIP 出现于 Fengmiao 1、Gawara Baya、Morecambe、老挝跨境走廊等多处。**这两家的欧洲海上新项目，新供应商进入难度高。**

## 值得跟的不是这个项目，是这个设计

**无过渡段单桩正在从个案变成北海的主流做法。** 对我方的实质影响是**整机与基础的界面重划**：

- 传统链条：单桩 → 过渡段（吸收垂直度偏差）→ 塔筒
- 无过渡段：单桩 → **塔筒直接对接**，偏差无缓冲层

这意味着整机厂要在合同里承接原本由过渡段吸收的施工公差风险，且塔筒底段需项目定制。**能不能做这套接口，在北海项目上正在变成资格条件。** 详见 [[无过渡段单桩直连塔筒的整机界面重划]]。

## 待办
- [ ] **两周内**：查清 Zeevonk 整机商与机型（Vattenfall 官网项目页、荷兰 RVO 补贴公示、EEW 新闻稿细节）—— 若已定，把 `oem` 补上、`opportunity` 维持「低」；若确认未定，立即上调为「高」并建 P0
- [ ] 核实 Zeevonk 与 IJmuiden Ver 各场址的对应关系（Alpha / Beta / Gamma），与本库 [[荷兰-IJmuidenVerGamma-2GW]] 并线，避免同一场址重复建条目
- [ ] 取得无过渡段单桩的塔筒接口技术要求，评估我方塔筒底段的适配性与改造成本 —— 这是北海项目的准入前置项

## 关联
- [[2026-09-16-Zeevonk一期1GW单桩基础授予EEW采用无过渡段设计]]
- [[无过渡段单桩直连塔筒的整机界面重划]]
- [[荷兰-IJmuidenVerGamma-2GW]]
- [[荷兰-RVO-Nederwiek I-B]]
- [[大直径单桩量产产能年200支节奏]]
- [[英国-CIP-Morecambe 海上风电]]
