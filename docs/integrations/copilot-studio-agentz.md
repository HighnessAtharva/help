---
title: Prompt Firewall for Microsoft Copilot Studio with AgentZ
description: Connect Microsoft Copilot Studio to AgentZ so your Prompt Firewall guardrails check every agent tool call before it runs, and block the risky ones.
---

# Prompt Firewall for Microsoft Copilot Studio

AgentZ checks every tool call a Microsoft Copilot Studio agent makes, before the tool runs. Copilot Studio sends the conversation and the tool call to AgentZ. AgentZ runs your Prompt Firewall guardrails and answers allow or block. A blocked call never reaches the tool, and the user sees that the action was blocked.

<iframe width="560" height="315" src="https://www.youtube.com/embed/LmMvT-rI_Dk" title="Prompt Firewall for Copilot Studio Agents With AgentZ" frameborder="0" allowfullscreen></iframe>

## AgentZ Answers Before the Tool Runs

![Copilot Studio sends each tool call to AgentZ, AgentZ answers allow or block, and Copilot Studio calls the tool only when AgentZ allows it](./images/copilot-studio-agentz/how-it-works.png)

A tool call is anything the agent does beyond its own reasoning: a web search, an MCP server, a connector, a skill or a data lookup. AgentZ sees the whole conversation at the moment of the call, so a guardrail can judge the request in context. Every check shows in AgentZ under **Guardrails**, then **Events**, and the full conversation shows under **Traces**.

## Prerequisites

- An AgentZ account at [agentzharness.ai](https://agentzharness.ai/).
- The Azure CLI on the machine you run the commands from.
- An Azure admin with two roles: Cloud Application Administrator and Power Platform Administrator.
- A Copilot Studio environment with at least one agent.

## Connect Copilot Studio in 10 Steps

Start in AgentZ. Open **External agents**, click **Add external agent** and pick **Microsoft Copilot Studio**. The panel shows every command below with your values filled in, so copy the commands from the panel.

### Connect Azure

1. Sign in to Azure and copy your tenant ID. Paste the ID into **Directory tenant ID**.

    ```bash
    az login --tenant YOUR_TENANT_ID --allow-no-subscriptions
    az account show --query tenantId -o tsv
    ```

2. Create one Entra app for your organization. Paste the ID the command returns into **Application client ID**.

    ```bash
    CALLER_APP_ID=$(az ad app create --display-name "AgentZ Microsoft Copilot Studio" --sign-in-audience AzureADMyOrg --query appId -o tsv)
    az ad sp create --id "$CALLER_APP_ID" --query appId -o tsv
    ```

3. Register the AgentZ app in your tenant. Copy this command from the **Add AgentZ** box in the panel, because it carries the AgentZ application ID. A message that the service principal already exists means the app is registered.

    ```bash
    az ad sp create --id <AgentZ application ID from the panel>
    ```

### Connect AgentZ

4. In the Power Platform admin center, open **Manage**, then **Environments**, then your environment. Copy the **Environment ID** into **Power Platform environment ID** in AgentZ.
5. Click **Add connection**.
6. Run the federated credential command that AgentZ shows next. The credential lets Copilot Studio sign in as your app with a token from Microsoft, so there is no client secret to store.

    ```bash
    az ad app federated-credential create --id <your application client ID> --parameters '{
      "name": "<name from the panel>",
      "issuer": "https://login.microsoftonline.com/<your tenant ID>/v2.0",
      "subject": "<subject from the panel>",
      "audiences": ["api://AzureADTokenExchange"]
    }'
    ```

### Connect Power Platform

7. In the Power Platform admin center, open **Security**, then **Threat detection**, then **Additional threat detection and protection for Copilot Studio agents**. Pick your environment and click **Set up**. Turn on **Allow Copilot Studio to share data with a threat detection partner**. Paste the **Azure Entra App ID** and the **Endpoint link** from AgentZ. Set the error behavior to **Block the query**, then click **Save**. AgentZ shows **Validated by Microsoft** when the link works.

### Add a guardrail and test it

8. In AgentZ, open the Copilot Studio connection, go to **Policies** and add a guardrail. For a first test, add a check that blocks phone numbers with a regular expression.
9. In Copilot Studio, ask the agent to search the web for a phone number, such as `+91 9999999999`. The reply says the action was blocked by threat detection tools.
10. In AgentZ, open **Guardrails**, then **Events**. The blocked call is at the top, with the check that fired.

## Five Caveats to Know Before You Roll Out

- **Only tool calls are checked.** A chat that never calls a tool does not reach AgentZ, so a guardrail on plain chat text never fires. A phone number typed into a chat that needs no tool passes through.
- **AgentZ must answer within one second.** Microsoft sets this limit. With **Block the query**, Copilot Studio blocks any call that AgentZ cannot check in time. A regular expression check answers fastest. A check that calls a model can take longer.
- **Each environment needs its own connection.** The Power Platform step runs in the admin center only, with no API, so connect each environment by hand.
- **Every agent in a connected environment is covered.** You cannot pick some agents in an environment and leave others out.
- **The Microsoft feature is in preview.** The Power Platform screens and labels can change.
