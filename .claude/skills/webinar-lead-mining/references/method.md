# Webinar Lead Mining Playbook

Use this playbook to build a ranked account list for any AccuKnox webinar. It has two sources: Factors.ai and the webinar and event spreadsheet. Both are required. Each one covers what the other misses.

First used on 3 November 2026 for the AccuKnox x Ariovis webinar on 3 December 2026. The result is in `references/example-2026-12-03-ariovis/`.

## Factors and the Spreadsheet Cover Different Halves

**Source 1: Factors.ai account export.** It shows which companies visit accuknox.com.

- Fields we use: company, domain, industry, city, sessions in 30 days, page views, cumulative pages, identified visitors, first seen, latest activity.
- It has no names, emails, job titles or page URLs.
- The "Confirmed French" evidence text is identical on every row. Treat it as a template, not as proof.
- The "Sessions (90d)" column in the Top 20 export reads 1 on every row. Do not trust it. Use the 30-day column.
- Industry labels are sometimes wrong. WWF France shows as Management Consulting.

**Source 2: the webinar and event spreadsheet.** It shows which people registered or filled a form.

- Location: Google Drive file `19zCV6qV_EWgq5t_IN3JywPHaZz6DuXo7`, named "[FULL] WEBINAR + EVENT + WEBSITE FORM FILLS - 28th Oct.xlsx".
- It is an .xlsx file, so the Sheets API cannot read it. Download it with `gws drive files get` and read it with openpyxl.
- Tabs: `1. Luma Registrants`, `2. Meetup Registrants`, `Webinar Regs Filtered JAHANA +`, `Website Form Fills DEBJANI MAM`, and a `4. Scorecard` tab with formulas only.
- It has names and emails, so never copy it into a repo. Keep only tab and row references.
- It is India-heavy. In the Website Form Fills tab, 382 of 604 rows are in India. Only 2 rows are in France and 0 are in Belgium.
- Only the Website Form Fills tab has a country. The Luma and Webinar tabs have a company domain and no location.

## Ten Steps From Raw Exports to a Ranked List

1. **Download both sources.** Save the Factors CSV into `inputs/`. Download the spreadsheet into a scratch folder, never into the repo.
2. **Read the tabs and columns.** Write down which fields can target. Company domain and country are the only two that can.
3. **Deduplicate.** Match on email first, then on company domain. Keep the tab name and row number of every record. One Schneider Electric person appears in 2 tabs, so 6 rows are 3 people.
4. **Match the sheet to Factors by domain.** Also match French and Belgian companies that Factors misses, such as Eviden, Worldline, Natixis and Swift. A scan of `.fr` and `.be` domains finds personal mail and small firms.
5. **Label the geography evidence.**
   - Confirmed: the company HQ is public, or the form country is FR or BE.
   - Inferred: the HQ is French or Belgian and the person's location is unknown.
   - A French parent with Bengaluru staff counts as inferred, not confirmed.
6. **Score each account.** See the next section.
7. **Verify the top accounts on the public web.** Check identity, location and industry. Mark a company "unverified" when no source is found. Never invent a contact or an email.
8. **Flag records that should not get outreach.** Schools, agencies, vendors, distributors, personal mail domains, ambiguous domains and bot traffic go to the review list.
9. **Pick the language.** English for global and tech companies. French for French-first mutuals, mid-market firms and public bodies, with a note that the session is in English. The partner decides when unsure.
10. **Hand over.** Send the ranked CSV and the review CSV. Never send the spreadsheet itself.

## Scores Use Only Signals That Exist in the Data

Total is 0 to about 100. Every point comes from a field that exists in the data.

| Signal | Points |
|---|---|
| Sessions in the last 30 days | 20 |
| Last activity within 30 days, no session in 30 days | 12 |
| Last activity within 90 days | 6 |
| Page views 200 or more | 15 |
| Page views 50 to 199 | 11 |
| Page views 10 to 49 | 6 |
| Cumulative pages 100 or more | 12 |
| Cumulative pages 40 to 99 | 8 |
| 10 or more identified visitors | 5 |
| 25 or more identified visitors | 8 |
| Any webinar, event or form record in the sheet | 12 |
| Registered for 2 or more events | 5 |
| 3 or more people from one company | 4 |
| Registered for an agentic AI or product webinar | 4 |
| Fit: regulated or critical sector, or AI and cloud builder | 15 |
| Fit: other enterprise or SaaS | 8 |
| Fit: small firm or unclear | 3 |
| Fit: vendor or distributor | 0 |

A visit alone is not buying intent. A high score means "worth a human look", not "ready to buy".

Confidence levels:

- **High:** Factors shows a session in the last 30 days and the sheet has a record.
- **Medium:** one of the two sources is recent, or the sheet shows a regulated company.
- **Low:** the company identity is unverified, the traffic may be a bot, or the last visit is old.

## Five Traps That Distort the Ranking

- A visit spike with no identified visitors can be a crawler or one researcher. WWF France shows 82 sessions in 30 days and 0 identified visitors. KLESIA shows 95 sessions since 13 October. Check both before outreach.
- Capgemini, SocGen and Schneider show up in the sheet with Indian locations. The French signal is in Factors, not in the sheet.
- Systems integrators such as Capgemini, Sopra Steria and Eviden are buyers and partners. Offer the ecosystem angle.
- `gws` writes files only inside the current folder. Run it from a scratch folder.
- The `.ma` and `.ci` domains are French-speaking. The sheet has 30 `.ma` registrants. They sit outside a France and Belgium brief, so list them as a separate market.

## Five Data Gaps to Close Before the Next Webinar

1. Factors page-level data: which URLs each company viewed.
2. Factors job titles or LinkedIn matches for identified visitors.
3. A country column on the Luma and Webinar tabs.
4. A Belgium filter in Factors.
5. Traffic source and campaign for each Factors visit.

## Where Each Output Lives in the Repo

- `references/example-2026-12-03-ariovis/summary.md`: approach, top 20, reasons and gaps.
- `references/example-2026-12-03-ariovis/ranked_accounts.csv`: all ranked accounts.
- `references/example-2026-12-03-ariovis/needs_review.csv`: records to exclude or check.
- `references/example-2026-12-03-ariovis/inputs/`: the two Factors exports.
- `references/example-2026-12-03-ariovis/scripts/`: `build.py` and `load.py`. Rerun with `SHEET_XLSX`, `FACTORS_CSV` and `OUT_DIR` set.

Rebuild command, from the `scripts/` folder:

```bash
SHEET_XLSX=/path/to/sheet.xlsx python3 build.py
```

The scripts need `openpyxl`. Install it in a virtual environment first.
