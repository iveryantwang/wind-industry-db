# -*- coding: utf-8 -*-
"""
风电行业数据库 —— 静态表格重建脚本
=====================================
作用：扫描 vault 内所有笔记的 YAML frontmatter，把汇总表格以「静态 Markdown 表格」
      写回各索引页的 <!-- AUTO-TABLE --> 区块，并刷新 00-总览 的统计与高亮。

为什么需要它：Obsidian Publish 不渲染 Dataview 查询。本地用 Dataview 灵活筛选，
              发布页则读取脚本生成的静态表格，两边都能看到数据。

安全性：脚本只改写标记区块之间的内容，绝不触碰笔记正文与 frontmatter。
        标记为 manual: true 的笔记同样只被读取，永不被修改。

运行：python rebuild_tables.py            # 自动定位 vault 根目录
      python rebuild_tables.py <vault路径>
仅依赖 Python 3 标准库。
"""

import os
import re
import sys
import io
import datetime

# ---------------------------------------------------------------- 配置

SECTIONS = [
    {
        "folder": "01-每日新闻",
        "index": "01-每日新闻/_索引-每日新闻.md",
        "type": "news",
        "sort": ("date", True),
        "limit": 400,
        "columns": [
            ("date", "日期", 12),
            ("__link__", "标题", 70),
            ("region", "区域", 10),
            ("country", "国别", 12),
            ("segment", "板块", 8),
            ("importance", "重要性", 6),
            ("source_name", "来源", 18),
        ],
        "link_title_field": "title",
    },
    {
        "folder": "02-客户与项目",
        "index": "02-客户与项目/_索引-客户与项目.md",
        "type": "project",
        "sort": ("capacity_mw", True),
        "limit": 1000,
        "columns": [
            ("opportunity", "机会", 6),
            ("region", "区域", 10),
            ("country", "国别", 12),
            ("customer", "业主/客户", 30),
            ("__link__", "项目", 40),
            ("capacity_mw", "容量MW", 8),
            ("unit_mw", "单机MW", 6),
            ("turbine_count", "台数", 6),
            ("segment", "类型", 8),
            ("status", "状态", 10),
            ("oem", "整机商（空=未定）", 16),
            ("cod_year", "并网年", 6),
        ],
        "link_title_field": "project",
    },
    {
        "folder": "03-风电政策",
        "index": "03-风电政策/_索引-风电政策.md",
        "type": "policy",
        "sort": ("issued", True),
        "limit": 500,
        "columns": [
            ("region", "区域", 10),
            ("country", "国别", 12),
            ("__link__", "政策名称", 46),
            ("issued", "发布日期", 12),
            ("issuer", "发布机构", 22),
            ("impact_level", "影响", 6),
            ("summary", "核心内容", 90),
        ],
        "link_title_field": "policy",
    },
    {
        "folder": "04-竞争对手",
        "index": "04-竞争对手/_索引-竞争对手.md",
        "type": "competitor",
        "sort": ("date", True),
        "limit": 500,
        "columns": [
            ("date", "日期", 12),
            ("country", "国别", 12),
            ("competitor", "竞争对手", 20),
            ("event_type", "动态类型", 10),
            ("__link__", "内容", 46),
            ("counterparty", "签约客户", 22),
            ("contract_value", "合同金额", 14),
            ("capacity_mw", "容量MW", 8),
            ("turbine_count", "台数", 6),
        ],
        "link_title_field": "competitor",
    },
    {
        "folder": "05-技术方案",
        "index": "05-技术方案/_索引-技术方案.md",
        "type": "tech",
        "sort": ("date", True),
        "limit": 500,
        "columns": [
            ("country", "国别", 12),
            ("__link__", "技术方案/场景", 40),
            ("provider", "提供方", 20),
            ("use_case", "应用场景", 24),
            ("maturity", "成熟度", 8),
            ("description", "描述", 80),
            ("date", "日期", 12),
        ],
        "link_title_field": "solution",
    },
    {
        "folder": "06-投资财务",
        "index": "06-投资财务/_索引-投资财务.md",
        "type": "finance",
        "sort": ("date", True),
        "limit": 500,
        "columns": [
            ("country", "国别", 12),
            ("__link__", "项目/模型", 40),
            ("capex", "投资规模", 16),
            ("irr", "IRR", 10),
            ("lcoe", "LCOE", 12),
            ("biz_model", "商业模式", 16),
            ("funding", "资金来源", 22),
            ("date", "日期", 12),
        ],
        "link_title_field": "subject",
    },
    {
        "folder": "07-战略判断",
        "index": "07-战略判断/_索引-战略判断.md",
        "type": "strategy",
        "sort": ("priority", False),
        "limit": 500,
        "columns": [
            ("priority", "优先级", 6),
            ("country", "国别", 12),
            ("owner_party", "业主/开发商", 30),
            ("__link__", "项目", 36),
            ("capacity_mw", "容量MW", 8),
            ("action", "建议行动", 70),
            ("deadline", "行动窗口", 12),
            ("status", "状态", 8),
        ],
        "link_title_field": "project",
    },
]

