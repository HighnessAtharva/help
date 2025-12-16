---
title: LLM Static Scans
description: Learn how to perform LLM Static Scans using AccuKnox for OpenAI, Ollama and Custom Large Language Models.
---

# LLM Static Scans

AccuKnox provides static analysis for Large Language Models (LLM) to identify vulnerabilities, security risks, and compliance issues. This guide walks you through setting up and running LLM Static Scans for models hosted on OpenAI, Ollama, and Custom Large Language Models.

!!! tip "Subprompts and Probes"
    For a detailed list of subprompts and probes that ML and LLM scans rely on, please refer to the [Subprompts Categories](https://help.accuknox.com/use-cases/subprompts-categories/) page.

??? info "Why are LLM Scans Needed?"

    Large Language Models are becoming integral parts of modern applications, but they also introduce new attack vectors. LLM Static Scans are essential for:

    * **Vulnerability Detection**: Identifying known vulnerabilities in model files and configurations.
    * **Supply Chain Security**: Ensuring that models imported from public repositories (like Hugging Face) are safe to use.
    * **Compliance**: Meeting security standards by scanning AI/LLM assets for risks.
    * **Model Integrity**: Verifying that model weights and configurations have not been tampered with.

## Setting up an LLM Static Scan

Follow these steps to configure a scan for your LLM models.

### Step 1: Add a New Collector

1. Navigate to **Settings** > **Collectors** in the AccuKnox dashboard.
2. Click on **Add Collector**.
3. Select **LLM-Static-Scan** from the available options.
4. Choose your platform: **Custom Model**, **Ollama Model**, or **OpenAI Model** depending on LLM type.

![alt text](image-11.png)

### Step 2: Configure Repository Details

Enter the required credentials and repository information.

!!! example "Configuration Details"

    === "Custom Models"

        | Parameter              | Description |
        |------------------------|-------------|
        | **Endpoint URL**       | Enter the Endpoint URL for the model. Example: `https://api.example.com/v1/llm` |
        | **Secret Token**       | Enter the Secret Key for authentication. Example: `sk-xxx` |
        | **Model Name**         | Enter the name of the model. Example: `my-llm-model` |
        | **Model ID**           | Enter the ID of the model to be scanned by the LLM static scan. Example: `model-12345` |
        | **Scan Category**      | Select the list of categories to scan on the model. This is based on predefined categories. |
        | **Request Template**   | Enter the request payload structure in JSON format. Use `$INPUT` where user input should be injected. Example:<br><br>`{ "query": "$INPUT", "history": [] }` |
        | **Pre-defined Prompts**| Choose **Scan with Default Prompts** or **Upload Custom Prompts File**. |

        !!! info "Using Custom Prompts"
            When uploading a custom prompts file, ensure it is in JSON format with an array of prompt strings. Example:

            ```json
            {
              "query": "$INPUT",
              "history": []
            }
            ```
        ![alt text](image-12.png)

    === "Ollama Models"

        | Parameter              | Description |
        |------------------------|-------------|
        | **Ollama Host URL**    | Enter the Ollama Host URL. Example: `http://localhost:11434` |
        | **Scan Category**         | Select the list of categories to scan on the model. This is based on predefined categories. |
        | **Pre-defined Prompts**| Choose **Scan with Default Prompts** or **Upload Custom Prompts File**. |

        ![alt text](image-13.png)

    === "OpenAI Models"

        | Parameter              | Description |
        |------------------------|-------------|
        | **Secret Token**       | Enter the Secret Key for authentication. Example: `sk-xxx` |
        | **Model Name**         | Enter the name of the model. Example: `gpt-4` |
        | **Model ID**           | Enter the ID of the model to be scanned. Example: `model-12345` |
        | **Pre-defined Prompts**| Choose **Scan with Default Prompts** or **Upload Custom Prompts File**. |

        ![alt text](image-14.png)

### Step 3: Add Identifiers

Add **Labels** and **Tags** to categorize your LLM models. This helps in filtering and managing assets within the AccuKnox platform.

![alt text](image-15.png)

### Step 4: Validate Connection

Once you have entered the credentials, click on **Test** to validate the connection to your repository. Ensure the validation is successful before proceeding.

### Step 5: Schedule the Scan

Configure the **Schedule and Notification** settings:

1. Under **Cron Job**, define the frequency of the scan (e.g., daily, weekly).
2. The system will display the **Next Scan** time based on your configuration.

![Schedule Scan](image-4.png)

Click **Save** to create the LLM collector.

![alt text](image-16.png)

![alt text](image-17.png)

## Viewing Scan Results

Once the scan is triggered (either manually or via the schedule), AccuKnox will analyze the repository.

1. Go to **Issues** or the **Collectors** page.
2. Click on the **Findings** count for your LLM Static Scan collector.

![alt text](image-18.png)

You will be redirected to the **LLM Findings** page, which lists details such as:
`Scan Category`, `Probe`, `Detector`, `Goal`, `Prompt`, `Output Description`, `Risk Factor`, `Detector Safety Score`, `Category Safety Score`, `Compliance Name`, `AVID`

## Analyzing Findings

Click on any finding to open the **Detailed Pane**. Here you can:

* View a detailed **Description** of the vulnerablity for the LLM.

* **Create Ticket**: Integrate with your ticketing system (e.g., Jira) to track remediation.
* **Ask AI**: Use the "Ask AI" button for assisted remediation advice.

![alt text](image-19.png)

See the recommended **Solution**.
![alt text](image-20.png)

Access **Output** to see what the LLM returned for the given prompt and the **Prompt** shows the exact input used for scanning along with Goal and AVID details.
![alt text](image-21.png)
