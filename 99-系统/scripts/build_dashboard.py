# -*- coding: utf-8 -*-
"""
风电行业数据库 —— 数据看板生成脚本
=====================================
作用：扫描 vault 内所有笔记的 YAML frontmatter，生成一个**自包含的单文件 HTML 看板**。
      七个板块各一个 Tab，支持全局搜索、多列筛选、点列头排序、点标题跳转到笔记详情页。

为什么需要它：Quartz 把每条笔记渲染成独立页面，索引页上的静态 Markdown 表格既不能排序
              也不能筛选。看板补上这一层，同事拿到的体验接近 Excel。

自包含：数据以 JSON 内联在 HTML 里，不依赖任何 CDN、不发网络请求。
        双击本地文件就能看，也能直接丢到静态站根目录当首页。

隐私开关：07-战略判断 含我方投标策略与竞对判断，默认**不导出**。
          要发布就加 --with-strategy，或设环境变量 PUBLISH_STRATEGY=1。

运行：python build_dashboard.py                          # 输出到 vault 根/看板.html
      python build_dashboard.py <vault路径> -o out.html
      python build_dashboard.py --with-strategy
仅依赖 Python 3 标准库。
"""

import os
import io
import re
import sys
import json
import html
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rebuild_tables import read_notes, find_vault  # noqa: E402  复用同一套解析逻辑

# ---------------------------------------------------------------- 板块定义
# key      : 内部标识，也用作 Tab 的 DOM id
# type     : 对应笔记 YAML 里的 type
# title    : Tab 显示名
# link     : 用作跳转标题的字段
# folder   : 笔记所在文件夹，用于拼 Quartz 页面地址
# sort     : (字段, 是否降序) 默认排序
# facets   : 需要生成筛选下拉框的字段
# columns  : (字段, 表头, CSS 类) —— 特殊字段见下
#            __link__  跳转到笔记详情的标题列
#            __src__   原文外链列

