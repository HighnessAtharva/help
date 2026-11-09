#!/usr/bin/env python3
"""Newsletter Clicks analyzer for AccuKnox newsletter statistics exports.

Input: a folder or .zip with one subfolder per email list. Each list folder holds
four Excel files: bounce_, unsubscribe_, open_click_ and click_details_.

Output: report.html, summary.json, link_table.csv and human_clickers.csv.
The output holds customer emails. Never write it inside a git repo.

Run with: python3 -I analyze.py --input <dir or zip> [--sent "NAT CRM=12000,TGACRM=20000"]
Needs only openpyxl.
"""
import argparse
import collections
import csv
import html
import json
import math
import re
import sys
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse

import openpyxl

EXPECTED_LISTS = ["NAT CRM", "TGACRM"]
KINDS = {
    "bounce_": "bounce",
    "unsubscribe_": "unsub",
    "open_click_": "open_click",
    "click_details_": "click_details",
}
HEADERS = {
    "bounce": ["First Name", "Last Name", "Email", "Mail State"],
    "unsub": ["First Name", "Last Name", "Email", "Mail State"],
    "open_click": ["First Name", "Last Name", "Email", "Mail State"],
    "click_details": ["First Name", "Last Name", "Email", "Clicked Link"],
}
TEMPLATE_SHARE = 0.5      # a link clicked by this share of clickers is a newsletter link
SCANNER_COVERAGE = 0.8    # a clicker who hit this share of newsletter links is a machine
MIN_TEMPLATE_LINKS = 3    # below this the scanner test is not reliable
BOUNCE_LIMIT = 0.02       # bounce rate of sent mail above this needs list cleaning
UNSUB_LIMIT = 0.003
MONTHS = ("january february march april may june july august september "
          "october november december").split()


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def pct(a, b):
    return f"{100.0 * a / b:.1f}%" if b else "n/a"


def read_sheet(path):
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb.worksheets[0]
    it = ws.iter_rows(values_only=True)
    header = [str(c).strip() if c is not None else "" for c in next(it, [])]
    rows = [r for r in it if r and any(c not in (None, "") for c in r)]
    return ws.title, header, rows


def clean_url(u):
    p = urlparse(u.strip())
    q = [(k, v) for k, v in parse_qsl(p.query) if not (k.startswith("utm_") or k == "si")]
    return p._replace(query=urlencode(q), fragment="").geturl().rstrip("/")


def link_type(u):
    p = urlparse(u)
    host = p.netloc.lower().removeprefix("www.")
    seg = p.path.strip("/").split("/")[0]
    if host.endswith("youtube.com") or host == "youtu.be":
        return "youtube"
    if host.endswith("accuknox.com"):
        return seg or "home"
    return host


def short(u, n=70):
    u = re.sub(r"^https?://(www\.)?", "", u)
    return u if len(u) <= n else u[: n - 1] + "…"


def find_lists(root):
    groups = collections.defaultdict(list)
    for f in sorted(root.rglob("*.xlsx")):
        if "__MACOSX" in f.parts or f.name.startswith("~$"):
            continue
        groups[f.parent].append(f)
    return groups


def load_list(name, files, checks):
    d = {"name": name, "files": {}, "campaign_id": None, "tags": set(), "months": set()}
    for f in files:
        kind = next((k for p, k in KINDS.items() if f.name.lower().startswith(p)), None)
        if not kind:
            checks.append(("WARN", f"{name}: unknown file", f.name))
            continue
        if kind in d["files"]:
            checks.append(("WARN", f"{name}: two {kind} files", f"using {d['files'][kind].name}, ignoring {f.name}"))
            continue
        d["files"][kind] = f
        m = re.search(r"AccuKnox_Newsletter_([A-Za-z0-9]+)", f.stem)
        if m:
            d["tags"].add(m.group(1))
        d["months"].update(w for w in MONTHS if w in f.stem.lower())
    for kind in KINDS.values():
        if kind not in d["files"]:
            note = "click-level analysis is impossible for this list" if kind == "click_details" else "file is required"
            checks.append(("FAIL", f"{name}: {kind} file missing", note))
    d["data"] = {}
    for kind, f in d["files"].items():
        title, header, rows = read_sheet(f)
        if header != HEADERS[kind]:
            checks.append(("FAIL", f"{name}: {kind} headers", f"found {header}"))
            continue
        if not rows:
            checks.append(("FAIL", f"{name}: {kind} file empty", f.name))
        m = re.search(r"(\d+)\s*$", title)
        if m:
            d["campaign_id"] = d["campaign_id"] or m.group(1)
        d["data"][kind] = rows
        if kind != "click_details":
            em = [(r[2] or "").strip().lower() for r in rows]
            dup = len(em) - len(set(em))
            if dup:
                checks.append(("WARN", f"{name}: {kind} duplicate emails", f"{dup} repeated rows"))
    if d["tags"] and norm(name) not in {norm(t) for t in d["tags"]}:
        checks.append(("WARN", f"{name}: file names use another list tag", f"folder '{name}', files '{', '.join(sorted(d['tags']))}'"))
    return d


