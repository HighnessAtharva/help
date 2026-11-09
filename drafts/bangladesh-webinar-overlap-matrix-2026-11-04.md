# Bangladesh Webinar: Technical Overlap Matrix, Agenda and SME Questions

Status: DRAFT for Atharva's review. Not sent. Not published.
Webinar: Nov 26, 2026, 11:30 AM IST (11:00 AM Bangladesh time), with SmartData.
Prepared: Nov 4, 2026.

## Inputs Came From Granola, Gmail and the Help Repo

| Input | What it is |
|---|---|
| Granola note | Marketing Scrum, Nov 4, 2026, 12:00 PM IST. Atharva commits to the agenda and the overlap matrix. Jahana and Kavitha build the landing page, script and PPT from it. |
| Gmail thread | Kausar Ahmed (SmartData), Nov 3, 2026, "Re: Follow-up on Webinar Discussion and Next Steps". |
| Attachment 1 | `BB_Cybersecurity Framework.pdf`. Version 1.0 (2026). 62 PDF pages. Cited as **CSF**. |
| Attachment 2 | `BB_Guidelines on Cloud Computing.pdf`. Version 1.0 (March 2023). 28 PDF pages. Cited as **CLD**. |
| Attachment 3 | `BB_Guideline on ICT Security.pdf`. Version 4.0 (2023). 96 PDF pages. Cited as **ICT**. |
| Help docs | `help` repo, `docs/` folder, branch `chore/oct-2026-working-files`. URL pattern: `docs/use-cases/cwpp.md` is `help.accuknox.com/use-cases/cwpp/`. |

The email names two attachments. It carries three. The ICT Security Guideline is the third, and it holds the AI chapter (ICT 14). I read all three.

**Page convention.** Every `p.` is the PDF page. Printed page is PDF page minus 10 for CSF and ICT, and minus 1 for CLD.

## Nine Findings Change How We Position the Webinar

**F1. No help page mentions Bangladesh Bank.** A search of `docs/` for "Bangladesh" returns zero files. The compliance list in `use-cases/compliance.md` holds 30+ frameworks (NIST CSF, ISO 27001, PCI, SOC 2, CIS and others) and no Bangladesh Bank framework. We hold no evidence to claim compliance, certification or a Bangladesh Bank score.

**F2. CSF names CNAPP.** CSF 6.1.3.12(p), p.46, lists "Cloud-Native Application Protection Platform (CNAPP)" among the security solutions the organization shall implement. CSF Appendix A item 28, p.57, lists cloud security. This is the strongest hook for the webinar. It is a named solution category, not a compliance statement.

**F3. The title leads with words the documents never use.** The webinar title is "Zero Trust for Bangladesh's Banks and Telcos - Compliance to Runtime". None of the three documents mention zero trust, Kubernetes or runtime security. "Container" appears only as a definition (CLD 1.4, p.10 and CLD 2.2, p.14). Position runtime protection as support for the CSF Detect and Respond functions. Do not say the guidelines require it.

**F4. The documents cover banks and financial firms, not telcos.** CSF 1.1, p.11, applies to banks, financial institutions, mobile financial service providers, payment service providers and payment system operators. The word "telecom" appears only in cabling and infrastructure text. The telco audience needs a different regulator reference. Ask SmartData (Q-P1).

**F5. Legal status is unclear.** CSF calls itself a "baseline" with "minimum requirements" (p.11). The word "mandatory" never appears. No effective date or circular number is printed. The CLD circular (p.1) is in a legacy Bengali font. The extracted text suggests a deadline of Dec 31, 2023 for running cloud services. Treat that as unverified until someone reads the PDF image.

**F6. Data residency is the sharpest technical risk.** CLD 2.3.1.2 and 2.3.4.5, p.15, bar customers' financial and other sensitive data from cross-border public or hybrid cloud without prior Bangladesh Bank approval. AccuKnox SaaS regions are US, EU, Middle East and India. There is no Bangladesh region. Lead with the On-Premises and Your Cloud models for this audience (M22).

**F7. Log retention does not match CLD 4.6.3.** CLD 4.6.3, p.21, wants the cloud provider to keep logs for at least 2 years. AccuKnox keeps alerts 180 days, CWPP telemetry 30 days and CDR cloud logs 90 days (M16).

**F8. Seven asks have no help-doc evidence.** Privileged access management, DLP, WAF, next-generation firewall and IPS, DDoS protection, SIEM or 24/7 SOC, and endpoint antivirus or EDR. Do not claim any of them (section "Eleven Asks Have No Help-Docs Evidence").

**F9. The Oct 21 agenda fills 30 minutes of a 60-minute slot.** The five items add to 5 + 5 + 5 + 10 + 5. Kausar agreed to one hour. The agenda below fills 60 minutes.

## How to Read the Matrix