SECTIONS = [
    {
        "key": "project", "type": "project", "title": "客户与项目",
        "folder": "02-客户与项目", "link": "project",
        "sort": ("capacity_mw", True),
        "facets": ["oem_state", "opportunity", "region", "country", "segment", "status", "oem"],
        "columns": [
            ("opportunity", "机会", "c-tag"),
            ("region", "区域", "c-sm"),
            ("country", "国别", "c-sm"),
            ("customer", "业主 / 客户", "c-md"),
            ("__link__", "项目", "c-lg"),
            ("capacity_mw", "容量MW", "c-num"),
            ("unit_mw", "单机MW", "c-num"),
            ("turbine_count", "台数", "c-num"),
            ("segment", "类型", "c-xs"),
            ("status", "状态", "c-sm"),
            ("oem", "整机商", "c-sm"),
            ("cod_year", "并网年", "c-xs"),
            ("__src__", "原文", "c-src"),
        ],
    },
    {
        "key": "news", "type": "news", "title": "每日新闻",
        "folder": "01-每日新闻", "link": "title",
        "sort": ("date", True),
        "facets": ["region", "country", "segment", "importance"],
        "columns": [
            ("date", "日期", "c-date"),
            ("importance", "重要性", "c-tag"),
            ("__link__", "标题", "c-lg"),
            ("summary", "摘要", "c-xl"),
            ("region", "区域", "c-sm"),
            ("country", "国别", "c-sm"),
            ("segment", "板块", "c-xs"),
            ("source_name", "来源", "c-md"),
            ("__src__", "原文", "c-src"),
        ],
    },
    {
        "key": "policy", "type": "policy", "title": "风电政策",
        "folder": "03-风电政策", "link": "policy",
        "sort": ("issued", True),
        "facets": ["region", "country", "segment", "impact_level"],
        "columns": [
            ("issued", "发布日期", "c-date"),
            ("impact_level", "影响", "c-tag"),
            ("country", "国别", "c-sm"),
            ("__link__", "政策名称", "c-lg"),
            ("issuer", "发布机构", "c-md"),
            ("summary", "核心内容", "c-xl"),
            ("__src__", "原文", "c-src"),
        ],
    },
    {
        "key": "competitor", "type": "competitor", "title": "竞争对手",
        "folder": "04-竞争对手", "link": "competitor",
        "sort": ("date", True),
        "facets": ["competitor", "region", "country", "event_type", "importance"],
        "columns": [
            ("date", "日期", "c-date"),
            ("importance", "重要性", "c-tag"),
            ("__link__", "竞争对手", "c-md"),
            ("event_type", "动态", "c-xs"),
            ("country", "国别", "c-sm"),
            ("counterparty", "签约客户", "c-md"),
            ("capacity_mw", "容量MW", "c-num"),
            ("turbine_count", "台数", "c-num"),
            ("contract_value", "合同金额", "c-sm"),
            ("__src__", "原文", "c-src"),
        ],
    },
    {
        "key": "tech", "type": "tech", "title": "技术方案",
        "folder": "05-技术方案", "link": "solution",
        "sort": ("date", True),
        "facets": ["country", "maturity", "provider"],
        "columns": [
            ("date", "日期", "c-date"),
            ("__link__", "方案 / 场景", "c-lg"),
            ("provider", "提供方", "c-md"),
            ("use_case", "应用场景", "c-md"),
            ("maturity", "成熟度", "c-xs"),
            ("description", "描述", "c-xl"),
            ("country", "国别", "c-sm"),
            ("__src__", "原文", "c-src"),
        ],
    },
    {
        "key": "finance", "type": "finance", "title": "投资财务",
        "folder": "06-投资财务", "link": "subject",
        "sort": ("date", True),
        "facets": ["country", "biz_model"],
        "columns": [
            ("date", "日期", "c-date"),
            ("__link__", "项目 / 模型", "c-lg"),
            ("capex", "投资规模", "c-sm"),
            ("irr", "IRR", "c-xs"),
            ("lcoe", "LCOE", "c-sm"),
            ("biz_model", "商业模式", "c-sm"),
            ("funding", "资金来源", "c-md"),
            ("country", "国别", "c-sm"),
            ("__src__", "原文", "c-src"),
        ],
    },
    {
        "key": "strategy", "type": "strategy", "title": "战略判断",
        "folder": "07-战略判断", "link": "project",
        "sort": ("priority", False),
        "facets": ["priority", "country", "status"],
        "internal": True,          # 敏感板块，默认不导出
        "columns": [
            ("priority", "优先级", "c-tag"),
            ("country", "国别", "c-sm"),
            ("owner_party", "业主 / 开发商", "c-md"),
            ("__link__", "项目", "c-lg"),
            ("capacity_mw", "容量MW", "c-num"),
            ("action", "建议行动", "c-xl"),
            ("deadline", "行动窗口", "c-date"),
            ("status", "状态", "c-xs"),
        ],
    },
]

# 需要染色的取值 —— 值 -> CSS 修饰类
TAG_TONE = {
    "高": "t-hot", "P0": "t-hot", "已失单": "t-dead",
    "中": "t-warm", "P1": "t-warm",
    "低": "t-cool", "P2": "t-cool",
    "已完成": "t-done", "已放弃": "t-dead",
}

FIELD_LABEL = {
    "opportunity": "机会等级", "region": "区域", "country": "国别",
    "segment": "类型", "status": "状态", "oem": "整机商",
    "importance": "重要性", "impact_level": "影响", "competitor": "竞争对手",
    "event_type": "动态类型", "maturity": "成熟度", "provider": "提供方",
    "biz_model": "商业模式", "priority": "优先级",
    "oem_state": "整机",
}

# 派生字段：不存在于 YAML，由脚本算出来，只用于筛选
DERIVED = {
    # 对整机厂来说最该用的一个筛选：这个项目的整机到底定没定
    "oem_state": lambda n: "已定标" if flat(n.get("oem")) else "未定标",
}


