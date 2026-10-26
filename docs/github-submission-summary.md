# Deal or No Deal AI — Multi-Agent Deal Review Pipeline

*Every deal has a story. Our agents find the plot holes.*

**Project 3B** coordinates commercial-loan review from uploaded documents to a
source-linked credit memo. This local educational application uses fictional
deals and simulated roles, without real lending authority.

## Problem and solution

Credit analysts manually reconcile contracts, financial schedules, collateral and
policies before drafting a review. Deal or No Deal AI prepares source-linked
fields, reproducible ratios and explicit exceptions for the analyst to challenge.
The principle is simple: accelerate analysis while preserving transparency and
human accountability. Productivity gains have not yet been measured.

## Multi-agent architecture

- **Extraction Agent:** Uses Nebius to extract structured terms and financial
  inputs with source references.
- **Compliance Agent:** Applies configured educational policies in Python.
- **Risk and Summary Agent role:** Combines deterministic risk flags/available
  authored ratings with an evidence-linked AI explanation and proposal.
- **LangGraph Orchestrator Agent:** Coordinates state, validated handoffs,
  conditional stops, persistence and human checkpoints.
- **Supporting services:** Financial calculations and Python memo generation.

Uploaded reviews fan out Financial, Compliance and Risk branches and join before
synthesis. Only extraction and synthesis normally call an LLM; historical
execution policies remain preserved.

## Product experience

Six connected screens cover Deal Dashboard, New Deal, Review Workspace, Agent
Activity, Credit Memo and Decision History. Users inspect PDFs, confirm reporting
context, run analysis, navigate evidence and record role-controlled actions.
One Deal ID connects the results. AI proposals, readiness and human decisions
remain separate. Educational overrides are labeled and do not clear unresolved
requirements.

## Demo and evidence

Example Equipment LLC requests a fictional USD1.2 million equipment loan. Its
annual DSCR is 1.50x and LTV60%; an illustrative Low score does not resolve an
incomplete annual-reporting covenant. Effective readiness remains Pending Review.

**Design insight: a financially attractive deal is not necessarily ready for approval.**

An actual uploaded Standard Deal completed live Nebius generation and browser
memo download. The expanded general-upload/checkpoint path has offline test
coverage; a fresh complete general-profile live walkthrough remains to verify.
Recorded acceptance testing passed 57 tests and 55 subtests, without establishing
broad model accuracy. Live-answer RAGAS remains Phase 2 work; saved-answer
evaluation is documented separately.

**Submission proof still required:** one continuous fresh-upload recording with
real fact and narrative verification, specialist fan-out/join, live synthesis and
same-deal navigation. Deterministic nodes own independent contracts; they are not
presented as autonomous LLM agents. Confirm that interpretation with the examiner.

**Stack:** Python3.12, Streamlit, LangGraph, langchain-core, Nebius Qwen generation,
Pydantic, pypdf, Decimal, SQLite and pytest. Runtime grounding uses bounded cited
pages, not an asserted production vector-RAG deployment.

**Assignment coverage:** Three specialist roles, working orchestration, structured
agent communication and a sample financial review output.

**GitHub:** [INSERT LINK — NOT VERIFIED]  
**Demo recording:** [INSERT LINK — NOT VERIFIED]  
**Application:** Local only; no public deployment link verified.