| Coverage | Meaning |
|---|---|
| Direct | A help page describes a capability that does what the clause names. |
| Partial | The page covers part of the clause, or only some environments. |
| Unclear | The docs hint at it but do not state it. Needs SME review. |
| No evidence | A search of `docs/` found nothing. |

Every row describes a **security capability that supports a requirement**. None describes regulatory compliance. "[SME]" marks a statement that needs a technical SME to confirm before any public use.

The three documents hold about 1,080 requirement rows (CLD 214, CSF 425, ICT 445). I grouped the technical ones into 26 themes. Each theme lists every clause it draws on. The full row lists are in the scratchpad (see "Working Files").

## Twenty-Six Themes Map Clauses to Help-Docs Evidence

### A. Identify

| Ref | Source and section | Requirement | AccuKnox capability | Help-docs evidence | Coverage | Gaps and dependencies | Safe webinar wording |
|---|---|---|---|---|---|---|---|
| M1 | CSF 3.1.1.1, 3.1.1.5, 3.1.7.6 (p.24, 28), 5.1.2.18 (p.42). ICT 5.1.2.2 (p.27). CLD 4.7.2.2 (p.21). | Keep an asset and software inventory. Know every cloud service in use. Run discovery often (CSF says daily). | CSPM scans onboarded cloud accounts for hosts, apps, Web APIs, containers and clusters in one inventory. AI-SPM lists models, agents and datasets. | `use-cases/asset-inventory.md`, intro ("scans the cloud account for assets like hosts, applications, Web APIs, containers, clusters"). `use-cases/aiml-usecases.md`, "Which Module for Which Job" (AI-SPM and Shadow AI rows). | Partial | Not a CMDB. No fields for purchase date, license number or physical location (ICT 5.1.2.2). On-premises hardware outside VMs and Kubernetes: no evidence. Docs say scans run "on a scheduled interval". The minimum interval is unstated [SME]. | "One inventory of your cloud, Kubernetes and AI assets. It supports your asset-management controls." |
| M2 | CLD 2.1.1.2 b (p.13), 4.7.2.3 (p.21). CSF 3.1.4.5 (p.26), 4.1.6.2 (p.37), 4.1.8.10 (p.39). ICT 5.5 intro (p.37). | Find cloud services open to any source IP. Keep environment baselines, review them and handle deviations. | CSPM runs 1,000+ out-of-the-box checks and tracks configuration drift. Checks can be switched off or re-rated per account. | `use-cases/compliance.md`, intro ("more than 1,000 out-of-the-box compliance checks"). `use-cases/cspm.md`, "AccuKnox Features" (Drift Detection). `use-cases/cloud-misconfigurations.md` (public S3 bucket example, drift). `use-cases/cloud/gcp-network.md` (open ports). | Direct for cloud configuration | The docs do not name an "any source IP" check. Confirm a security-group exposure check exists on AWS, Azure and GCP [SME]. | "Continuously finds risky cloud configurations such as public storage and open ports, and tracks drift from your baseline." |
| M3 | ICT 6.1.1-6.1.3 (p.49), 6.2.1-6.2.3 (p.50). CSF 4.1.6.16 (p.38), 4.1.8.12 (p.39), 6.1.4.6 (p.48). CLD 6.4.1-6.4.2 (p.25). | Find vulnerabilities from outside sources. Rate risk. Scan on schedule and after change. Fix by criticality. | Container image scan, VM host package scan, ASPM vulnerability management. Findings are enriched with NVD, EPSS and CISA KEV data. | `use-cases/container-scan.md` ("Vulnerabilities Tab"). `resources/vulnerability-database.md` (sources). `use-cases/aspm.md` cards "Vulnerability Management" and "EPSS Scoring for Prioritization". `faqs/general.md` Q17 ("Host Scanning"). | Direct | Scan cadence (half-yearly internal, yearly independent, ICT 6.2.2-6.2.3) is the institution's process duty. AccuKnox is not an independent third party. | "Scans images, hosts and code for known vulnerabilities. Ranks them by exploit likelihood and known exploitation." |
| M4 | ICT 5.11.1-5.11.4 (p.42-43). CSF 4.1.4.12 (p.35), 4.1.8.7-4.1.8.8 (p.38). CLD 4.7.3.1 (p.21). | Prioritize patches, test them, apply within set timeframes. | Shows vulnerable packages and fix guidance. | `use-cases/container-scan.md`, "Remediating the Vulnerability". `faqs/general.md` Q17. | Partial | No evidence that AccuKnox deploys patches. Patch testing and rollout stay with the institution. | "Shows which workloads need a patch, and in what order. Your patch tooling applies it." |
| M5 | CLD 2.2.2.2 c (p.14), 4.4.3 (p.18). ICT 5.1.3.1-5.1.3.5 (p.27-28). CSF 4.1.4.2 (p.34). | Analyze vulnerabilities inherited from the platform. Ban unlicensed software. Follow software licenses. | SCA, SBOM license findings, XBOM integration. | `getting-started/3.6-release.md`, "SBOM License Findings". `use-cases/aspm.md`, SCA card. `integrations/azure-xbom.md`. | Partial | None of the three documents say "SBOM". Do not headline it. Detection of unlicensed software at runtime: no evidence. | "Flags vulnerable dependencies and open-source license obligations." |
| M6 | ICT 6.1.7 (p.49-50), 6.2.4 (p.50), 10.3.1-10.3.11 (p.66), 10.8.1-10.8.8 (p.67-68). CLD 4.5.4.1-4.5.4.3 (p.20). CSF 6.1.3.12(m) (p.46), Appendix A item 12 (p.57). | Secure coding and review. Security testing before release. Secure APIs (keys, token expiry, real-time monitoring). Protect public web apps. | SAST, DAST, SCA, secret scan and IaC scan in CI/CD. API inventory from live traffic, spec upload and API scan. | `use-cases/aspm.md` (card list). `use-cases/api-security.md`, sections 2 to 6. | Direct for pre-release testing and API inventory. Partial overall | ICT 10.8.7 asks for real-time API monitoring with fast key revocation. No evidence of key revocation. WAF (CSF 6.1.3.12(f), ICT 6.2.4): no evidence. | "Finds code, dependency, secret and API weaknesses before release. Builds a live API inventory." |

