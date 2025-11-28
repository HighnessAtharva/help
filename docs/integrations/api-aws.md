---
title: AWS API Gateway Integration
description: Integration guide for AWS API Gateway with AccuKnox API Security.
---

# AWS API Gateway Integration

This guide provides the steps required to connect AWS API Gateway to AccuKnox API Security.

![alt text](<Screenshot 2025-11-28 132113.png>)

!!! info "Quick Rundown of Steps"
    - Deploy the AccuKnox CloudFormation templates in your AWS account.
    - Enable logging for your API Gateway stages.
    - Configure permissions for the Lambda function to forward logs.
    - Upload your OpenAPI specification to AccuKnox.
    - Run a scan and review your API inventory and findings.

## 1. Deploy the AccuKnox CloudFormation Template

The deployment process requires running two specific CloudFormation stacks in sequence.

### Stack 1: Base Stack

⬇️ [**DOWNLOAD CLOUDFORMATION BASE TEMPLATE**](./cloudformation-base.yaml)

The base stack creates the necessary IAM role and permissions required for the integration.

1. Download the base stack template above.
2. In your AWS account, open **CloudFormation → Create Stack** and upload the template.
3. Select "**Delete all newly created resources**" to ensure clean reversion if needed.
4. Launch the stack.

![alt text](image-1.png)

![alt text](image-2.png)

### Stack 2: Standard CloudFormation Stack

⬇️ [**DOWNLOAD CLOUDFORMATION TEMPLATE**](./cloudformation.yaml)

This stack must be run once for each deployment stage (e.g., Dev, Staging, Prod).

1. Download the standard CloudFormation template above.
2. In your AWS account, open **CloudFormation → Create Stack** and upload the template.
3. Configure the following parameters:

| Parameter             | Typical Value / Notes                                      |
|-----------------------|------------------------------------------------------------|
| **Stage**             | `True` (99% of cases when API is deployed and working)     |
| **Create Lambda**     | `True` (first run), `False` (subsequent runs)              |
| **Log Collection URL**| (Provide your log collector endpoint)                      |
| **REST API ID**       | (Copy from AWS API Gateway)                                |
| **Stage Name**        | `dev`, `stage`, `prod`, etc.                               |

Launch the stack so it creates:

- A **CloudWatch Log Group** for API Gateway logs.
- A **Lambda subscription function** to forward logs to the AccuKnox API Agent.

![alt text](image-4.png)

## 2. Enable Logging in AWS API Gateway

1. Navigate to **API Gateway → Stages → [Select Stage]**.
2. Click on **Logs/Tracing**.
3. Click **Edit**.
4. Enable the following settings as shown in the image below.
5. Click **Save changes**.

Once enabled, API Gateway begins writing API request and response logs to CloudWatch.

![alt text](image-5.png)

!!! info "Log Forwarding"
    The Lambda function created by CloudFormation automatically subscribes to the API Gateway Log Group and forwards logs to the AccuKnox API Agent (EC2 instance). The agent processes these logs and sends data to the AccuKnox Control Plane.

## 3. Real-Time API Inventory in AccuKnox

As soon as logs reach the control plane:

- API endpoints appear in the **Inventory** tab.
- Inventory shows method, path, request and response bodies, and sensitive-data classification.
- External and internal calls are labeled accordingly.

Inventory updates continuously as logs arrive.

![alt text](image-6.png)

!!! info "Auto-Creation of Collections"
    A collection is automatically created based on the **Host endpoint** once the API agent receives logs. This provides immediate organization of your API endpoints without manual intervention.

## 4. Create API Collections

While collections are automatically created based on host endpoints, you can also create custom collections to better organize your API inventory.

1. Go to **API Security → Collections**.
2. Click **Create Collection**.
3. Define filters using the following options:
    - **Host**: Filter by specific host/domain
    - **Name**: Filter by endpoint name
    - **Regex**: Use regular expressions for pattern matching
    - **Method**: Select from dropdown options (GET, POST, PUT, DELETE, PATCH, etc.)
4. Save your collection.

Collections help organize endpoints before scanning and provide logical groupings for security analysis.

![alt text](image-7.png)

## 5. Upload Your OpenAPI Specification

API Specifications (OpenAPI/Swagger format) can be uploaded to define the expected API structure for comparison during scans.

### Method 1: Via Inventory Page

1. Navigate to **API Security → Inventory**.
2. Click on the upload option.
3. Select your OpenAPI specification file (YAML or JSON).
4. Upload the file.

![alt text](image-8.png)

### Method 2: During Scan Configuration

1. Navigate to **API Security → Scans → New Scan**.
2. During the scan setup, you'll have the option to upload your specification.
3. Select your OpenAPI specification file (YAML or JSON).
4. Upload the file.

!!! info "Use Case"
    The API specification is essential for scan comparisons. It serves as the baseline to identify Shadow APIs (undocumented endpoints), Orphan APIs (documented but unused), and validate Active APIs against your intended design.

## 6. Scan API Endpoints

1. Go to **API Security → Scans → New Scan**.
2. Select the OpenAPI spec you uploaded.
3. Choose the inventory or a collection.
4. Run the scan.

![alt text](image-9.png)

The scan compares runtime traffic with your specification.

## 7. Review Findings

![alt text](image-10.png)

AccuKnox displays four types of findings:

| Finding Type   | Description                                                                                   |
|----------------|-----------------------------------------------------------------------------------------------|
| Zombie APIs    | Detected endpoints that are no longer active but still exist in the spec.                     |
| Shadow APIs    | Endpoints seen in runtime traffic but not present in the spec.                                |
| Orphan APIs    | Endpoints defined in the spec but never seen in traffic.                                      |
| Active APIs    | Endpoints currently receiving traffic.                                                        |

Each finding includes request, response, and occurrence details.

![alt text](image-11.png)