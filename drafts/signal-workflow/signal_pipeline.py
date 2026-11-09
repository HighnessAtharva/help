"""AccuKnox hiring-signal pipeline: job post -> company -> buyer -> verified email.

treg fetches and Jev judges. One signal profile per run. Add a profile to SIGNALS to run a
new signal through the same stages.

    python signal_pipeline.py cloud-native-hiring --cap 0.60 --target 30
"""
import argparse
import concurrent.futures as cf
import json
import sys
from pathlib import Path

sys.path.insert(0, r"D:\Atharva\NOTES\SCRIPTS\gtm")
from common import Ledger, output, stamp  # noqa: E402

HERE = Path(__file__).parent
STATE = HERE / ".state"
STATE.mkdir(exist_ok=True)

PRODUCT = ("AccuKnox is a cloud and AI security platform: CNAPP (cloud posture, Kubernetes and container "
           "runtime protection, CI/CD and IaC scanning), AI and LLM security, and zero trust. It is sold to "
           "security leaders at mid-size and large enterprises.")

SIGNALS = {
    "cloud-native-hiring": {
        "label": "Hiring for cloud-native, container or CI/CD security",
        "queries": ["cloud native security engineer", "container security Kubernetes", "DevSecOps CI/CD security",
                    "CNAPP cloud security posture", "application security engineer cloud-native",
                    "AI security engineer LLM", "Kubernetes security", "cloud security architect",
                    "product security engineer containers", "senior application security engineer"],
        "location": "United States", "posted": "month",
        "signal_q": "Is this job a security role whose main work is cloud-native, container, Kubernetes, "
                    "CI/CD pipeline, cloud posture or AI and LLM security?",
    },
}

# Five Jev checks per person. Same bars as SCRIPTS/gtm/buyer_signal.py.
TIERS = {
    "high":      {"buyer": 0.75, "offer": 0.60, "competitor_max": 0.25, "can_buy": 0.70, "evidence": 0.80},
    "qualified": {"buyer": 0.55, "offer": 0.50, "competitor_max": 0.40, "can_buy": 0.50, "evidence": 0.60},
}
FIT = [{"not a lead": "recruiters, HR, sales, students, finance, or anyone whose work is not security or cloud infrastructure"},
       {"practitioner": "a security or DevOps engineer or analyst who feels the problem but does not select tools"},
       {"decision maker": "a CISO, VP, head or director of security, cloud security, product security or DevSecOps, "
                          "or a principal or staff security architect who selects or approves security tools"}]
BUYS = {"type": "choice", "instructions": "Which offer fits this person best? `product` is AccuKnox, the seller.",
        "criteria": {"accuknox": "a security leader or architect who would evaluate a cloud, container or AI security platform",
                     "neither": "not a buyer of cloud or AI security tooling"}}
ROLE = {"type": "choice", "instructions": "What is this person's role?",
        "criteria": {"ciso_exec": "CISO, VP or head of security or infrastructure",
                     "sec_director": "director or senior manager of security, cloud security, product security or DevSecOps",
                     "architect": "security architect or principal or staff engineer",
                     "engineer": "security, cloud or DevOps engineer or analyst",
                     "other": "anything else"}}


def to_int(x):
    try:
        return int(str(x).replace(",", "").split("-")[0].replace("+", "").strip())
    except ValueError:
        return 0


def same_org(email, domain):
    """The email domain must belong to the company: first 5 letters of the domain name match."""
    e = email.split("@")[1].lower().split(".")
    c = domain.lower().split(".")
    return e[-2][:5] == c[-2][:5] if len(e) > 1 and len(c) > 1 else False