# ---------------------------------------------------------------- 工具

def slugify(segment):
    """复刻 Quartz v4 的 slugifyFilePath 分段规则，保证链接能对上生成的页面。"""
    return (segment.replace(" ", "-")
                   .replace("&", "-and-")
                   .replace("%", "-percent")
                   .replace("?", "")
                   .replace("#", ""))


def flat(value):
    if value is None:
        return ""
    if isinstance(value, list):
        return " / ".join(str(v).strip() for v in value if str(v).strip())
    return str(value).strip()


def num_or_none(value):
    s = flat(value).replace(",", "")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


# ---------------------------------------------------------------- 数据组装

def is_draft(note):
    """与 Quartz 的 RemoveDrafts 插件保持一致：draft: true 的笔记不出现在站上，
    看板也必须跟着藏，否则会出现「表里有这条、点进去 404」。"""
    return str(note.get("draft", "")).strip().lower() in ("true", "yes", "1")


def build_payload(notes, include_internal):
    notes = [n for n in notes if not is_draft(n)]
    by_type = {}
    for n in notes:
        by_type.setdefault(n.get("type"), []).append(n)

    sections = []
    for spec in SECTIONS:
        if spec.get("internal") and not include_internal:
            continue
        items = by_type.get(spec["type"], [])

        rows = []
        for n in items:
            base = n["__basename__"]
            label = flat(n.get(spec["link"])) or base
            row = {
                # 带 .html 后缀：GitHub Pages / Cloudflare Pages / Netlify 全都能直接命中，
                # 不依赖各家对「无扩展名 URL」的不同处理方式
                "_url": "%s/%s.html" % (slugify(spec["folder"]), slugify(base)),
                "_label": label,
                "_src": flat(n.get("source_url")),
                "_hay": "",
            }
            for (field, _h, _c) in spec["columns"]:
                if field in ("__link__", "__src__"):
                    continue
                row[field] = flat(n.get(field))
            for field in spec["facets"]:
                if field in DERIVED:
                    row[field] = DERIVED[field](n)
            # 搜索索引：所有列 + 标题 + 摘要/描述，全部小写
            hay = [label, base]
            hay += [str(v) for k, v in row.items() if not k.startswith("_")]
            hay += [flat(n.get(k)) for k in ("summary", "description", "customer",
                                             "action", "rationale", "impact", "source_name")]
            row["_hay"] = " ".join(x for x in hay if x).lower()
            rows.append(row)

        # 默认排序
        field, desc = spec["sort"]
        def keyf(r, _f=field):
            v = r.get(_f, "")
            nv = num_or_none(v)
            return (0, nv, "") if nv is not None else (1, 0, v)
        rows.sort(key=keyf, reverse=desc)
        if desc:                      # 空值统一沉底
            rows = [r for r in rows if flat(r.get(field))] + \
                   [r for r in rows if not flat(r.get(field))]

        facets = []
        for f in spec["facets"]:
            vals = sorted({flat(r.get(f)) for r in rows if flat(r.get(f))})
            if len(vals) > 1:
                facets.append({"field": f, "label": FIELD_LABEL.get(f, f), "values": vals})

        sections.append({
            "key": spec["key"],
            "title": spec["title"],
            "columns": [{"f": f, "h": h, "c": c} for (f, h, c) in spec["columns"]],
            "facets": facets,
            "rows": rows,
        })
    return sections


