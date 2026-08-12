---
type: project
region: "中东非"
country: "哈萨克斯坦"
customer: "Aktas Energy（TotalEnergies 60% / KMG Green Energy 20% / Qazaq Green Power 20%）"
project: "Mirny 陆上风电场"
description: "TotalEnergies 主导的江布尔州大型陆上风电项目，2026 年 3 月开始施工安装，2028 年首次供电。整机已由远景能源（124 台）与三一重能（26 台）分食。"
capacity_mw: 1000
turbine_count: 150
turbine_model: ""
unit_mw: 
segment: "陆上"
status: "在建"
oem: "远景能源 / 三一重能"
opportunity: "已失单"
cod_year: 2028
capex: "约 USD 12 亿"
owner_contact: ""
source_url: "https://www.windpowermonthly.com/article/1953462/construction-starts-totalenergies-1gw-kazakh-wind-farm-chinese-turbines"
manual: false
publish: true
first_logged: 2026-07-28
updated: 2026-08-12
---

## 项目简介

TotalEnergies Renewables 持股 60% 的合资项目，2026 年 3 月进入施工安装阶段，2028 年并网。总投资约 12 亿美元，约 75% 为外部融资（EBRD、Proparco、DBK、DEG、法国兴业、QNB、中国建设银行、渣打）。含 600MWh 储能。

## 整机采购状态

**已失单（2026-07-30 核实）。**

**2026-07-30 更新：** 整机归属已查实，**窗口早在 2025 年 10 月即已关闭**：

- **远景能源（Envision Energy）** 2025 年 10 月签 Letter of Award，供 **124 台**
- **三一重能（SANY Renewable Energy）** 同月签 Letter of Award，供其余 **26 台**
- 另有 Samruk-Kazyna × SANY 合资的 **Shu 工业园工厂**获 TotalEnergies **200MW 机组**供货中标函。该 200MW 口径与上述 150 台的关系尚未厘清，**两个口径并列记录不做合并**：150 台来源为 Windpower Monthly（2026-03-31），200MW 来源为 Samruk-Kazyna 新闻室
- 字段修正：`turbine_count` 由空白改为 150，`capex` 由空白改为约 12 亿美元，`oem` 由空白改为「远景能源 / 三一重能」

**此前记为 `opportunity: 高`、`oem` 留空（2026-07-28 建库时），已修正为 `已失单`。原机会分析保留于下方作为复盘材料。**

### 原机会分析（2026-07-28 记录，保留原文）

> **整机厂需核实。** 施工已启动，整机大概率已定或在定标末期。

复盘：方向判断没错（「大概率已定」），但归到 `高` 是错的 —— 阶段已到「在建」时应默认整机锁定。**建议把「status = 在建 且 oem 为空」的默认机会等级由 `高` 下调为 `低` 并附核实标记**，库内同类条目需一并复核。

**2026-08-12 更新：融资结构已补录，且它推翻了本库此前的一个隐含假设。**

EBRD 官方口径（2026-04-24 发布，早于本次更新窗口，按「对库内已有条目的状态更新」规则收录）：

- **A/B 贷合计最高 USD 5.48 亿（EUR 4.67 亿）** —— A 贷最高 USD 2.50 亿由 EBRD 自有账户提供；B 贷最高 USD 2.98 亿银团化，成员含**中国建设银行**、卡塔尔国民银行、法国兴业银行、渣打银行
- 联合融资方：**Proparco**（法国开发署子公司）、**DEG**（德国投资公司）、**哈萨克斯坦开发银行（DBK）**
- 项目源于**哈萨克斯坦与法国的政府间协议**
- 股权口径（EBRD 表述）：Aktas Energy 为 **TotalEnergies、Samruk-Kazyna（主权财富基金）与 KazMunayGas** 的合资公司。**与本笔记 YAML 中已记的「TotalEnergies 60% / KMG Green Energy 20% / Qazaq Green Power 20%」口径不完全一致，两者并列保留不做合并** —— EBRD 未披露持股比例，本库原口径来源为项目方公告
- 储能口径细化为 **300MW / 600MWh**（本库原记「含 600MWh 储能」，与之相容）
- 定性：哈萨克斯坦最大陆上风电开发项目，**该国首个工业级风储一体化电站**，年减排约 250 万吨 CO₂

**为什么这条重要：** 本项目由 EBRD + 法德开发金融机构 + 政府间协议支撑，整机最终仍归中国厂商（远景 124 台 / 三一 26 台）。**这说明多边开发银行融资并不构成对中国整机厂的准入障碍** —— 若我方曾以「EBRD 项目采购规则难进」为由下调哈国及中亚同类项目的优先级，该假设应予推翻。真正的门槛是本地产能与交付业绩，不是资金来源。相关判断已同步更新至 [[P0-哈萨克斯坦本地产能门槛应对]]。

融资结构全文见 [[哈萨克斯坦Mirny 1GW EBRD 5.48亿美元AB贷款结构]]。

## 待办
- [x] 核实整机厂 —— 已查实为远景能源 + 三一重能
- [ ] 厘清 EBRD 与项目方两个股权口径的差异（EBRD 未提 KMG Green Energy / Qazaq Green Power，直接写 KazMunayGas 与 Samruk-Kazyna）
- [ ] 厘清 150 台 与 Shu 工厂 200MW 两个口径的关系
- [ ] 通过 TotalEnergies 集团采购渠道确认其中亚后续项目管道，判断远景是否已进入其框架供应商名录
- [ ] 复核库内其他「在建 + oem 空」项目：[[哈萨克斯坦-Masdar-Jambyl 1GW风储]]、[[哈萨克斯坦-Karaganda Wind Power-500MW]]

## 关联
- [[远景能源-哈萨克斯坦Mirny 1GW整机供货]]
- [[三一重能-哈萨克斯坦Mirny与Shu本地产能]]