### B. Protect

| Ref | Source and section | Requirement | AccuKnox capability | Help-docs evidence | Coverage | Gaps and dependencies | Safe webinar wording |
|---|---|---|---|---|---|---|---|
| M7 | CLD 4.5.2.1-4.5.2.9 (p.19-20), 2.2.1.2 b (p.14). CSF 4.1.2.5, 4.1.2.12, 4.1.2.16 (p.32). ICT 8.3.2 (p.58). | IAM policy. MFA for cloud access. Access review. Segregation of duties. Least privilege. Detect unauthorized accounts. | CIEM lists users, groups and roles across AWS, GCP, Azure and Oracle, shows attached policies and draws the access graph. Console sign-in by SAML SSO. Multi-tenant RBAC on the platform. | `getting-started/ciem-overview.md` (description and "The Access Graph Traces an Identity to Its Policies"). `integrations/saml-sso.md`. `resources/multitenancy.md`, "Layer 1: Users, RBAC, and Tenant Management". | Partial | Docs do not say CIEM enforces MFA, runs access reviews or flags new accounts [SME]. No page describes MFA on the AccuKnox console. | "Shows who holds access in each cloud and traces it to policies. It supports your access reviews." |
| M8 | CLD 4.5.2.7-4.5.2.8 (p.20). CSF 6.1.3.12(b) (p.46), Appendix A item 3 (p.57). ICT 8.3.2 (p.58). | Privileged access management and break-glass. | None. Secrets Manager stores and audits secrets, which is adjacent. | `secrets-manager/overview.md`. A search of `docs/` for PAM returns no product page. | No evidence | Do not claim PAM. | None. If asked: "AccuKnox does not replace your PAM." |
| M9 | CLD 3.1.3 (p.16), 4.5.3.1-4.5.3.6 (p.20). ICT 5.18.1-5.18.19 (p.47-48). CSF 4.1.5.2, 4.1.5.13, 4.1.5.17, 4.1.5.18 (p.35-36). | Encrypt data at rest and in transit. Manage keys. Use dedicated keys. Rotate and destroy keys. | Secrets Manager Transit engine (encrypt, decrypt, sign, verify without the app holding keys). The platform encrypts its data at rest and in transit. CSPM lists a "CSPM Encryption Program". | `secrets-manager/transit.md`. `resources/data-usage-policy.md`, "For SaaS Deployment" (Security). `use-cases/compliance.md` (support matrix). | Partial | No evidence for HSM, customer-managed keys on the platform, or key rotation detail. The content of the "CSPM Encryption Program" is not described [SME]. Confirm Secrets Manager is in the webinar scope [SME]. | "AccuKnox encrypts its own data in transit and at rest. Secrets Manager offers encryption as a service for your applications." |
| M10 | CLD 2.1.1.2 a, c (p.13), 4.5.1.1-4.5.1.7, 4.5.1.11 (p.19). ICT 5.5.1.9 (p.38), 5.6.1.3, 5.6.2.1 (p.39), 5.6.2.7 (p.40). CSF 4.1.2.14 (p.32), 6.1.3.12(d), (g), (i) (p.46), 6.1.3.13(h) (p.47). | Segment networks and workloads. Inspect east-west traffic. Firewalls, IPS, DDoS protection. Review rules. | Kubernetes micro-segmentation at pod level. L3 and L4 network policy with DNS-based egress rules. Dashboard widget for workloads without network policies. | `use-cases/network-segmentation.md`. `use-cases/cwpp.md`, "Key Technical Features". `use-cases/cnapp-security-overview.md`, widget 8. | Partial | AccuKnox is not a perimeter firewall, NGFW, IPS, DDoS service or proxy. No evidence for any of them. CSF 6.1.3.13(h) says "inspect" east-west traffic. Policy enforcement is not firewall inspection [SME]. | "Controls east-west traffic between Kubernetes workloads to limit lateral movement. It sits alongside your perimeter firewall." |
| M11 | ICT 5.4.3.1-5.4.3.4 (p.37), 5.5 intro (p.37), 10.6.4 (p.67). CSF 4.1.4.1 (p.34), 4.1.8.4 (p.38), 4.1.8.10 (p.39). | Harden servers. Remove unused services. Allow-list authorized software. Least functionality. | CWPP on KubeArmor (eBPF and Linux Security Modules): process allow-listing, file and network limits, STIG and CIS host hardening, learned baseline, then BLOCK mode. | `use-cases/cwpp.md`, "Core Capabilities". `use-cases/zero-trust.md`. `use-cases/hardening.md`. `faqs/general.md` Q17 ("Host Hardening"). | Direct for Kubernetes workloads and Linux VMs | Windows servers and workstations: no evidence on these pages. `support-matrix/vms.md` lists Linux distributions only [SME]. | "Learns what each workload does, then blocks everything outside that baseline." |
| M12 | ICT 5.4.3.7 (p.37), 5.10.4 (p.42), 5.13.1-5.13.5 (p.45). CSF 5.1.2.17, 5.1.2.29 (p.42), 6.1.3.12(c), (q), (r) (p.46). | Anti-malware on servers and workstations. Behavior-based detection. Anti-APT. Sandboxing. | Host malware scanning for processes and files on VMs. Runtime blocking of processes outside the baseline. Malware scan of ML models. | `faqs/general.md` Q17 ("Malware Scanning"). `support-matrix/vms.md` (note). `use-cases/zero-trust.md` ("Unknown malware and unknown signatures are automatically rejected"). `index.md` (model scan). | Partial for servers and workloads | No evidence for workstation antivirus or EDR, MDM, sandboxing, anti-APT or email security. Malware detail rests on one FAQ line [SME]. | "On servers and workloads, AccuKnox blocks processes outside the learned baseline. It does not replace endpoint antivirus." |
| M13 | ICT 6.3.8 (p.51), 6.3.11 (p.51). CSF Appendix A item 4 (p.57). | Alert on unauthorized changes to critical files and configuration. | File integrity monitoring policies for VMs. They monitor and block changes to binaries, config files and credential paths. | `use-cases/vm-file-integrity.md`, "Purpose". `use-cases/cards/FIM.md`. | Direct | ICT 6.3.11 also names the registry. No Windows evidence. | "Real-time file-integrity policies for critical paths on VMs and workloads." |
| M14 | CLD 2.3.1.1 (p.15), 3.1.1, 3.1.2 (p.16), 6.7.1 f, g (p.26). CSF 4.1.5.3-4.1.5.6 (p.35), 5.1.2.24 (p.42). | Classify data before cloud hosting. Identify sensitive PII. Include data discovery. | DSPM scanner: 283 data classes, regulation mapping, read-only access, classification inside your region. | `getting-started/dspm-overview.md`: "What the Scanner Detects", "Supported Data Stores", "Data Privacy". | Partial | The 62 country packs include IN, PK and LK. They do not list Bangladesh, so Bangladesh NID and TIN are not named. Google Cloud Storage, Oracle Database and file shares are unsupported. The scanner "does not assess the controls around that data". | "Finds where regulated and sensitive data sits in your AWS and Azure data stores, and rates it by sensitivity." |
| M15 | CLD 2.2.1.2 d, e (p.14). ICT 5.3.4.1-5.3.4.6 (p.36). CSF 4.1.5.10 (p.36), 4.1.5.25 (p.37), Appendix A item 17 (p.57). | DLP policies and tools. Monitor data sharing. | None. DSPM only discovers data. Prompt Firewall blocks leaks in AI prompts. | A search of `docs/` for DLP returns no page. `getting-started/dspm-overview.md`, "Compliance Mapping". `use-cases/aiml-usecases.md` (Prompt Firewall row). | No evidence (AI prompts: Partial) | Do not claim DLP. | None. |

