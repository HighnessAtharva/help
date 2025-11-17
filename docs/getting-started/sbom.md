---
title: SBOM
description: Documentation for SBOM onboarding, ingestion, scanning, and reporting.
---

# SBOM Overview

This documentation explains how developers can configure SBOM onboarding inside the platform. It describes the workflow for generating, uploading, analyzing, and acting on SBOM data, supporting new users by clarifying the core concepts and expected actions.

## Goals and Assumptions

The SBOM feature provides developers with:

- A simple way to bring SBOM data into the system
- Visibility into dependencies, component versions, and risk indicators through a clean interface
- A consistent experience across onboarding, ingestion, scanning, and reporting
- The ability to compare SBOMs across application versions
- A clear method to track risks linked to dependencies

!!! info "Prerequisites"
    - Developers understand their build process and can produce SBOM data through their existing tools
    - SBOMs follow a recognized industry format
    - Users can upload SBOM files or integrate automated ingestion through their pipeline
    - Security scanning occurs after ingestion

## Use Cases

| Use Case                | Description                                                                                     |
|-------------------------|-------------------------------------------------------------------------------------------------|
| **Generating SBOMs**    | Developers generate SBOMs during the build process to track all dependencies in their applications. |
| **Ingesting SBOMs**     | Users upload SBOM files or automate ingestion, enabling the system to scan them without manual intervention. |
| **Viewing Components**  | The platform provides visibility into components, licenses, and versions, helping users track changes over time. |
| **Receiving Notifications** | Users are notified of new issues in previously scanned SBOMs, allowing them to address risks early. |
| **Tracking Version History** | The system maintains a history of SBOMs, enabling users to compare changes between application releases. |

## AccuKnox SBOM Features Overview

| Feature                | Description                                                                                     |
|------------------------|-------------------------------------------------------------------------------------------------|
| **Ingestion**          | Supports file uploads in common formats, automated CI/CD ingestion, and versioned artifact storage tied to applications. |
| **Scanning & Analysis**| Parses component names, versions, and metadata; evaluates risks like version issues and license concerns; associates results with applications and SBOM versions. |
| **Visualization**      | Provides dependency tables with filtering/sorting, relationship visualization, and comparison views between SBOM versions. |
| **Reporting**          | Enables export of results for audits or reviews, offering both summary-level and detailed reporting options. |

## Technical Breakdown

The SBOM processing pipeline consists of six key layers:

| Layer | Function |
|-------|----------|
| **SBOM Intake Layer** | Users upload a file or configure an automated feed from their pipeline |
| **Parsing Layer** | The system reads dependency data, metadata, structure, and fields defined by the SBOM format |
| **Analysis Layer** | The system evaluates components for known risks and compliance indicators |
| **Correlation Layer** | SBOM data is aligned with applications, versions, and any user-defined classification tags |
| **Storage Layer** | Versioned SBOMs and their analysis results are stored for long-term reference |
| **Query + Display Layer** | The UI presents dependency lists, component metadata, comparison views, and summaries |

## How to Onboard and Use SBOMs with AccuKnox

| Step | Description                                                                                                     |
|------|-----------------------------------------------------------------------------------------------------------------|
| **Configuration** | Users set up how SBOM data will enter the system through either upload or automated ingestion. <br> !!! tip "Configuration Options" <br> Choose the ingestion method that best fits your workflow. Automated ingestion is recommended for continuous delivery pipelines. |
| **SBOM Generation** | Users generate SBOMs within their build process using any tool of their choice. |
| **Ingestion** | Users upload the file or complete pipeline integration. The system confirms the SBOM is valid and begins processing. |
| **Scan Execution** | Analysis begins automatically and users can monitor progress throughout the scanning process. |
| **Viewing Dependencies** | Results appear in the Dependencies section where users can filter, sort, and inspect components.  |
| **Comparing Builds** | Users compare SBOM versions to see new, removed, or changed dependencies across releases. |
| **Reporting** | Users export summaries or detailed views for compliance or internal review purposes. |


!!! note "Dependency Navigation"
    Use the filtering and sorting controls to quickly locate specific components or identify high-risk dependencies.