def analyze_list(d):
    r = {"name": d["name"], "campaign_id": d["campaign_id"]}
    oc = d["data"].get("open_click", [])
    state = {(x[2] or "").strip().lower(): x[3] for x in oc}
    r["tracked"] = len(state)
    r["click_state"] = sum(1 for s in state.values() if s == "Click")
    r["open_state"] = sum(1 for s in state.values() if s == "Open")
    r["bounced"] = len({(x[2] or "").strip().lower() for x in d["data"].get("bounce", [])})
    r["unsub"] = len({(x[2] or "").strip().lower() for x in d["data"].get("unsub", [])})
    r["has_details"] = "click_details" in d["data"]
    d["state"] = state
    if not r["has_details"]:
        return r
    per = collections.defaultdict(list)
    for x in d["data"]["click_details"]:
        if x[2] and x[3]:
            per[x[2].strip().lower()].append(clean_url(x[3]))
    clickers = len(per)
    link_clickers = collections.defaultdict(set)
    for e, v in per.items():
        for u in set(v):
            link_clickers[u].add(e)
    tpl = [u for u, s in link_clickers.items() if clickers and len(s) / clickers >= TEMPLATE_SHARE]
    need = math.ceil(SCANNER_COVERAGE * len(tpl))
    reliable = len(tpl) >= MIN_TEMPLATE_LINKS
    scanners = {e for e, v in per.items() if reliable and len(set(v) & set(tpl)) >= need}
    humans = {e for e in per if e not in scanners}
    names = {(x[2] or "").strip().lower(): f"{x[0] or ''} {x[1] or ''}".strip() for x in d["data"]["click_details"]}
    r.update(per=per, clickers=clickers, template=tpl, scanner_reliable=reliable,
             scanners=scanners, humans=humans, names=names,
             raw_clicks=sum(len(v) for v in per.values()),
             scanner_clicks=sum(len(per[e]) for e in scanners),
             human_clicks=sum(len(per[e]) for e in humans))
    return r


def build(root, expected, sent, month_arg):
    checks = []
    groups = find_lists(root)
    lists = {}
    for folder, files in groups.items():
        lists[folder.name] = load_list(folder.name, files, checks)
    have = {norm(n): n for n in lists}
    for e in expected:
        if norm(e) in have:
            checks.append(("OK", f"List present: {e}", f"{len(lists[have[norm(e)]]['files'])} of 4 files"))
        else:
            checks.append(("FAIL", f"List missing: {e}", "no folder with this name in the export"))
    for n in lists:
        if norm(n) not in {norm(e) for e in expected}:
            checks.append(("WARN", f"Extra list not in the expected set: {n}", "add it to --expect if it is real"))
    months = set().union(*[d["months"] for d in lists.values()]) if lists else set()
    for n, d in lists.items():
        if not d["months"]:
            checks.append(("WARN", f"{n}: no month in file names", "cannot confirm which month this export covers"))
    if len(months) > 1:
        checks.append(("WARN", "Months differ between lists", ", ".join(sorted(months))))
    ids = collections.Counter(d["campaign_id"] for d in lists.values() if d["campaign_id"])
    for cid, c in ids.items():
        if c > 1:
            checks.append(("WARN", f"Campaign id {cid} appears in {c} lists", "the same send was exported twice"))

    res = {n: analyze_list(d) for n, d in lists.items()}
    for n, d in lists.items():
        r, st = res[n], d["state"]
        bounce_f = {(x[2] or "").strip().lower() for x in d["data"].get("bounce", [])}
        bounce_s = {e for e, s in st.items() if s == "Bounce"}
        if d["data"].get("bounce") is not None and bounce_f != bounce_s:
            checks.append(("WARN", f"{n}: bounce file and open_click disagree", f"file {len(bounce_f)}, open_click {len(bounce_s)}"))
        unsub_f = {(x[2] or "").strip().lower() for x in d["data"].get("unsub", [])}
        unsub_s = {e for e, s in st.items() if s == "Unsubscribe"}
        if unsub_f != unsub_s:
            checks.append(("WARN", f"{n}: unsubscribe file and open_click disagree", f"file {len(unsub_f)}, open_click {len(unsub_s)}"))
        if r["has_details"]:
            det = set(r["per"])
            miss = len(det - set(st))
            if miss:
                checks.append(("WARN", f"{n}: clickers in click_details but not in open_click", f"{miss} people"))
            nodet = len({e for e, s in st.items() if s == "Click"} - det)
            if nodet:
                checks.append(("WARN", f"{n}: Click state with no click detail", f"{nodet} people"))
            op = len({e for e in det if st.get(e) == "Open"})
            if op:
                checks.append(("WARN", f"{n}: marked Open but have click details", f"{op} people"))
            bc = len(det & bounce_f)
            if bc:
                checks.append(("WARN", f"{n}: bounced addresses with click details", f"{bc} people"))
            if not r["scanner_reliable"]:
                checks.append(("WARN", f"{n}: too few newsletter links to detect scanners", f"{len(r['template'])} links"))
    seen = collections.defaultdict(set)
    for n, d in lists.items():
        for e in d["state"]:
            seen[e].add(n)
    both = sum(1 for s in seen.values() if len(s) > 1)
    if both:
        checks.append(("WARN", "Same address on more than one list", f"{both} addresses"))
    for n in lists:
        if norm(n) not in {norm(k) for k in sent}:
            checks.append(("WARN", f"{n}: sent count not given", "rates need --sent"))
    return lists, res, checks, months


