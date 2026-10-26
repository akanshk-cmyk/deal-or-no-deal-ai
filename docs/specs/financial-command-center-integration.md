# Financial command-center integration — APP-READ-1.0

## Accepted policy-display correction — POLICY-VIEW-1.0

The user's audit-fix instruction authorizes this read-only correction. Workspace
policy cards, exception count and policy evidence use the selected run's recorded
post-synthesis final_policy when available, matching the memo. Before synthesis,
show the recorded compliance panel as preliminary; a missing result is Pending,
never Pass. Display workflow-control results separately from policy outcomes.
Bind final-policy selection to run scope, case dependency and synthesis input.
Patch only a copied evidence dictionary after exact source-packet verification;
never mutate the original request, stored artifacts, report or historical state.
When source verification fails, withhold citation buttons, including policy links.
Developer details retain the original pre-synthesis artifact with explicit labeling.
No rerun, rule recalculation, model call, financial approval or source registration
is authorized by this display fix. Financial HITL, fulfilment and additional cases
remain separately unfinished implementation work.

Presentation update: the user's [V2 redesign](../design/redesign-v2.md) now groups
run records by deal, retains selection across destinations and renders Workspace
tabs/evidence, activity cards, memo framing and a separate business-decision empty
state. The root history no longer repeats every technical stage event; Activity
owns that log. Read-model, financial and provenance boundaries below are unchanged.

Authorized by the user's 2026-10-24 instruction to fix frontend/backend alignment.
This refines SPEC-010/013; it adds no financial rule, model call or database schema.

The root Streamlit app exposes six destinations over the existing SQLite records:
Dashboard, New Deal, Review Workspace, Agent Activity, Credit Memo, Decision History.
The implemented financial path is E-N01/default FIXTURE only. New Deal explicitly
starts that registered case; arbitrary uploads remain unavailable rather than
silently being treated as this case. All reads are side-effect free, including an
empty workspace. Starting a run is an explicit Analyst action with a session-held
operation UUID; retrying that UUID uses worker admission/idempotency.

One read service checks workspace and allowed deal scope before reading a run.
It joins context, outcome, progress, execution claim and original stage artifacts
in one SQLite read transaction. Busy/uncertain claims override stale RUNNING
labels. Artifacts must match their digests and execution scope. Citations resolve
from the exact registered packet only when its dependency/input digests match the
recorded run; changed or absent sources produce an explicit unavailable state.
Never rebuild historical findings from latest source values.

Dashboard shows execution status, not human credit approval. Workspace separates
authored credit risk, policy exceptions, evidence support and AI recommendation.
Source, calculation, policy and assessment references are selectable; show original
page/version/body and dependency links. Agent Activity shows recorded events only.
Memo reads the stored markdown, without regeneration or additional model calls.
Decision History shows financial execution events separately from credit decisions;
no human decision is inferred from a generated report. Legacy event timestamps are
Not captured; do not backfill generation time as event time.

The existing illustrative role-action/history preview remains a separate tool and
never accepts financial records. Financial interrupt/resume, evidence fulfilment,
Conditional review and additional registered cases remain explicit prerequisites,
not buttons that simulate completion. Live remains disabled pending provider and
spending checks. These are outstanding implementation tasks, not a request to
invent missing lending policy or approve paid calls.

Acceptance: empty navigation writes no database; one explicit E-N01 start reaches
all six screens; reload does not dispatch; out-of-scope reads fail; source changes
withhold citations; uncertain execution is not completed/approved; memo and events
match the original worker output. Offline tests prohibit outbound network.
