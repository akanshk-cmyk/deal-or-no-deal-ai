# Offline Jupyter Graph and Clickable HTML Walkthrough

**Current artifacts:** notebooks/01_workflow.ipynb derives SVG/Mermaid from the
shared compiled StateGraph without invoking it or creating a database. SVG uses
only local code; no remote Mermaid renderer. IPython/Jupyter kernel is optional
and not installed/verified in the current environment. tools/export_html_demo.py
reads scoped registered fixture records and produces prototype/index.html, a
six-destination local snapshot with evidence selection and disabled execution.
No duplicate financial rules/calculations exist in HTML. The notebook's code cells
are syntax-checked; runtime kernel execution must be reported separately.

Feature ID: SPEC-012
Version: 1.9
Status: Graph-only saved/live notebook and versioned clickable HTML implemented and checked; fresh-kernel notebook execution and manual browser assessment deferred
PRD requirements: FR-008, FR-011, FR-013, FR-015–016, FR-019–020; PRD required deliverables
Role instructions: [Orchestrator](../agents/orchestrator.md), [Report Generator](../agents/report-generator.md)
Shared definitions: [CONTRACT-1.0 and decision register](overview.md)
Evaluation: [Evaluation plan](../evaluation/evaluation-plan.md)

## User story and boundaries

A learner understands the real graph in Jupyter and can click through a lightweight HTML explanation. Neither artifact should duplicate the financial engine or imply execution that did not occur.

## Workflow and rules

Notebook graph-only sequence: explain synthetic boundary -> import shared graph factory/metadata without provider construction -> obtain actual node/edge metadata -> render locally -> explain direct route, required review, missing-data stop and correction flow -> distinguish possible routes from recorded execution.

Display three core agents, seven specialist responsibilities, deterministic routing and the two possible model calls. Human interrupt/resume, direct-report branch and Report Generator must be visible. A resumed-node example explains repeated invocation/accounting and MemorySaver RAM limits. Use RESUME-1.0's validated application receipt rather than unrestricted raw reviewer state; RUN-OUTCOME-1.0 distinguishes paused invoke/information END from actual completion. Graph-only display performs none of these operations. Static HTML snapshots preserve those labels, historical/current distinctions and COVERAGE-1.0 original source locations without claiming live resume or source validation.

P3-09 proposes local NetworkX/Matplotlib rendering from actual graph metadata after compatibility/licensing checks. Do not use remote Mermaid PNG endpoints or hand-maintain a separate notebook pipeline. Remote rendering is not an acceptable fallback; explain local rendering failure.

HTML is a local five-screen visual walkthrough reusing the approved scenarios and labels. Clicks navigate Dashboard -> New Deal -> Workspace -> Activity -> Memo and show source/review/blocked-state examples. Clearly label illustrative snapshots or executed fixture run snapshots with lineage. Upload/Run affordances explain demonstration-only behavior, not simulate arbitrary document processing. No provider key, runtime API, embedded financial rules, copied evaluator answers or external deployment.

The user confirmed a professional, realistic appearance on2026-10-23: compact navy navigation, white surfaces, restrained blue actions, readable financial tables and consistent spacing/type, matching SPEC-010. Use realistic coherent synthetic documents/states rather than invented activity or institution branding. Visual polish must preserve illustration/execution labels and unavailable-action explanations. Exact design tokens remain subject to the later design-system phase; this preference does not authorize building or deploying the prototype yet.

Apply UX-1.0 from SPEC-010 to the walkthrough: five default dashboard columns, three-step intake presentation, Workspace overview with all mandatory blockers and finding/evidence pairing, one contextual primary action, expandable technical Activity detail and separate memo recommendation/review/report labels. Illustrative correction interactions explain impact, saved/stale state and explicit continuation without mutating records. Preserve keyboard focus/navigation and useful narrow-layout evidence return; static examples never imply an actual upload, rerun, recorded approval or measured timing occurred. The offline graph notebook remains a teaching artifact, not a new command-center screen.

The existing Policies detail example includes View rule evaluation from RULEVIEW-1.0: compact condition/observed value/outcome plus source/formula/rule-version detail. Reuse recorded snapshot fields or clearly labeled illustrative E-P01 values (DSCR1.15<1.25 -> Exception); HTML contains no copied policy evaluator, editable thresholds, validation stamp or live Deploy/Accept behavior. Demonstrate missing/not-yet-evaluated/stale details through approved snapshot states, with source links preserving context. Extend existing TEST-012-04 rather than adding a screen or model call.

The Risks snapshot shows three independent SCOREVIEW-1.0 assessments: credit score/band or Insufficient Data, policy exceptions, missing required evidence. Copy recorded RISK-EDU-1.0 ratings/weights/contributions/material-input and source/configuration context; explain coverage in detail. Before a scoped executed case exists, label41 Moderate as Illustrative arithmetic example, not an executed review. Display Python's required action/owner/tier and independent mandatory blockers; AI-proposed action is available only with accepted current synthesis lineage. An unrelated evidence gap can coexist with a complete score; a material scoring gap cannot. Show missing/unknown/not-run/stale states explicitly. No second bank/customer model, default probability, HTML scoring/routing engine or editable sliders. Existing TEST-012-04/05 verify labels, snapshot lineage and no fake execution.

