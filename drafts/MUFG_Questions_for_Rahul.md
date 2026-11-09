Hi Rahul,

MUFG Bank in Tokyo sent four CNAPP questions before they agree to a deep-dive or PoC. I drafted answers from the help docs, the AgentZ docs and the AI Agent Security deck. The draft is in `help/drafts/MUFG_Response_Draft.md`.

I cannot confirm 7 points from the docs. Can you answer each with Yes, No or Partly, plus one line of detail? MUFG is a bank, so a wrong "yes" costs us more than a slow answer. Today's deadline is the end of the day, India time.

**Q1. KubeArmor overhead (MUFG question 1).**
The docs say only that overhead is "extremely low". MUFG asked for the expected impact on workload resources.
- What are the typical CPU and memory numbers per node in audit mode and in block mode?
- Do we have a benchmark or a customer reference we can share?
- If we have none, can we run a quick test on a MUFG-like cluster during the PoC?

**Q2. CIEM availability (question 1).**
The docs mark CIEM "coming soon" and list standalone accounts only.
- Is CIEM generally available today, or in which release?
- Can we show it to MUFG as a live feature or only as a roadmap item?
- Does it work for AWS organization accounts yet?

**Q3. Agentless scanning with an on-prem control plane (question 2).**
MUFG wants everything inside their own infrastructure.
- Can the agentless cloud scan (CSPM) report to an on-premises or air-gapped control plane?
- Can the agentless VM scanner, which runs in the customer's cloud account, send findings to it?
- If not, which parts only work with SaaS?

**Q4. Data in SaaS and a Japan region (question 2).**
- Is a Japan or APAC SaaS region planned, and when?
- In SaaS, which data leaves the customer: only findings and metadata, or also workload data from agents?
- The Data Usage Policy page has an `<ANSWER>` placeholder about updates in air-gapped environments. What is the correct answer?

**Q5. Nutanix and OCI agentless support (question 1).**
The deployment page lists Nutanix and VMware under agentless. The VM scanning page says OCI and Nutanix are planned.
- Which statement is right today?

**Q6. AgentZ lock-in (question 3).**
- Can a customer export agents, workflows and sandbox settings built in AgentZ and run them elsewhere?
- Which parts depend on Cilium or on AccuKnox services?
- Can the Prompt Firewall and AI-SPM run with no AgentZ installed? I believe yes.

**Q7. Minimum PoC for MUFG (question 4).**
- Is "phase 1 agentless only, in one non-production account, then optional KubeArmor on one cluster" an approach you would offer?
- For an on-premises PoC, is the 3-node spec in the install guide still correct for v3.8?
- Would you join the technical session during your Tokyo visit, and should we offer it after MUFG reviews the written answers?

Thanks,
Atharva
