---
title: Data Processing Addendum
description: How AccuKnox processes personal data for customers, covering roles, security measures, sub-processors, international transfers, breach notice, and deletion rights.
---

# Data Processing Addendum

This Data Processing Addendum (DPA) forms part of the agreement between AccuKnox, Inc. and the
customer that subscribes to the AccuKnox platform. It applies whenever AccuKnox processes personal
data on the customer's behalf. Where a term here conflicts with the main agreement, this DPA wins
for personal data and the main agreement continues to govern everything else.

You do not need to sign this document to rely on it. It applies automatically to every SaaS
subscription. A customer who needs a countersigned copy, or a copy on their own paper, can request
one from [support@accuknox.com](mailto:support@accuknox.com).

!!! info "Deployment model decides how much of this page applies"
    In an on-premises or air-gapped deployment, all security data stays inside your own
    infrastructure. AccuKnox sends nothing outward unless you configure an outbound integration
    yourself, such as a SIEM forwarder. In that model AccuKnox processes no personal data for you,
    and only Sections 1, 5 and 12 below have any effect. Everything else describes the SaaS
    platform.

## 1. Terms used in this document

| Term | What it means here |
| :-- | :-- |
| **Applicable Data Protection Law** | Every privacy law that applies to the processing, including the EU General Data Protection Regulation (Regulation (EU) 2016/679), the UK GDPR and the UK Data Protection Act 2018, the Swiss Federal Act on Data Protection, and the California Consumer Privacy Act as amended. |
| **Controller** | The party that decides why and how personal data is processed. The customer is the controller. |
| **Processor** | The party that processes personal data on the controller's instructions. AccuKnox is the processor. |
| **Customer Personal Data** | Personal data inside the security telemetry, findings, account records and support correspondence that the customer sends to the AccuKnox platform. |
| **Data Subject** | The identified or identifiable person the personal data relates to. |
| **Sub-processor** | A third party AccuKnox engages to process Customer Personal Data. Annex 4 lists them. |
| **Security Incident** | A confirmed breach of security that leads to accidental or unlawful destruction, loss, alteration, or unauthorised disclosure of or access to Customer Personal Data. |
| **SCCs** | The standard contractual clauses in European Commission Implementing Decision (EU) 2021/914. |
| **UK Addendum** | The International Data Transfer Addendum to the SCCs issued by the UK Information Commissioner's Office. |
| **Restricted Transfer** | A transfer of personal data to a country with no adequacy decision covering it. |

Read the GDPR articles cited on this page in the
[official EUR-Lex text of Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj).

## 2. The customer is the controller and AccuKnox is the processor

You decide which clusters, cloud accounts, repositories and workloads you connect, and which fields
that telemetry carries. AccuKnox never decides that for you, so you hold the controller obligations
under Article 24 of the GDPR and AccuKnox holds the processor obligations under Article 28.

AccuKnox processes Customer Personal Data only to deliver, secure, support and bill the platform,
and only on your documented instructions. Your instructions are this DPA, the main agreement, your
configuration in the console, and any later written instruction you send. AccuKnox does not sell
Customer Personal Data, does not share it for cross-context behavioural advertising, and does not
use it to train any AccuKnox model or any third-party model.

If AccuKnox believes an instruction you give breaks Applicable Data Protection Law, AccuKnox tells
you and may pause that processing until the two parties resolve it. AccuKnox does not act on the
instruction in the meantime.

## 3. Everyone who touches the data is under a confidentiality duty

AccuKnox limits access to Customer Personal Data to staff who need it to run, support or secure the
platform. Every such person is bound by a written confidentiality obligation that survives the end
of their engagement, and access is removed when the need ends.

## 4. Security measures AccuKnox applies

AccuKnox applies technical and organisational measures appropriate to the risk, as Article 32 of the
GDPR requires. Annex 3 lists the current measures. AccuKnox may update a measure at any time and
will not make a change that lowers the overall level of protection.

Some controls are yours rather than ours. Choosing who gets an account, assigning roles, revoking
access when someone leaves, and deciding which integrations to enable are all customer decisions,
and no vendor control substitutes for them.

## 5. Sub-processors and how you get told about a change