def merge_links(res):
    human = collections.defaultdict(set)
    allc = collections.defaultdict(set)
    rawclicks = collections.Counter()
    scan = collections.defaultdict(set)
    tpl = set()
    for r in res.values():
        if not r["has_details"]:
            continue
        tpl.update(r["template"])
        for e, v in r["per"].items():
            for u in v:
                rawclicks[u] += 1
            for u in set(v):
                allc[u].add(e)
                (human if e in r["humans"] else scan)[u].add(e)
    rows = []
    for u in allc:
        rows.append({"link": u, "type": link_type(u), "newsletter_link": u in tpl,
                     "human_clickers": len(human[u]), "scanner_clickers": len(scan[u]),
                     "raw_clicks": rawclicks[u]})
    return rows


def sections(res, checks, links, sent, month):
    det = [r for r in res.values() if r["has_details"]]
    nodet = [r for r in res.values() if not r["has_details"]]
    clickers = sum(r["clickers"] for r in det)
    scan = sum(len(r["scanners"]) for r in det)
    hum = sum(len(r["humans"]) for r in det)
    share = scan / clickers if clickers else 0
    work, notw, rec = [], [], []

    ranked = sorted(links, key=lambda x: (-x["human_clickers"], -x["raw_clicks"]))
    top5 = ranked[:5]
    worst5 = sorted(links, key=lambda x: (x["human_clickers"], -x["raw_clicks"]))[:5]
    zero = [x for x in links if x["human_clickers"] == 0]
    bytype = collections.Counter()
    for x in links:
        bytype[x["type"]] += x["human_clickers"]

    if top5 and top5[0]["human_clickers"] and hum:
        t = top5[0]
        work.append(f"Best link: {short(t['link'])} with {t['human_clickers']} human clickers ({pct(t['human_clickers'], hum)} of human clickers).")
    if bytype and hum:
        (ty, n), = bytype.most_common(1)
        work.append(f"Best content type: {ty} links drew {n} human link clicks, the most of any type.")
    deep = sum(1 for r in det for e in r["humans"] if set(r["per"][e]) - set(r["template"]))
    if deep:
        work.append(f"{deep} human clickers went past the newsletter links to other pages. These are the warmest readers.")
    for r in res.values():
        s = next((v for k, v in sent.items() if norm(k) == norm(r["name"])), None)
        if s:
            br, ur = r["bounced"] / s, r["unsub"] / s
            if br <= BOUNCE_LIMIT:
                work.append(f"{r['name']}: bounce rate {pct(r['bounced'], s)} is under the {BOUNCE_LIMIT:.0%} limit.")
            if ur <= UNSUB_LIMIT:
                work.append(f"{r['name']}: unsubscribe rate {pct(r['unsub'], s)} is under the {UNSUB_LIMIT:.1%} limit.")
    if not work:
        work.append("No metric clears its bar yet. Give --sent counts so rates can be judged.")

    if det and share >= 0.5:
        notw.append(f"{scan} of {clickers} clickers ({pct(scan, clickers)}) are security scanners. They hit nearly every link, so reported clicks are inflated.")
    elif det and scan:
        notw.append(f"{scan} of {clickers} clickers ({pct(scan, clickers)}) look like scanners and are excluded.")
    if det:
        notw.append(f"Real engagement is small: {hum} human clickers across the lists with click details.")
    for r in nodet:
        line = f"{r['name']} has no click detail file, so its {r['click_state']} reported clickers cannot be checked."
        if det and clickers:
            line += f" If it behaves like the other lists, about {round(r['click_state'] * share)} of them are scanners (estimate)."
        notw.append(line)
    if links and zero:
        notw.append(f"{len(zero)} of {len(links)} clicked links drew no human click. Scanners found them and no person wanted them.")
    for r in res.values():
        s = next((v for k, v in sent.items() if norm(k) == norm(r["name"])), None)
        if s and r["bounced"] / s > BOUNCE_LIMIT:
            notw.append(f"{r['name']}: bounce rate {pct(r['bounced'], s)} is above the {BOUNCE_LIMIT:.0%} limit.")
        if s and r["unsub"] / s > UNSUB_LIMIT:
            notw.append(f"{r['name']}: unsubscribe rate {pct(r['unsub'], s)} is above the {UNSUB_LIMIT:.1%} limit.")
    if not any(norm(r["name"]) in {norm(k) for k in sent} for r in res.values()) and len(res) > 1:
        big = max(res.values(), key=lambda r: r["bounced"] / max(r["tracked"], 1))
        notw.append(f"{big['name']} has the highest bounce share of tracked records ({pct(big['bounced'], big['tracked'])}). Tracked records are people with any event, not all sent mail.")

    fails = [c for c in checks if c[0] == "FAIL"]
    if fails:
        rec.append("Fix the data gaps in the sanity check first. Re-export the missing files and run this skill again.")
    if det and share >= 0.5:
        rec.append("Report human clicks, not raw clicks. Ask the email platform to filter machine clicks, or use this report's human count.")
        rec.append("Do not score leads on raw clicks. A scanner click is not buying intent.")
    if hum:
        rec.append("Send the human clickers file to sales. Start with people who clicked beyond the newsletter links.")
    if zero:
        rec.append("Review the links with no human click. Cut them from the next issue, or move them lower, unless a business reason keeps them.")
    if top5 and top5[0]["human_clickers"]:
        rec.append(f"Lead the next issue with the topic of the best link: {short(top5[0]['link'])}.")
    bounce_total = sum(r["bounced"] for r in res.values())
    if bounce_total:
        rec.append(f"Suppress all {bounce_total} bounced addresses before the next send.")
    dup = [c for c in checks if "more than one list" in c[1]]
    if dup:
        rec.append(f"Remove duplicates across lists ({dup[0][2]}) so people do not get the issue twice.")
    if any("sent count" in c[1] for c in checks):
        rec.append("Give the sent count for each list. Then bounce, unsubscribe and click rates can be judged against the limits.")
    return work, notw, rec, top5, worst5, hum, scan, clickers


