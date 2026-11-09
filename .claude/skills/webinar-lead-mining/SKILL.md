---
name: webinar-lead-mining
description: Build a ranked list of target accounts for an AccuKnox webinar or partner event, from two required sources, the Factors.ai website-visitor export and the webinar and event registrant spreadsheet. Starts with a hard intake gate that forces the user to define the audience, geography, exclusions and goal before any data is touched. Use for "target accounts for the webinar", "who should we invite", "Ariovis list", "France account list", "mine leads for the event", "rank Factors accounts", or any co-hosted webinar outreach.
---

# Webinar Lead Mining

A visit is not buying intent, and a long list is not a target list. This skill turns two noisy sources into a short ranked list that a human can act on. It was built on 3 November 2026 for the AccuKnox x Ariovis webinar on 3 December 2026. The worked example is in `references/example-2026-12-03-ariovis/`.

The two sources are fixed. Both are required:

1. **Factors.ai account export.** Companies that visit accuknox.com.
2. **The webinar and event spreadsheet.** People who registered or filled a form.

## Step 0 Is a Gate That Forces Clear Thinking

Do not open a file, search the web or write a script until the intake is complete. A vague brief produces a confident wrong list.

Ask with `AskUserQuestion`, at most 4 questions per call. Two calls cover it. Wait for the answers. Then print the brief back and get a "yes".

### Call 1: Who and Why

1. **Event.** Title, date, language, format and co-host. What is the one thing a registrant does after the session?
2. **Goal.** Pick one: registrations, qualified meetings, or pipeline. Ask for the number. "Many registrants" is not a goal.
3. **Buyer.** Which 2 or 3 industries and which roles should the list favor? Name what makes an account a fit for this topic.
4. **Geography.** Which countries or regions count? Which languages? Does a French parent with Indian staff count?

### Call 2: Limits and Sources

1. **Exclusions.** Which customers, partners, competitors, vendors and schools stay off the list? Ask who owns the customer list.
2. **Sources.** Give the path of the Factors export and the Drive file ID or path of the spreadsheet. Ask for the export date.
3. **Owner.** Who sends the outreach, and who picks the language per account? Does the partner see the list?
4. **Size.** How many accounts can the team contact in the next 2 weeks? The answer sets the cut line.

### Push Back on Weak Answers

Do not accept these. Ask one sharper question each time.

| Weak answer | Sharper question |
|---|---|
| "Enterprise companies" | Which industries? Which size? Which of your last 3 wins looks like the target? |
| "Everyone in Europe" | Which 2 countries first? Which language does the invite go out in? |
| "As many as possible" | How many can your team contact in 2 weeks? |
| "Anyone who visited" | What would you accept as proof that a visit means interest? |
| "Skip the exclusions" | Who must never get this email? Name one customer and one competitor. |

### Brief Card

Print this card and wait for "yes" before step 1. If any line stays empty, say which line and stop.

```text
Event:       <title, date, language, co-host>
Goal:        <registrations | meetings | pipeline> = <number>
Buyer:       <industries, roles, fit test>
Geography:   <countries, languages, parent-vs-local rule>
Exclusions:  <customers, partners, competitors, vendors, schools>
Sources:     <Factors file and date> + <spreadsheet and date>
Owner:       <sender, language decider>
Cut line:    <accounts to contact in 2 weeks>
```

## Both Sources Must Pass Four Checks

Stop and ask for a file when a check fails. Never pretend you read a source.

1. **Open it.** Read every tab and column. List what is usable for targeting. Company domain and country are usually the only two.
2. **Date it.** Say how old each export is. A Factors export older than 14 days is stale.
3. **Find the geography.** Count rows per country. When the brief names a country with 0 rows, say so before ranking.
4. **Mark personal data.** The spreadsheet holds names and emails. Never copy it into a repo or send it to a partner. Keep tab and row references only.

Facts that cost time last run:

- The spreadsheet is an .xlsx on Drive, so the Sheets API cannot read it. Run `gws drive files get --params '{"fileId":"<id>","alt":"media"}' --output sheet.xlsx` from a scratch folder, because `gws` writes only inside the current folder.
- Read it with openpyxl in a virtual environment.
- Factors rows say "Confirmed French (HQ + visitor geo)" on every line. That text is a template. Treat it as a claim.
- The Factors "Sessions (90d)" column read 1 on every row. Use the 30-day column.
- Factors industry labels can be wrong. WWF France showed as Management Consulting.

## Seven Steps From Brief to Ranked List

1. **Deduplicate.** Match people by email, then companies by domain. Keep tab and row. A company with 6 rows can be 3 people.
2. **Merge by domain.** Match the spreadsheet to Factors. Also scan the spreadsheet for companies whose parent sits in the target geography but Factors misses.
3. **Label the geography evidence.** Confirmed means a public HQ or a form country. Inferred means the parent is in the target country and the person's location is unknown.
4. **Score.** Use the model in `references/method.md`. Every point must come from a field in the data.
5. **Verify the top 25 on the public web.** Check identity, location and industry. Write "unverified" when no source exists. Never invent a contact or an email.
6. **Flag.** Move schools, agencies, vendors, distributors, personal mail, ambiguous domains and possible bots to the review list.
7. **Hand over.** Write `ranked_accounts.csv`, `needs_review.csv` and `summary.md`. Send the partner only the two CSVs.

Rewrite the `META` table in `scripts/build.py` for each campaign. It holds the type, fit, language and note per company. The fit points come from the buyer line in the brief.

## The Summary Must Answer Six Questions

`summary.md` always holds these, in this order:

1. What data exists and what can target. State plainly when the target country has few or no rows.
2. Which sheet rows link to target-geography companies, with tab and row references.
3. The ranked top 20 with company, domain, region, source, signals, fit, evidence level, confidence, language and next action.
4. Why the ranking looks this way, in 4 to 6 bullets.
5. Companies worth investigating that are in neither source, kept in their own table, with no contacts.
6. The records that need manual review, and the missing data that would improve the list.

## Rules That Protect the Ranking

- **A visit alone is not intent.** It earns recency and depth points only.
- **Confidence is separate from rank.** A high-traffic company with an unverified identity or a bot pattern stays at Low confidence.
- **Integrators are buyers and partners.** Offer them the ecosystem angle.
- **Keep suggestions apart.** Companies from public research never mix into the ranked table.
- **Show the data gaps.** Page URLs, job titles, a country on every tab and the partner's customer list move the ranking most.

## Files in This Skill

- `references/method.md`: the full method, scoring table and traps.
- `references/example-2026-12-03-ariovis/`: the worked example with inputs, ranked CSV, review CSV and summary.
- `scripts/load.py` and `scripts/build.py`: the loader and the scorer. Run from `scripts/` with `SHEET_XLSX`, `FACTORS_CSV` and `OUT_DIR` set.

```bash
cd .claude/skills/webinar-lead-mining/scripts && SHEET_XLSX=/path/to/sheet.xlsx FACTORS_CSV=/path/to/factors.csv OUT_DIR=/path/to/out python3 build.py
```