SME fixes apply to notebook/HTML presentation without a new graph: label prepared complete cases versus unregistered partial upload; distinguish recorded factual support from credit disposition; show supplied entity/annual period, covenant EXTRACTED_NOT_EVALUATED and deferred reported-EBITDA reconciliation. Full-term/balloon/refinancing adequacy remains Not evaluated. Conditions show recorded provenance/owner/status and outstanding proposals without claiming fulfillment or clearing existing mandatory issues. A clickable support/condition control in static HTML is navigation or explicitly labeled simulation, never an actual persisted review, graph continuation, provider call or observed execution. Only executed current artifacts can supply real status snapshots.
CX-1.0 in SPEC-010 also applies to the five-screen HTML presentation: show the sample introduction and prepared/partial distinction, accessible fixed term help, explicit local-demo handoff, saved/pending/uncertain recovery examples and the recorded outcome/conditions/next-action recap. Use approved illustrative or executed snapshot fields with their actual lineage; sample selection/help/navigation never pretends to start a review, notify a colleague, persist support, incur a charge or complete an action. Individually checked support examples cannot imply blanket verification. Static role changes are clearly labeled walkthrough selection, not runtime authorization. Extend existing TEST-012-04/05; do not add a new screen, financial engine or provider call.

## Contracts and data changes

Proposed shared reads: get_graph_description(graph_factory) -> GraphDescription; build_walkthrough_snapshot(scoped validated fixture artifacts) -> WalkthroughSnapshot. These are local project contracts, not claims about exact external API names.
GraphDescription: graph/config version, node IDs/labels/core-role/responsibility/execution kind, edge source/target/condition, legend.
WalkthroughSnapshot: synthetic scenario/deal/run/revision/mode, snapshot_kind ILLUSTRATIVE/EXECUTED_FIXTURE, event/report/source refs, generated_at/cutoff, safe display fields. Executed label requires actual run artifacts; illustrative label cannot fabricate handoff timestamps or usage.

No application schema changes beyond snapshot metadata. Notebook output and local HTML are generated only after implementation gates, not now.

## AI and evidence behavior

Graph-only cells construct/render without invoking graph/model/tool operations, initializing provider clients, requiring keys or mutating persistent app state. Optional execution cells are separate, fixture-only by default and unmistakably labeled; Live examples require separate explicit execution allowance.

Citations show source versions and synthetic source excerpts for a screenshot/walkthrough, and explain that illustrative links are examples. No fake evidence provenance presented as measured output.

CITEVIEW-1.0 in SPEC-010 adds visible inline source labels beside snapshot facts/findings/conditions/policy checks and View calculation and sources beside metrics. Clicking shows the available exact snapshot passage/rule/formula with source version/context and return-to-detail navigation. If the actual original page/highlight is unavailable, disclose it rather than fake a working viewer. Illustrative citations stay labeled illustrations; executed-fixture citations require recorded source lineage. No live model/retrieval request, fabricated verification or mutation can occur through a static citation link. Existing TEST-012-04/05 cover this behavior without another screen or runtime engine.

## Authorization

Local read-only artifacts; no real authorization/approval via HTML. HTML review buttons may demonstrate permitted/blocked states but cannot change app records. No real customer information, credentials, external requests or publication.

## UI states

Notebook: dependency missing/fresh-kernel error gives local instructions, no network fallback. HTML: selected scenario/screen visible; unsupported actions explain demo boundary; empty/error/blocked/partial/stale snapshots use the same approved meaning as Streamlit. Keyboard navigation and text status labels required.

## Reliability and stopping

Graph construction/render must be deterministic for the same graph configuration. Fresh-kernel tests intercept outbound calls and storage writes. HTML opens locally without a server/remote assets and has no paid side effects. No graph, scenario or arithmetic engine is forked into notebook/HTML.

## Analytics

No remote analytics in notebook/HTML. Optional local validation report records graph version, node/edge equality, fixture snapshot lineage, offline checks and accessibility result. App screen analytics remain SPEC-010/011.

## Tests and acceptance

- TEST-012-01: Fresh-kernel graph-only notebook succeeds without credentials, provider construction or outbound renderer.
- TEST-012-02: Rendered IDs/edges/conditional labels equal actual shared graph, including all seven responsibilities.
- TEST-012-03: No database/state writes in graph-only cells; optional execution distinct from static diagram.
- TEST-012-04: All five HTML destinations/source/review states clickable offline and keyboard usable; UX-1.0 hierarchy, selected-finding/evidence return, correction impact and separate recommendation/source-support/credit-review/report summaries match Streamlit. Prepared/partial scope, condition provenance/outstanding status, covenant-not-evaluated, annual-only and deferred-EBITDA markers are accurate; clicks cannot claim real persistence, support, execution, fulfillment or funding.
- TEST-012-05: Fixture versus illustrative snapshots, audit/memory limits and no real approval clearly labeled.
- TEST-012-06: No keys/remote assets/duplicate pipeline logic; sample generated report linked to its actual run when available.

Targets: all notebook/offline presentation checks pass; graph-only provider calls zero. No notebook/HTML has been generated or run.

## Dependencies and implementation boundary

Uses SPEC-007 shared graph metadata, SPEC-009 report and SPEC-010 screen conventions. Renderer/package choice remains subject to Phase 4 review. No notebook, HTML, build command, hosting or external publishing is created in Phase 3.