def build_stats(notes):
    by_type = {}
    for n in notes:
        by_type.setdefault(n.get("type"), []).append(n)
    projects = by_type.get("project", [])
    total_mw = sum(num_or_none(p.get("capacity_mw")) or 0 for p in projects)
    open_mw = sum(num_or_none(p.get("capacity_mw")) or 0
                  for p in projects if not flat(p.get("oem")))
    return [
        ("累计条目", "%d" % len(notes), ""),
        ("在库项目", "%d" % len(projects), "合计 %s MW" % format(int(total_mw), ",")),
        ("整机未定容量", "%s MW" % format(int(open_mw), ","),
         "占 %.0f%%" % (100.0 * open_mw / total_mw) if total_mw else ""),
        ("高机会项目", "%d" % sum(1 for p in projects if flat(p.get("opportunity")) == "高"), "个"),
        ("竞对动态", "%d" % len(by_type.get("competitor", [])), "条"),
        ("已失单", "%d" % sum(1 for p in projects if flat(p.get("opportunity")) == "已失单"), "个"),
    ]


# ---------------------------------------------------------------- 模板

CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#f6f8fb; --panel:#fff; --line:#dfe5ee; --line2:#eef2f7;
  --ink:#14213d; --ink2:#5b6b82; --ink3:#8a97a9;
  --brand:#1b3a5c; --brand2:#3d6ea5; --accent:#0d7ea8;
  --hot:#c0392b; --hotbg:#fdecea; --warm:#b7791f; --warmbg:#fdf4e3;
  --cool:#3d6ea5; --coolbg:#eaf1f9; --dead:#7a8595; --deadbg:#eef0f3;
  --done:#2d7a4f; --donebg:#e8f5ee;
  --shadow:0 1px 2px rgba(20,33,61,.06),0 4px 16px rgba(20,33,61,.06);
}
@media (prefers-color-scheme:dark){:root{
  --bg:#0d1622; --panel:#131f30; --line:#25344a; --line2:#1c2939;
  --ink:#e6edf6; --ink2:#9fb0c6; --ink3:#6c7d94;
  --brand:#8fb8e0; --brand2:#7aa5d2; --accent:#4fb3d9;
  --hot:#ff8a7a; --hotbg:#3a1f1c; --warm:#e0b45f; --warmbg:#352a15;
  --cool:#8fb8e0; --coolbg:#1a2942; --dead:#8593a6; --deadbg:#1e2733;
  --done:#6ec696; --donebg:#16301f;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 4px 16px rgba(0,0,0,.25);
}}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font:14px/1.55 "Noto Sans SC","PingFang SC","Microsoft YaHei",system-ui,-apple-system,"Segoe UI",sans-serif}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1680px;margin:0 auto;padding:22px 20px 60px}

header.top{display:flex;flex-wrap:wrap;gap:14px;align-items:baseline;margin-bottom:16px}
header.top h1{margin:0;font-size:21px;font-weight:700;letter-spacing:.2px;color:var(--brand)}
.sub{color:var(--ink3);font-size:12.5px}
.topnav{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap}
.topnav a{border:1px solid var(--line);background:var(--panel);padding:6px 12px;
  border-radius:7px;font-size:12.5px;color:var(--ink2);white-space:nowrap}
.topnav a:hover{border-color:var(--brand2);color:var(--brand2);text-decoration:none}

.stats{display:grid;gap:10px;margin-bottom:18px;
  grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;
  padding:11px 13px;box-shadow:var(--shadow)}
.stat b{display:block;font-size:20px;font-weight:700;line-height:1.25;color:var(--brand)}
.stat span{display:block;font-size:11.5px;color:var(--ink3);margin-top:1px}
.stat em{font-style:normal;font-size:11.5px;color:var(--ink2)}

.tabs{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:-1px;position:relative;z-index:2}
.tab{appearance:none;border:1px solid var(--line);border-bottom-color:transparent;
  background:transparent;color:var(--ink2);font:inherit;font-size:13px;cursor:pointer;
  padding:8px 15px;border-radius:9px 9px 0 0}
.tab:hover{color:var(--brand2)}
.tab[aria-selected="true"]{background:var(--panel);color:var(--brand);font-weight:600;
  border-color:var(--line);border-bottom-color:var(--panel)}
.tab .n{color:var(--ink3);font-weight:400;font-size:11.5px;margin-left:5px}
.tab.hit .n{color:var(--hot);font-weight:700}
.tab.miss{opacity:.42}
.tab.miss .n{color:var(--ink3)}