### C. Detect

| Ref | Source and section | Requirement | AccuKnox capability | Help-docs evidence | Coverage | Gaps and dependencies | Safe webinar wording |
|---|---|---|---|---|---|---|---|
| M16 | ICT 4.2.4 (p.23), 5.17.1-5.17.6 (p.47). CSF 3.1.9.1-3.1.9.15 (p.29-30), 5.1.2.3-5.1.2.9 (p.41). CLD 4.5.5.3 (p.20), 4.6.2-4.6.3 (p.21). | Central log management. Tamper protection. Retention. CLD 4.6.3: provider keeps logs 2 years and gives a GUI. | EventTrail records platform actions (who, when, result). Alerts and telemetry are stored with set retention. Export to Splunk, Sentinel, QRadar, rsyslog, CloudWatch and Sumo Logic. Backup to your own S3. | `getting-started/audit-trail-logs.md`. `resources/data-retention-policy.md`, "Retention Periods". `integrations/splunk.md`, `azure-sentinel.md`, `ibm-qradar.md`, `rsyslog.md`. `resources/scan-data-backup.md`. | Partial | Retention: alerts 180 days, EventTrail 180, CWPP telemetry 30, CDR cloud logs 90. The page allows custom windows by contract. The docs disagree: `data-usage-policy.md` says default 60 days and `scan-data-backup.md` says one month. AccuKnox is not the institution's central log platform. | "AccuKnox keeps its own audit trail and forwards alerts to your SIEM. Longer retention is available by contract." |
| M17 | ICT 5.17.3-5.17.4 (p.47), 6.3.6-6.3.13 (p.51). CSF 5.1.1.1-5.1.1.6 (p.40), 5.1.2.30-5.1.2.31 (p.42), 6.1.3.4-6.1.3.5 (p.45), 6.1.3.12(a), (s) (p.46). CLD 4.6.1, 4.6.4 (p.21). | Correlate events. SIEM. 24/7 SOC. Anomaly analytics. | Real-time workload behavior auditing and alerts. Behavioral baseline with anomaly alerts. Cloud-event detection (CDR). AI-DR. Forwarding to your SIEM. | `use-cases/cwpp.md` ("Key Technical Features"). `faqs/general.md` Q17 ("Anomaly Detection"). `use-cases/cdr.md`. `use-cases/aidr.md`. | Partial | AccuKnox acts as sensor, detector and forwarder. No page claims a SIEM or a 24/7 SOC. `cdr.md` says "SIEM/CNAPP Control Plane" and the retention page lists "SIEM" logs. Do not call AccuKnox a SIEM. `resources/managed-cloud-security-services.md` embeds a PDF I did not read [SME]. | "Detects at the workload and cloud layer, then feeds your SIEM and SOC." |
| M18 | CLD 2.2.1.2 a (p.14), 4.5.2.9 (p.20), 6.3.2 (p.25). CSF 5.1.1.1 (p.40). | Detect rogue services and compromised accounts. Detect unauthorized account creation. Capture changes in real time. | CDR ingests CloudTrail and cloud audit logs, detects policy violations and runs webhook or CI/CD remediation. | `use-cases/cdr.md`: "The Solution", "Primary Use Cases". | Direct for the events it has policies for | Docs show S3 exposure and unknown-region access. "Compromised account" detection is not stated [SME]. | "Reads cloud logs, spots risky changes as they happen and can revert them automatically." |
| M19 | ICT 6.5.1-6.5.3 (p.52). CSF 3.1.4.8 (p.26), Appendix A item 8 (p.57). | Threat intelligence platform and feeds. Integrate feeds with the SIEM. | Findings are enriched from NVD, EPSS, CISA KEV and OTX AlienVault. | `resources/vulnerability-database.md`. | Partial | No threat intelligence platform claim. No regulator or national CIRT feed (ICT 6.5.2 names them) [SME]. | "Enriches findings with public exploit and threat intelligence." |

