# Deal or No Deal AI — Product Requirements Document

> **Approval record — 2026-10-22:** The user approved moving from PRD v1.4 to HLD, then explicitly selected “Role simulation for the demo only.” Version 1.5 records that authorized scope change: simulated roles replace real sign-in for the synthetic local demo. The branding, selected stack, Nebius direction, Jupyter notebook, five-day target, and budget/quality targets remain the baseline; targets are unmeasured. Open business definitions and model/account decisions remain explicit. The [previous baseline](prd-v0.1-approved.md) is historical. Approval authorizes Phase 2 design only; no model calls, paid services, deployment, implementation scaffolding, or external repository creation are authorized.

**Document Version:** 1.5
**Date:** October 22, 2026  
**Status:** Approved baseline for Phase 2 — v1.5 incorporates the explicitly authorized demo-role simulation change
**Product Category:** Agentic AI / Financial Services / Credit Underwriting  
**Initial Market:** Commercial Banking  
**Delivery:** 5-Day Hackathon MVP + Local Streamlit Demonstration
**Architecture:** LangGraph Supervisor-Orchestrated Multi-Agent System

---

## Table of Contents

1. [Problem](#1-problem)
2. [User](#2-user)
3. [Core Metrics, Prioritisation & Roadmap](#3-core-metrics-prioritisation--roadmap)
4. [MVP Features](#4-mvp-features)
5. [Constraints](#5-constraints)
6. [Technical Requirements](#6-technical-requirements)
7. [Grounding Strategy](#7-grounding-strategy)
8. [Prompt Strategy](#8-prompt-strategy)
9. [Hallucination Guardrails](#9-hallucination-guardrails)
10. [Evaluation Strategy](#10-evaluation-strategy)
11. [Production Readiness Criteria & Metrics (HHH)](#11-production-readiness-criteria--metrics-hhh)
12. [Pricing](#12-pricing)
13. [Assumptions](#13-assumptions)

---

# 1. Problem

## 1.1 Problem Statement

Financial institutions review complex transactions involving financial statements, credit agreements, term sheets, lending policies, collateral records, and supporting documentation.

The review process requires multiple teams to extract information, calculate financial metrics, check compliance with policy, identify risks, and prepare recommendations for authorized decision-makers.

Although many banks use loan origination and credit management software, significant analytical work can still involve manual document review and coordination.

Typical challenges include:

1. **Fragmented information:** Relevant deal facts exist across documents and systems.
2. **Manual extraction:** Analysts must identify and normalize terms from unstructured materials.
3. **Inconsistent rule interpretation:** Applicable lending policies and exceptions require careful validation.
4. **Repeated financial analysis:** Ratios and forecasts must be updated when source information changes.
5. **Disconnected reviews:** Credit, compliance, legal, and risk functions may examine overlapping information.
6. **Limited traceability:** Reviewers need to understand where material findings originated.
7. **Time-consuming reporting:** Credit memoranda require consolidation of analytical outputs.
8. **Human coordination overhead:** Missing evidence, exceptions, and corrections create multiple handoffs.

### Core User Problem

> Credit analysts and risk officers need a faster and more consistent way to review deal packages without sacrificing accuracy, evidence traceability, policy controls, or authorized human decision-making.

## 1.2 Business Context

The initial product targets commercial banking credit-review workflows.

An illustrative deal package may contain:

- Credit application
- Commercial loan term sheet
- Historical financial statements
- Debt schedule
- Borrower projections
- Collateral information
- Credit policy documentation
- Supporting legal documents

Reviewers must determine whether the available information supports further approval consideration and which issues require resolution.

Deal or No Deal AI will automate preparation and initial analysis while preserving human responsibility for judgment and decisions.

### Opportunity

Deliver a unified workspace where AI specialists perform distinct review responsibilities and a coordinating agent compiles their outputs into an evidence-backed review package.

### Business Hypotheses

**H1:** Automating extraction, rule checking, and draft preparation will reduce analyst preparation time.

**H2:** Deterministic financial calculations and evidence validation will improve consistency.

**H3:** Clear agent ownership and structured handoffs will reduce avoidable rework.

**H4:** Source-linked findings and visible review status will increase user trust.

These are hypotheses to test, not proven business outcomes.

## 1.3 Product Vision

Create a trustworthy multi-agent financial deal review assistant that can:

- Understand uploaded deal documents.
- Extract and normalize key information.
- Evaluate financial metrics.
- Check applicable policy requirements.
- Identify material risks and exceptions.
- Verify supporting evidence.
- Produce a draft credit review memorandum.
- Route the package to an authorized human reviewer.

The system must provide transparent execution status, explainable findings, and a complete review history.

## 1.4 Product Positioning

**Product Name:** Deal or No Deal AI

**Tagline:** Every deal has a story. Our agents find the plot holes.

**Product Description:** An AI application that analyzes deals and flags financial risks.

**Positioning Statement:**

For commercial lending teams that spend significant time reviewing complex financial deals, Deal or No Deal AI is a multi-agent credit analysis assistant that transforms source documents into structured, validated, and reviewable credit packages. It combines specialist-agent coordination, deterministic policy checks, financial calculations, source citations, and human approval controls.

## 1.5 Current Workflow

| Step | Primary Owner | Current Activity | Potential Pain Point |
|---|---|---|---|
| Deal Intake | Relationship Manager | Collect deal package | Missing or inconsistent documents |
| Document Review | Credit Analyst | Extract financial terms | Repetitive manual work |
| Financial Analysis | Credit Analyst | Calculate ratios and trends | Recalculation and data quality |
| Policy Review | Credit / Risk Officer | Check policy compliance | Complex rules and exceptions |
| Risk Review | Risk Officer | Identify weaknesses | Fragmented information |
| Credit Memo | Credit Analyst | Consolidate findings | Repetitive drafting |
| Credit Review | Authorized Reviewer | Review assumptions and evidence | Multiple clarification cycles |
| Approval | Authorized Credit Authority | Make formal lending decision | Must remain governed and documented |

## 1.6 Proposed Workflow

1. User creates a deal workspace and uploads source documents.
2. Intake service validates document format, identifies types, and extracts readable content.
3. Orchestrator initializes the deal state and execution plan.
4. Extraction Agent identifies structured deal facts and source references.
5. Financial Agent calculates ratios using deterministic functions.
6. Policy Agent checks validated deal facts against the applicable policy rules.
7. Risk Agent synthesizes risk indicators, exceptions, and potential mitigants.
8. Evidence Agent verifies that findings are supported and internally consistent.
9. Memo Agent produces a structured draft review memorandum.
10. Orchestrator validates completion criteria and routes the package for human review.
11. Authorized reviewer accepts the draft analysis, requests changes, or rejects it.
12. System records the review decision, findings, source versions, and execution trace.

**Important:** Acceptance of an AI-generated review package is not the same as formal loan approval.

## 1.7 Business Value

| Value Driver | Expected Benefit | Validation |
|---|---|---|
| Productivity | Reduced review preparation effort | Baseline versus assisted time |
| Quality | Fewer extraction and calculation errors | Golden evaluation dataset |
| Consistency | Repeatable application of defined policy rules | Policy correctness tests |
| Transparency | Source-linked material findings | Citation verification |
| Governance | Clear human ownership of review decisions | Approval audit trail |
| Scalability | Reusable agent patterns and schemas | Cost to add new deal types |

---

# 2. User

## 2.1 Primary Users

### Persona 1 — Credit Analyst

**Primary MVP user**

Responsible for reviewing borrower financials, preparing credit analysis, calculating ratios, and drafting credit memoranda.

**Jobs to Be Done**

- When a new loan package arrives, help me identify and extract material deal information.
- When financial data changes, recalculate the relevant credit metrics.
- When preparing a credit memo, organize evidence and findings into a consistent format.
- When information is missing, identify the gap rather than making assumptions.

**Success Criteria**

- Reduced manual preparation time.
- Accurate financial outputs.
- Source references for material findings.
- Easy correction of extracted data.
- Reduced rework.

### Persona 2 — Credit Risk Manager

Responsible for reviewing credit risks, policy exceptions, and underwriting assumptions.

**Jobs to Be Done**

- Identify policy exceptions quickly.
- Understand how the system reached each conclusion.
- Compare borrower financial risk indicators.
- Challenge unsupported recommendations.
- Escalate material exceptions for appropriate review.

**Success Criteria**

- High recall of material exceptions.
- Clear policy references.
- Reproducible calculations.
- Complete evidence packages.
- Reliable escalation behavior.

### Persona 3 — Authorized Credit Reviewer

Responsible for reviewing the prepared credit analysis and, where separately authorized, participating in formal credit decisions.

**Jobs to Be Done**

- Review concise deal summaries.
- Inspect material risks and exceptions.
- Navigate directly to supporting documents.
- Provide corrections or request additional evidence.
- Record an auditable review disposition.

**Success Criteria**

- Faster understanding of deal risks.
- Complete review package.
- Transparent uncertainty.
- No hidden changes to source facts.
- Clearly documented review actions.

## 2.2 Secondary Users

- Relationship Managers
- Compliance Officers
- Legal Reviewers
- Portfolio Managers
- Credit Operations Teams
- Model Risk and AI Governance Teams
- Product and Engineering Administrators

## 2.3 User Journey

| Stage | User Action | System Behavior | Desired UX |
|---|---|---|---|
| Create | Initiates new review | Creates unique deal ID | Simple intake |
| Upload | Uploads documents | Validates and catalogs files | Immediate feedback |
| Review Terms | Opens extracted terms | Displays values and citations | Document-linked facts |
| Analyze | Runs deal review | Orchestrates specialist agents | Transparent progress |
| Investigate | Reviews findings | Shows risks, rules, calculations | Explainable results |
| Correct | Edits or disputes findings | Records correction and reruns dependent steps | Controlled revisions |
| Approve Draft | Reviews final memo | Records reviewer disposition | Clear authority boundary |
| Export | Downloads review package | Produces versioned artifact | Reusable output |

## 2.4 User Permissions

| Role | Create Deal | View Deal | Edit Extracted Facts | Review Findings | Approve Draft Analysis | Configure Policies |
|---|---|---|---|---|---|---|
| Credit Analyst | Yes | Assigned | Yes, audited | Yes | No | No |
| Risk Manager | Optional | Authorized | Suggest correction | Yes | Yes | No |
| Authorized Reviewer | No | Authorized | Request changes | Yes | Yes | No |
| Administrator | Configurable | Authorized only | No by default | Operational only | No by default | Yes |

Role names and permissions describe simulated demo personas. On 2026-10-22 the user explicitly selected role simulation for the demo only, replacing the earlier real-sign-in requirement. Show a persistent simulation banner and record the selected persona on actions. A local operator may switch among predefined personas to demonstrate the workflow; these are not verified identities. Application services must still enforce the selected persona's allowed actions and deal scope. Simulated permissions tests demonstrate workflow rules, not authenticated user isolation or production access security. Real-data/shared deployment requires a separately approved authentication and authorization design.

---

# 3. Core Metrics, Prioritisation & Roadmap

## 3.1 North Star Metric

**Verified Deal Review Preparation Time**

Definition:

Time required for a user to produce a review package that passes required quality and evidence checks.

Measure both:

- Active human preparation time.
- Total elapsed time to review-ready output.

The metric must not reward fast but incorrect analysis.

## 3.2 Business Metrics

| Metric | Definition | Initial Objective |
|---|---|---|
| Preparation time reduction | Percentage decrease versus manual baseline | Test 20–30% hypothesis |
| Cost per verified review | Total operating cost / successful reviews | Establish measured baseline |
| Rework rate | Reviews returned for correction / completed drafts | Lower than manual baseline |
| Review throughput | Verified drafts completed per period | Demonstrate improvement |
| Reviewer acceptance | Drafts accepted without material correction | Measure during pilot |

The 20–30% time-reduction figure is a test hypothesis, not a guaranteed outcome.

## 3.3 User Metrics

| Metric | Definition | Proposed MVP Target |
|---|---|---|
| Task completion | Users completing a full test review | ≥90% |
| Critical task success | Users successfully finding evidence and exceptions | ≥95% |
| Reviewer clarity | Reviewers rating findings understandable | ≥4/5 average |
| Correction usability | Users correcting an extracted field successfully | ≥90% |
| Source navigation | Valid citation opened successfully | ≥95% |

Small-sample results should be labeled preliminary.

## 3.4 AI-Quality Metrics

| Metric | Target |
|---|---|
| Required term extraction accuracy | ≥95% |
| Policy outcome correctness | ≥98% |
| Deterministic calculation correctness | 100% on controlled fixtures |
| Material risk recall | ≥90% |
| Citation support rate | ≥95% |
| Missing-information detection | ≥95% |
| Valid agent handoffs | ≥99% |
| Unauthorized financial actions | 0 |
| Critical policy exceptions missed | 0 on MVP critical test set |

All targets are proposed acceptance gates requiring empirical validation.

## 3.5 Prioritisation Framework

Use RICE with the formula:

**RICE = Reach × Impact × Confidence / Effort**

Scores below are preliminary planning assumptions, not observed research data.

| Feature | Reach | Impact | Confidence | Effort | Indicative RICE | Priority |
|---|---:|---:|---:|---:|---:|---|
| Document intake | 100 | 2 | 0.9 | 2 | 90 | P0 |
| Terms extraction | 100 | 3 | 0.8 | 3 | 80 | P0 |
| Financial calculations | 90 | 3 | 0.9 | 2 | 121.5 | P0 |
| Policy checks | 90 | 3 | 0.8 | 3 | 72 | P0 |
| Risk summary | 90 | 2 | 0.7 | 3 | 42 | P0 |
| Agent orchestration | 100 | 3 | 0.8 | 4 | 60 | P0 |
| Evidence validation | 100 | 3 | 0.8 | 3 | 80 | P0 |
| Credit memo | 80 | 2 | 0.8 | 2 | 64 | P0 |
| Review checkpoint | 70 | 3 | 0.9 | 2 | 94.5 | P0 |
| Cross-document reconciliation | 70 | 2 | 0.6 | 4 | 21 | P1 |
| External web research | 50 | 1 | 0.5 | 4 | 6.25 | P2 |
| Persistent personal memory | 20 | 1 | 0.4 | 4 | 2 | P2 |

RICE informs sequencing but does not override mandatory safety or technical dependencies.

## 3.6 Delivery Roadmap

| Day | Workstream | Deliverable |
|---|---|---|
| Day 1 | Approved specifications, schemas, synthetic fixtures, sample rules, and Streamlit intake skeleton | Testable foundation and local intake journey |
| Day 2 | Parsing, cited extraction, deterministic Financial specialist, and unit tests | Structured terms and verified financial calculations |
| Day 3 | Policy specialist, Risk Agent, orchestrator dependencies, deterministic Evidence specialist, and Jupyter graph visualization | Bounded graph with evidence-linked findings, exceptions, and a readable notebook diagram |
| Day 4 | Memo Agent, persisted human review, correction invalidation, and agent timeline UI | Complete local review journey |
| Day 5 | End-to-end evaluations, notebook fresh-kernel checks, regression checks, cost/latency measurement, fixes, and local demonstration | Submission package with measured results and documented limitations |

The five-day target covers implementation after the required PRD, HLD, feature-specification, repository-design, and execution-plan approvals. Tests and synthetic evaluations start with each component; Day 5 consolidates results rather than beginning quality work. This is a delivery target, not evidence that all scope is feasible in five days. If quality gates fail, report the gap and request a scope/schedule decision. External deployment is not included or authorized.

## 3.7 Future Roadmap

**Phase 2 — Analyst Productivity**

- Cross-document contradictions.
- Advanced comparison and source navigation.
- Reviewer feedback analytics.
- Policy version management.

**Phase 3 — Enterprise Integration**

- Approved document repositories.
- Role-based access integrations.
- Loan origination system connectivity.
- Durable approvals and case management.

**Phase 4 — Additional Markets**

- Insurance underwriting.
- Investment committee reviews.
- Private credit due diligence.
- Commercial real estate financing.

---

# 4. MVP Features

## 4.1 Feature Inventory

| Feature ID | Feature | Priority | Owner Component |
|---|---|---|---|
| F-001 | Deal workspace and intake | P0 | Intake Service |
| F-002 | Document parsing and validation | P0 | Ingestion Service |
| F-003 | Key-term extraction | P0 | Extraction Agent |
| F-004 | Financial ratio computation | P0 | Financial Agent |
| F-005 | Policy compliance checks | P0 | Policy Agent |
| F-006 | Risk detection and synthesis | P0 | Risk Agent |
| F-007 | Evidence verification | P0 | Evidence Agent |
| F-008 | Multi-agent orchestration | P0 | Orchestrator |
| F-009 | Credit memo generation | P0 | Memo Agent |
| F-010 | Human review and correction | P0 | Review Service |
| F-011 | Agent execution timeline | P0 | Observability/UI |
| F-012 | Evaluation and regression tests | P0 | Evaluation Service |
| F-013 | Cross-document conflict detection | P1 | Evidence Service |
| F-014 | Semantic policy RAG | P1 | Retrieval Layer |
| F-015 | Downloadable review package | P1 | Export Service |
| F-016 | Live external system integrations | P2 | Integration Layer |
| F-017 | Jupyter notebook for workflow graph visualization | P0 | Developer Learning / Orchestrator |

## 4.2 Functional Requirements

### FR-001 — Deal Creation

The user must be able to create a deal workspace with a unique identifier and optional metadata.

**Acceptance Criteria**

- A new deal ID is generated.
- The workspace initially contains no findings.
- The deal has a visible lifecycle status.
- Users cannot accidentally access other unauthorized deal workspaces.

### FR-002 — Document Upload

The system must accept supported deal documents and validate their basic properties.

**Acceptance Criteria**

- MVP supports text-based PDF files.
- Users can upload multiple files.
- Invalid and unreadable files produce explicit errors.
- Every file receives a source ID and version.
- File size and count limits are enforced.
- Unreadable scans are marked unsupported unless an approved OCR capability is enabled.

### FR-003 — Document Extraction

The Extraction Agent must produce normalized deal fields with source references.

**Required Fields**

- Borrower and legal entity.
- Facility type.
- Principal amount and currency.
- Term or maturity.
- Interest-rate terms.
- Repayment structure, where stated.
- Collateral, where stated.
- Guarantees, where stated.
- Financial covenants.
- Use of proceeds.
- Relevant financial data.

**Acceptance Criteria**

- Each field includes source provenance.
- Missing information is represented explicitly.
- Currency and units are normalized.
- Malformed model output is rejected.
- Users can correct an extracted value.
- Material corrections are logged.

### FR-004 — Financial Analysis

The Financial Agent must calculate supported ratios using deterministic functions.

**MVP Calculations**

- Debt / EBITDA.
- Debt Service Coverage Ratio.
- Revenue growth, when data is provided.
- Current ratio, when inputs are available.
- Basic interest coverage, when inputs and definitions are available.

**Acceptance Criteria**

- Results identify calculation inputs and formula definitions.
- Divide-by-zero and invalid inputs are handled.
- Missing inputs do not produce fabricated values.
- Controlled numerical tests pass exactly within defined rounding tolerances.
- Ratios are not calculated from incompatible periods or units.

### FR-005 — Policy Compliance

The Policy Agent must compare validated deal information with applicable versioned policy rules.

**Supported Outcomes**

- Pass.
- Exception.
- Unknown / insufficient evidence.
- Not applicable.

**Acceptance Criteria**

- Each finding includes a policy rule ID.
- The applied policy version is recorded.
- The applicable comparator is deterministic.
- Unsupported interpretations are escalated.
- Missing data never silently results in a pass.
- Source policy passages can be inspected.

### FR-006 — Risk Assessment

The Risk Agent must identify material risks and present their supporting evidence.

**MVP Risk Categories**

- High leverage.
- Weak debt-service coverage.
- Liquidity concerns.
- Missing collateral evidence.
- Policy exceptions.
- Missing or conflicting terms.
- Material borrower or repayment concentration when supplied data supports the assessment.

**Acceptance Criteria**

- Each finding includes category, severity, evidence, and recommended follow-up.
- Unsupported risks are marked unverified.
- Severity is based on documented rules or transparent heuristics.
- The agent does not claim to predict default probabilities without a validated model.

### FR-007 — Evidence Verification

The Evidence Agent must check whether material claims can be traced to source material or verified calculations.

**Acceptance Criteria**

- Every material factual claim has a usable reference.
- The system validates whether cited source locations exist.
- Unverified material claims are withheld or clearly marked.
- Contradictory evidence is surfaced.
- The review status cannot become verified when a critical evidence check fails.

### FR-008 — Agent Orchestration

The Orchestrator must coordinate agent execution using explicit dependencies and shared state.

**Acceptance Criteria**

- Each specialist has bounded inputs and outputs.
- Dependencies are enforced.
- Node results are validated before downstream use.
- Agent status is visible.
- Failed steps cannot silently become successful.
- Retries, recursion, and execution limits are enforced.
- Critical missing inputs cause a controlled pause or escalation.

### FR-009 — Credit Review Memo

The Memo Agent must generate a structured draft credit review package.

**Required Sections**

1. Deal summary.
2. Borrower overview.
3. Facility terms.
4. Financial metrics.
5. Policy findings.
6. Material risks.
7. Missing information.
8. Potential mitigants.
9. Recommended follow-up actions.
10. Source appendix.
11. Human review status.

**Acceptance Criteria**

- The memo uses validated upstream information.
- Calculated values are not altered during writing.
- Material findings include citations.
- Draft status is clearly shown.
- Unresolved exceptions appear prominently.
- The document does not claim the transaction has been approved.

### FR-010 — Human-in-the-Loop Review

Authorized users must review the AI package before it is marked reviewed.

**Review Actions**

- Accept draft analysis.
- Request correction.
- Reject draft analysis.
- Escalate unresolved concerns.

**Acceptance Criteria**

- Selected simulated reviewer persona and action are logged and labeled as unverified demo attribution.
- Corrections retain previous values and evidence.
- A material correction invalidates affected downstream outputs.
- The system reruns dependent analysis before re-review.
- Reviewing a draft never triggers loan approval or disbursement.

### FR-011 — Execution Transparency

Users must be able to inspect the agent workflow.

**Acceptance Criteria**

- Display step and agent status.
- Show execution duration.
- Show errors and retries.
- Display source and rule references.
- Display final stop reason.
- Avoid exposing credentials, hidden model reasoning, or sensitive tool payloads unnecessarily.

### FR-012 — Evaluation Dashboard

Developers must be able to inspect evaluation results for individual specialists and full workflows.

**Acceptance Criteria**

- Store test inputs and expected results.
- Run deterministic tests.
- Run representative end-to-end cases.
- Compare agent outcomes across versions.
- Report accuracy, latency, cost, and failures.

### FR-013 — Jupyter Workflow Graph Notebook

Provide a Jupyter notebook that helps the user see and understand the application's LangGraph workflow.

**Acceptance Criteria**

- Import the shared application graph definition rather than maintain a separate notebook-only pipeline or hand-drawn replacement.
- Display a readable workflow diagram showing the orchestrator's coordination, six specialist responsibilities, start/end points, conditional routes, and human-review checkpoint. Distinguish deterministic specialists from model-backed work.
- Explain each stage's purpose and handoff in simple language. A diagram of possible routes must not be presented as a trace of an actual completed run.
- Generate/display the graph locally without a Nebius API key, inference call, paid service, or external diagram-rendering request.
- Work from a fresh kernel using the approved setup and a separate notebook data context; rendering must not start a review or alter existing review state.
- Keep credentials and confidential data out of saved notebook outputs. Any optional synthetic execution example must be labeled fixture/demo and obey the same application controls and budgets.

The notebook filename, rendering dependency/mechanism, and exact reproducibility checks will be defined in the feature specifications and repository-design phases. This requirement does not authorize creating notebook code before the implementation gate.

## 4.3 MVP Screens

**Screen 1 — Deal Dashboard**

Shows deals, status, owners, exceptions, and recent activity.

**Screen 2 — New Deal**

Accepts document uploads, displays validation results, and initiates review.

**Screen 3 — Review Workspace**

Displays extracted terms, financial metrics, policy checks, risks, and cited evidence.

**Screen 4 — Agent Activity**

Displays agent execution progress, errors, and relevant handoffs.

**Screen 5 — Credit Memo**

Presents the draft memorandum, unresolved issues, and review actions.

## 4.4 Explicit Non-Goals

The MVP will not:

- Approve or reject real loan applications.
- Disburse or transfer funds.
- Make binding borrower commitments.
- Modify production lending systems.
- Conduct full regulatory AML/KYC adjudications.
- Guarantee legal or regulatory compliance.
- Train a credit default prediction model.
- Replace certified financial professionals.
- Support unrestricted web-browsing agents.
- Process real customer data without approved controls.
- Implement a fully distributed A2A infrastructure.
- Maintain long-term personal memory.

---

# 5. Constraints

## 5.1 Time and Scope

**Constraint:** Five-day hackathon implementation and local demonstration target, after the required specification and design approvals.

The team must prioritize a complete demonstrable journey over enterprise breadth.

**Required Demo**

- One correctly structured commercial loan.
- One deal with material policy exceptions.
- One deal with missing or conflicting evidence.

## 5.2 Data Constraints

- Use synthetic or appropriately licensed public sample data.
- Do not use confidential bank or customer information for the initial public demo.
- Policy rules are fictional examples and must be labeled as such.
- Synthetic risk outcomes must not be represented as real underwriting decisions.

## 5.3 Regulatory and Governance Constraints

The product is an analytical decision-support tool.

Formal lending decisions remain governed by the institution's internal credit policies, delegated authorities, and applicable laws.

Production adoption requires institution-specific compliance, information-security, model-risk, and legal assessments.

## 5.4 Infrastructure Constraints

- Python-based implementation.
- Streamlit interface.
- LangGraph orchestration.
- Nebius-hosted LLM API for MVP; provider selected by the user, exact model/configuration not yet selected.
- Deterministic calculation and rule engines.
- Restricted external tool access.
- No requirement for GPU hosting or model fine-tuning.

## 5.5 Error and Quality Constraints

- Unsupported information must not become invented facts.
- Calculation errors must be caught before report finalization.
- Agent failures must not be concealed.
- The system must not silently substitute outdated policies.
- User corrections must not overwrite source evidence.

---

# 6. Technical Requirements

## 6.1 Architecture Overview

**Recommended Pattern:** Supervisor-Orchestrated Multi-Agent Graph.

The system includes:

1. Intake Service.
2. Orchestrator.
3. Extraction Agent.
4. Financial Agent.
5. Policy Agent.
6. Risk Agent.
7. Evidence Agent.
8. Memo Agent.
9. Human Review Service.
10. Evaluation and Observability Layer.

Six specialist responsibilities are defined. Not all need to run as autonomous LLM agents; deterministic specialists are permitted and preferred where appropriate.

## 6.2 Execution Flow

```text
User / Streamlit
       |
       v
Document Intake
       |
       v
Document Validation
       |
       v
Orchestrator
       |
       v
Extraction Agent
       |
       v
Schema Validation
       |
       +-----------------------+
       |                       |
       v                       v
Financial Agent       Independent Policy Checks
       |                       |
       +----------+------------+
                  |
                  v
          Dependent Policy Checks
                  |
                  v
             Risk Agent
                  |
                  v
           Evidence Agent
                  |
                  v
          Verified Findings?
             /         \
           No           Yes
           |             |
           v             v
     Escalate or      Memo Agent
     Request Data         |
                          v
                    Human Review
                          |
                          v
                Reviewed Report
```

The Orchestrator manages state, dependency validation, and controlled branching.

## 6.3 Technology Stack

The user selected the stack below on 2026-10-22. Selection establishes technology direction; package versions, adapter contracts, deployment settings, and compatibility evidence belong in the revised HLD/specifications. No dependencies or services have been installed or activated.

| Layer | Choice | Purpose and decision status |
|---|---|---|
| Development assistant | Codex | Selected to help implement approved specifications, write tests, review changes, and explain code; development role only |
| Model inference | Nebius Token Factory | Selected provider/service; account endpoint, model ID, pricing, and configuration pending verification |
| Agent orchestration | LangGraph + selected LangChain primitives | Selected for explicit dependencies, structured handoffs, shared state, checkpointing, and human-review pauses |
| Interface | Streamlit | Selected Python review workspace for the local prototype |
| Graph visualization and learning | Jupyter notebook / JupyterLab with a Python kernel | Selected by user to visualize the shared LangGraph workflow and explain its stages; offline graph rendering is required |
| Validation | Pydantic | Selected to validate facts, findings, and agent handoffs before downstream use |
| Financial calculations | Python Decimal; pandas where useful | Selected deterministic arithmetic and policy comparisons; pandas is optional when tabular operations justify it |
| Persistence | SQLite + compatible LangGraph checkpointer | Selected to save deal state, corrections, findings, and review progress; exact adapter and restart/deletion behavior need verification |
| Documents | PyMuPDF, subject to dependency/licensing review | Selected parser direction; preserve page references and verify runtime compatibility/licensing before adoption |
| Testing | pytest + synthetic evaluation cases | Selected to test arithmetic, policies, workflow controls, and AI quality separately |
| Observability | Local diagnostics first + LangSmith | Selected: local timings, usage, errors, and handoffs are the baseline; LangSmith is the chosen tracing/evaluation integration, with hosted tracing disabled until approved/configured |
| Application and package management | Python + uv | Retained project foundation; interpreter and dependency versions will be pinned after compatibility checks |
| Policy rules | Versioned JSON/YAML + Python | Retained sample rule definitions and deterministic comparisons; exact rule content still needs approval |
| Demonstration | Local Streamlit execution | Five-day delivery target; external hosting remains outside the current authorization |

Pinecone, LlamaIndex, Langfuse, and additional providers are future alternatives rather than MVP dependencies. Changes to the selected stack require an explicit recorded decision. Learning notebooks continue to call shared Python application logic without a separate implementation.

LangSmith selection does not replace pytest or local AI evaluations. Local diagnostics must remain usable without a LangSmith account/connection. Hosted tracing configuration must define allowed fields, redaction, retention, account limits, and any costs before activation; ordinary telemetry excludes raw deal documents and credentials.

### 6.3.1 Nebius Provider Requirements

The user will supply Nebius access instead of OpenAI API access. Use one explicitly configured Nebius provider adapter; there is no OpenAI-hosted inference fallback. OpenAI Codex remains a development assistant, separate from the application's inference provider.

Nebius Token Factory documents an OpenAI-compatible API and a Python quickstart using `https://api.tokenfactory.nebius.com/v1/` with `NEBIUS_API_KEY`. Treat this as the documented Token Factory endpoint, not proof that the user's account uses that endpoint rather than a dedicated deployment. Verify the account endpoint and exact model ID before configuring execution. An OpenAI-compatible client library, if used, is a transport choice; requests must be directed only to the configured Nebius endpoint. [Nebius quickstart](https://docs.tokenfactory.nebius.com/quickstart)

Provider selection does not finalize the LangChain adapter/package. Prefer a maintained provider integration when it preserves required usage and model fields; otherwise verify a compatible client wrapper. API compatibility does not establish complete support for tools, streaming, JSON schemas, token accounting, retries, or provider-specific fields. Check these against the selected model and package before approving HLD/specifications.

Use a model supporting the needed structured-output behavior; validate every returned payload with Pydantic regardless of provider formatting. Nebius documents both JSON schema and JSON object formats, with support varying by model. Treat output-cap, context-size, tokenizer, timeout, and any reasoning-token behavior as model-specific checks. [Structured output](https://docs.tokenfactory.nebius.com/ai-models-inference/json)

At implementation time, load the key from local `NEBIUS_API_KEY` environment/secret configuration. The key is not needed for PRD/HLD work and must not appear in chat requests, committed files, notebook outputs, model prompts, traces, or exports. Do not request an OpenAI API key. No secret/configuration file is created during this phase.

Preserve the five-day target and section 12.3 budgets. Provider choice is confirmed, while the exact model, dated pricing, account rate limits, data-transfer terms, and first authorized execution remain unresolved. No live API call or account change is performed by this document revision.

## 6.4 Agent Input/Output Contracts

All specialist agents must return schema-validated outputs.

Example shared state:

```python
class DealState(TypedDict, total=False):
    deal_id: str
    source_documents: list
    extracted_terms: dict
    financial_metrics: dict
    policy_findings: list
    risk_findings: list
    evidence_review: dict
    credit_memo: str
    review_status: str
    errors: list
```

Every workflow event should also track:

- Task ID.
- Agent identity.
- Start and end time.
- Input and output references.
- Validation outcome.
- Retry count.
- Error category.
- Relevant model and prompt versions.

## 6.5 Agent Permission Boundaries

| Agent | Read Documents | Calculations | Read Policies | Change Source Facts | External Writes |
|---|---|---|---|---|---|
| Extraction | Yes | Limited | No | No | No |
| Financial | Validated data | Yes | Applicable definitions | No | No |
| Policy | Validated data | Yes | Yes | No | No |
| Risk | Validated results | Limited | Read-only | No | No |
| Evidence | Yes | Verify only | Yes | No | No |
| Memo | Validated outputs | No new calculations | Cited findings | No | No |
| Orchestrator | References and state | No direct calculation | Metadata | No | No |

Only approved application services may persist reviews or modify workflow metadata.

No agent may directly approve or fund a loan.

## 6.6 Human Review Technical Requirements

- Persistent approval state.
- Explicitly labeled simulated reviewer persona for the local synthetic demo; no real sign-in or identity provider is required by the user-authorized scope change.
- Review action permitted for the selected demo persona, enforced by application services.
- Resume after interruption.
- Revalidation after correction.
- Reviewer comments.
- Audit history.

LangGraph interrupts and checkpointing may be used for this workflow.

## 6.7 Nonfunctional Requirements

| ID | Requirement | MVP Target |
|---|---|---|
| NFR-001 | Standard review latency | P95 ≤90 seconds on defined test packages |
| NFR-002 | Application availability | Best-effort demo; no SLA claimed |
| NFR-003 | Evaluation reproducibility | Same fixtures and versions produce equivalent deterministic outcomes |
| NFR-004 | Structured output validity | 100% accepted outputs conform to required schemas |
| NFR-005 | Audit completeness | 100% review decisions recorded |
| NFR-006 | Unauthorized external writes | 0 |
| NFR-007 | Execution limit | Maximum 20 graph node executions per review |
| NFR-008 | Retry limit | At most 1 retry per transient operation, within the global 5-model-attempt limit and all remaining budgets |
| NFR-009 | Model cost | Target ≤$0.10 per standard synthetic review; hard model/tool ceiling $0.25 per review |
| NFR-010 | Document size | Proposed maximum 20 MB per file |
| NFR-011 | Access isolation | No cross-deal access without authorization |
| NFR-012 | Error transparency | Failures return explicit error or review-needed status |
| NFR-013 | Token budget | At most 8,000 aggregate input and 2,000 aggregate output tokens per review across all calls, retries, corrections, and resumes |
| NFR-014 | Inference attempt limit | At most 5 model attempts per review; aim for at most 4 on the normal path |
| NFR-015 | Active runtime and tools | Maximum 180 active seconds per review, 45 seconds per model call bounded by remaining time, and 12 tool invocations |

Cost and latency targets are proposals to validate after baseline measurements.

## 6.8 State and Memory

**MVP decision:** No cross-user or long-term personal memory.

Store only:

- Deal-specific workflow state.
- Normalized deal facts.
- References to source files.
- Review corrections and decisions.
- Execution metadata.
- Necessary audit information.

Do not allow agents to use one deal's confidential contents as memory for another deal.

**MVP retention assumption:** Automatically delete disposable demo documents and associated operational state after 30 days, unless the user explicitly requests earlier deletion or retention is required by an applicable agreement.

For production, retention periods must be determined by the deploying institution's legal, records-management, privacy, and audit requirements.

Memory controls must include deletion, access restriction, versioning, and protection against stale facts.

## 6.9 Tool Execution Boundaries

All tool calls must:

- Match a registered schema.
- Be authorized for the calling role.
- Validate input arguments.
- Apply timeouts.
- Record safe execution metadata.
- Return structured errors.
- Avoid implicit write operations.
- Reject unknown tools.

External actions, if introduced in a later phase, require explicit human authorization and idempotent execution where applicable.

---

# 7. Grounding Strategy

## 7.1 Approved Knowledge Sources

| Source | Approved for MVP | Use |
|---|---|---|
| Uploaded synthetic deal documents | Yes | Financial and transaction facts |
| Uploaded synthetic financial statements | Yes | Ratio inputs |
| Versioned sample credit policies | Yes | Policy conditions |
| Validated deterministic outputs | Yes | Financial metrics and rule outcomes |
| Reviewer corrections | Yes, deal-scoped | Updated validated facts |
| General LLM knowledge | Limited | Explanations, never authoritative deal facts |
| Public web | No by default | Future contextual research |
| Unverified model memory | No | Never authoritative |

## 7.2 Source Authority

The application must not use a simplistic "newest document always wins" rule.

For conflicting facts:

1. Identify source type and authority.
2. Determine whether the source is applicable.
3. Check document date and version.
4. Determine whether the documents address the same field.
5. Compare values and qualifications.
6. Apply explicit precedence rules only when defined.
7. Otherwise flag the conflict for human review.

## 7.3 Document Processing Pipeline

```text
Upload
  → Validate
  → Parse
  → Segment
  → Assign Document IDs
  → Normalize Metadata
  → Extract Fields
  → Validate Schema
  → Preserve Source References
  → Downstream Agents
```

Document metadata should include:

- Source ID.
- Original filename.
- File hash.
- Document type.
- Upload timestamp.
- Document date, if available.
- Version.
- Page and section identifiers.
- Access scope.

## 7.4 Citation Requirements

**CIT-001:** Every extracted material term must have a source reference.

**CIT-002:** Every policy exception must include the applicable rule and version.

**CIT-003:** Every calculated metric must identify its input values and definitions.

**CIT-004:** Every material risk statement must have evidence or be explicitly labeled as an inference.

**CIT-005:** The final memo must support navigation to the relevant source content.

**CIT-006:** Invalid or unresolved citations must prevent a claim from being classified as verified.

## 7.5 Source Navigation UX

Clicking a citation should display:

- Document title.
- Page or section.
- Relevant passage or table.
- Extracted field.
- Normalized value.
- Reason it supports the finding.

For the MVP, page-level navigation is required where parsing supports page identification. Precise highlighting of scanned text is a later enhancement.

## 7.6 Retrieval Strategy

For MVP:

- Direct retrieval for small known document sets.
- Deterministic lookup for validated policy rules.
- No vector database required initially.

For larger future document collections:

- Metadata-filtered retrieval.
- Hybrid lexical and semantic search.
- Optional reranking.
- Applicability checks.
- Citation verification.

Pinecone may be introduced if experiments demonstrate a material retrieval benefit.

---

# 8. Prompt Strategy

## 8.1 Core Principles

Each agent should have:

- A narrowly defined role.
- Approved inputs.
- Explicit tool permissions.
- A structured output contract.
- Instructions for missing or conflicting information.
- A bounded task objective.
- Clear stopping and escalation rules.

Prompts must not replace deterministic application controls.

## 8.2 Orchestrator Prompt Contract

**Role:** Coordinate specialized financial review activities.

**Responsibilities**

- Determine required subtasks.
- Delegate to authorized specialists.
- Enforce dependencies.
- Inspect structured completion statuses.
- Route unresolved issues.
- Stop at completion or configured limits.

**Restrictions**

- Do not fabricate specialist results.
- Do not overwrite financial calculations.
- Do not bypass missing evidence.
- Do not approve transactions.
- Do not initiate unauthorized external actions.

## 8.3 Extraction Agent Prompt Contract

**Goal:** Extract only information explicitly supported by the provided document.

**Required Behavior**

- Preserve numerical precision.
- Normalize units.
- Separate raw and normalized values.
- Return missing fields as unknown.
- Include source locations.
- Distinguish borrowed terms from inferred interpretations.

**Output:** Validated structured deal schema.

## 8.4 Policy Agent Prompt Contract

**Goal:** Identify applicable rules and produce verifiable policy findings.

**Required Behavior**

- Apply only approved rule packs.
- Verify applicability and effective version.
- Use deterministic comparisons.
- Return pass, exception, unknown, or not applicable.
- Explain the relevant source condition.
- Escalate ambiguous interpretations.

## 8.5 Financial Agent Prompt Contract

**Goal:** Calculate supported financial measures using authorized calculation tools.

**Required Behavior**

- Use supplied verified financial inputs.
- Check units and periods.
- Use approved metric definitions.
- Return formulas, inputs, and outputs.
- Refuse to invent missing inputs.
- Record calculation errors.

## 8.6 Risk Agent Prompt Contract

**Goal:** Identify material risks supported by validated deal information.

**Required Behavior**

- Distinguish facts from interpretations.
- Identify potential mitigants.
- Explain materiality.
- Avoid unsupported probability-of-default claims.
- Flag missing information.
- Return structured risk findings with evidence.

## 8.7 Evidence Agent Prompt Contract

**Goal:** Verify material factual claims and internal consistency.

**Required Behavior**

- Check source references.
- Verify numeric consistency.
- Identify unsupported claims.
- Detect contradictions.
- Return verified, unverified, or needs-review status.

## 8.8 Memo Agent Prompt Contract

**Goal:** Transform validated findings into a review-ready memorandum.

**Required Behavior**

- Use approved sections and templates.
- Do not introduce new numerical facts.
- Preserve open exceptions.
- Cite material findings.
- Display draft status.
- Include reviewer action requirements.

## 8.9 Prompt Version Management

Every model invocation must record:

- Prompt ID.
- Prompt version.
- Model identifier.
- Input schema version.
- Output schema version.
- Relevant tool version.
- Evaluation run ID where applicable.

Prompt changes must be evaluated against the regression dataset before acceptance.

---

# 9. Hallucination Guardrails

## 9.1 Guardrail Model

Use layered protection:

**Layer 1 — Input Validation**

Check format, document type, and required fields.

**Layer 2 — Source Grounding**

Require evidence for material extracted claims.

**Layer 3 — Structured Outputs**

Validate model outputs with Pydantic schemas.

**Layer 4 — Deterministic Financial Tools**

Use code for numerical calculations and rule comparisons.

**Layer 5 — Evidence Validation**

Verify citations, contradictions, and consistency.

**Layer 6 — Human Review**

Require authorized review for material findings and final packages.

**Layer 7 — Audit and Monitoring**

Record failures, corrections, and review decisions.

## 9.2 Missing Information Behavior

When information is missing:

- Return `unknown`.
- Identify the missing field.
- Explain which calculation or check cannot proceed.
- Request the necessary document or data.
- Block dependent conclusions where appropriate.

**Example:**

"EBITDA is not available in the supplied financial documents. Debt/EBITDA cannot be calculated reliably. Provide the applicable financial statement or approved EBITDA reconciliation."

## 9.3 Conflicting Information Behavior

When documents disagree:

- Show both values.
- Show both sources.
- Identify the affected metric or rule.
- Apply explicit source precedence only when authorized.
- Otherwise escalate.

The model must not resolve material contradictions by confidence alone.

## 9.4 Unsupported Requests

The system must decline or redirect requests to:

- Fabricate financial statements.
- Hide material risks.
- Falsify compliance.
- Create nonexistent citations.
- Modify immutable source evidence.
- Bypass authorized review.
- Approve or disburse loans without authority.
- Access another customer's confidential information.

The system may provide a compliant alternative, such as drafting a transparent exception request or identifying missing evidence.

## 9.5 Prompt Injection Defense

Uploaded documents are untrusted source content.

Any embedded instruction attempting to change agent roles, reveal credentials, disable checks, or initiate external actions must be treated as document text rather than instructions.

Tool execution permissions must be enforced outside the model.

## 9.6 Retry and Recovery

- At most 1 retry per transient operation, only when the remaining global token, cost, time, tool, and model-attempt budgets can cover the attempt.
- Count framework/provider retries and structured-output repair calls toward the same global limits; disable unaccounted automatic retries.
- No blind retry of ambiguous write operations.
- Validate state before resuming.
- Stop when critical dependencies fail.
- Preserve partial validated outputs.
- Escalate when recovery is not possible.

---

# 10. Evaluation Strategy

## 10.1 Evaluation Objectives

Demonstrate that the system can:

1. Extract correct deal facts.
2. Calculate correct financial ratios.
3. Apply the correct policy rules.
4. Detect material risks and exceptions.
5. Produce source-supported findings.
6. Coordinate specialist agents reliably.
7. Handle uncertainty and failures safely.
8. Generate useful review packages.

## 10.2 Evaluation Dataset

Use a curated synthetic evaluation suite.

**Initial Target:** 30 deal scenarios.

| Scenario Type | Minimum Cases |
|---|---:|
| Standard compliant cases | 5 |
| Policy exceptions | 5 |
| Financial ratio edge cases | 5 |
| Missing information | 4 |
| Contradictory documents | 4 |
| Invalid documents and tool failures | 4 |
| Prompt injection and authorization attempts | 3 |
| **Total** | **30** |

Each case should include:

- Input documents.
- Applicable rule pack.
- Expected structured facts.
- Expected financial calculations.
- Expected policy findings.
- Expected risks or abstentions.
- Expected workflow terminal status.

## 10.3 Component Evaluation

| Component | Evaluation | Proposed Threshold |
|---|---|---|
| Extraction | Field-level accuracy | ≥95% |
| Financial | Numerical correctness | 100% controlled fixtures |
| Policy | Rule-outcome correctness | ≥98% |
| Risk | Material risk recall | ≥90% |
| Evidence | Supported claim rate | ≥95% |
| Memo | Required sections and factual consistency | ≥98% |
| Orchestrator | Expected execution path | ≥95% |
| HITL | Authorization control | 100% of controlled tests |

## 10.4 End-to-End Evaluation

Track:

- End-to-end task success.
- Total duration.
- Number of agent steps.
- Model tokens.
- Cost per run.
- Tool failures.
- Retry counts.
- Unverified claims.
- Reviewer corrections.
- Final result status.

## 10.5 Evaluation Methods

**Deterministic testing**

Use pytest for calculations, schemas, rules, permissions, and workflow conditions.

**Golden dataset evaluation**

Compare agent results with expert-defined expected outcomes.

**LLM-as-a-judge**

Use for qualitative aspects such as explanation clarity, memo completeness, and relevance.

Do not use LLM-as-a-judge as the sole authority for numerical accuracy or legal/compliance correctness.

**Human evaluation**

Have an appropriately qualified reviewer assess material risk findings and report usefulness.

**Regression testing**

Rerun tests after changes to prompts, rules, models, extraction logic, and orchestration.

## 10.6 Evaluation Acceptance Gates

The MVP passes only if:

- All critical financial tests pass.
- No unauthorized action occurs.
- No critical synthetic policy exception is missed.
- All required graph nodes are exercised.
- Missing information is handled correctly.
- Human review cannot be bypassed.
- Citation behavior meets the threshold.
- A complete report is generated for valid scenarios.

## 10.7 Failure Taxonomy

Track failures using consistent categories:

- `EXTRACTION_ERROR`
- `MISSING_DATA`
- `UNIT_MISMATCH`
- `POLICY_MISAPPLICATION`
- `CALCULATION_ERROR`
- `UNSUPPORTED_CLAIM`
- `INVALID_CITATION`
- `AGENT_HANDOFF_ERROR`
- `TIMEOUT`
- `PERMISSION_DENIED`
- `REVIEW_REQUIRED`
- `LOOP_LIMIT_REACHED`

## 10.8 Experiment Plan

| Experiment | Baseline | Variant | Decision Metric |
|---|---|---|---|
| Extraction approach | Single prompt | Structured extraction + validation | Field accuracy |
| Policy checking | LLM-only | Deterministic rule engine | Policy correctness |
| Risk synthesis | Unconstrained prompt | Evidence-constrained specialist | Grounding + risk recall |
| Review workflow | Single monolithic LLM | Specialist graph | Quality per dollar |
| Evidence | Basic citation instructions | Independent evidence check | Citation support |
| Retrieval | Direct lookup | Semantic/hybrid retrieval | Applicable policy recall |

Multi-agent complexity is justified only if its measured benefits exceed added cost and latency.

---

# 11. Production Readiness Criteria & Metrics (HHH)

For this PRD, HHH is defined as **Helpful, Honest, and Harmless**.

This is a proposed interpretation for the project's acceptance framework.

## 11.1 Helpful

The system delivers useful analysis that improves deal-review work.

| Metric | MVP Criterion |
|---|---|
| Verified task completion | ≥95% on supported test scenarios |
| Financial analysis correctness | 100% on controlled fixtures |
| Required memo sections | ≥98% completeness |
| Usability | ≥4/5 average pilot rating |
| Manual preparation time | Demonstrate a measured reduction |

## 11.2 Honest

The system provides supported facts and clearly communicates uncertainty.

| Metric | MVP Criterion |
|---|---|
| Material citation support | ≥95% |
| Missing-information detection | ≥95% |
| Fabricated monetary values | 0 in critical test cases |
| Unsupported completion claims | 0 |
| Invalid source references | 0 in accepted verified findings |

## 11.3 Harmless

The system respects authorization boundaries and avoids harmful operational behavior.

| Metric | MVP Criterion |
|---|---|
| Unauthorized loan approvals | 0 |
| Unauthorized disbursements | 0 |
| Sensitive cross-deal leakage | 0 in security tests |
| Unreviewed consequential writes | 0 |
| Critical policy bypass | 0 |
| Prompt injection success on protected actions | 0 |

## 11.4 MVP Readiness Versus Bank Production Readiness

**Hackathon MVP Readiness**

- Synthetic data only.
- Correct basic multi-agent workflow.
- Passing controlled tests.
- Functional review checkpoint.
- Traceable findings.
- Documented limitations.
- No production financial actions.

**Production Banking Readiness**

Additional work required:

- Institution-specific risk assessments.
- Formal security and privacy review.
- Vendor and model risk governance.
- Legal/compliance approval.
- Role and entitlement integration.
- Data residency and retention controls.
- Disaster recovery and incident response.
- Model performance monitoring.
- Human reviewer training.
- Independent validation.
- Ongoing policy maintenance.
- Formal change management.
- Production support and SLAs.

The project must not advertise regulatory compliance or production approval without these activities.

## 11.5 Security and Privacy Requirements

**Data minimization**

Only collect information necessary for the review.

**Least privilege**

Agents and users must have the smallest required set of permissions.

**Encryption**

Use encryption in transit and at rest in production.

**Secret handling**

Store credentials in environment-based secret management, never prompts or repository files.

**Telemetry**

Avoid sending raw sensitive borrower documents to analytics platforms unless explicitly approved and configured.

**Deletion**

Provide controlled deletion consistent with retention obligations.

**Access logging**

Record sensitive operations without exposing confidential values in logs.

## 11.6 Audit Requirements

The audit record must capture:

- Deal ID.
- Source documents and versions.
- Applied policy versions.
- Material extracted values.
- Financial calculations.
- Agent outputs and validation status.
- Reviewer decisions.
- Changes and corrections.
- Timestamps.
- Final report version.

## 11.7 Go/No-Go Decision

A demo can proceed when all critical MVP acceptance gates pass.

Any failure involving fabricated critical financial values, unauthorized actions, or bypassed review checkpoints is a launch blocker.

---

# 12. Pricing

## 12.1 MVP Cost Strategy

The initial project is a demonstration, not a commercial product launch.

**Primary cost components**

- LLM input and output tokens.
- Embeddings if semantic retrieval is enabled.
- Application hosting.
- Storage.
- Observability.
- Optional document-processing services.

## 12.2 Unit Economics

Define:

**Cost per Verified Deal Review = Total Processing Cost / Number of Verified Completed Reviews**

Track cost separately for:

- Extraction.
- Financial analysis.
- Policy checks.
- Risk synthesis.
- Evidence validation.
- Memo generation.
- Retries.

## 12.3 Proposed MVP Budgets

| Budget Item | Target |
|---|---|
| Standard deal review | Target ≤$0.10 model/API cost |
| Maximum permitted model/tool cost per review | Hard ceiling $0.25, including retries and corrections |
| Aggregate input tokens | Maximum 8,000 per review across all model calls |
| Aggregate output tokens | Maximum 2,000 per review across all model calls |
| Model attempts | Aim for ≤4 on the normal path; hard maximum 5 including retries and repair calls |
| Standard deal processing | P95 ≤90 seconds |
| Active processing stop | 180 seconds total; at most 45 seconds per model call, bounded by remaining time |
| Execution steps | ≤20 cumulative graph node executions per review, including retries and resumed work |
| Tool invocations | Maximum 12 per review |
| Transient retries | At most 1 per operation, subject to every global limit |
| Model output per call | Explicit task-specific cap reserved within the remaining 2,000-token aggregate output allowance |

The budget values are provisional engineering targets. No actual provider quote or measured workload cost has been established.

Cost-limit breaches must stop execution safely and preserve validated partial outputs.

### 12.3.1 Token and Cost Optimization

Keep all six specialist responsibilities while avoiding six mandatory model calls:

- Use deterministic graph routing for the supervisor and ordinary Python tools for the Financial specialist and structural Evidence checks. These steps require no model inference.
- Aim for four focused model tasks: extraction, ambiguous policy-clause interpretation when needed, risk synthesis, and memo drafting. Skip model policy interpretation when structured facts and deterministic rules suffice. Semantic evidence uncertainty remains visible for human review; structural checks do not prove a claim is true.
- Parse each document once. Select relevant source passages with original source IDs; pass compact validated facts and finding references downstream instead of resending whole PDFs or full agent conversations.
- Generate a concise template-based memo. Reuse validated outputs for unchanged inputs, and invalidate/rerun only dependent stages after corrections. Keep document, policy, model, prompt, and schema versions in cache keys.
- Use one explicitly approved model configuration. Any lower-cost configuration must pass the same evaluation gates. Do not silently switch providers, add judge-model calls, or lower quality thresholds to meet the budget.
- Reserve input/output tokens and conservative priced usage before every call. If a task cannot fit, stop with a clear budget/context message or request a smaller supported package; never silently drop material evidence.
- Keep cumulative usage across UI refreshes, retries, corrections, and resumes. A new attempt cannot reset the same review's allowance. Exceeding an allowance requires explicit approval of a new budget.
- Report input/output tokens, attempt counts, cache hits, estimated inference cost, and any unavailable usage. A provider's dated rates must be verified before priced calls; these budget values are not provider price quotes or observed results.

The USD 0.10 target is 90% lower than the supplied v1.0 USD 1 target; the USD 0.25 hard ceiling is 90% lower than its USD 2.50 ceiling. These are proposed engineering limits implementing the user's request for lower budgets. Provider/model feasibility remains unmeasured. No paid execution is approved, and a separately approved total batch allowance is required before running paid evaluation suites.

### 12.3.2 Nebius-Specific Cost and Latency Checks

Nebius documents best-effort automatic prefix caching and model-specific cached-input pricing. Keep stable instructions/tool definitions first and changing deal content later. Record actual cache usage where available; reserve the budget assuming no cache hit. Cached input remains part of the 8,000-token input ceiling. Application-result caching is separate and may avoid an inference call entirely. [Nebius cached tokens](https://docs.tokenfactory.nebius.com/cached-tokens)

For the selected model, verify current uncached-input, cached-input, and output prices. Count cached tokens as a subset of total input, not an additional input charge. Verify whether additional reasoning tokens are billed within output and preserve the provider's usage fields rather than inferring charges from visible text alone. The USD 0.10 target and USD 0.25 ceiling are unvalidated budgets, not Nebius price quotes.

Use the actual account's limits and returned rate-limit metadata; do not copy example quotas into the application. A transient rate-limit retry must fit the existing one-retry, total-attempt, token, monetary, and remaining-time limits. Keep one active review rather than adding speculative parallel model calls. [Nebius rate limits](https://docs.tokenfactory.nebius.com/ai-models-inference/rate-limits)

Earlier OpenAI-specific cache settings, Batch discounts, retention options, tokenizer assumptions, and SDK features are not Nebius requirements or verified benefits. Any Nebius batch evaluation mode needs its own documented compatibility/pricing checks and explicit execution allowance. No particular discount or latency improvement is promised.

## 12.4 Commercial Pricing Hypotheses

Possible future commercial pricing models:

**Per Deal Review**

Charge per completed analysis package, differentiated by document volume and review complexity.

**Team Subscription**

Charge per team or workspace, potentially with usage allowances.

**Enterprise License**

Contracted annual pricing based on usage, integrations, hosting requirements, security, support, and governance capabilities.

No customer willingness-to-pay research has been completed. Pricing must be validated through customer discovery and actual cost analysis.

## 12.5 Packaging Hypothesis

| Tier | Audience | Potential Features |
|---|---|---|
| Pilot | Small analyst group | Document intake, review agents, export |
| Professional | Larger underwriting team | Collaboration, analytics, policy packs |
| Enterprise | Regulated financial institution | Private deployment, audit controls, integrations, governance |

These are exploratory commercial concepts, not committed offerings.

---

# 13. Assumptions

## 13.1 Confirmed Design Decisions

The following have been selected for the project:

- Product category: Multi-Agent Deal Review Pipeline.
- Initial workflow: Commercial lending and credit analysis.
- Orchestration pattern: Supervisor with specialist agents.
- Core responsibilities: Extraction, Policy, Financial, Risk, Evidence, Memo.
- Framework: LangGraph with selected LangChain agent/tool primitives.
- Development language: Python.
- UI: Streamlit.
- Reviewer access: simulated demo personas only, explicitly selected by the user; no claim of authenticated identity or production-grade access control.
- Graph visualization: Jupyter notebook importing and displaying the same application graph, with plain-language explanations and no inference required for rendering.
- Development assistant: Codex.
- Model inference provider/service: Nebius Token Factory; exact model/configuration pending.
- Validation: Pydantic.
- Financial calculations: Python Decimal, with pandas where useful.
- Persistence: SQLite with a compatible LangGraph checkpointer; adapter verification pending.
- Document parser: PyMuPDF, subject to dependency/licensing review.
- Tests and AI evaluations: pytest and synthetic cases, with separate quality measurements.
- Observability: local diagnostics first plus LangSmith as the selected tracing/evaluation integration; hosted tracing remains disabled until approved/configured.
- Deterministic rules and calculations.
- Human review before finalizing the analysis.
- MVP-first delivery.
- No autonomous financial commitments.

## 13.2 Working Assumptions

**A-001:** The user requested a five-day implementation delivery target. It begins after required specification/design approvals; exact calendar dates, team capacity, and feasibility are not established.

**A-002:** Synthetic deal documents can be created and used.

**A-003:** Commercial term loans are the initial product type.

**A-004:** English-language, text-based PDFs are sufficient for MVP.

**A-005:** The initial policy corpus is small and version controlled.

**A-006 — confirmed provider choice:** The MVP will use the user's Nebius API access rather than OpenAI-hosted inference. Nebius Token Factory is the proposed service mapping; exact account endpoint, model ID, configuration, pricing, and execution permission remain to be confirmed. Choosing the provider does not activate it.

**A-007:** SQLite with a compatible LangGraph checkpointer is the selected persistence direction. Suitability, adapter/runtime compatibility, restart recovery, and deletion behavior remain unvalidated.

**A-008:** A domain reviewer can validate the evaluation answers or the demo uses explicitly synthetic golden rules and outcomes.

**A-009:** No live bank systems or confidential customer data are connected.

**A-010:** Human acceptance applies to the AI review package, not the final lending decision.

**A-011:** Long-term user memory is unnecessary.

**A-012:** MCP and A2A are optional extensions rather than first-week requirements.

## 13.3 Dependencies

| Dependency | Purpose | Criticality |
|---|---|---|
| Synthetic deal dataset | Representative test and demo inputs | Critical |
| Sample policy rule pack | Deterministic compliance checking | Critical |
| Approved metric definitions | Reliable financial calculation | Critical |
| Nebius API access and selected model | Extraction, policy interpretation when needed, risk narrative, and memo generation; model capability checks pending | Critical |
| LangGraph environment | Workflow orchestration | Critical |
| Source parser | PDF extraction and references | Critical |
| Test framework | Automated evaluation | Critical |
| Tracing platform | Agent debugging and quality measurement | High |
| Deployment environment | Accessible live demo | High |
| Domain validation | Evaluation credibility | High |

## 13.4 Key Risks

| Risk ID | Risk | Severity | Mitigation |
|---|---|---|---|
| R-001 | Incorrect extracted facts | High | Grounded extraction and human correction |
| R-002 | Wrong policy applicability | Critical | Versioned rules and deterministic validation |
| R-003 | Incorrect calculations | Critical | Python functions and unit tests |
| R-004 | Unsupported credit recommendation | High | Evidence validation and draft status |
| R-005 | Agent loops or repeated actions | Medium | Step and retry limits |
| R-006 | Multi-agent coordination errors | High | Explicit shared state and structured handoffs |
| R-007 | Sensitive information exposure | Critical | Synthetic data for MVP, security controls for production |
| R-008 | Human overreliance | High | Source navigation and reviewer accountability |
| R-009 | High inference cost | Medium | Token controls and focused agent responsibilities |
| R-010 | Hackathon schedule slippage | High | P0 scope and staged implementation |

## 13.5 Open Questions

**[NEEDS INPUT — Q1]** Should the first MVP focus exclusively on commercial term loans, or support revolving credit facilities as well?

**[NEEDS INPUT — Q2]** Will the project use only generated synthetic documents, or include appropriately licensed public financial reports and sample legal agreements?

**[NEEDS INPUT — Q3]** Is the primary demonstration goal to emphasize agent-to-agent coordination, financial-analysis accuracy, or business workflow productivity? All three will be supported, but this choice determines which area receives the most development and evaluation effort.

## 13.6 Final MVP Definition of Done

The MVP is complete when a user can:

1. Upload a supported synthetic commercial loan package.
2. Run the multi-agent review pipeline.
3. Inspect extracted terms with source references.
4. View verified financial calculations.
5. Identify applicable policy exceptions.
6. Review material risks and missing evidence.
7. Inspect agent execution progress and errors.
8. Generate a draft credit review memorandum.
9. Accept, reject, or request corrections to the draft analysis.
10. Export or inspect the resulting review package.

Additionally:

- Critical evaluation tests must pass.
- No unauthorized actions may occur.
- The demo must show at least one exception case and one missing-evidence case.
- The repository must contain setup instructions, synthetic test data, architecture documentation, and evaluation results.
- A Jupyter notebook must display the shared workflow graph from a fresh kernel without API credentials or model calls, as specified in FR-013.
- The product must clearly state that it is a decision-support prototype, not a lending approval system.

---

## Product Summary

**Deal or No Deal AI** demonstrates how a controlled multi-agent architecture can improve complex financial deal-review workflows by combining specialized reasoning, deterministic financial rules, evidence grounding, coordinated execution, and human oversight.

The initial product should optimize for **correctness, traceability, and review usability**, rather than maximizing autonomous behavior.

Success means enabling a credit professional to understand a deal more efficiently while preserving the institution's authority over financial decisions.

**End of PRD — Version 1.5**
---

## Revision Review Notes — History and Carried-Forward Decisions

These notes preserve revision history. PRD v1.4 was approved for HLD work on 2026-10-22; v1.5 records the user's subsequent explicit choice of role simulation for the demo only. Budgets and execution controls are accepted targets with feasibility unmeasured. Questions without an explicit answer remain open for HLD/specifications. The old baseline's business rules are not carried forward automatically.

### Revision summary

| Area | Previously approved v0.1 | Current v1.5 baseline |
|---|---|---|
| Name and positioning | DealLens; small-business loan and same-loan debt-investment review | Deal or No Deal AI; commercial banking credit review; tagline: Every deal has a story. Our agents find the plot holes. |
| Specialist responsibilities | Extraction, policy, combined risk/summary; deterministic evidence checks | Extraction, Financial, Policy, Risk, Evidence, Memo; deterministic specialists explicitly permitted |
| Reviewer access | One local operator; reviewer labels, no verified identity | User-approved analyst/manager/reviewer/admin role simulation; selected-persona permissions enforced, no real sign-in |
| Financial measures | DSCR, debt/EBITDA, collateral coverage | DSCR, debt/EBITDA, revenue growth, current ratio, interest coverage; collateral still appears in facts/risks |
| Input limits and parser | Text PDF/text; 3 documents, 10 MB combined; pypdf proposed | English text-based PDF; PyMuPDF required; 20 MB per file proposed; aggregate count/page/size limits unspecified |
| Inference and observability | Provider undecided; no activation approved | Nebius Token Factory selected; model/endpoint/configuration pending; local diagnostics plus LangSmith selected, hosted tracing disabled pending configuration/approval |
| Runtime targets | p95 120 seconds; 180 active-second limit; 6 model attempts; 12 tools; one retry/stage | p95 90 seconds; 20 cumulative nodes; 5 model attempts; 12 tools; one retry/operation; 8,000 input/2,000 output tokens; 180 active seconds |
| Monetary budgets | Conditional USD 0.10 inference ceiling | USD 0.10 standard review target and USD 0.25 hard model/tool ceiling; exact limits proposed and unvalidated |
| Evaluation data | 12 development plus 12 held-out acceptance cases | 30 scenarios; development/acceptance partition not specified |
| Delivery | Phase gates, no fixed implementation deadline | User-requested five-day implementation/local-demo target after document approvals; no external deployment |

### Carried-forward decisions and original review observations

1. **Product boundary:** Section 13.5 asks term loans versus revolving facilities. Recommendation pending approval: commercial term loans only for the first version. The previously approved same-loan debt-investment view is absent from the new MVP; confirm whether it is intentionally deferred or should be restored.
2. **Data and demonstration:** Sections 5.2 and 13.5 allow licensed public examples, while grounding and the definition of done emphasize synthetic inputs. Recommendation pending approval: synthetic-only acceptance/demo cases first. Public data would require explicit source/license/data-access review. Select the principal demo emphasis: coordination, financial accuracy, or productivity.
3. **Access model — resolved by explicit user choice:** Use role simulation for the demo only. Preserve service-level persona/action/deal checks, visible simulation labels, and attributed review history. Do not represent the role selector as real authentication or claim production user-isolation security from simulated permission tests.
4. **Financial and policy definitions:** The new draft does not include the former POL-01–07 sample thresholds or complete definitions for the added ratios. The old rules are historical only, not automatically approved for this revision. Approve a versioned sample rule pack, exact numerator/denominator definitions, periods, units, debt basis, collateral treatment, severity rubric, and rounding before implementation specifications. No business thresholds will be invented silently.
5. **Execution limits — accepted targets:** Section 12.3 sets cumulative ceilings across corrections, retries, and resumes: 20 node executions, 5 model attempts, 12 tools, 8,000 input/2,000 output tokens, USD 0.25 maximum priced inference/tool usage, and 180 active seconds with 45-second call limits. HLD/specifications must define enforcement and usage accounting. Feasibility is unmeasured; no live execution is enabled by requirements approval.
6. **Metric consistency and measurement:** Distinguish section 3's 90% user task-completion target from section 11's 95% supported-scenario completion target using separate denominators. Define scoring for memo completeness versus factual consistency, handoff validity versus rejected malformed outputs, critical versus general risks, and citation coverage versus support. Specify development/held-out splits, run counts, latency workload, and reporting of failures/cost estimates in Phase 3. The original MET-01–12 definitions are historical and must not silently become the new scoring contract.
7. **MVP priorities:** F-015 makes downloadable export P1, while the user journey and definition of done mention export or inspection. F-013 makes conflict detection P1, while FR-006/007 and the required demo need material contradictions surfaced. Resolve which exact minimum export and contradiction behavior is P0. Recommendation pending approval: keep material conflict surfacing P0, defer advanced reconciliation, and explicitly choose whether export is required or inspection alone is sufficient.
8. **Delivery and consent:** The requested five-day schedule is a planning target after the required document approvals, not permission to skip gates or an agreed calendar deadline. The hosted-API assumption and reduced budget targets are not consent to incur charges. The roadmap now ends in a local demonstration; the remaining live-demo dependency does not authorize external hosting. Local demonstration remains the permitted boundary unless the user separately approves provider execution, charges, data transfer, and/or deployment.
9. **Retention feasibility:** Section 6.8 asks for automatic 30-day deletion, but the local application's behavior while stopped is not defined. Decide whether startup/access-time cleanup suffices or a background scheduler is required. Define deletion of checkpoints, caches, managed exports, and late results; do not promise forensic erasure or deletion of user-made copies.
10. **Dependency verification:** The stack in section 6.3 is selected. PyMuPDF, the Nebius/LangChain integration, compatible SQLite checkpointer, and LangSmith/identity dependencies still need capability, compatibility, licensing, limit, and cost review during the revised HLD. Selection does not approve a repository license, service connection, dependency installation, or provider activation. Pinecone/LlamaIndex/Langfuse remain future alternatives and are not selected MVP dependencies.

### Document authority and phase gate

- Current requirements baseline: PRD v1.5, incorporating approval of v1.4 plus the explicitly authorized role-simulation change, selected stack, five-day target, Nebius, budgets, Jupyter notebook, and carried-forward open decisions.
- Historical approved reference: [PRD v0.1](prd-v0.1-approved.md). It does not override this approved revision.
- Current design work: [HLD](../../architecture/hld.md) and architecture decisions are reconciled against v1.5. The earlier HLD is preserved as a superseded proposal; no architecture approval is inferred from PRD approval.
- Gate outcome: PRD v1.4 approved for Phase 2 on 2026-10-22, with the demo-role change explicitly authorized and recorded as v1.5. Review the revised HLD next, then request approval before Phase 3 specifications and evaluations.
- Work completed for this edit: preserved the prior baseline, incorporated the replacement PRD, and flagged affected design documents. No application code, tests, evaluations, dependencies, paid calls, or deployment were created/run.
