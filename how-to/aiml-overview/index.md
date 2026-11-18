---
title: AI Security Posture Management (AI-SPM)
description: "Get started with AccuKnox AI-SPM. Onboard AI/ML assets and set up every AI security module: AI-DR, Agentic AI Security, Model & Dataset Security, Red Teaming, and Prompt Firewall guardrails."
hide:
  - toc
---

# AI Security Posture Management (AI-SPM)

<style>
  .nt-card-title{
    text-align: center;
  }

  .nt-card-img img{
    color: #00025;
  }

  /* Module chips: the 8 AI security modules as a compact pill row. Wraps
     naturally on narrow screens, no fixed column count to fight.
     The selector has to out-specify Material's own
     `.md-typeset ul:not([hidden]){display:flow-root}`, hence the
     `ul.ak-modules:not([hidden])` shape rather than a plain class. */
  .md-typeset ul.ak-modules:not([hidden]) {
    display: flex;
    flex-wrap: wrap;
    gap: .5rem;
    margin: .9rem 0 1.4rem;
    padding: 0;
    list-style: none;
  }

  .md-typeset ul.ak-modules li {
    margin: 0;
    padding: 0;
    list-style: none;
  }

  .md-typeset ul.ak-modules li::marker { content: none; }

  .md-typeset .ak-module {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    padding: .38rem .8rem;
    border: 1px solid var(--md-default-fg-color--lightest);
    border-radius: 999px;
    background: var(--md-code-bg-color);
    color: var(--md-default-fg-color);
    font-size: .78rem;
    font-weight: 600;
    line-height: 1.35;
    text-decoration: none;
    transition: border-color .15s, background .15s, color .15s;
  }

  .md-typeset a.ak-module {
    color: var(--md-default-fg-color);
  }

  .md-typeset a.ak-module:hover {
    border-color: var(--md-primary-fg-color);
    background: var(--md-primary-fg-color);
    color: var(--md-primary-bg-color);
  }

  .md-typeset a.ak-module::after {
    content: "→";
    font-weight: 400;
    opacity: .55;
  }

  .md-typeset .ak-module--soon {
    border-style: dashed;
    background: transparent;
    color: var(--md-default-fg-color--light);
    font-weight: 500;
  }

  .md-typeset .ak-module--soon span {
    padding: .05rem .35rem;
    border-radius: 4px;
    background: var(--md-default-fg-color--lightest);
    font-size: .64rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .03em;
  }
</style>

AccuKnox AI-SPM discovers and protects your AI/ML assets. Run every AI security module from one console:

<ul class="ak-modules">
  <li><a class="ak-module" href="/use-cases/aidr/">AI Detect &amp; Respond (AI-DR)</a></li>
  <li><a class="ak-module" href="/use-cases/modelarmor/">Agentic AI Security</a></li>
  <li><a class="ak-module" href="/use-cases/modelarmor-pickle-code/">AI Model &amp; Dataset Security</a></li>
  <li><a class="ak-module" href="/use-cases/red-teaming/">AI Red Teaming &amp; Pen Testing</a></li>
  <li><a class="ak-module" href="/use-cases/prompt-firewall-overview/">AI Guardrails (Prompt Firewall)</a></li>
  <li><span class="ak-module ak-module--soon">AI Identity Security <span>Coming soon</span></span></li>
  <li><span class="ak-module ak-module--soon">AI Compliance <span>Coming soon</span></span></li>
</ul>

New to the platform? Read the [AI security architecture](../getting-started/ai-security-arch.md) first. It maps which collection method reaches which kind of asset, and that decides what you install below.