SKIP_FOLDERS = {".obsidian", ".git", ".trash", "90-模板", "99-系统"}

# 这些 type 是页面骨架，不算数据条目
META_TYPES = {"index", "dashboard", "log", "template", "doc"}


# ---------------------------------------------------------------- YAML 解析

def parse_frontmatter(text):
    """极简 frontmatter 解析器，只处理本库使用的 key: value / key: [a,b] 形式。"""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    data = {}
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith(" ") or line.startswith("\t"):
            continue  # 不支持嵌套，忽略
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        # 去掉行内注释（仅当 # 前有空格且不在引号内）
        if val and not val.startswith(('"', "'")):
            m = re.search(r"\s+#", val)
            if m:
                val = val[: m.start()].strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            data[key] = [x.strip().strip("\"'") for x in inner.split(",") if x.strip()] if inner else []
        else:
            if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
                val = val[1:-1]
            data[key] = val
    return data


def read_notes(vault):
    notes = []
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in SKIP_FOLDERS and not d.startswith(".")]
        rel_root = os.path.relpath(root, vault)
        if rel_root != "." and rel_root.split(os.sep)[0] in SKIP_FOLDERS:
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            if fn.startswith("_") or fn.startswith("模板-"):
                continue
            path = os.path.join(root, fn)
            try:
                with io.open(path, "r", encoding="utf-8") as f:
                    text = f.read()
            except Exception as e:
                print("  ! 读取失败 %s: %s" % (path, e))
                continue
            fm = parse_frontmatter(text)
            if not fm.get("type") or fm.get("type") in META_TYPES:
                continue
            fm["__basename__"] = fn[:-3]
            fm["__path__"] = path
            notes.append(fm)
    return notes


# ---------------------------------------------------------------- 表格渲染

def cell(value, width):
    if value is None:
        return ""
    if isinstance(value, list):
        value = " / ".join(str(v) for v in value)
    s = str(value).strip()
    s = s.replace("|", "\\|").replace("\n", " ").replace("\r", "")
    if width and len(s) > width:
        s = s[: width - 1] + "…"
    return s


def wiki_link(note, title_field):
    base = note["__basename__"]
    label = note.get(title_field) or ""
    if isinstance(label, list):
        label = " ".join(str(x) for x in label)
    label = str(label).strip()
    if not label:
        label = base
    label = label.replace("|", "\\|").replace("]", "］").replace("[", "［")
    if len(label) > 70:
        label = label[:69] + "…"
    if label == base:
        return "[[%s]]" % base
    return "[[%s\\|%s]]" % (base, label)


def sort_key_factory(field):
    def key(n):
        v = n.get(field)
        if v in (None, "", []):
            return (1, "")
        try:
            return (0, float(str(v)))
        except (ValueError, TypeError):
            return (0, str(v))
    return key


def render_table(notes, spec):
    field, desc = spec["sort"]
    rows = sorted(notes, key=sort_key_factory(field), reverse=desc)
    # 数值降序时空值应排在最后，上面的 (1,"") 在 reverse 下会跑到最前，修正一下
    if desc:
        filled = [n for n in rows if n.get(field) not in (None, "", [])]
        empty = [n for n in rows if n.get(field) in (None, "", [])]
        rows = filled + empty
    rows = rows[: spec["limit"]]

    if not rows:
        return "_暂无数据。用 `90-模板/` 下的对应模板新建笔记，或等待每日自动更新。_"

    heads = [h for (_, h, _) in spec["columns"]]
    out = ["| " + " | ".join(heads) + " |",
           "|" + "|".join(["---"] * len(heads)) + "|"]
    for n in rows:
        cells = []
        for (fld, _h, width) in spec["columns"]:
            if fld == "__link__":
                cells.append(wiki_link(n, spec["link_title_field"]))
            else:
                cells.append(cell(n.get(fld), width))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def replace_block(text, marker, new_body):
    start = "<!-- %s:START -->" % marker
    end = "<!-- %s:END -->" % marker
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    replacement = start + "\n" + new_body + "\n" + end
    if not pat.search(text):
        return text, False
    return pat.sub(lambda _m: replacement, text, count=1), True


def write_block(path, marker, body):
    if not os.path.exists(path):
        print("  ! 索引页不存在: %s" % path)
        return False
    with io.open(path, "r", encoding="utf-8") as f:
        text = f.read()
    new_text, ok = replace_block(text, marker, body)
    if not ok:
        print("  ! 未找到标记 %s: %s" % (marker, path))
        return False
    if new_text != text:
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_text)
    return True


