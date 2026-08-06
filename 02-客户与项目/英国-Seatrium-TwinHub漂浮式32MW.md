---
type: project
region: 欧洲
country: 英国
customer: "Seatrium（新加坡，2026 年自 Hexicon 收购 Wave Hub Ltd 100% 股权）"
project: "TwinHub 漂浮式海上风电测试与示范（凯尔特海，英格兰西南外海）"
description: "32MW 凯尔特海漂浮式测试与示范项目，英国首个漂浮式 CfD 中标项目（AR4）。Hexicon 因 CfD 被终止而计提减值并以 GBP 1 的对价将 Wave Hub Ltd 100% 股权出售；2026-08-05 经 reNEWS 确认买方为新加坡海工企业 Seatrium。Seatrium CEO Chris Ong 在 2026-07-31 的半年报说明会上表示，该项目将用于部署其自研漂浮式半潜基础 FWSS，该基础设计支持 15MW 级机组。整机供应商尚未公开。"
capacity_mw: 32
unit_mw: 15
turbine_count: 2
turbine_model: ""
segment: 漂浮式
status: 前期
oem: ""
cod_year: ""
capex: "股权对价 GBP 1（不含后续建设投资）"
owner_contact: ""
opportunity: 中
manual: false
publish: true
first_logged: 2026-08-06
updated: 2026-08-06
---

## 项目简介

TwinHub 是英国**第一个在 CfD 拍卖（AR4）中中标的漂浮式海上风电项目**，位于英格兰西南凯尔特海，容量 32MW，属测试与示范性质。项目公司为 Wave Hub Ltd。

股权变动链条：

| 时间 | 事件 |
|---|---|
| 2026-02 | Hexicon 就 TwinHub 计提减值，宣布寻求出售（CfD 已被终止） |
| 2026 年上半年 | Hexicon 以 **GBP 1** 的对价出售 Wave Hub Ltd 100% 股权（含资产与负债），买方未披露 |
| 2026-07-31 | Seatrium 半年报说明会上 CEO Chris Ong 提及该项目 |
| **2026-08-05** | reNEWS 确认买方为 **Seatrium** |

**CfD 已被终止是本条的关键背景** —— 项目失去了原有的收入保障机制，Seatrium 接手的动机不是电站收益，而是**给自己的漂浮式基础找一个实证场地**。

## 整机采购状态

**整机未定 —— `oem` 留空即机会，但机会的性质特殊。**

- Seatrium 明确说明该场址将用于部署其自研半潜式漂浮基础 **FWSS（floating wind semi-submersible）**，该设计**面向 15MW 级机组**
- 32MW ÷ 15MW ≈ **2 台**，`turbine_count` 与 `unit_mw` 据此推算，非官方披露，**待核实**
- 窗口判断：**CfD 已终止，项目没有确定的收入模型，短期内不会有正式整机招标。** 这不是「几个月内定标」的项目，`opportunity` 因此定 `中` 而非 `高`（容量 32MW 也低于「高」的 100MW 门槛）

**但战略价值高于 32MW 这个数字：**

1. **业主是船厂不是电力开发商。** Seatrium 是海工建造企业，采购逻辑接近油气行业 —— 关心的是基础与整机的载荷接口、安装工艺、可制造性，**对整机厂的国别敏感度通常低于纯电力系业主**。本库在 [[英国-Cierco-Llyr漂浮式2x100MW]] 中对 SBM Offshore 已有同类判断。
2. **谁的机组装在 FWSS 上，谁就进入了 Seatrium 后续所有漂浮式项目的默认配置。** Seatrium 同时在给 TenneT 2GW 平台、Sofia 等项目做建造与运维（见 [[2026-07-30-Seatrium英国Lowestoft海上风电运维枢纽开工]]），是凯尔特海与北海的活跃承包商。
3. 这与 Llŷr 项目构成同一判断：**凯尔特海的漂浮式示范项目正在被「基础方 + 船厂」主导，而不是被开发商主导。** 我方接触对象应相应调整。

## 待办
- [ ] 核实 32MW 的机组配置（2×15MW 为推算）与 Seatrium FWSS 的载荷接口参数
- [ ] 确认 CfD 终止后 Seatrium 打算用什么收入模型推进（企业 PPA？自用？纯示范不发电？）—— 决定这个项目是否真会走到整机采购
- [ ] 经海工/造船产业链渠道（而非风电开发商渠道）接触 Seatrium 漂浮式团队，议题应是基础-整机接口而非商务报价
- [ ] 与 [[英国-Cierco-Llyr漂浮式2x100MW]] 并案跟踪：凯尔特海两个示范项目的整机若被同一家拿下，商业轮次的技术准入基本关闭

## 关联
- 同海域示范项目：[[英国-Cierco-Llyr漂浮式2x100MW]]
- 技术侧：[[船厂自持漂浮式示范验证自研半潜基础]] · [[漂浮式半潜平台商业化运维]]
- 英国漂浮式路径：[[英国漂浮式2050年40GW产业化路径]]
- 本地含量：[[P1-英国本地含量劣势对冲]]

## 来源
- <https://www.renews.biz/offshore-wind/seatrium-confirms-twinhub-acquisition/>（2026-08-05）
- <https://www.offshorewind.biz/2026/02/02/hexicon-books-impairment-related-to-twinhub-seeks-to-divest-floating-wind-project/>（2026-02-02，背景）