You give AccuKnox general written authorisation to engage the sub-processors listed in Annex 4.
Each one is engaged under a written contract that imposes data-protection duties no weaker than
this DPA, and AccuKnox stays fully liable to you for what a sub-processor does.

AccuKnox updates Annex 4 before a new sub-processor starts processing Customer Personal Data, and
gives you at least [confirm the notice period, for example 30 days] advance notice. To receive that
notice by email, ask [support@accuknox.com](mailto:support@accuknox.com) to add your address to the
sub-processor notification list.

You may object to a new sub-processor in writing within [confirm the objection window, for example
30 days] of the notice, stating your data-protection grounds. AccuKnox will then try to offer a
change that avoids the processing. If no reasonable change is available, you may terminate the
affected subscription and receive a pro-rata refund of prepaid fees for the unused term.

!!! note "An integration you connect yourself is not a sub-processor"
    When you send AccuKnox findings to your own Jira, Slack, Splunk or Jenkins, that vendor
    processes data for you and not for AccuKnox. Those tools never appear in Annex 4. Your own
    agreement with that vendor covers them.

## 6. AccuKnox helps you answer data subject requests

The AccuKnox console lets an administrator read, correct, export and delete user account records
directly, which resolves most requests without contacting AccuKnox.

Where a request needs more, AccuKnox gives you reasonable assistance to meet your obligations under
Articles 12 to 22 of the GDPR, taking account of what a processor can see. If a data subject
contacts AccuKnox directly about your data, AccuKnox does not answer the substance. AccuKnox
forwards the request to you without undue delay and tells the person that you are the controller.

## 7. Assistance with impact assessments

AccuKnox gives you reasonable assistance with a data protection impact assessment under Article 35
of the GDPR, and with prior consultation of a supervisory authority under Article 36, so far as the
assistance relates to processing that AccuKnox performs. Annex 2 and Annex 3 answer most assessment
questions on their own.

## 8. What happens after a security incident

AccuKnox notifies you without undue delay after becoming aware of a Security Incident affecting
Customer Personal Data. The notice describes the nature of the incident, the categories and
approximate volume of data involved, the likely consequences, the measures taken, and the contact
point for follow-up. Where AccuKnox cannot provide all of that at once, the information follows in
stages.

Article 33 of the GDPR gives you, the controller, 72 hours from becoming aware to notify your
supervisory authority. AccuKnox timing supports that deadline and does not replace it, because the
duty to notify the authority and the affected people stays with you.

An AccuKnox notice is not an admission of fault. Do not name AccuKnox publicly in connection with an
incident without written approval, unless a law or a regulator requires it.

## 9. Audit rights and the evidence AccuKnox provides

AccuKnox makes available the information needed to show compliance with Article 28 of the GDPR.
In the first instance that means the current audit report and security documentation, which you can
request from [support@accuknox.com](mailto:support@accuknox.com).

Where a report does not answer your question, you may audit once in any twelve-month period, on 30
days written notice, during business hours, without disrupting the platform, and under
confidentiality. A supervisory authority exercising a statutory power is not subject to those
limits. You may also audit after a Security Incident that affected your data.

## 10. International transfers

AccuKnox runs the SaaS control plane in four regions, so most customers can keep processing inside
one of them.

| Region | Console address |
| :-- | :-- |
| United States | `app.accuknox.com` |
| Europe | `app.eu.accuknox.com` |
| Middle East | `app.me.accuknox.com` |
| India | `app.in.accuknox.com` |

Your tenant stays in the region you onboard into. AccuKnox does not move your findings, telemetry or
reports to another region without your instruction. Support staff and sub-processors may still
access data from another country, which makes a Restricted Transfer, so the safeguards below apply.

Where a Restricted Transfer happens, the SCCs apply and are incorporated into this DPA by reference.
Module Two, controller to processor, applies. The optional docking clause applies. In Clause 9,
option two, general written authorisation, applies with the notice period in Section 5. In Clause
11, the optional independent dispute resolution body does not apply. In Clause 17, the governing law
is the law of [confirm the SCC governing law, for example Ireland]. In Clause 18, the forum is
[confirm the SCC forum, matching the Clause 17 choice]. Annex 1 and Annex 2 of this page populate
Annexes I and II of the SCCs.