!!! note "Useful Links"
    - For supported platforms refer to the [**AI Security Support Matrix**](https://help.accuknox.com/support-matrix/aiml-support-matrix/)
    - For use cases refer to the [**AI Security Use Cases**](https://help.accuknox.com/use-cases/aiml-usecases/)

## Cloud Onboarding

Onboard a cloud account to discover AI/ML assets and enable red teaming and posture scanning across your models and datasets.

::cards:: cols=4

- title: AWS
  image: ./icons/aws-vm.svg
  url: /how-to/aiml-aws-onboard/

- title: Azure
  image: ./icons/azure-vm.svg
  url: /how-to/aiml-azure-onboard/

- title: GCP
  image: ./icons/gcp-vm.svg
  url: /how-to/aiml-gcp-onboard/

- title: On-Prem Models
  image: ./icons/onprem.svg
  url: /how-to/aiml-saas-vs-onprem/

::/cards::

## Onboard an AI App

Pick the path that fits how your application calls the model. Select a box to open its guide.

<div class="ak-dia" role="img" aria-label="Decision tree. Your AI application asks how it calls the model. Three branches. AI Gateway: change the base URL and key, best for OpenAI-compatible clients and many applications. SDK method: add scan calls to your code, best for Python code where you choose where each scan runs. API method: call the runtime endpoint, best for custom applications that can call an HTTP API.">
<svg viewBox="0 0 900 430" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="agPathArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="head-acc"/></marker></defs>
<rect class="plane" x="290" y="10" width="320" height="64" rx="12"/>
<text class="t-plane t-xl" x="450" y="39" text-anchor="middle" style="font-size:20px">Your AI application</text>
<text class="t-pill t-md" x="450" y="60" text-anchor="middle">How does it call the model?</text>
<path class="ln-acc w" d="M450 74 V104"/>
<path class="ln-acc w" d="M150 104 H750"/>
<path class="ln-acc w" d="M150 104 V134" marker-end="url(#agPathArrow)"/>
<path class="ln-acc w" d="M450 104 V134" marker-end="url(#agPathArrow)"/>
<path class="ln-acc w" d="M750 104 V134" marker-end="url(#agPathArrow)"/>
<a href="/getting-started/ai-gateway-onboarding/">
<rect class="p" x="10" y="134" width="280" height="280" rx="12"/>
<circle class="plane" cx="58" cy="186" r="26"/><g class="ico" transform="translate(42.0,170.0) scale(1.33)"><path d="M12 3a9 9 0 100 18 9 9 0 000-18z"/><path d="M3 12h18"/><path d="M12 3c3 3 3 15 0 18"/><path d="M12 3c-3 3-3 15 0 18"/></g>
<text class="t-xl" x="100" y="194">AI Gateway</text>
<rect class="acc" x="30" y="232" width="240" height="36" rx="18"/>
<text class="t-md" x="150" y="256" text-anchor="middle" style="font-weight:600">Change the base URL and key</text>
<text class="t-sm" x="32" y="304" style="letter-spacing:.1em">BEST FOR</text>
<text class="t-md" x="32" y="330" style="font-size:16px">OpenAI-compatible clients</text>
<text class="t-md" x="32" y="352" style="font-size:16px">and many applications</text>
<text class="t-acc t-md" x="32" y="390" style="font-size:16px">Open the guide →</text>
</a>
<a href="/how-to/llm-defense-app-onboard/">
<rect class="p" x="310" y="134" width="280" height="280" rx="12"/>
<circle class="plane" cx="358" cy="186" r="26"/><g class="ico" transform="translate(342.0,170.0) scale(1.33)"><path d="M8 8l-4 4 4 4"/><path d="M16 8l4 4-4 4"/><path d="M13 6l-2 12"/></g>
<text class="t-xl" x="400" y="194">SDK method</text>
<rect class="acc" x="330" y="232" width="240" height="36" rx="18"/>
<text class="t-md" x="450" y="256" text-anchor="middle" style="font-weight:600">Add scan calls to your code</text>
<text class="t-sm" x="332" y="304" style="letter-spacing:.1em">BEST FOR</text>
<text class="t-md" x="332" y="330" style="font-size:16px">Python code where you</text>
<text class="t-md" x="332" y="352" style="font-size:16px">choose where each scan runs</text>
<text class="t-acc t-md" x="332" y="390" style="font-size:16px">Open the guide →</text>
</a>
<a href="/how-to/aiml-runtime-onboard/">
<rect class="p" x="610" y="134" width="280" height="280" rx="12"/>
<circle class="plane" cx="658" cy="186" r="26"/><g class="ico" transform="translate(642.0,170.0) scale(1.33)"><path d="M9 3v5"/><path d="M15 3v5"/><path d="M7 8h10v4a5 5 0 01-10 0V8z"/><path d="M12 17v4"/></g>
<text class="t-xl" x="700" y="194">API method</text>
<rect class="acc" x="630" y="232" width="240" height="36" rx="18"/>
<text class="t-md" x="750" y="256" text-anchor="middle" style="font-weight:600">Call the runtime endpoint</text>
<text class="t-sm" x="632" y="304" style="letter-spacing:.1em">BEST FOR</text>
<text class="t-md" x="632" y="330" style="font-size:16px">Custom applications that</text>
<text class="t-md" x="632" y="352" style="font-size:16px">can call an HTTP API</text>
<text class="t-acc t-md" x="632" y="390" style="font-size:16px">Open the guide →</text>
</a>
</svg></div>

## Set Up a Security Module

::cards:: cols=4

- title: Red Teaming & Pen Testing
  image: ./icons/model-safety.svg
  url: /how-to/aiml-custom-model-redteaming/

- title: LLM Static Scans
  image: ./icons/sast.svg
  url: /how-to/llm-static-scan/

- title: ML Static Scans
  image: ./icons/supply-chain-attacks.svg
  url: /how-to/ml-static-scan/

- title: Prompt Firewall Setup
  image: ./icons/AIML.svg
  url: /how-to/prompt-firewall/

- title: Prompt Firewall App (SDK)
  image: ./icons/AIML.svg
  url: /how-to/llm-defense-app-onboard/

- title: Runtime Defense (API)
  image: ./icons/mcp-security.svg
  url: /how-to/aiml-runtime-onboard/

- title: AI-DR (Azure Setup)
  image: ./icons/model-safety.svg
  url: /how-to/azure-aidr/

- title: Model Scan in CI/CD
  image: ./icons/cicd-pipeline.svg
  url: /how-to/model-scan-cicd/

::/cards::

!!! tip "Red team a model for its purpose"
    Start a red teaming scan from the **Assets** page. Choose **Intelligent Scan** and describe what the model is for. AccuKnox generates prompts for that purpose, such as medical prompts for a medical assistant. **Static Scan** runs a fixed set of general prompts. The new scan flow covers managed models. See [Intelligent Red Teaming Scans](../getting-started/3.6-release.md#intelligent-red-teaming-scans).

## Featured Videos

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin: auto; font-family: Arial, sans-serif;">

  <!-- Model Safety -->
  <div style="background:#fff; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.06); overflow:hidden;">
    <div style="aspect-ratio:16/9;">
      <iframe width="100%" height="100%" src="https://www.youtube.com/embed/eK69KNytMWo" title="Model Safety" frameborder="0" allowfullscreen style="border:0;"></iframe>
    </div>
    <div style="padding:8px;">
      <h4 style="margin:0 0 4px; display:flex; align-items:center; gap:6px;">
        Model Safety
      </h4>
      <p style="margin:0; font-size:0.75rem; color:#555;">Safeguard models from misuse and ensure responsible AI behavior through explainability and guardrails.</p>
    </div>
  </div>

  <!-- Securing AI Factories -->
  <div style="background:#fff; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.06); overflow:hidden;">
    <div style="aspect-ratio:16/9;">
      <iframe width="100%" height="100%" src="https://www.youtube.com/embed/HzJQKl-YPAo" title="Securing AI Factories" frameborder="0" allowfullscreen style="border:0;"></iframe>
    </div>
    <div style="padding:8px;">
      <h4 style="margin:0 0 4px; display:flex; align-items:center; gap:6px;">
        Securing AI Factories
      </h4>
      <p style="margin:0; font-size:0.75rem; color:#555;">Implement end-to-end security for AI pipelines, from data ingestion to model deployment.</p>
    </div>
  </div>

</div>
