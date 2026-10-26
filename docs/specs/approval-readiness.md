# READINESS-1.0 - approval eligibility separate from AI proposal and human decision

User approved implementation and refinements on 2026-10-24. No paid model or SEC
requests during validation. Integrate the deterministic gate inside route_review;
no new model call/node, altered fixture, threshold, source or historical event.

Store ai_proposal (exact original wire plus source reference), approval_readiness
(versioned assessment), and human_decision separately. Readiness outcomes: Ready
for Human Decision; Pending Review; Additional Information Required; Exception
Review Required; Recovery Required. Only the first is approval eligible. An AI
Approve or Low risk cannot satisfy any missing prerequisite. Reject is not derived
from readiness; independently supported rejection paths retain existing guards.

Requirements cover mandatory usable financial calculations, covenant coverage and
each covenant's applicability, timing, due date, evidence and compliance result,
applicable policy/control checks, current semantic evidence verification and open
critical exceptions. Unknown is not not-applicable. Future obligations with reviewed
applicability, explicit source-backed timing/due date and Not yet due status do not
need future fulfilment now; unknown timing remains Pending, never auto-breached.
Use the explicit deal review-as-of date; no expiry or host-clock-based reassessment.

Assessments bind scope, input revision, exact analysis/source basis, evaluated
requirements, blockers/evidence, allowed next actions, version, assessment digest,
UTC evaluation time and prior assessment reference. Store append-only snapshots and
an optimistic-versioned current pointer in the existing SQLite app_records. Source
or analysis changes invalidate approval eligibility. Reading is side-effect free;
legacy records without assessment are explicitly Not assessed / Pending Review.

New reports may be generated with pending readiness; they are draft review reports,
not approvals. Existing memo bytes/events/responses remain historical originals.
UI shows the same current assessment on Dashboard, Workspace, Memo and History;
new decision events freeze their actual assessment snapshot. Current UI projection
never changes an earlier human decision or fills old missing event-time readiness.

Backend approval and conditional approval require current eligible readiness plus
existing role/tier/gate permissions. Commands/resumes revalidate source/analysis and
latest assessment version; concurrency is checked with the existing transactional
record versions. Evidence/covenant review metadata does not execute models or grant
credit authority. Support records are source/target-bound, role-scoped, reasoned
and timestamped. Duplicate submissions return their original event, never another
analysis/decision. Review evaluation cannot fabricate a due date from an unqualified
annual covenant or from today's date.

Expected unchanged Standard Deal: raw proposal Approve; readiness Pending Review;
primary blocker Mandatory covenant evaluation incomplete; no human decision; next
Evaluate the annual financial-statement reporting covenant, including its
contractual timing and requirements. Its financial calculations and historical
nine-stage execution remain intact. Existing final approval tests must now supply
actual readiness prerequisites or assert the intentionally blocked approval.