### D. Respond

| Ref | Source and section | Requirement | AccuKnox capability | Help-docs evidence | Coverage | Gaps and dependencies | Safe webinar wording |
|---|---|---|---|---|---|---|---|
| M20 | ICT 6.3.1-6.3.5 (p.51), 6.6.1-6.6.4 (p.52-53). CLD 6.5.1-6.5.2 (p.25). CSF 6.1.3.2 (p.45), 6.1.4.9 (p.48). | Track incidents. Support forensic investigation. Route alerts to the right people. | Rule Engine creates tickets (Jira, ServiceNow) and notifies Slack and email. Process, file, network and syscall forensics. EventTrail records actions. | `use-cases/forensics.md`. `integrations/servicenow.md`. `use-cases/aspm.md`, "Rules Engine & Automated Ticket Creation". `getting-started/audit-trail-logs.md`. | Partial | The incident response plan, CIRT and regulator reporting (ICT 6.4.3) belong to the institution. | "Gives your responders the evidence and opens the ticket. The response plan stays yours." |

### E. Cloud, Residency and AI

| Ref | Source and section | Requirement | AccuKnox capability | Help-docs evidence | Coverage | Gaps and dependencies | Safe webinar wording |
|---|---|---|---|---|---|---|---|
| M21 | CLD 1.4 (p.11, multi-cloud, recommended), 2.3.1.3, 2.3.2.2, 2.3.4.3 (p.15). CSF 3.1.7.6 (p.28). | Complete visibility over public, private and hybrid cloud. Use a management platform for multi-cloud. | One view across AWS, Azure, GCP and OCI, plus OpenShift, EKS, AKS, VMware and Nutanix. | `use-cases/cspm.md` ("Multi-Cloud Platform"). `resources/deployment.md`, SaaS section. | Direct | None found. | "One view across your clouds, clusters and VMs." |
| M22 | CLD 2.3.1.2, 2.3.4.5, 2.3.3.2 (p.15), 5.2.10 m (p.23), 6.2.2 b (p.24), 6.9.1 (p.26). | Sensitive customer data stays out of cross-border public or hybrid cloud without prior Bangladesh Bank approval. Contracts name locations. | Four deployment models: SaaS, Your Cloud, On-Premises, Air-Gapped. The last three keep data local. DSPM classifies inside your region and sends only a findings file. | `resources/deployment.md`. `resources/data-usage-policy.md`, "Deployment Regions". `getting-started/dspm-overview.md`, "Data Privacy". | Partial | No Bangladesh SaaS region. SaaS keeps metadata, logs and findings outside Bangladesh. Whether that counts as "sensitive data" under CLD 2.3.1.2 is a legal question (Q-P3). `data-usage-policy.md` contains a literal `<ANSWER>` placeholder. | "Run the control plane in your own data center or cloud account. No data leaves." |
| M23 | CLD 4.8.1-4.8.3 (p.21). ICT chapter 9 (p.64). CSF section 7 (p.49-51). | Backup, DR and continuity. | Platform RTO 6 hours and RPO 24 hours. Runtime enforcement continues during control plane recovery. | `getting-started/accuknox-arch.md`, "SLA Commitments". | Partial | Covers the AccuKnox platform only. AccuKnox is not a backup product for customer data. | "Runtime enforcement keeps working if the control plane is down." |
| M24 | CSF 3.1.7.4 (p.28), 3.1.7.9 (p.28), Appendix C (p.59-62). ICT 7.1.2 (p.56). | Prove cloud services meet regulatory requirements. Self-assessment checklist. | Compliance dashboards across 30+ frameworks with scheduled and on-demand reports. SAMA Cyber Security Framework added in v3.6. | `use-cases/compliance.md`. `resources/sample-reports.md`. `getting-started/3.6-release.md`, "SAMA Cyber Security Framework". | Partial | No Bangladesh Bank framework in the list. CSF states it follows the NIST CSF functions and "mostly" ISO 27001 (CSF 1, p.11). NIST CSF and ISO 27001 reports are the nearest, but they are not a Bangladesh Bank score. Can a framework be added the way SAMA was (Q-S3)? The `compliance.md` matrix table omits SAMA and CSCRF, which the 3.6 notes list. | "Score your cloud accounts against NIST CSF and ISO 27001, which the framework draws on. AccuKnox does not issue a Bangladesh Bank score." |
| M25 | ICT 14.1.2.1, 14.1.2.4, 14.1.2.5 (p.89-90), 14.2.2.1-14.2.2.4 (p.90-91), 14.3.2.2, 14.3.2.6 (p.91), 14.4.1-14.4.6 (p.91-92). | Safeguard AI from corruption. Monitor AI. Protect PII. Inspect training data. Test for poisoning. Control bot access. | Model and dataset static scans, red teaming, Prompt Firewall, AI-DR, Agentic AI Security (ModelArmor), Shadow AI discovery, AI-SPM. | `use-cases/aiml-usecases.md`, "Which Module for Which Job". `getting-started/ai-security-arch.md`, "Known Limits". `use-cases/modelarmor.md`. `use-cases/prompt-firewall-overview.md`. `use-cases/red-teaming.md`. | Partial | Maps: 14.2.2.1 (model and dataset scans), 14.1.2.4 (AI-DR), 14.1.2.5 (Prompt Firewall), 14.4.3 (agent limits). Does not map: 14.2.2.2-14.2.2.4 (ground-truth tests, adversarial training), which are training duties. AI-DR detects and does not block. AI Identity Security and AI-GRC are not available yet. | "AccuKnox secures the AI you adopt and deploy. It scans models, tests them, filters prompts and watches for abuse." |