For a transfer covered by UK law, the UK Addendum applies to the SCCs and the UK Information
Commissioner is the supervisory authority. For a transfer covered by Swiss law, references in the
SCCs to the GDPR read as references to the Swiss Federal Act on Data Protection, the Swiss Federal
Data Protection and Information Commissioner is the supervisory authority, and the term "member
state" does not stop a Swiss data subject from suing where they live.

AccuKnox certification under the EU-U.S. Data Privacy Framework is [confirm whether AccuKnox, Inc.
is certified under the EU-U.S. Data Privacy Framework, and the certification date].

## 11. How long data stays and what happens at the end

Retention is set per data type, not per contract. The
[Data Retention Policy](data-retention-policy.md) gives the exact window for each one, from 30 days
for workload telemetry to 365 days for raw scanner reports in object storage. Data is deleted
automatically once its window ends.

When the subscription ends, AccuKnox deletes Customer Personal Data or returns it to you, at your
choice, within [confirm the post-termination deletion window, for example 30 days] of the request.
Export your evidence before you cancel, because deletion after that window is not reversible.

AccuKnox may keep a copy where a law requires it. Any copy kept for that reason stays isolated,
stays under the security measures in Annex 3, and is processed for no purpose other than the legal
requirement until deletion becomes permitted. Backups follow their own rotation and are overwritten
on the normal cycle.

## 12. Changes to this page

AccuKnox may update this DPA to reflect a change in law, in the platform, or in the sub-processor
list. A change that materially reduces your rights takes effect only after notice to you. A change
to Annex 4 follows the notice and objection process in Section 5.

Effective date: [confirm the effective date]. Last reviewed: [confirm the review date]. Review
cadence: quarterly.

---

## Annex 1, the parties

**Data exporter (controller).** The customer named on the order form, at the address and contact
details held in that order form or in the customer's AccuKnox account. Activity: receiving cloud
and workload security services from AccuKnox.

**Data importer (processor).** AccuKnox, Inc., 333 Ravenswood Ave, Menlo Park, CA 94025, USA.
Contact for data protection questions: [support@accuknox.com](mailto:support@accuknox.com).
Activity: providing
the AccuKnox platform, which scans cloud accounts, Kubernetes clusters, hosts, container images,
source code and AI models, and reports the findings back to the customer.

**Competent supervisory authority.** The authority of the EEA member state where the customer is
established, or where the customer's EU representative sits, or where the affected data subjects
are mostly located.

## Annex 2, what is processed

| Item | Detail |
| :-- | :-- |
| **Categories of data subject** | Employees, contractors and agents of the customer who hold a console account. People whose identifiers appear inside security telemetry, findings, cloud metadata or source code the customer connects. |
| **Categories of personal data** | Account records such as name, work email address, role and authentication metadata. Console and API activity logs. Support correspondence and its attachments. Cloud and workload metadata, such as IAM principal names, resource owner tags, process and user identifiers in runtime events, and commit author identifiers in code findings. Billing contact and transaction records. |
| **Special category data** | None is requested and none is required. The customer controls what its telemetry carries, so the customer must not route special category data into the platform. |
| **Frequency of processing** | Continuous for telemetry and findings while a subscription is active. Ad hoc for support and billing. |
| **Nature of processing** | Collection, storage, structuring, correlation, analysis against policy and benchmark rules, reporting, and deletion at the end of the retention window. |
| **Purpose of processing** | Delivering the platform, supporting it, securing it, and billing for it. |
| **Retention** | Per data type, as set out in the [Data Retention Policy](data-retention-policy.md). |
| **Sub-processor processing** | Each sub-processor in Annex 4 processes only the data categories named in its row, for the purpose named in its row, and for as long as AccuKnox needs the service. |

## Annex 3, technical and organisational measures

1. **Encryption.** Customer data is encrypted in transit and at rest. [Confirm the cipher suites and
   the minimum TLS version to state here.]
2. **Tenant isolation.** The platform separates tenants at the user, data and workload layers.
   Access is scoped by tenant and can be narrowed further to a resource group, so a team sees only
   the assets assigned to it.