def qualify(w):
    if w.get("p_buyer") is None:
        return None, "jev failed"
    for tier, t in TIERS.items():
        if (w["p_buyer"] >= t["buyer"] and w["p_offer"] >= t["offer"] and w["p_competitor"] <= t["competitor_max"]
                and w["p_can_buy"] >= t["can_buy"] and w["p_evidence"] >= t["evidence"]):
            return tier, ""
    t = TIERS["qualified"]
    if w["p_evidence"] < t["evidence"]:
        return None, "vague title"
    if w["p_competitor"] > t["competitor_max"]:
        return None, "competitor"
    if w["p_buyer"] < t["buyer"]:
        return None, "wrong role"
    if w["p_offer"] < t["offer"]:
        return None, "wrong offer"
    return None, "cannot buy"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("signal", choices=SIGNALS)
    ap.add_argument("--cap", type=float, default=0.60)
    ap.add_argument("--target", type=int, default=30)
    ap.add_argument("--min-employees", type=int, default=1000)
    ap.add_argument("--max-companies", type=int, default=70)
    ap.add_argument("--per-company", type=int, default=3)
    a = ap.parse_args()
    S = SIGNALS[a.signal]
    L = Ledger(a.cap)
    run = {"signal": a.signal, "label": S["label"]}

    # 1. Signal: job posts from the last month.
    jobs = {}
    for q in S["queries"]:
        d = L.treg_call("crawl4ai.linkedin.search.jobs",
                        body={"query": q, "location": S["location"], "posted": S["posted"], "limit": 60}, max_cost=0.005)
        for r in (d or {}).get("rows", []):
            jobs.setdefault(r["job_id"], dict(r, query=q))
    print(f"1. {len(jobs)} job posts · treg ${L.treg:.4f}")

    # 2. Jev: is the job really the signal? One call per job, three questions.
    def judge_job(item):
        jid, j = item
        r = L.jev({"title": j["title"], "company": j["company"], "location": j["location"]}, {
            "signal": {"type": "noul", "instructions": S["signal_q"]},
            "agency": {"type": "noul", "instructions": "Is `company` a staffing agency, recruiter or job board rather than the employer?"},
            "vendor": {"type": "noul", "instructions": "Is `company` a cybersecurity or cloud-security software vendor that competes with a CNAPP platform?"}})
        if r:
            A = r["answers"]
            j.update(p_signal=A["signal"]["noul"], p_agency=A["agency"]["noul"], p_vendor=A["vendor"]["noul"])
        else:
            j.update(p_signal=None)
        return jid, j
    with cf.ThreadPoolExecutor(6) as ex:
        jobs = dict(ex.map(judge_job, jobs.items()))
    good = [j for j in jobs.values() if j.get("p_signal") is not None and j["p_signal"] >= 0.6
            and j["p_agency"] < 0.5 and j["p_vendor"] < 0.5]
    by_co = {}
    for j in sorted(good, key=lambda j: -j["p_signal"]):
        by_co.setdefault(j["company"], []).append(j)
    print(f"2. {len(good)} signal jobs at {len(by_co)} companies")
    run["jobs_found"], run["jobs_signal"], run["companies_signal"] = len(jobs), len(good), len(by_co)

    # 3. treg enriches each company, then the size gate.
    companies = {}
    for name in list(by_co)[:a.max_companies]:
        d = L.treg_call("treg.companies.enrich", body={"name": name}, max_cost=0.01)
        o = output(d) if d else None
        if o and o.get("domain"):
            companies[name] = {"name": o.get("name") or name, "domain": o["domain"], "industry": o.get("industry"),
                               "employees": to_int(o.get("employees")), "linkedin": o.get("linkedin_url"),
                               "jobs": by_co[name]}
    sized = {k: c for k, c in companies.items() if c["employees"] >= a.min_employees}
    print(f"3. {len(companies)} enriched, {len(sized)} with {a.min_employees}+ staff · treg ${L.treg:.4f}")
    run["companies_enriched"], run["companies_sized"] = len(companies), len(sized)

    # 4. treg finds security people at each company for free, Jev runs the five checks.
    people = {}
    for k, c in sized.items():
        d = L.treg_call("treg.people.search", body={"company_domain": c["domain"], "title": "security", "limit": 25}, max_cost=0.05)
        for p in (output(d) or {}).get("people", []) if d else []:
            if p.get("first_name") and p.get("title") and p.get("employee_linkedin"):
                people[p["employee_linkedin"]] = {
                    "name": f'{p["first_name"]} {p["last_name"]}'.strip(), "first": p["first_name"], "last": p["last_name"],
                    "title": p["title"], "linkedin": p["employee_linkedin"], "company": c["name"], "domain": c["domain"],
                    "employees": c["employees"], "industry": c["industry"], "has_email": p.get("has_email"),
                    "job": c["jobs"][0]["title"], "job_url": c["jobs"][0]["url"], "job_posted": c["jobs"][0]["posted_on"]}
    print(f"4. {len(people)} people found · treg ${L.treg:.4f}")

    qs = {"fit": {"type": "score", "instructions": "How good a sales lead is this person for `product`? Judge by the role in `position`.", "criteria": FIT},
          "role": ROLE, "buys": BUYS,
          "competitor": {"type": "noul", "instructions": "Does this person work at a company that sells cloud, container or AI security software? `product` is the seller, never this person's.",
                         "criteria": {"true": "their title or company sells cybersecurity or cloud security products or services",
                                      "false": "they work in-house at a company that would buy security tooling"}},
          "can_buy": {"type": "noul", "instructions": "Can this person select or approve a security platform purchase, given the role and the company size?"},
          "evidence": {"type": "noul", "instructions": "Does the `position` text itself name a security leadership role such as CISO, VP, head, director, architect or principal? A vague or empty headline is no."}}

    def judge(item):
        pid, w = item
        r = L.jev({"position": w["title"], "company": w["company"], "industry": w["industry"], "employees": w["employees"], "product": PRODUCT}, qs)
        if r:
            A = r["answers"]
            w.update(role=A["role"]["choice"], p_buyer=A["fit"]["probabilities"].get("2", 0),
                     p_offer=A["buys"]["probabilities"].get("accuknox", 0), p_competitor=A["competitor"]["noul"],
                     p_can_buy=A["can_buy"]["noul"], p_evidence=A["evidence"]["noul"])
        else:
            w["p_buyer"] = None
        w["tier"], w["reject"] = qualify(w)
        return pid, w
    with cf.ThreadPoolExecutor(6) as ex:
        people = dict(ex.map(judge, people.items()))
    leads = [w for w in people.values() if w["tier"]]
    rejects = {}
    for w in people.values():
        if not w["tier"]:
            rejects[w["reject"]] = rejects.get(w["reject"], 0) + 1
    print(f"   {len(leads)} pass the five checks, dropped: {rejects}")
    run["people_found"], run["people_pass"], run["rejects"] = len(people), len(leads), rejects

    # Best people per company, high tier first, so one big company cannot fill the sheet.
    leads.sort(key=lambda w: (w["tier"] != "high", -(w["p_buyer"] + w["p_offer"] + w["p_can_buy"] + w["p_evidence"])))
    per, chosen = {}, []
    for w in leads:
        if per.get(w["company"], 0) < a.per_company:
            per[w["company"]] = per.get(w["company"], 0) + 1
            chosen.append(w)

    # 5. treg finds the email, then verifies it for free. Stop at the target.
    verified, tried = [], 0
    for w in chosen:
        if len(verified) >= a.target or L.left() < 0.03:
            break
        tried += 1
        d = L.treg_call("treg.people.email.find", body={"first_name": w["first"], "last_name": w["last"], "domain": w["domain"]}, max_cost=0.03)
        em = (output(d) or {}).get("email") if d else None
        w["email"] = em
        if em:
            v = L.treg_call("treg.people.email.verify", body={"email": em}, max_cost=0.003)
            w["email_status"] = (output(v) or {}).get("status") if v else None
            w["email_raw"] = output(v) if v else None
        if em and w.get("email_status") == "valid" and same_org(em, w["domain"]):
            verified.append(w)
    print(f"5. {tried} email lookups, {len(verified)} verified · treg ${L.treg:.4f} · jev ${L.jev_usd:.5f}")
    run.update(email_lookups=tried, emails_verified=len(verified), treg_usd=round(L.treg, 4), jev_usd=round(L.jev_usd, 5))

    out = STATE / f"{a.signal}-{stamp()}.json"
    out.write_text(json.dumps({"run": run, "leads": verified, "chosen": chosen, "jobs": good, "companies": list(sized.values())},
                              indent=1, default=str), encoding="utf-8")
    print("saved", out)


if __name__ == "__main__":
    main()
