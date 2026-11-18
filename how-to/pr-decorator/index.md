---
title: Pull Request Decorator
description: Add an AccuKnox security review to every pull request, with a summary, ranked fixes, a findings map and inline suggestions.
---

# Pull Request Decorator

!!! warning "Draft"
    This page describes a feature that is not released. It is not in the navigation. Confirm the action name, the supported platforms and the release with the feature owner before you publish it.

The pull request decorator posts an **AccuKnox Security Review** on each pull request. It runs the AccuKnox ASPM scanner CLI in your pipeline, so it does not depend on one CI/CD tool.

## Add the Action to a GitHub Workflow

Add a step that runs the action after `actions/checkout`. Set `fetch-depth: 0` on the checkout.

{% raw %}
```yaml
- name: Run AccuKnox scan + PR Decorator
  uses: <public-action-name>
  with:
    scan_type: sast,sca,iac,secret,quality
    accuknox_endpoint: ${{ secrets.ACCUKNOX_ENDPOINT }}
    accuknox_token: ${{ secrets.ACCUKNOX_TOKEN }}
    accuknox_label: ${{ secrets.ACCUKNOX_LABEL }}
    soft_fail: "true"
    pr_decorator: "true"
```
{% endraw %}

Give the workflow `pull-requests: write` permission so it can comment. The demo workflow also passed `llm_api_key`, `llm_base_url` and `llm_model`. [Confirm with the feature owner what these inputs do and whether they are optional.]

## Read the Review on the Pull Request

The comment holds these parts.

- **Pull Request Summary**: what the change does, a table of key changes per file, and an impact analysis.
- **Top fixes**: the findings to fix first, ordered by risk.
- **Findings by File**: a map of files and the findings in each.
- **Security Findings**: counts by severity, and the quality conditions that failed, such as `CRITICAL: found 3, threshold 0`.

The decorator also adds an inline comment on the changed line for each finding. A comment shows the severity, the reason and the CWE. When a fix exists, it offers a suggested change that you apply with one click. When none exists, the comment says the fix needs a manual review.

## Platform Support

The team tested GitHub and GitLab. Azure DevOps and Bitbucket are not tested. The decoration step is specific to each platform, so confirm support before you promise it.