def domain_tables(lists, res):
    human_dom = collections.Counter()
    scanner_dom = collections.Counter()
    bounce_dom = collections.Counter()
    for n, r in res.items():
        if r["has_details"]:
            for e in r["humans"]:
                human_dom[e.split("@")[-1]] += 1
            for e in r["scanners"]:
                scanner_dom[e.split("@")[-1]] += 1
        for x in lists[n]["data"].get("bounce", []):
            bounce_dom[(x[2] or "").strip().lower().split("@")[-1]] += 1
    return human_dom, scanner_dom, bounce_dom


def esc(x):
    return html.escape(str(x), quote=True)


CSS = """
:root{--bg:#f5f5f7;--card:#fff;--ink:#1d1d1f;--ink2:#424245;--mute:#6e6e73;--line:#d2d2d7;--soft:#ececf0;
--blue:#0066cc;--blue-bg:#e8f1fb;--gray-bar:#c7c7cc;--red:#c0271d;--red-bg:#fdecea;--amber:#8a5a00;--amber-bg:#fff4dc;
--green:#1a7f37;--green-bg:#e6f4ea;--r:18px;color-scheme:light}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"SF Pro Text","Inter","Segoe UI",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:1040px;margin:0 auto;padding:48px 24px 72px}
h1{font-size:2.25rem;line-height:1.1;letter-spacing:-.02em;margin:0 0 6px;font-weight:700;text-wrap:balance}
h2{font-size:1.5rem;letter-spacing:-.015em;margin:56px 0 16px;font-weight:700;text-wrap:balance}
h3{font-size:1.0625rem;margin:0 0 12px;font-weight:600}
p,li,span,b{overflow-wrap:anywhere}p{margin:0}
.sub{color:var(--mute);font-size:1.0625rem}
.card{background:var(--card);border-radius:var(--r);padding:28px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.lead{font-size:1.375rem;line-height:1.35;letter-spacing:-.01em;font-weight:600;max-width:46ch;text-wrap:pretty;margin-bottom:24px}
.facts{display:flex;flex-wrap:wrap;gap:28px;margin-top:26px;padding-top:22px;border-top:1px solid var(--soft)}
.fact b{display:block;font-size:1.75rem;line-height:1.1;letter-spacing:-.02em;font-weight:700;font-variant-numeric:tabular-nums}
.fact span{color:var(--mute);font-size:.9375rem}
.lbar{margin:18px 0}
.lbar .hd{display:flex;justify-content:space-between;gap:12px;font-size:.9375rem;margin-bottom:8px;flex-wrap:wrap}
.lbar .hd b{font-weight:600}
.lbar .hd span{color:var(--mute);font-variant-numeric:tabular-nums}
.track{display:flex;height:22px;border-radius:11px;overflow:hidden;background:var(--soft)}
.seg-h{background:var(--blue);min-width:3px}
.seg-s{background:var(--gray-bar)}
.seg-u{background:repeating-linear-gradient(45deg,#e3e3e8 0 6px,#f1f1f4 6px 12px)}
.legend{display:flex;gap:18px;flex-wrap:wrap;margin-top:6px;color:var(--mute);font-size:.875rem}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:baseline}
.chips{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px}
.chip{padding:6px 14px;border-radius:999px;font-weight:600;font-size:.9375rem}
.chip.fail{background:var(--red-bg);color:var(--red)}
.chip.warn{background:var(--amber-bg);color:var(--amber)}
.chip.ok{background:var(--green-bg);color:var(--green)}
.checks{list-style:none;margin:0;padding:0}
.checks li{display:grid;grid-template-columns:64px minmax(0,1fr);gap:14px;padding:12px 0;border-top:1px solid var(--soft);align-items:baseline}
.checks li:first-child{border-top:0}
.pill{display:inline-block;text-align:center;padding:2px 0;border-radius:8px;font-size:.8125rem;font-weight:700;width:56px}
.pill.fail{background:var(--red-bg);color:var(--red)}
.pill.warn{background:var(--amber-bg);color:var(--amber)}
.pill.ok{background:var(--green-bg);color:var(--green)}
.checks .t{font-weight:600}
.checks .d{display:block;color:var(--mute);font-size:.9375rem}
details{margin-top:8px}
summary{cursor:pointer;color:var(--blue);font-weight:600;padding:10px 0}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px}
.two>div,.card.col{padding:28px}
.ticks{list-style:none;margin:0;padding:0}
.ticks li{position:relative;padding:10px 0 10px 34px;border-top:1px solid var(--soft);font-size:1rem}
.ticks li:first-child{border-top:0}
.ticks li::before{position:absolute;left:0;top:10px;width:22px;height:22px;border-radius:50%;text-align:center;font-size:.8125rem;font-weight:700;line-height:22px}
.ticks.good li::before{content:"\\2713";background:var(--green-bg);color:var(--green)}
.ticks.bad li::before{content:"!";background:var(--red-bg);color:var(--red)}
ol.recs{margin:0;padding:0;list-style:none;counter-reset:r}
ol.recs li{counter-increment:r;display:grid;grid-template-columns:34px minmax(0,1fr);gap:12px;padding:14px 0;border-top:1px solid var(--soft)}
ol.recs li:first-child{border-top:0}
ol.recs li::before{content:counter(r);width:26px;height:26px;border-radius:50%;background:var(--blue);color:#fff;font-weight:700;font-size:.8125rem;display:grid;place-items:center}
.bars{list-style:none;margin:0;padding:0}
.bars li{padding:12px 0;border-top:1px solid var(--soft)}
.bars li:first-child{border-top:0}
.bars .nm{display:flex;justify-content:space-between;gap:12px;align-items:baseline}
.bars a{color:var(--ink);text-decoration:none;font-weight:500;overflow-wrap:anywhere}
.bars a:hover{color:var(--blue);text-decoration:underline}
.bars .n{font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap}
.bars .meta{color:var(--mute);font-size:.875rem;margin-top:2px}
.bar{height:8px;border-radius:4px;background:var(--soft);margin-top:8px;overflow:hidden}
.bar i{display:block;height:100%;background:var(--blue);border-radius:4px;min-width:2px}
.bar.zero i{background:var(--gray-bar)}
.note{color:var(--mute);font-size:.9375rem;margin:-6px 0 12px}
.three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
table{width:100%;border-collapse:collapse;font-size:.9375rem;font-variant-numeric:tabular-nums}
th{text-align:left;color:var(--mute);font-weight:600;font-size:.8125rem;padding:8px 10px;border-bottom:1px solid var(--line)}
td{padding:10px;border-bottom:1px solid var(--soft)}
td.r,th.r{text-align:right}
.scroll{overflow-x:auto}
.foot{margin-top:56px;color:var(--mute);font-size:.875rem}
a:focus-visible,summary:focus-visible{outline:3px solid var(--blue);outline-offset:2px;border-radius:4px}
@media (max-width:760px){.wrap{padding:28px 16px 56px}h1{font-size:1.75rem}.two,.three{grid-template-columns:minmax(0,1fr)}.card{padding:20px}.lead{font-size:1.1875rem}}
@media print{body{background:#fff}.card{box-shadow:none;border:1px solid var(--line);break-inside:avoid}h2{break-after:avoid}.wrap{padding:0}details>*{display:block}}
"""


