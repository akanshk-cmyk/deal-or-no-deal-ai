# Deal or No Deal AI - Multi-Agent Deal Review Pipeline

### Every deal has a story. Our agents find the plot holes.

**Understand the deal. Check the numbers. See what still needs attention.**

A loan can look attractive on paper and still be unready for approval. Deal or No Deal AI brings document extraction, financial analysis, policy checks and human review into one connected experienceâ€”so reviewers can understand the evidence behind a recommendation.

Built for **Week 3 Project: Multi-Agent Deal Review Pipeline**, this educational application uses fictional commercial loans and simulated roles. It supports human judgment; it does not authorize real lending.

## Why we built it

A credit analyst receives a loan agreement, financial statements and collateral documents. The borrower looks promisingâ€”but do the figures cover the same period? Is the collateral sufficient? Does a reporting covenant still need review?

Reviewers must connect evidence, calculate ratios and explain unresolved concerns. One confident AI response can hide unsupported assumptions.

## One connected review experience

| Traditional review | Deal or No Deal AI |
|---|---|
| Read documents and copy important figures | Extract structured terms with source references |
| Calculate ratios in a separate worksheet | Apply reproducible Python calculations |
| Reconcile policy requirements manually | Surface configured policy findings and unknowns |
| Assemble a written credit review | Combine findings into a source-linked draft memo |
| Track review actions across files | Keep comments, decisions and timestamps together |

## From documents to a reviewable recommendation

1. **Start in New Deal.** Select a sample or upload one fictional package: up to three text PDFs, ten combined pages and 10 MB. Inspect parsed pages and confirm suggested reporting information.
2. **Run AI Deal Review.** Explicitly start live extraction of borrower details, terms, figures and source references.
3. **Check the facts.** New general uploads pause for permitted reviewers to verify facts and reporting basis.
4. **Inspect the analysis.** Financial, Compliance and Risk specialists run in parallel on verified inputs, then join before synthesis.
5. **Review the explanation.** Verify the generated narrative against its evidence. The readiness gate identifies unresolved requirements.
6. **Use the findings.** Download a permitted partial or complete memo and record authorized simulated review actions.

One Deal ID connects the documents and downstream screens. Preliminary upload calculations are labeled unverified; viewing them does not complete a graph stage or a human checkpoint.

### See the application

**Deal Dashboard â€” what needs attention next?** View the deal queue, status and recorded findings.

Six connected screens
Deal Dashboard: Prioritize deals needing attention.
New Deal: Upload, inspect and start analysis.
Review Workspace: Explore terms, calculations, policy findings, risks and sources.
Agent Activity: Inspect recorded execution and handoffs.
Credit Memo: Read and download the report.
Decision History: Inspect decisions, comments and audit events.

These actual captures show retained fictional reviews, not a newly executed upload journey. Counts reflect local demonstration history.
<img width="1907" height="820" alt="image" src="https://github.com/user-attachments/assets/08cd3997-a93a-4f8e-9d1f-d947906c71b3" />
<img width="1747" height="867" alt="image" src="https://github.com/user-attachments/assets/614c75c4-6a87-4c97-acc0-ac0618ddbc16" />
<img width="1735" height="832" alt="image" src="https://github.com/user-attachments/assets/dc80a780-b1db-4d14-868a-728a8bb85f7f" />
<img width="1780" height="855" alt="image" src="https://github.com/user-attachments/assets/fc5e8359-f6bc-4ad5-8291-1239204ccfaf" />
<img width="1811" height="857" alt="image" src="https://github.com/user-attachments/assets/d8a20506-421f-47fb-b723-5fac9d1fae59" />
<img width="1811" height="871" alt="image" src="https://github.com/user-attachments/assets/63b1f930-7779-4361-953c-79682608d4b9" />
<img width="1821" height="865" alt="image" src="https://github.com/user-attachments/assets/d73b29d6-c1f6-4212-b4b2-12adeba504e6" />


## Multi-agent flow: how data becomes analysis

LangGraph acts as the **Orchestrator Agent**: it passes structured, source-linked information between specialists, records progress and pauses when human checks are required. The workflow has two normal LLM stages and three deterministic Python specialist nodes.

| Stage | Data processing and reviewer value |
|---|---|
| Document intake | Parses PDF text, retains page references and checks upload limits. Parsing does not verify financial facts. |
| Extraction Agent ? Nebius | Turns document text into structured borrower details, loan terms and financial inputs with citations. Pydantic checks the output structure, not factual truth. |
| Human fact verification | Reviewers compare values, units, reporting periods and applicability with the cited pages. AI-assisted checks never count as human verification. |
| Financial Specialist ? Python | Applies reproducible formulas to supported inputs: debt coverage, collateral coverage and leverage. Missing operands remain unresolved. |
| Compliance Specialist ? Python | Applies configured sample-policy rules; unknown applicability and incomplete covenant checks remain visible. |
| Risk Specialist ? Python | Aggregates available risk factors and flags. Missing factor assessments produce Insufficient Data, not an assumed Low score. |
| Synthesizer Agent ? Nebius | Combines joined findings into a rationale, outstanding concerns, conditions and next actions. |
| Readiness and reporting | After narrative verification, deterministic checks set decision readiness. Permitted reports preserve findings and evidence; human decisions are recorded separately. |