.panel{background:var(--panel);border:1px solid var(--line);border-radius:0 10px 10px 10px;
  box-shadow:var(--shadow);overflow:hidden}
.toolbar{display:flex;gap:9px;flex-wrap:wrap;align-items:center;
  padding:12px 14px;border-bottom:1px solid var(--line2)}
.search{flex:1 1 260px;min-width:200px;position:relative}
.search input{width:100%;padding:8px 11px 8px 31px;border:1px solid var(--line);
  border-radius:7px;background:var(--bg);color:var(--ink);font:inherit;font-size:13px}
.search input:focus{outline:none;border-color:var(--brand2);
  box-shadow:0 0 0 3px color-mix(in srgb,var(--brand2) 18%,transparent)}
.search svg{position:absolute;left:9px;top:50%;transform:translateY(-50%);
  width:14px;height:14px;stroke:var(--ink3);fill:none;stroke-width:2}
select.f{padding:7px 9px;border:1px solid var(--line);border-radius:7px;
  background:var(--bg);color:var(--ink);font:inherit;font-size:12.5px;max-width:190px}
select.f:focus{outline:none;border-color:var(--brand2)}
select.f.on{border-color:var(--brand2);color:var(--brand2);font-weight:600}
.reset{border:1px solid var(--line);background:var(--bg);color:var(--ink2);
  font:inherit;font-size:12.5px;padding:7px 12px;border-radius:7px;cursor:pointer}
.reset:hover{border-color:var(--hot);color:var(--hot)}
.count{margin-left:auto;font-size:12.5px;color:var(--ink3);white-space:nowrap}
.count b{color:var(--brand);font-weight:700}

.scroll{overflow:auto;max-height:min(72vh,900px)}
table{border-collapse:separate;border-spacing:0;width:100%;font-size:13px}
th,td{padding:8px 11px;text-align:left;vertical-align:top;
  border-bottom:1px solid var(--line2)}
thead th{position:sticky;top:0;z-index:1;background:var(--panel);
  font-size:11.5px;font-weight:600;color:var(--ink2);letter-spacing:.4px;
  white-space:nowrap;cursor:pointer;user-select:none;border-bottom:1.5px solid var(--line)}
