---
type: competitor
competitor: Vestas
event_type: 订单
counterparty: "Edison、SIMIC"
contract_value: ""
capacity_mw:
turbine_count:
region: 欧洲
country: 意大利
segment: 陆上
date: 2026-09-16
description: "Vestas 公布意大利三笔陆上订单合计 170MW：Castellani、Foiano 与一个未披露项目，业主为 Edison 与 SIMIC。三笔中两个项目采用 EnVentus 平台机型，全部配长期运维协议，自 2027 年下半年起实施。与本库 09-08 记录的意大利 105MW（Castellani 45MW + 未披露 60MW）存在重复计入可能，两个口径并列保留。"
importance: 中
source_name: "reNEWS"
source_url: "https://www.renews.biz/onshore-wind/vestas-lands-170mw-italy-orders/"
publish: true
created: 2026-09-17
---

> ## 🔴 2026-09-21 更新：口径分歧已解决 —— 两个 170MW 是同一个 170MW
>
> **本次运行查 Vestas 官方订单披露页（投资者关系，权威一手口径），意大利三季度全部已公告订单如下：**
>
> | 日期 | 内容 | MW |
> |---|---|---|
> | 2026-08-24 | Vestas announces a new 65 MW order in Italy | **65** |
> | 2026-09-08 | Vestas announces two new orders in Italy for a total of 105 MW | **105** |
> | 2026-09-16 | Vestas announces three new orders for a total of 119 MW | 119 —— **荷兰 / 比利时 / 波兰，非意大利** |
> | | **意大利 Q3 合计** | **170** |
>
> 来源：<https://www.vestas.com/en/investor/announcements/wind-turbines-orders>
>
> **结论：Vestas 官方 Q3 意大利订单总额 = 65 + 105 = 170MW，且 09-16 当天没有任何意大利新订单。** reNEWS 09-16 的《Vestas lands 170MW Italy orders》是对 8-24 与 9-08 两批的**累计综述**，不是第三笔新订单。
>
> **三处修正：**
> 1. **`capacity_mw` 由 170 改为留空。** 此前记为 170，会与本库既有的 [[Vestas-意大利65MW订单]]（65）、[[Vestas-意大利SIMIC Castellani 45MW与未披露60MW订单]]（105）在汇总表里重复计入。**本条的新增容量实为 0，故留空而非填 0。**
> 2. **下方「累计约 340MW」的表格数字有误 —— 真实累计为 170MW。** 原表保留不删，以本段为准。
> 3. **原「待办」第一条（核实是否重复计入）已完成。**
>
> **⚠️ 但有一件事没有被这次核实推翻，反而被坐实了：Edison 确实出现了。** reNEWS 把 Edison 列为业主之一，而 Vestas 官方 09-08 的两笔意大利订单业主未全部披露。**「EDF 集团在欧洲陆上按市场分区把渠道给了 Vestas（意大利）与 Nordex（英国）」这条集团级判断不受本次修正影响，仍然成立。** 修正的只是容量口径，不是判断。

## 事件

**2026-09-16**，Vestas 公布意大利三笔陆上订单：**Castellani + Foiano + 一个未披露项目，合计 170MW**，业主 **Edison** 与 **SIMIC**。两个项目用 **EnVentus** 平台，三笔**全部配长期运维协议**，**2027 年下半年**起实施。

### 口径分歧（并列保留，不取其一）

| 口径 | 日期 | 内容 |
|---|---|---|
| A（本库既有） | 2026-09-08 | 意大利两笔 **105MW**：SIMIC Castellani 45MW + 未披露 60MW |
| B（本条） | 2026-09-16 | 意大利三笔 **170MW**：Castellani + Foiano + 未披露，业主 Edison 与 SIMIC |

**Castellani 在两个口径中重复出现** → 170MW 很可能是对 105MW 的合并/追加披露，真实新增约 65MW。来源未说明，**不取平均、不取其一**，以 Vestas 三季度订单披露为准。

## 对我方的含义

### 一、Vestas 在意大利的成交节奏已经不是「陆续」，是「清场」

| 日期 | 容量 | 业主 |
|---|---|---|
| 2026-08-24 | 65MW | 未披露 |
| 2026-09-08 | 105MW | SIMIC + 未披露 |
| **2026-09-16** | **170MW** | **Edison + SIMIC** |
| 累计（含重复计入风险） | **约 340MW** | 三周半内 |

### 二、真正的新信息是 Edison —— 这是一个集团级结论

**Edison 是 EDF 集团意大利子公司**，此前不在本库意大利开发商名单内。结合本库既有记录：

| 市场 | EDF 系主体 | 整机 | 形式 |
|---|---|---|---|
| 英国 / 爱尔兰陆上 | EDF power solutions | **Nordex** | 明面独家框架，最高 900MW |
| **意大利陆上** | **Edison** | **Vestas** | **订单 + 长期运维协议** |

**EDF 集团在欧洲陆上的采购已分区固化，两个区我方都没有入口。** 这不是两个孤立项目，是一个需要在集团层面回答的问题。

**必须查清、不能假设：Edison × Vestas 合同是否含后续项目优先权或框架条款。** 与本库在 [[GEVernova-英国ESB Chleansaid 96MW整机与长协]] 上提出的是同一个问题：
- 若含 → Edison 意大利管道整体关闭
- 若不含 → 剩余管道仍可争，但要抢在第二批定标前

### 三、时间点：整机在 FER X 拍卖之前就定完了

三笔全部排 **2027 年下半年**交付。而意大利 **FER X 首场竞争性程序的预资格申请截止日是 2026-09-30** —— **开发商不等拍卖结果就在锁产能。**

这把 [[P1-意大利FERX首场拍卖前的开发商绑定]] 的核心判断又验证了一次：**窗口不是拍卖后打开，是拍卖前就在关闭。** 该条 deadline 2026-09-30，今日起剩 13 天，`status` 仍为「待启动」。

## 待办
- [x] ~~核实 170MW 与 09-08 的 105MW 是否重复计入（Vestas 三季度订单披露）~~ —— **2026-09-21 已完成：是重复计入，意大利 Q3 实为 65 + 105 = 170MW，09-16 无意大利新订单。见页首更新段**
- [ ] 查 Foiano 与未披露项目的容量、大区、机型
- [ ] 查 Edison 意大利陆上与海上管道全貌 —— **这是本条真正的标的，不是这 170MW**
- [ ] 核实 Edison × Vestas 是否含后续优先权条款
- [ ] 在集团层面评估 EDF 系渠道的整体应对（英国 + 意大利并案）

## 关联
- [[2026-09-16-Vestas获意大利Edison与SIMIC三笔订单合计170MW]]
- [[意大利-Edison-Foiano 陆上风电]]
- [[意大利-SIMIC Group-Castellani 45MW]]
- [[Vestas-意大利SIMIC Castellani 45MW与未披露60MW订单]]
- [[Vestas-意大利65MW订单]]
- [[P1-意大利中小陆上标的被Vestas连续拿下的渠道补位]]
- [[P1-意大利FERX首场拍卖前的开发商绑定]]
- [[Nordex-EDF英国最高900MW独家供货框架]]
- [[P1-英国陆上EDF渠道被Nordex锁定后的替代路径]]