# ---------------------------------------------------------------- 总览

def build_stats(by_type, notes):
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)

    def recent_count(items, field):
        c = 0
        for n in items:
            d = str(n.get(field) or "")[:10]
            try:
                if datetime.date.fromisoformat(d) >= week_ago:
                    c += 1
            except ValueError:
                pass
        return c

    total = len(notes)
    news = by_type.get("news", [])
    projects = by_type.get("project", [])
    total_mw = 0.0
    for p in projects:
        try:
            total_mw += float(str(p.get("capacity_mw") or 0))
        except ValueError:
            pass

    lines = [
        "| 指标 | 数值 |",
        "|---|---|",
        "| 累计条目 | **%d** |" % total,
        "| 客户与项目 | **%d** 个（合计 %s MW） |" % (len(projects), ("%.0f" % total_mw) if total_mw else "—"),
        "| 竞争对手动态 | **%d** 条 |" % len(by_type.get("competitor", [])),
        "| 风电政策 | **%d** 条 |" % len(by_type.get("policy", [])),
        "| 技术方案 | **%d** 条 |" % len(by_type.get("tech", [])),
        "| 投资财务 | **%d** 条 |" % len(by_type.get("finance", [])),
        "| 战略判断事项 | **%d** 项（P0: %d） |" % (
            len(by_type.get("strategy", [])),
            sum(1 for s in by_type.get("strategy", []) if str(s.get("priority", "")).upper() == "P0"),
        ),
        "| 近 7 天新增新闻 | **%d** 条 |" % recent_count(news, "date"),
        "| 最后更新 | %s |" % today.isoformat(),
    ]
    return "\n".join(lines)


def build_highlight(by_type):
    """最新 15 条标记为「高」重要性的新闻，不设日期下限，避免首日为空。"""
    picked = []
    for n in by_type.get("news", []):
        d = str(n.get("date") or "")[:10]
        try:
            dt = datetime.date.fromisoformat(d)
        except ValueError:
            continue
        if str(n.get("importance", "")).strip() in ("高", "High", "high"):
            picked.append((dt, n))
    picked.sort(key=lambda x: x[0], reverse=True)
    if not picked:
        return "_暂无标记为「高」重要性的动态。_"
    out = []
    for dt, n in picked[:15]:
        out.append("- `%s` %s — %s" % (
            dt.isoformat(),
            wiki_link(n, "title"),
            cell(n.get("summary"), 120) or "",
        ))
    return "\n".join(out)


def append_log(vault, summary_lines):
    path = os.path.join(vault, "99-系统", "更新日志.md")
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = "\n## %s\n\n%s\n" % (stamp, "\n".join("- " + s for s in summary_lines))
    header = """---
type: log
publish: true
---

# 更新日志

> 每次自动更新的记录，最新在最上方。
"""
    if os.path.exists(path):
        with io.open(path, "r", encoding="utf-8") as f:
            text = f.read()
        idx = text.find("\n## ")
        if idx == -1:
            text = text.rstrip() + "\n" + entry
        else:
            text = text[:idx] + entry + text[idx:]
    else:
        text = header + entry
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


# ---------------------------------------------------------------- 主流程

def find_vault():
    if len(sys.argv) > 1:
        return os.path.abspath(sys.argv[1])
    here = os.path.dirname(os.path.abspath(__file__))
    # scripts -> 99-系统 -> vault根
    return os.path.abspath(os.path.join(here, "..", ".."))


def main():
    vault = find_vault()
    if not os.path.isdir(vault):
        print("找不到 vault: %s" % vault)
        return 1
    print("Vault: %s" % vault)

    notes = read_notes(vault)
    by_type = {}
    for n in notes:
        by_type.setdefault(n["type"], []).append(n)

    log = []
    for spec in SECTIONS:
        items = [n for n in by_type.get(spec["type"], [])]
        body = render_table(items, spec)
        ok = write_block(os.path.join(vault, spec["index"].replace("/", os.sep)), "AUTO-TABLE", body)
        status = "OK" if ok else "跳过"
        print("  [%s] %-14s %d 条" % (status, spec["folder"], len(items)))
        log.append("%s：%d 条" % (spec["folder"], len(items)))

    overview = os.path.join(vault, "00-总览.md")
    write_block(overview, "AUTO-STATS", build_stats(by_type, notes))
    write_block(overview, "AUTO-HIGHLIGHT", build_highlight(by_type))
    print("  [OK] 00-总览 统计与高亮已刷新")

    append_log(vault, log + ["总条目：%d" % len(notes)])
    print("完成。总条目 %d" % len(notes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
