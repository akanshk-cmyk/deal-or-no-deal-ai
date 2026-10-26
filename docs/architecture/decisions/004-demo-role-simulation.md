# ADR-004: Simulated personas with prototype action guards

Version: 1.10  
Status: Accepted educational architecture baseline through Phase 3; dependency verification and implementation pending  
Date: 2026-10-22  
Reference requirements: PRD section 2; FR-001/010/020  
Context: [Current HLD](../hld.md), [Current PRD](../../product/prd.md)

Scope: Working local educational demo required; Nebius access will be supplied later. Preserve phase gates before implementation. No operational banking use, real borrower data, or deployment is included.

## Context

The user selected role simulation for the demo only. A working prototype is required; real sign-in and verified accounts remain outside scope.

## Accepted architecture direction

Provide Credit Analyst, Risk Manager, Compliance Officer, Authorized Approver (the existing Reviewer role), and Administrator personas with a persistent SIMULATED ROLES — SYNTHETIC DATA ONLY label. Record unverified persona attribution.

Enforce agreed persona/action/deal/revision rules in application services as well as UI controls. A reviewer accepts an analysis package, not a loan or investment. Generic acceptance cannot clear every mandatory specialty gate. Finalize any specialist fixture/capability mapping in specifications.

Keep human interrupt/resume in a separate zero-inference node. Because pre-interrupt code may execute again, completed paid stages must remain upstream. Review disposition/rerender does not rerun unchanged extraction or synthesis.

Synthesizer's Approve / Conditional Approve / Reject values are simulated panel recommendations, not real committee decisions or reviewer signatures. Python derives the routing flag from requested loan amount ≥ USD 10M OR confidence < 0.7, plus any other mandatory referral. True requires review; false with required gates satisfied proceeds to reporting, explicitly marked Not required rather than Reviewed. Record the human disposition separately from PanelDecision.

Resume uses the same thread and validated pending revision/persona. Proposed actions are Approve, Reject, or Conditional Approve with modified conditions. Preserve model recommendation and human disposition separately; generic acceptance cannot clear a specialty block. The accepted SAMPLE-LOAN-POLICY-1.0 retires SYN-ESC-003's USD-4M exposure rule; keep its ID for history only. Follow [Human Review instructions](../../agents/human-review.md); fine-grained specialty capabilities remain to be specified and unmapped actions are denied.

The five-screen command center adds local owner assignments, attributed notes, and issue/review handoffs, not real authenticated collaboration or external messages. These metadata actions do not trigger inference or clear issues. Workspace/Memo use the same guarded service for current-revision dispositions. Compliance/specialty capabilities must be defined in specifications; persona naming alone grants no clearing authority.

## Trade-offs and validation

Simulation teaches workflow ownership but does not establish authentication, secure account isolation, or verified signatures. The operator can switch personas.

Verify correction attribution, allowed/denied actions, stale-revision rejection, dependent-output invalidation, and visible simulation labels. No accounts, identity provider, or production authorization system is required. These controls are planned, not implemented.

Approval clarification: the user accepted the architecture/specification direction through Phase3; the subsequent issue-fix request authorizes documentary corrections. This does not select a project/parser license, validate dependencies, approve new R4-01–08 choices or authorize paid execution. [Current scope/contracts](../../specs/overview.md) govern the five-day core.