3. **Access control.** Role-based access control governs both customer accounts and AccuKnox
   internal access. AccuKnox grants internal access on a need-to-know basis and removes it when the
   need ends.
4. **Regional residency.** The four control-plane regions in Section 10 keep a tenant's data in the
   region it was onboarded into.
5. **Automatic deletion.** Retention windows are enforced by the platform rather than by a manual
   process, so data expires on schedule.
6. **Logging.** EventTrail records control-plane activity, including who changed a finding's status
   and when a ticket was created, and is retained for 180 days.
7. **Vulnerability management.** AccuKnox scans its own platform with the same engines it ships to
   customers, covering container images, infrastructure as code, source code and cloud posture.
8. **Independent assessment.** AccuKnox holds a SOC 2 certification. [Confirm the report type, the
   audit period, and how a customer requests the report.]
9. **Personnel.** Staff with access to Customer Personal Data are under written confidentiality
   obligations and complete security training. [Confirm the background-check practice and the
   training cadence.]

## Annex 4, sub-processors

Every third party below processes Customer Personal Data on AccuKnox's behalf. Not every one is used
for every service or every deployment. An on-premises deployment usually involves none of them.

| Sub-processor | Purpose | Data categories | Legal entity and headquarters | Processing location | Transfer mechanism |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **[Confirm the cloud infrastructure provider, and the contracting entity per region]** | Hosting and storage for the AccuKnox control plane and customer data | Account data, telemetry, findings, reports, raw scanner output | [Confirm] | [Confirm the region mapping for the US, Europe, Middle East and India consoles] | [Confirm] |
| **Brevo** | Delivery of transactional, system and notification email | Name, email address | Sendinblue SAS, trading as Brevo, Paris, France | [Confirm] | [Confirm] |
| **Jira Service Management** | Support ticketing and case management for requests raised to `support@accuknox.com` | Name, email address, ticket contents and attachments | Atlassian Pty Ltd, Sydney, Australia, and Atlassian, Inc., San Francisco, USA | [Confirm] | [Confirm] |
| **Sentry** | Application error and exception monitoring | Diagnostic and error event data, which can carry user and account identifiers | Functional Software, Inc., trading as Sentry, San Francisco, USA | [Confirm] | [Confirm] |
| **PostHog** | Product usage analytics | Usage and event data, user and account identifiers | PostHog, Inc., San Francisco, USA | [Confirm] | [Confirm] |
| **OpenAI** | AskAI, remediation guidance and Copilot, running on GPT-4o. Disabled by default and active only when the customer opts in. | Asset name, asset ID, resource type, and the technical detail of a finding. No PII, no raw payloads, no unrelated database content. | [Confirm the contracting OpenAI entity, and whether the model is reached through the OpenAI API or a cloud provider's hosted endpoint] | [Confirm] | [Confirm] |
| **[Confirm the payment and billing processor]** | Subscription billing and payment processing | Billing contact, transaction data | [Confirm] | [Confirm] | [Confirm] |
| **[Confirm whether a CDN, WAF or DDoS provider fronts the control plane]** | Edge protection and content delivery | Source IP address, request metadata | [Confirm] | [Confirm] | [Confirm] |
| **[Confirm any remaining vendor with access to production data or customer contact data, including monitoring, log aggregation, CRM and code hosting]** | [Confirm] | [Confirm] | [Confirm] | [Confirm] | [Confirm] |

The AI features in the OpenAI row stay off until you ask for them. To enable them, contact
[support@accuknox.com](mailto:support@accuknox.com). Leaving them off keeps every finding inside the
AccuKnox control plane.

## Questions

Send data protection questions, audit report requests, countersignature requests and platform
support questions to [support@accuknox.com](mailto:support@accuknox.com). That address reaches the
queue described in the [Ticketing Procedures](ticket-procedure.md), and a data protection request
is routed from there to the AccuKnox legal and GRC team.

For how AccuKnox handles personal data as a controller, on its own website and in its own sales and
marketing, read the [AccuKnox privacy policy](https://www.accuknox.com/privacy-policy). This DPA
covers the separate case where AccuKnox processes data on your instructions.