### F. Position Check

| Ref | Item | Finding |
|---|---|---|
| M26 | Containers, Kubernetes, zero trust, runtime | No requirement in CSF, ICT or CLD. Definitions only (CLD 1.4 p.10-12, 2.2 p.14). Say: "Runtime protection supports the Detect and Respond functions." Never say: "The guideline requires runtime security." |

## Eleven Asks Have No Help-Docs Evidence

These asks appear in the attachments. The help docs do not substantiate them. Do not claim them on the landing page, in the script or in the PPT.

| Code | Ask | Where the attachments raise it |
|---|---|---|
| G1 | Privileged access management | CLD 4.5.2.7, CSF 6.1.3.12(b), ICT 8.3.2 |
| G2 | Data loss prevention | CLD 2.2.1.2 d, ICT 5.3.4, CSF 4.1.5.25 |
| G3 | Web application firewall | CSF 6.1.3.12(f), ICT 6.2.4 |
| G4 | NGFW, IPS, DDoS protection, proxy | CSF 6.1.3.12(d), (g), (i), (l), CLD 4.5.1.3, 4.5.1.11 |
| G5 | SIEM, SOAR and 24/7 SOC | CSF 6.1.3.4-6.1.3.5, 6.1.3.12(a), ICT 6.3.10, 6.3.13 |
| G6 | Endpoint antivirus, EDR, MDM, email security (SPF, DKIM, DMARC), DNS protection | CSF 5.1.2.17, 4.1.3.19, 4.1.3.20, ICT 5.13 |
| G7 | Sandboxing, anti-APT, deception | CSF 6.1.3.12(c), (n), (q) |
| G8 | Network access control and VPN | CLD 4.5.1.4, CSF Appendix A item 19 |
| G9 | Log retention of 2 years | CLD 4.6.3 |
| G10 | Bangladesh-specific data classes (NID, TIN) | CLD 3.1.2 c i |
| G11 | A Bangladesh Bank compliance score | Whole of CSF and CLD |

