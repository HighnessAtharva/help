"""Reuse the companies of a saved run, find more buyers per company, verify emails until the target is met."""
import json, sys, concurrent.futures as cf
sys.path.insert(0, r"D:\Atharva\NOTES\SCRIPTS\gtm")
from common import Ledger, output
import signal_pipeline as sp
f, target, cap = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
d = json.load(open(f, encoding="utf-8")); L = Ledger(cap)
done = {w["linkedin"] for w in d["chosen"]}
people = {}
for c in d["companies"]:
    r = L.treg_call("treg.people.search", body={"company_domain": c["domain"], "title": "security", "limit": 25}, max_cost=0.05)
    for p in (output(r) or {}).get("people", []) if r else []:
        li = p.get("employee_linkedin")
        if p.get("first_name") and p.get("title") and li and li not in done:
            people[li] = {"name": f'{p["first_name"]} {p["last_name"]}'.strip(), "first": p["first_name"], "last": p["last_name"],
                          "title": p["title"], "linkedin": li, "company": c["name"], "domain": c["domain"], "employees": c["employees"],
                          "industry": c["industry"], "job": c["jobs"][0]["title"], "job_url": c["jobs"][0]["url"], "job_posted": c["jobs"][0]["posted_on"]}
print(len(people), "new people")
qs = {"fit": {"type": "score", "instructions": "How good a sales lead is this person for `product`? Judge by the role in `position`.", "criteria": sp.FIT},
      "role": sp.ROLE, "buys": sp.BUYS,
      "competitor": {"type": "noul", "instructions": "Does this person work at a company that sells cloud, container or AI security software? `product` is the seller, never this person's.",
                     "criteria": {"true": "their title or company sells cybersecurity or cloud security products or services", "false": "they work in-house at a company that would buy security tooling"}},
      "can_buy": {"type": "noul", "instructions": "Can this person select or approve a security platform purchase, given the role and the company size?"},
      "evidence": {"type": "noul", "instructions": "Does the `position` text itself name a security leadership role such as CISO, VP, head, director, architect or principal? A vague or empty headline is no."}}
def judge(item):
    pid, w = item
    r = L.jev({"position": w["title"], "company": w["company"], "industry": w["industry"], "employees": w["employees"], "product": sp.PRODUCT}, qs)
    if r:
        A = r["answers"]
        w.update(role=A["role"]["choice"], p_buyer=A["fit"]["probabilities"].get("2", 0), p_offer=A["buys"]["probabilities"].get("accuknox", 0),
                 p_competitor=A["competitor"]["noul"], p_can_buy=A["can_buy"]["noul"], p_evidence=A["evidence"]["noul"])
    else:
        w["p_buyer"] = None
    w["tier"], w["reject"] = sp.qualify(w)
    return pid, w
with cf.ThreadPoolExecutor(6) as ex:
    people = dict(ex.map(judge, people.items()))
new = sorted((w for w in people.values() if w["tier"]), key=lambda w: (w["tier"] != "high", -(w["p_buyer"] + w["p_offer"] + w["p_can_buy"] + w["p_evidence"])))
per = {}
for w in d["chosen"]: per[w["company"]] = per.get(w["company"], 0) + 1
pick = []
for w in new:
    if per.get(w["company"], 0) < 4:
        per[w["company"]] = per.get(w["company"], 0) + 1; pick.append(w)
print(len(new), "pass,", len(pick), "to look up")
def good(w): return bool(w.get("email")) and w.get("email_status") == "valid" and sp.same_org(w["email"], w["domain"])
for w in d["chosen"]: w.setdefault("email_status", None)
have = sum(good(w) for w in d["chosen"])
for w in pick:
    if have >= target or L.left() < 0.03: break
    r = L.treg_call("treg.people.email.find", body={"first_name": w["first"], "last_name": w["last"], "domain": w["domain"]}, max_cost=0.03)
    em = (output(r) or {}).get("email") if r else None
    w["email"] = em
    if em:
        v = L.treg_call("treg.people.email.verify", body={"email": em}, max_cost=0.003)
        w["email_status"] = (output(v) or {}).get("status") if v else None
    d["chosen"].append(w); have += good(w)
d["leads"] = [w for w in d["chosen"] if good(w)]
r = d["run"]; r["people_pass"] += len(new); r["people_found"] += len(people); r["emails_verified"] = len(d["leads"])
r["email_lookups"] = sum("email" in w for w in d["chosen"]); r["treg_usd"] = round(r["treg_usd"] + L.treg, 4); r["jev_usd"] = round(r["jev_usd"] + L.jev_usd, 5)
json.dump(d, open(f.replace("run1", "final"), "w", encoding="utf-8"), indent=1, default=str)
print(len(d["leads"]), "verified leads · extra treg", round(L.treg, 4))
