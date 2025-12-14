---
title: Agent-Based VM Scanning for Linux
description: Comprehensive guide for Agent-based Vulnerability and Malware Scanning on Linux VMs.
---

# Agent-Based VM Scanning for Linux

This guide provides step-by-step instructions to onboard Linux Virtual Machines (VMs) for agent-based security scanning.

## Prerequisites

- Root or sudo access to the Linux VM.
- Outbound internet connectivity to AccuKnox SaaS.
- `curl` installed on the VM.

## Installation

### 1. Install Knoxctl

Download and install the `knoxctl` CLI tool:

```bash
curl -sfL https://knoxctl.accuknox.com/install.sh | sudo sh -s -- -b /usr/bin
```

### 2. Onboard the VM

Run the onboarding command to install the necessary agents. You can generate this command from the AccuKnox dashboard under **Settings > Manage Cluster > Onboard Now > VM**.

Example command:

```bash
knoxctl onboard vm cp-node \
  --version v0.10.7 \
  --join-token=<YOUR_JOIN_TOKEN> \
  --spire-host=spire.accuknox.com \
  --pps-host=pps.accuknox.com \
  --knox-gateway=knox-gw.accuknox.com:3000 \
  --vm-mode="systemd" \
  --enable-host-policy-discovery \
  --hostViz="process,network,file,capabilities" \
  --viz="process,network,file"
```

!!! tip
    Replace `<YOUR_JOIN_TOKEN>` with the token provided in the dashboard.

## Vulnerability & Malware Scanning

Once the agent is installed and the VM is onboarded, vulnerability and malware scanning capabilities are enabled based on your policy configuration. Ensure that the necessary policies are applied to your VM to start scanning.