## Out of Scope for Product Mapping

Most rows are governance, people or premises duties. No security product maps to them. Row counts from my inventory:

| Group | CSF | CLD | ICT |
|---|---|---|---|
| Governance and policy | 43 | 22 | 40 |
| Third-party and contract duties | 13 | 30 | 24 |
| Awareness and training | 6 | 7 | 17 |
| Physical security | 9 | 0 | 16 |
| Backup and DR (mostly institution duties) | 23 | 7 | 21 |

ICT chapter 11 (ATM, cards, mobile banking, SWIFT, p.69-77) and ICT 5.2 (data center facilities) have no match in the help docs either.

## A 60-Minute Agenda Fills the Full Hour

Title kept from the Oct 21 email: "Zero Trust for Bangladesh's Banks and Telcos - Compliance to Runtime". Consider a title change (Q-P1, F3).

| Time | Segment | Who | Content |
|---|---|---|---|
| 0:00-0:03 | Welcome | SmartData moderator | Housekeeping and speaker intros. |
| 0:03-0:10 | Bangladesh threat landscape | SmartData | Local incidents and the reason cloud security matters now. |
| 0:10-0:20 | What the Bangladesh Bank documents ask of security teams | SmartData and AccuKnox SME | The CSF functions (Identify, Protect, Detect, Respond, Recover). Data residency in CLD 2.3.1.2. Logging and access themes. |
| 0:20-0:30 | From requirement to control | AccuKnox SME | The matrix summary: where a cloud-native platform supports a clause, where it supports part, and where it does not apply (G1-G11). |
| 0:30-0:45 | Live demo | AccuKnox SME | 1) A risky cloud setting found and scored (M2, M24). 2) Sensitive data located (M14). 3) A runtime block on an unapproved process, with a ticket and an alert to a SIEM (M11, M17, M20). |
| 0:45-0:50 | Deployment for data residency | AccuKnox SME | On-Premises and Your Cloud models for in-country data (M22). |
| 0:50-0:53 | AI security | AccuKnox SME | Shadow AI discovery, model scan, Prompt Firewall, and the link to ICT chapter 14 (M25). |
| 0:53-1:00 | Joint POC offer and Q&A | Both | Offer terms from SmartData. Open questions. |

Demo notes:

1. Demo only what a help page documents. Rehearse each step in an environment that matches what the audience runs.
2. Replace "compliance report exported" from the Oct 21 agenda with "posture scored against NIST CSF and ISO 27001". A Bangladesh Bank report does not exist today (F1).
3. Replace "Bangladesh Bank ICT and Cloud Guidelines mapped to controls" with "what the guidelines ask, and where our capabilities support them". The word "mapped" reads as a compliance claim.

## Safe Wording for the Landing Page, Script and PPT

Use:

1. "Security capabilities that support the Bangladesh Bank Cybersecurity Framework and Cloud Guidelines."
2. "Aligns with the Identify, Protect, Detect, Respond and Recover functions." (CSF states it uses the NIST CSF functions.)
3. "Run the control plane in your own data center or cloud account."
4. "A CNAPP capability, a solution category named in CSF 6.1.3.12(p)."

Avoid:

1. "Compliant with", "certified for", "meets" or "satisfies" any Bangladesh Bank document.
2. "Bangladesh Bank-ready" or a Bangladesh Bank compliance report.
3. "The guideline requires zero trust or runtime security."
4. Claims for PAM, DLP, WAF, SIEM, 24/7 SOC or endpoint protection.
5. Claims about telcos being in scope of these documents.

## Open Questions Need SME and Partner Answers Before Nov 26

### For the AccuKnox Technical SME