def render_html(month, res, checks, work, notw, rec, top5, worst5, hdom, sdom, bdom, links, hum, scan, clickers, sent):
    fails = sum(1 for c in checks if c[0] == "FAIL")
    warns = sum(1 for c in checks if c[0] == "WARN")
    oks = sum(1 for c in checks if c[0] == "OK")
    det_names = ", ".join(n for n, r in res.items() if r["has_details"])
    if clickers:
        lead = (f"In {esc(det_names)}, {pct(scan, clickers)} of reported clickers are security scanners. "
                f"Only {hum} of {clickers:,} are likely people.")
    else:
        lead = "No click details were found, so real readers cannot be counted."
    h = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
         f"<title>AccuKnox Newsletter Clicks, {esc(month)}</title><style>{CSS}</style></head><body><main class='wrap'>"]
    h.append(f"<h1>Newsletter Clicks</h1><p class='sub'>AccuKnox newsletter, {esc(month)}</p>")

    # hero
    h.append("<section class='card' style='margin-top:28px'>")
    h.append(f"<p class='lead'>{lead}</p>")
    for n, r in res.items():
        if r["has_details"]:
            tot = max(r["clickers"], 1)
            hp, sp = 100 * len(r["humans"]) / tot, 100 * len(r["scanners"]) / tot
            h.append(f"<div class='lbar'><div class='hd'><b>{esc(n)}</b><span>{len(r['humans'])} people, {len(r['scanners']):,} scanners, {r['clickers']:,} clickers in detail</span></div>"
                     f"<div class='track' role='img' aria-label='{len(r['humans'])} human and {len(r['scanners'])} scanner clickers'>"
                     f"<div class='seg-h' style='width:{hp:.2f}%'></div><div class='seg-s' style='width:{sp:.2f}%'></div></div></div>")
        else:
            h.append(f"<div class='lbar'><div class='hd'><b>{esc(n)}</b><span>{r['click_state']:,} reported clickers, no click detail file</span></div>"
                     f"<div class='track' role='img' aria-label='unchecked'><div class='seg-u' style='width:100%'></div></div></div>")
    h.append("<div class='legend'><span><i class='dot' style='background:var(--blue)'></i>Likely people</span>"
             "<span><i class='dot' style='background:var(--gray-bar)'></i>Security scanners</span>"
             "<span><i class='dot' style='background:#e3e3e8'></i>Not checked</span></div>")
    h.append(f"<div class='facts'><div class='fact'><b>{hum}</b><span>likely people</span></div>"
             f"<div class='fact'><b>{pct(scan, clickers) if clickers else 'n/a'}</b><span>scanner share</span></div>"
             f"<div class='fact'><b>{fails} / {warns}</b><span>data FAIL / WARN</span></div></div></section>")

    # sanity
    h.append("<h2>The Data Check Found Gaps to Fix</h2><section class='card'>")
    h.append(f"<div class='chips'><span class='chip fail'>{fails} fail</span><span class='chip warn'>{warns} warn</span><span class='chip ok'>{oks} ok</span></div>")
    order = {"FAIL": 0, "WARN": 1, "OK": 2}
    bad = [c for c in sorted(checks, key=lambda c: order[c[0]]) if c[0] != "OK"]
    good = [c for c in checks if c[0] == "OK"]
    row = lambda c: (f"<li><span class='pill {c[0].lower()}'>{c[0]}</span><span><span class='t'>{esc(c[1])}</span>"
                     f"<span class='d'>{esc(c[2])}</span></span></li>")
    h.append("<ul class='checks'>" + "".join(row(c) for c in bad) + "</ul>")
    if good:
        h.append("<details><summary>Passed checks</summary><ul class='checks'>" + "".join(row(c) for c in good) + "</ul></details>")
    h.append("</section>")

    # working / not working
    h.append("<h2>What Works and What Does Not</h2><div class='two'>")
    h.append("<section class='card'><h3>Working</h3><ul class='ticks good'>" + "".join(f"<li>{esc(x)}</li>" for x in work) + "</ul></section>")
    h.append("<section class='card'><h3>Not working</h3><ul class='ticks bad'>" + "".join(f"<li>{esc(x)}</li>" for x in notw) + "</ul></section></div>")

    # recommend
    h.append("<h2>What We Recommend Next</h2><section class='card'><ol class='recs'>" + "".join(f"<li><span>{esc(x)}</span></li>" for x in rec) + "</ol></section>")

    # links
    def bars(L, zero_ok):
        mx = max([x["human_clickers"] for x in top5] + [1])
        out = ["<ul class='bars'>"]
        for x in L:
            w = 100 * x["human_clickers"] / mx
            cls = " zero" if x["human_clickers"] == 0 else ""
            out.append(f"<li><div class='nm'><a href='{esc(x['link'])}' target='_blank' rel='noopener noreferrer'>{esc(short(x['link'], 58))}</a>"
                       f"<span class='n'>{x['human_clickers']}</span></div>"
                       f"<div class='bar{cls}'><i style='width:{w:.1f}%'></i></div>"
                       f"<div class='meta'>{esc(x['type'])} &middot; {x['scanner_clickers']:,} scanners &middot; {x['raw_clicks']:,} raw clicks</div></li>")
        out.append("</ul>")
        return "".join(out)
    tie = sum(1 for x in links if worst5 and x["human_clickers"] == worst5[0]["human_clickers"])
    h.append("<h2>The Links People Clicked and Skipped</h2><p class='note'>Bars show likely people, not raw clicks.</p><div class='two'>")
    h.append(f"<section class='card'><h3>Top 5</h3>{bars(top5, False)}</section>")
    h.append(f"<section class='card'><h3>Worst 5</h3><p class='note'>{tie} links tie at {worst5[0]['human_clickers'] if worst5 else 0} people. Ties show the most scanner-hit link first.</p>{bars(worst5, True)}</section></div>")

    # companies
    def dtable(title, head, data):
        rows = "".join(f"<tr><td>{esc(d)}</td><td class='r'>{n}</td></tr>" for d, n in data) or "<tr><td colspan='2'>None</td></tr>"
        return f"<section class='card'><h3>{title}</h3><table><tr><th>Email domain</th><th class='r'>{head}</th></tr>{rows}</table></section>"
    h.append("<h2>Which Companies Engage, Bounce and Scan</h2><div class='three'>")
    h.append(dtable("Top 5 by people", "People", hdom.most_common(5)))
    h.append(dtable("Worst 5 by bounces", "Bounced", bdom.most_common(5)))
    h.append(dtable("Scanner-heavy", "Scanners", sdom.most_common(5)))
    h.append("</div><p class='note' style='margin-top:12px'>Ignore clicks from scanner-heavy companies when sales picks leads.</p>")

    # numbers
    h.append("<h2>The Numbers by List</h2><section class='card'><div class='scroll'><table><tr><th>List</th><th class='r'>Campaign</th><th class='r'>Sent</th><th class='r'>Tracked</th>"
             "<th class='r'>Click</th><th class='r'>Open</th><th class='r'>Bounced</th><th class='r'>Unsub</th><th class='r'>Clickers in detail</th><th class='r'>Scanners</th><th class='r'>People</th></tr>")
    for n, r in res.items():
        s = next((v for k, v in sent.items() if norm(k) == norm(n)), None)
        cells = [esc(n), r["campaign_id"] or "?", f"{s:,}" if s else "not given", f"{r['tracked']:,}", f"{r['click_state']:,}", f"{r['open_state']:,}",
                 f"{r['bounced']:,}", r["unsub"], f"{r['clickers']:,}" if r["has_details"] else "no file",
                 f"{len(r['scanners']):,}" if r["has_details"] else "n/a", len(r["humans"]) if r["has_details"] else "n/a"]
        h.append("<tr>" + f"<td>{cells[0]}</td>" + "".join(f"<td class='r'>{c}</td>" for c in cells[1:]) + "</tr>")
    h.append("</table></div><p class='note' style='margin-top:12px'>Tracked means people with any event. It is not the sent count.</p>")
    h.append(f"<details><summary>How scanners are found</summary><p class='note'>A newsletter link is a link clicked by at least {TEMPLATE_SHARE:.0%} of a list's clickers. "
             f"A scanner is a clicker who hit at least {SCANNER_COVERAGE:.0%} of those links. The export has no click timestamps, so speed cannot be tested. "
             "Treat the scanner count as a strong estimate.</p></details></section>")
    h.append("<p class='foot'>Made by the newsletter-clicks skill. This file holds company names only. The people list is in human_clickers.csv beside it.</p>")
    h.append("</main></body></html>")
    return "".join(h)


