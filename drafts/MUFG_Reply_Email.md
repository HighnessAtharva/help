Subject: Re: [AccuKnox | MUFG Bank] Suggested answers to MUFG's 4 questions

Hi John, Rahul and team,

I went through our help docs, the AgentZ docs and the latest deck, and I have drafted an answer to each of MUFG's questions below. Most are ready to send. Five points need Rahul's confirmation, and they are listed at the end. John, once Rahul replies, the answers can go to Ishida-san.

Q1. Which capabilities (CSPM, CIEM, vulnerability management, CWPP) can run fully agentless? For capabilities that need agents, what are the deployment requirements and the impact on workloads?

A1. CSPM and vulnerability management run fully agentless. CSPM uses read-only cloud APIs and changes nothing in the account. VM scanning uses a scanner inside the customer's own account (AWS, GCP, Azure, OpenShift), and Kubernetes clusters scan remotely. CIEM uses the same read-only onboarding. Only runtime protection (CWPP) needs an agent, KubeArmor. It runs as a DaemonSet on Kubernetes and in systemd mode on VMs. It keeps enforcing if the control plane goes down. The VM scan service is capped at 2 GB memory and 10% CPU by default.
Pending with Rahul: CIEM availability (Q1 below) and KubeArmor CPU and memory numbers (Q2 below).
Evidence: https://help.accuknox.com/faqs/cspm/ , https://help.accuknox.com/how-to/vm-security/agentless/cloud-vm-scanning/ , https://help.accuknox.com/getting-started/accuknox-agents/

Q2. How much of the solution can run entirely in customer-managed infrastructure? Does any telemetry or workload data go to an AccuKnox-hosted environment?

A2. All of it. The full platform runs inside MUFG, on premises or air-gapped, and no data leaves. An air-gapped install makes no call-home. In SaaS, findings, metadata and logs go to AccuKnox cloud, encrypted in transit and at rest. We have no SaaS region in Japan today (US, Europe, Middle East, India), so on premises is the best fit. On premises has every feature except the AI CoPilot. The customer handles updates, image staging, monitoring and backups.
Pending with Rahul: on-premises in Tokyo, and agentless scans reporting to an on-premises control plane (Q3 and Q4 below).
Evidence: https://help.accuknox.com/resources/deployment/ , https://help.accuknox.com/resources/data-usage-policy/

Q3. Can AI-SPM be introduced without changing our existing AI, LLM and agent platform? Are there technical dependencies or vendor lock-in with AgentZ?

A3. Yes, AI-SPM needs no platform change. Discovery is agentless. The Prompt Firewall plugs into a gateway MUFG already runs, such as LiteLLM or Azure APIM, with no application code change. AgentZ has no vendor lock-in. It plugs into any MCP server and any model, and AI-SPM does not need it. We recommend AccuKnox for the assets MUFG already onboards. In that case AgentZ works as an agentic control plane that does reporting and triage on those assets, when MUFG wants it.
Pending with Rahul: nothing.
Evidence: https://help.accuknox.com/faqs/ai-security/ , https://docs.agentzharness.ai/configure/mcp-connections/

Q4. What are AccuKnox's key differentiators, and what is the minimum customer effort to evaluate?

A4. Three differences. We block attacks in the kernel at runtime instead of only alerting. The same platform runs as SaaS, on premises or air-gapped. AI security sits in the same console. The smallest evaluation is one read-only role in one non-production cloud account plus one scanner per region, which takes a few hours. KubeArmor on one non-production cluster is optional. An on-premises control plane needs 3 nodes and takes 2 to 3 weeks.
Pending with Rahul: whether Nutanix and OCI VMs are agentless today (Q5 below).
Evidence: https://help.accuknox.com/faqs/general/ , https://help.accuknox.com/getting-started/on-prem-installation-guide/

Rahul, please confirm these 5 points. Reply Yes, No or Partly, with one line each.
1. Is CIEM generally available today? Does it support AWS organization accounts?
2. What are the typical KubeArmor CPU and memory numbers per node? Do we have a benchmark?
3. Can agentless cloud and VM scanning report to an on-premises or air-gapped control plane?
4. Can we run the full platform on premises for MUFG in Tokyo? Is a Japan SaaS region planned?
5. Is agentless scanning live for Nutanix and OCI VMs? Our deployment page says yes, and the VM scanning page says planned.

Thanks,
Atharva

P.S. Vanisha, yes, I will walk you through my knowledge stack: the website, help docs, PPTs and sales page references, plus tools such as Firecrawl and Treg for social signals, competitor sites and real-time web indexing. Let's connect when you have time. From now on, please reply to some of these clarifying-question threads, so you build that muscle.