## How Deal or No Deal AI Works

**From deal documents to an evidence-backed credit review — with specialized agents working together and humans remaining in control.**

Think of Deal or No Deal AI as a financial deal-review team. Each specialist has a clear responsibility, while the orchestrator coordinates the work.

### End-to-End Multi-Agent Workflow

```mermaid
flowchart TD
    A["Upload deal documents"]
    B["Parse PDFs and retain page references"]
    C["Extraction Agent<br/>Reads terms, figures and supporting sources"]
    D["Human Reviewer<br/>Checks extracted facts and reporting periods"]
    E["Orchestrator<br/>Sends the same verified information to three specialists"]

    subgraph P["Run in Parallel"]
        direction LR
        F["Financial Specialist<br/>Calculate financial ratios"]
        G["Compliance Specialist<br/>Check applicable policies"]
        H["Risk Specialist<br/>Identify risk factors and flags"]
    end

    I["Orchestrator<br/>Combines all three specialist results"]
    J["Synthesizer Agent<br/>Explains findings, concerns and next actions"]
    K["Human Reviewer<br/>Checks explanation against source evidence"]
    L{"Readiness Gate<br/>Identifies unresolved requirements"}
    M["Credit Memo<br/>Permitted report with findings and sources"]
    N["Separate Human Decision<br/>Approve, reject or request information<br/>Only when role and required checks permit"]

    A --> B
    B --> C
    C --> D
    D --> E

    E --> F
    E --> G
    E --> H

    F --> I
    G --> I
    H --> I

    I --> J
    J --> K
    K --> L

    L --> M
    L --> N

    classDef upload fill:#eff6ff,stroke:#2563eb,color:#1e3a8a
    classDef agent fill:#f3e8ff,stroke:#9333ea,color:#581c87
    classDef human fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef specialist fill:#ecfdf5,stroke:#059669,color:#065f46
    classDef gate fill:#fff1f2,stroke:#e11d48,color:#881337
    classDef output fill:#f1f5f9,stroke:#64748b,color:#0f172a

    class A,B upload
    class C,E,I,J agent
    class D,K human
    class F,G,H specialist
    class L gate
    class M,N output
```

### Explore Each Stage

Click a section below to learn what happens behind the scenes.

<details>
<summary><strong>1. Upload Documents & Extract Deal Information</strong></summary>

Users upload deal documents.

The system parses the PDFs and keeps page references so reviewers can trace information back to its original source.

The **Extraction Agent** reads important loan terms, financial figures and supporting evidence.

</details>

<details>
<summary><strong>2. Human Verification — Check the Facts</strong></summary>

Before specialist analysis begins, a human reviewer checks the extracted facts and reporting periods.

This helps prevent inaccurate figures or incorrect reporting periods from being used in financial and policy analysis.

</details>

<details>
<summary><strong>3. Three Specialists Analyze the Deal in Parallel</strong></summary>

The **Orchestrator** sends the same verified information to three specialists, which work in parallel.

- **Financial Specialist:** Calculates financial ratios.
- **Compliance Specialist:** Checks applicable policies.
- **Risk Specialist:** Identifies risk factors and flags.

Each specialist produces its own findings.

</details>

<details>
<summary><strong>4. Orchestrator Combines Specialist Findings</strong></summary>

The Orchestrator collects the results from all three specialists and combines them.

The combined information is then passed to the Synthesizer Agent.

</details>

<details>
<summary><strong>5. Synthesizer Agent Explains the Findings</strong></summary>

The **Synthesizer Agent** explains the deal's findings, concerns and recommended next actions.

The goal is to make the analysis understandable rather than simply presenting technical scores.

</details>

<details>
<summary><strong>6. Human Verification — Check the Explanation</strong></summary>

A human reviewer checks the explanation against the supporting source evidence.

This provides another opportunity to identify unsupported findings or incomplete information.

</details>

<details>
<summary><strong>7. Readiness Gate — Identify Unresolved Requirements</strong></summary>

The **Readiness Gate** identifies unresolved requirements.

From this point, the workflow supports two separate downstream outcomes:

**Credit Memo:** A permitted report containing findings and source references.

**Separate Human Decision:** Approve, reject or request additional information — only when the user's role and required checks permit that action.

An AI recommendation is not automatically a human approval.

</details>

---
### Parallel analysis, coordinated handoffs