def write_outputs(out, lists, res, checks, months, sent, month_arg):
    links = merge_links(res)
    work, notw, rec, top5, worst5, hum, scan, clickers = sections(res, checks, links, sent, month_arg)
    hdom, sdom, bdom = domain_tables(lists, res)
    month = month_arg or (", ".join(m.title() for m in sorted(months, key=MONTHS.index)) if months else "month unknown")
    fails = sum(1 for c in checks if c[0] == "FAIL")
    warns = sum(1 for c in checks if c[0] == "WARN")

    page = render_html(month, res, checks, work, notw, rec, top5, worst5, hdom, sdom, bdom, links, hum, scan, clickers, sent)
    (out / "report.html").write_text(page, encoding="utf-8")

    with open(out / "link_table.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["link", "type", "newsletter_link", "human_clickers", "scanner_clickers", "raw_clicks"])
        for x in sorted(links, key=lambda x: (-x["human_clickers"], -x["raw_clicks"])):
            w.writerow([x["link"], x["type"], x["newsletter_link"], x["human_clickers"], x["scanner_clickers"], x["raw_clicks"]])
    with open(out / "human_clickers.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["list", "name", "email", "clicks", "distinct_links", "beyond_newsletter_links", "links"])
        for n, r in res.items():
            if not r["has_details"]:
                continue
            for e in sorted(r["humans"], key=lambda e: -len(set(r["per"][e]))):
                v = r["per"][e]
                extra = len(set(v) - set(r["template"]))
                w.writerow([n, r["names"].get(e, ""), e, len(v), len(set(v)), extra, " | ".join(sorted(set(v)))])
    summary = {"month": month, "checks": [list(c) for c in checks],
               "lists": {n: {k: v for k, v in r.items() if isinstance(v, (int, str, type(None)))} for n, r in res.items()},
               "totals": {"clickers_with_detail": clickers, "scanner_clickers": scan, "human_clickers": hum},
               "working": work, "not_working": notw, "recommended": rec,
               "top5_links": top5, "worst5_links": worst5}
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return fails, warns, clickers, scan, hum


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="folder or .zip with one subfolder per email list")
    ap.add_argument("--expect", default=",".join(EXPECTED_LISTS), help="comma list of expected list folder names")
    ap.add_argument("--sent", default="", help='sent counts, like "NAT CRM=12000,TGACRM=20000"')
    ap.add_argument("--month", default="", help="label for the report, like 'October 2026'")
    ap.add_argument("--out", default="", help="output folder, outside any git repo")
    a = ap.parse_args()

    src = Path(a.input).expanduser()
    tmp = None
    if src.suffix.lower() == ".zip":
        tmp = tempfile.TemporaryDirectory(prefix="newsletter-clicks-")
        with zipfile.ZipFile(src) as z:
            z.extractall(tmp.name)
        src = Path(tmp.name)
    if not src.is_dir():
        sys.exit(f"Input not found: {src}")
    sent = {}
    for part in filter(None, (p.strip() for p in a.sent.split(","))):
        k, _, v = part.rpartition("=")
        sent[k.strip()] = int(v.replace("_", ""))
    expected = [e.strip() for e in a.expect.split(",") if e.strip()]
    lists, res, checks, months = build(src, expected, sent, a.month)
    if not lists:
        sys.exit("No .xlsx files found in the input.")
    slug = norm(a.month) or "latest"
    out = Path(a.out).expanduser() if a.out else Path.home() / "Atharva/AccuKnox/newsletter-reports" / slug
    out.mkdir(parents=True, exist_ok=True)
    fails, warns, clickers, scan, hum = write_outputs(out, lists, res, checks, months, sent, a.month)
    print(f"Report: {out / 'report.html'}")
    print(f"Sanity: {fails} FAIL, {warns} WARN | clickers {clickers}, scanners {scan}, human {hum}")
    if tmp:
        tmp.cleanup()


if __name__ == "__main__":
    main()
