# MUFG Bank: Suggested Responses to the Four CNAPP Questions

Internal draft for John, Rahul, Murtaza, Maya and Technical Support. Every answer links to the page that backs it. Items marked **Confirm** need a yes from Rahul or Murtaza before this goes to MUFG. The list of open items is at the bottom.

## 1. CSPM and VM Scanning Run Fully Agentless, Runtime Needs an Agent

**Short answer.** CSPM and VM vulnerability scanning run fully agentless. Runtime protection (CWPP) needs the KubeArmor agent. One AccuKnox control plane covers both.

| Capability | Agentless? | How it works | Evidence |
|---|---|---|---|
| CSPM | Yes, fully | Read-only cloud APIs. AWS needs `ReadOnlyAccess` and `SecurityAudit`. Azure and GCP need read-only service credentials. It changes nothing in your account. | [CSPM FAQ](https://help.accuknox.com/faqs/cspm/) |
| CIEM | Yes, same read-only onboarding | Lists users, groups, roles and policies for AWS, GCP, Azure and OCI. **Confirm:** the docs mark CIEM "coming soon" in a newer release. It supports standalone accounts only, not organization accounts. | [CIEM overview](https://help.accuknox.com/getting-started/ciem-overview/) |
| Vulnerability management, VMs | Yes | A scanner VM in your account snapshots each VM disk and scans the copy. It supports AWS, GCP, Azure and OpenShift. OCI and Nutanix are planned. | [Agentless VM scanning](https://help.accuknox.com/how-to/vm-security/agentless/cloud-vm-scanning/) |
| Vulnerability management, Kubernetes | Yes | Remote scan through `kubeconfig`, or a Kubernetes job. | [Onboarding overview](https://help.accuknox.com/how-to/high-level-onboarding/) |
| VM STIG and risk assessment | No | Needs a lightweight VM agent. | [Onboarding overview](https://help.accuknox.com/how-to/high-level-onboarding/) |
| CWPP runtime | No | KubeArmor, built on eBPF and Linux Security Modules. | [AccuKnox Agents](https://help.accuknox.com/getting-started/accuknox-agents/) |
| AI-SPM discovery | Yes | Read-only APIs for Bedrock, SageMaker, Azure AI Foundry, Copilot Studio and Vertex. | [AI Security FAQ](https://help.accuknox.com/faqs/ai-security/) |

**Agent requirements and impact.**

- **Kubernetes:** KubeArmor deploys as a DaemonSet. **VMs:** it deploys in systemd mode. Both install with Helm or a script. ([Deployment FAQ](https://help.accuknox.com/faqs/deployment/))
- **Kernel:** it needs AppArmor, SELinux or BPF-LSM enabled. ([Support matrix](https://help.accuknox.com/support-matrix/kubearmor-support-matrix/))
- **Resource limits:** the VM scan service is capped at 2 GB memory and 10% CPU by default. Malware scanning is off by default because it is CPU-heavy. ([Linux agent](https://help.accuknox.com/how-to/vm-security/agent-based/linux/))
- **Availability:** runtime enforcement keeps running if the control plane goes down. ([Deployment FAQ](https://help.accuknox.com/faqs/deployment/))
- **Agentless cost:** one scanner costs about $30 to $68 a month per region in your cloud bill, before usage. ([Cost page](https://help.accuknox.com/resources/agentless-scan-cost/))
- **Confirm:** we publish no CPU or memory benchmark for KubeArmor. The FAQ says only that overhead is "extremely low".

## 2. The Full Platform Runs Inside MUFG With No Data Leaving

**Short answer.** Yes. The full platform runs inside MUFG infrastructure, on premises or air-gapped, and no data leaves.

| Model | Control plane runs in | Data leaving your network |
|---|---|---|
| SaaS | AccuKnox cloud | Findings, metadata and logs go to AccuKnox. Encrypted at rest and in transit. |
| Your Cloud | Your cloud account | None |
| On-Premises | Your servers, native install | None, unless you configure a SIEM or GenAI link |
| Air-Gapped | Your isolated network | None. No call-home. |

Evidence: [Deployment models](https://help.accuknox.com/resources/deployment/) and [Data Usage Policy](https://help.accuknox.com/resources/data-usage-policy/).

- **Features:** on premises has every feature except the AI CoPilot (AskADA). AI-SPM has full parity. ([AI-SPM SaaS vs on-prem](https://help.accuknox.com/how-to/aiml-saas-vs-onprem/))
- **AI assistant:** it is off by default. It turns on only by opt-in. ([Data Usage Policy](https://help.accuknox.com/resources/data-usage-policy/))
- **What MUFG runs on premises:** vulnerability database updates, container image staging, monitoring and backups. ([Deployment FAQ](https://help.accuknox.com/faqs/deployment/))
- **Sizing:** 3 nodes (one 4 CPU and 16 GB, two 8 CPU and 16 GB), 256 GB disk each, Debian 13. ([On-prem install guide](https://help.accuknox.com/getting-started/on-prem-installation-guide/))
- **SaaS regions:** US, Europe, Middle East and India. No Japan region is listed.

## 3. AI-SPM Needs No AgentZ and No Platform Change

**Short answer.** No dependency. AI-SPM runs beside your current AI platform. AgentZ is a separate product, and you do not need it for AI-SPM.

**AI-SPM, no platform change.**

- Discovery is agentless. Red teaming tests your models and apps by endpoint. ([AI Security FAQ](https://help.accuknox.com/faqs/ai-security/))
- The Prompt Firewall connects through an API gateway you already run: LiteLLM, Bifrost, AWS API Gateway, Azure APIM or Apigee. A gateway needs no application code change. The SDK option does. ([AI Security FAQ](https://help.accuknox.com/faqs/ai-security/))
- It inspects only traffic that passes through the gateway. Block direct egress to model providers to close the gap. ([AI Security FAQ](https://help.accuknox.com/faqs/ai-security/))

**AgentZ, lock-in facts.**

- AgentZ builds and runs new agents. It is not a CNAPP and it does not wrap external agents. ([AgentZ FAQ](https://docs.agentzharness.ai/reference/faq/))
- The source is open under Apache-2.0. You can self-host on Kubernetes 1.34 or later with Cilium. ([Hosted or self-hosted](https://docs.agentzharness.ai/deploy/hosted-or-self-hosted/))
- You bring your own model through any OpenAI-compatible or Anthropic-compatible endpoint. AgentZ ships no model. ([AgentZ FAQ](https://docs.agentzharness.ai/reference/faq/))
- For agents MUFG already runs, ModelArmor sandboxes them with KubeArmor and needs no code change. It covers LangGraph, n8n, CrewAI and Strands. ([ModelArmor](https://help.accuknox.com/use-cases/modelarmor/), AI Agent Security deck, slide 7)
- **Confirm:** the docs do not describe an export path for agents built in AgentZ.

## 4. Runtime Prevention Differentiates, and Phase 1 Takes Hours

**Differentiators.**

1. **Prevention at runtime.** KubeArmor blocks attacks in the kernel before damage, where most tools alert after. It is open source, with 10+ patents. ([General FAQ](https://help.accuknox.com/faqs/general/))
2. **One platform in every deployment model.** SaaS, your cloud, on premises and air-gapped carry the same policies. ([Deployment models](https://help.accuknox.com/resources/deployment/))
3. **AI security in the same control plane.** AI-SPM, Prompt Firewall and ModelArmor sit beside CSPM and CWPP. ([AI Agent Security deck](https://help.accuknox.com/use-cases/prompt-firewall-overview/))

**Minimum evaluation effort.**

| Phase | MUFG does | Time |
|---|---|---|
| 1. Agentless, read-only | Create one read-only role in one non-production cloud account. Run one Terraform scanner per region. | A few hours |
| 2. Runtime, optional | Install KubeArmor on one non-production cluster in audit mode. | Same week |
| 3. On-prem control plane, if required | Provide 3 nodes, egress on ports 80 and 443 during install, and 4 DNS names. | 2 to 3 weeks |

A standard PoC runs 5 days on SaaS. ([PoC timeline](https://help.accuknox.com/faqs/general/), [Deployment FAQ](https://help.accuknox.com/faqs/deployment/))

## Open Items Before Sending

1. **KubeArmor overhead:** get CPU and memory numbers from Rahul.
2. **CIEM release date:** the docs say "coming soon". Do not promise it as live.
3. **Japan region:** no SaaS region in Japan or APAC. Lead with on premises.
4. **Agentless with an on-prem control plane:** confirm the scanner can report to it.
5. **Nutanix conflict:** the deployment page lists Nutanix agentless, but the VM scanning page says planned. Claim neither.
6. **Data Usage Policy:** one note on the page holds an `<ANSWER>` placeholder. Fix it before linking it to MUFG.
7. **AgentZ export path:** no doc exists.