| Code | Question |
|---|---|
| Q-S1 | Who is the senior technical SME on Nov 26? The Nov 4 scrum says the AccuKnox speaker is not confirmed and must be senior. |
| Q-S2 | Does a CSPM check flag cloud services open to any source IP on AWS, Azure and GCP (CLD 2.1.1.2 b)? |
| Q-S3 | Can the Compliance module load a custom framework, as it did for SAMA in v3.6? How long would a Bangladesh Bank CSF take? |
| Q-S4 | Do CIEM or CSPM check MFA, unused accounts and new account creation (CLD 4.5.2.3, 4.5.2.9)? |
| Q-S5 | Does the console enforce MFA? Does the platform support customer-managed keys or an HSM? |
| Q-S6 | Can we state a 2-year log retention (CLD 4.6.3)? Which of the 60-day, 30-day and 180-day figures in the docs is right? |
| Q-S7 | Does the Managed Cloud Security Services PDF offer 24/7 monitoring? Can we call anything a SOC or SIEM? |
| Q-S8 | Does workload protection and malware scanning cover Windows servers, or only Linux? |
| Q-S9 | Is a Bangladesh DSPM country pack (NID, TIN, mobile numbers) on the roadmap? |
| Q-S10 | Does API Security revoke keys or tokens on suspicious use (ICT 10.8.7)? |
| Q-S11 | Which AI modules are generally available today: AI-DR, Prompt Firewall, ModelArmor, red teaming? |
| Q-S12 | Which demo steps can run live without risk? |

### For SmartData (Kausar Ahmed and team)

| Code | Question |
|---|---|
| Q-P1 | The documents apply to banks, financial institutions, MFS, PSP and PSO. Which regulator and document apply to the telco audience? Should we drop "Telcos" from the title? |
| Q-P2 | Is the Cybersecurity Framework v1.0 (2026) mandatory or a baseline? What is the circular number and effective date? What is the exact compliance date in the Cloud Guidelines circular (BRPD 05, March 16, 2023)? |
| Q-P3 | Does Bangladesh Bank treat a security SaaS that holds findings and metadata as "sensitive data" in a cross-border cloud (CLD 2.3.1.2)? Will your banks prefer an in-country control plane? |
| Q-P4 | Which requirements do your customers ask about most? Do you have an RFP matrix we can align to? |
| Q-P5 | Who is your moderator and speaker? When do you need the topic and final EDM content? |
| Q-P6 | Do you want to review the landing page wording before it goes live? |
| Q-P7 | Do you agree to the 60-minute run of show above? The Oct 21 agenda fills only 30 minutes. |

### Fixes in the Help Docs

| Code | Fix |
|---|---|
| D1 | `resources/data-usage-policy.md` contains a literal `<ANSWER>` placeholder under "How Are Updates Fetched on Airgapped/On-Prem Env?". |
| D2 | Retention figures conflict across `data-usage-policy.md` (60 days), `data-retention-policy.md` (30 to 365 days) and `scan-data-backup.md` (one month). |
| D3 | The support matrix table in `use-cases/compliance.md` omits SAMA and CSCRF SEBI. `getting-started/3.6-release.md` lists both as mappings. |

## What I Checked and What I Did Not

1. I read all 3 attachments in full. Three agents read one document each and wrote requirement inventories. I spot-checked 10 citations against the extracted text: CLD 2.3.1.2, 2.3.4.5, 4.6.3, ICT 6.3.11, 14.2.2.1, CSF 4.1.2.12, 6.1.3.12(p), 1.1 scope and the NIST and ISO sentence. All matched.
2. I did not check the other 1,070 rows one by one. Check any clause before you quote it.
3. CLD page 1 (the circular) is unreadable text from a legacy Bengali font. CLD-001 to CLD-003 are low confidence.
4. CSF Figures 2.3 and 2.4 did not extract. Some CSF table text is jumbled.
5. I read help-doc pages and sections cited above. I did not read every page in `docs/`. A "No evidence" row means a keyword search found nothing. It does not prove the capability is missing.
6. I did not run the product. Every capability line is what the docs say.
7. I did not send email, post to Slack or publish anything.

## Full Requirement Inventories Sit in the Scratchpad

Full requirement inventories, one row per clause, with exact section and page:

1. `/private/tmp/claude-501/-Users-atharva--claude-spares-spare-pwXavI/17373a0c-4b37-4935-b7b1-52caf657ed86/scratchpad/att/csf-requirements.md` (425 rows)
2. `/private/tmp/claude-501/-Users-atharva--claude-spares-spare-pwXavI/17373a0c-4b37-4935-b7b1-52caf657ed86/scratchpad/att/cloud-requirements.md` (214 rows)
3. `/private/tmp/claude-501/-Users-atharva--claude-spares-spare-pwXavI/17373a0c-4b37-4935-b7b1-52caf657ed86/scratchpad/att/ict-requirements.md` (445 rows)