thead th:hover{color:var(--brand2)}
thead th .ar{opacity:0;margin-left:3px;font-size:9px}
thead th.asc .ar,thead th.desc .ar{opacity:1;color:var(--brand2)}
thead th.desc .ar::after{content:"▼"}
thead th.asc .ar::after{content:"▲"}
tbody tr:hover{background:color-mix(in srgb,var(--brand2) 6%,transparent)}
tbody tr:last-child td{border-bottom:none}
td{max-width:0}
.c-xs{width:66px}.c-sm{width:96px}.c-date{width:96px;white-space:nowrap;color:var(--ink2);font-variant-numeric:tabular-nums}
.c-md{width:160px}.c-lg{width:240px}.c-xl{width:340px}
.c-num{width:82px;text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.c-src{width:52px;text-align:center}
.c-tag{width:74px}
.clip{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.c-xl .clip{white-space:normal;display:-webkit-box;-webkit-line-clamp:2;
  -webkit-box-orient:vertical;color:var(--ink2);font-size:12.5px}
.ttl{font-weight:600;color:var(--ink)}
.ttl:hover{color:var(--accent)}
.empty-oem{color:var(--hot);font-size:11.5px;font-weight:600}
.src{display:inline-block;width:22px;height:22px;line-height:21px;text-align:center;
  border:1px solid var(--line);border-radius:5px;color:var(--ink3);font-size:11px}
.src:hover{border-color:var(--accent);color:var(--accent);text-decoration:none}

.tag{display:inline-block;padding:1.5px 8px;border-radius:20px;font-size:11.5px;
  font-weight:600;white-space:nowrap;background:var(--deadbg);color:var(--dead)}
.t-hot{background:var(--hotbg);color:var(--hot)}
.t-warm{background:var(--warmbg);color:var(--warm)}
.t-cool{background:var(--coolbg);color:var(--cool)}
.t-dead{background:var(--deadbg);color:var(--dead)}
.t-done{background:var(--donebg);color:var(--done)}

.none{padding:44px 20px;text-align:center;color:var(--ink3);font-size:13.5px}
footer{margin-top:22px;color:var(--ink3);font-size:12px;line-height:1.7}
footer code{background:var(--line2);padding:1px 5px;border-radius:4px;font-size:11.5px}

@media (max-width:820px){
  .wrap{padding:14px 12px 40px}
  header.top h1{font-size:18px}
  .topnav{margin-left:0;width:100%}
  .panel{border-radius:10px}
  .tabs{overflow-x:auto;flex-wrap:nowrap;padding-bottom:2px}
  .tab{white-space:nowrap}
  .scroll{max-height:none}
  .count{margin-left:0;width:100%}
}
"""

JS = r"""
const DATA = __DATA__;
const TONE = __TONE__;
const $ = (s, r) => (r || document).querySelector(s);
const esc = s => String(s == null ? "" : s)
  .replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");

let cur = DATA[0] ? DATA[0].key : null;
let query = "";                        // 搜索词全局共享，切 Tab 时保留
const state = {};                      // key -> {filters:{}, sort:{field,dir}}
DATA.forEach(s => state[s.key] = {filters:{}, sort:null});

function tone(v){ return TONE[v] || ""; }
function isNum(v){ return v !== "" && v != null && !isNaN(parseFloat(String(v).replace(/,/g,""))); }

function terms(){
  const q = query.trim().toLowerCase();
  return q ? q.split(/\s+/) : [];
}

function matchQ(r, ts){ return ts.every(t => r._hay.indexOf(t) !== -1); }

function visible(sec){
  const st = state[sec.key], ts = terms();
  return sec.rows.filter(r => {
    for (const f in st.filters){
      if (st.filters[f] && r[f] !== st.filters[f]) return false;
    }
    return matchQ(r, ts);
  });
}

/* Tab 徽标：无搜索词时显示总条数，有搜索词时显示该板块的命中数，
   这样搜「越南」能一眼看到它在竞对、政策、投融资里各命中几条。 */
function paintTabs(){
  const ts = terms();
  document.querySelectorAll(".tab").forEach(b => {
    const sec = DATA.find(s => s.key === b.dataset.k);
    const n = ts.length ? sec.rows.filter(r => matchQ(r, ts)).length : sec.rows.length;
    const badge = b.querySelector(".n");
    badge.textContent = n;
    b.classList.toggle("hit", ts.length > 0 && n > 0);
    b.classList.toggle("miss", ts.length > 0 && n === 0);
  });
}

function sortRows(rows, sort){
  if (!sort) return rows;
  const {field, dir} = sort;
  const out = rows.slice();
  out.sort((a,b) => {
    const x = a[field] ?? "", y = b[field] ?? "";
    if (x === "" && y === "") return 0;
    if (x === "") return 1;              // 空值永远沉底
    if (y === "") return -1;
    let c;
    if (isNum(x) && isNum(y)) c = parseFloat(String(x).replace(/,/g,"")) - parseFloat(String(y).replace(/,/g,""));
    else c = String(x).localeCompare(String(y), "zh-Hans-CN");
    return dir === "desc" ? -c : c;
  });
  return out;
}

function cellHtml(sec, col, r){
  if (col.f === "__link__")
    return '<a class="clip ttl" href="'+esc(r._url)+'" title="'+esc(r._label)+'">'+esc(r._label)+"</a>";
  if (col.f === "__src__")
    return r._src ? '<a class="src" href="'+esc(r._src)+'" target="_blank" rel="noopener" title="打开原文">↗</a>' : "";
  const v = r[col.f] ?? "";
  if (col.c === "c-tag" && v) return '<span class="tag '+tone(v)+'">'+esc(v)+"</span>";
  if (col.f === "oem" && !v) return '<span class="empty-oem">未定</span>';
  if (!v) return "";
  return '<span class="clip" title="'+esc(v)+'">'+esc(v)+"</span>";
}

function render(){
  const sec = DATA.find(s => s.key === cur);
  if (!sec) return;
  const st = state[sec.key];
  let rows = sortRows(visible(sec), st.sort);

  $("#count").innerHTML = "<b>"+rows.length+"</b> / "+sec.rows.length+" 条";
  paintTabs();

  const th = sec.columns.map(c => {
    let cls = c.c;
    if (st.sort && st.sort.field === c.f) cls += " " + st.sort.dir;
    const sf = (c.f === "__link__") ? "_label" : c.f;
    return '<th class="'+cls+'" data-sf="'+esc(sf)+'">'+esc(c.h)+'<span class="ar"></span></th>';
  }).join("");

  const body = rows.map(r =>
    "<tr>" + sec.columns.map(c => '<td class="'+c.c+'">'+cellHtml(sec,c,r)+"</td>").join("") + "</tr>"
  ).join("");

  $("#tablewrap").innerHTML = rows.length
    ? '<div class="scroll"><table><thead><tr>'+th+"</tr></thead><tbody>"+body+"</tbody></table></div>"
    : '<div class="none">没有匹配的记录 —— 换个关键词，或点「重置」清掉筛选条件。</div>';

  document.querySelectorAll("#tablewrap th").forEach(el => {
    el.onclick = () => {
      const f = el.dataset.sf;
      st.sort = (st.sort && st.sort.field === f && st.sort.dir === "asc")
        ? {field:f, dir:"desc"} : {field:f, dir:"asc"};
      render();
    };
  });
}

function buildToolbar(){
  const sec = DATA.find(s => s.key === cur);
  const st = state[sec.key];
  const fs = sec.facets.map(f => {
    const opts = ['<option value="">'+esc(f.label)+"：全部</option>"]
      .concat(f.values.map(v =>
        '<option value="'+esc(v)+'"'+(st.filters[f.field]===v?" selected":"")+">"+esc(v)+"</option>"));
    return '<select class="f'+(st.filters[f.field]?" on":"")+'" data-f="'+esc(f.field)+'">'+opts.join("")+"</select>";
  }).join("");

  $("#filters").innerHTML = fs;
  $("#q").value = query;
  $("#q").placeholder = "搜索全部 " + DATA.reduce((a,s)=>a+s.rows.length,0) + " 条记录…（空格分隔多个词，如：越南 海上）";

  document.querySelectorAll("#filters select").forEach(el => {
    el.onchange = () => { st.filters[el.dataset.f] = el.value; buildToolbar(); render(); };
  });
}

function switchTab(key){
  cur = key;
  document.querySelectorAll(".tab").forEach(b =>
    b.setAttribute("aria-selected", String(b.dataset.k === key)));
  buildToolbar();
  render();
}

document.addEventListener("DOMContentLoaded", () => {
  $("#tabs").innerHTML = DATA.map((s,i) =>
    '<button class="tab" role="tab" data-k="'+esc(s.key)+'" aria-selected="'+(i===0)+'">'
    + esc(s.title) + '<span class="n">'+s.rows.length+"</span></button>").join("");
  document.querySelectorAll(".tab").forEach(b => b.onclick = () => switchTab(b.dataset.k));

  let timer;
  $("#q").addEventListener("input", e => {
    clearTimeout(timer);
    const v = e.target.value;
    timer = setTimeout(() => { query = v; render(); }, 120);
  });
  $("#reset").onclick = () => {
    query = "";
    state[cur] = {filters:{}, sort:null};
    buildToolbar(); render(); $("#q").focus();
  };
  document.addEventListener("keydown", e => {
    if (e.key === "/" && document.activeElement !== $("#q")) { e.preventDefault(); $("#q").focus(); }
    if (e.key === "Escape" && document.activeElement === $("#q")) $("#q").blur();
  });

  if (cur) switchTab(cur);
});
"""

PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="全球风电行业项目、政策、竞对与投融资数据库，每日自动更新。">
<meta name="robots" content="{robots}">
<style>{css}</style>
</head>
<body>
<div class="wrap">

<header class="top">
  <h1>{title}</h1>
  <span class="sub">数据截至 {updated} · 每日自动更新</span>
  <nav class="topnav">
    <a href="总览.html">📄 笔记详情站</a>
    <a href="说明/字段规范.html">字段说明</a>
  </nav>
</header>

<div class="stats">{stats}</div>

<div class="tabs" id="tabs" role="tablist"></div>

<div class="panel">
  <div class="toolbar">
    <div class="search">
      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
      <input id="q" type="search" autocomplete="off" aria-label="搜索">
    </div>
    <span id="filters" style="display:contents"></span>
    <button class="reset" id="reset" type="button">重置</button>
    <span class="count" id="count"></span>
  </div>
  <div id="tablewrap"></div>
</div>

<footer>
  点列头排序 · 按 <code>/</code> 快速搜索 · 点项目名进详情页看完整分析 · 点 <code>↗</code> 打开原文<br>
  「整机商」列显示<b>未定</b>即该项目整机尚未定标。数据来自公开渠道整理，引用请核对原文。
</footer>

</div>
<script>{js}</script>
</body>
</html>
"""


def render_stats(stats):
    out = []
    for label, value, note in stats:
        out.append(
            '<div class="stat"><b>%s</b><span>%s</span>%s</div>'
            % (html.escape(value), html.escape(label),
               ('<em>%s</em>' % html.escape(note)) if note else "")
        )
    return "".join(out)


def main():
    argv = [a for a in sys.argv[1:]]
    include_internal = "--with-strategy" in argv or os.environ.get("PUBLISH_STRATEGY") == "1"
    argv = [a for a in argv if a != "--with-strategy"]

    out_path = None
    if "-o" in argv:
        i = argv.index("-o")
        out_path = argv[i + 1]
        del argv[i:i + 2]

    vault = os.path.abspath(argv[0]) if argv else find_vault()
    if not os.path.isdir(vault):
        print("找不到 vault: %s" % vault)
        return 1
    if not out_path:
        out_path = os.path.join(vault, "看板.html")

    notes = read_notes(vault)
    drafts = [n for n in notes if is_draft(n)]
    sections = build_payload(notes, include_internal)
    stats = build_stats([n for n in notes if not is_draft(n)])

    js = (JS.replace("__DATA__", json.dumps(sections, ensure_ascii=False, separators=(",", ":")))
            .replace("__TONE__", json.dumps(TAG_TONE, ensure_ascii=False)))

    page = PAGE.format(
        title="全球风电行业数据库",
        updated=datetime.date.today().isoformat(),
        robots="index,follow" if not include_internal else "noindex,nofollow",
        css=CSS,
        stats=render_stats(stats),
        js=js,
    )

    out_dir = os.path.dirname(os.path.abspath(out_path))
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    with io.open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)

    print("已生成看板: %s" % out_path)
    for s in sections:
        print("  %-10s %3d 条  (%d 个筛选器)" % (s["title"], len(s["rows"]), len(s["facets"])))
    if include_internal:
        print("  ⚠ 已包含 07-战略判断（内部敏感），该页已标 noindex")
    else:
        print("  · 07-战略判断 未导出（如需发布：--with-strategy）")
    if drafts:
        print("  · 已跳过 %d 条 draft: true 的笔记：%s"
              % (len(drafts), "、".join(d["__basename__"] for d in drafts[:5])))
    print("  文件大小 %.0f KB" % (os.path.getsize(out_path) / 1024.0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