The diagram shows the **general-upload path**. Financial, Compliance and Risk receive the same verified input snapshot and execute in parallel. LangGraph joins all three outputs before synthesis. Sample drafts and historical reviews retain their own checkpoint policies; unverified drafts are labeled.

One Deal ID and source map connect results across screens. SQLite retains checkpoints and review history so permitted continuation uses the recorded state. Viewing a page starts no AI analysis. A memo can be generated while approval remains blocked.

### Why This Workflow Matters

**Specialized analysis. Traceable evidence. Human accountability.**

Deal or No Deal AI separates document extraction, financial calculations, policy checks, risk findings and human decisions.

This helps reviewers understand not only **what the system recommends**, but also **what evidence supports the findings and what still requires attention**.


### How recommendations support a decision

The recommendation explains **what supports the deal, what remains unresolved and what to do next**. Reviewers trace claims to source pages, compare calculations with inputs and inspect policy findings. They can identify missing evidence, request information or escalate exceptions instead of accepting a score alone.

The deterministic readiness gate determines the effective outcome; an AI-generated approval proposal cannot override mandatory blockers. Authorized users separately record simulated Approve, Reject or Pending actions with required comments and timestamps, subject to backend permissions and readiness checks.

## The demo story: Low Risk † Pending Review † Human Decision

**Example Equipment LLC requests a fictional $1.2 million equipment loan over 48 months.**

| Finding | Registered sample result |
|---|---|
| Debt-service coverage: annual cash available / annual debt payments | 1.50x |
| Loan-to-value: loan amount / collateral value | 60% |
| Debt / EBITDA: debt relative to operating earnings | 3.00x |
| Illustrative risk score | 21/100 - Low |
| Approval readiness | **Pending Review** |
| Human decision | **Not recorded** |

The annual financial-reporting covenant still needs evaluation. Favorable ratios and a Low rating cannot clear it. Future obligations are evaluated according to contractual timing, not automatically marked breached.

**A financially attractive deal is not necessarily ready for approval.**

The sample score depends on supplied educational factor assessments, not a calibrated default-probability model. New uploads never inherit those ratings. Any permitted educational approval override is explicitly labeled and audited; outstanding checks remain unchanged.

## What makes this project stand out?

**Specialized responsibilities, reproducible calculations, visible evidence and separate human accountability.** Reviewers see both the findings and how the system reached them.

## Technology, simply explained

Streamlit provides the interface; LangGraph and LangChain Core support orchestration. Python 3.12 handles calculations and rules, Pydantic validates structured outputs, pypdf extracts PDF text, SQLite stores local reviews and checkpoints, and pytest supports verification.

Nebius uses `Qwen/Qwen3-30B-A3B-Instruct-2507` for extraction and synthesis. Runtime grounding uses supplied cited documents; a completed semantic-retrieval benchmark is not claimed.

## Run locally

Install Python 3.12 and [uv](https://docs.astral.sh/uv/). From PowerShell:

```powershell
git clone https://github.com/akanshk-cmyk/deal-or-no-deal-ai.git
cd deal-or-no-deal-ai
uv sync --frozen --python 3.12 --group dev --extra evaluation
Copy-Item .env.example .env
```

Populate `NEBIUS_API_KEY` in local `.env`; never commit it. The evaluation extra supplies tokenizer support for live sizing; installation does not run evaluations. Explicitly download tokenizer files only, then start Streamlit:

```powershell
uv run --frozen --extra evaluation python tools/setup_live_tokenizer.py
uv run --frozen --extra evaluation streamlit run app.py --server.address 127.0.0.1
```

Check **Live AI demo: setup and readiness** in the sidebar. A key alone does not establish request fit, provider access or spending readiness. Fresh clones do not inherit ignored runtime evidence or completed reviews.

`config/app.toml` currently selects `LIVE`; `FIXTURE` uses saved sample answers without model calls. One Run action serves both. Live calls incur charges within the shared allowance; navigation starts no model call, and failures never substitute saved answers.

Run offline application tests:

```powershell
uv run --frozen --extra evaluation pytest
```

## Evidence and boundaries

[Recorded Phase 1 results](docs/evaluation/phase1-demo-results.md) document live Standard Deal extraction, synthesis and draft-memo generation, with **67 functional tests and 63 subtests** at that checkpoint. Historical results do not establish current full-suite success or general accuracy.

Saved-answer evaluations and mocked tests are separate from live-model evidence. The newest general-upload path still needs a complete fresh live walkthrough with genuine human checkpoints. AI-assisted evidence checks do not count as human verification.

Scanned/encrypted PDFs, real banking integrations, production authentication and calibrated credit predictions are outside scope. A project license has not been selected.

**Deal or No Deal AI helps explain the evidence, calculations, risks and unresolved questions behind a recommendation.**

*Educational use only. All demonstration deals are fictional and roles simulated. AI recommendations and demo decisions do not authorize real loans.*
