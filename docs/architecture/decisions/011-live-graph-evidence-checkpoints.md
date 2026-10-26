# ADR-011 - Shared live graph with explicit evidence checkpoints

Status: implemented under the user's LIVE-GRAPH-1.0 request, 2026-10-24.

Decision: keep build_graph and existing deterministic services, one SQLite database,
durable admission and cumulative ledger. Add a live branch and source-bound
ReviewedLiveCase; never replace a model response with an expected sample answer or
change registration hashes to make it match. The paid transport accepts the
worker's held claim rather than attempting a conflicting nested admission.

Freeze each exact paid request without credentials before dispatch, in the same
transaction as spending reservation. Preserve original response, schema validation
outcome, reported usage and verified-rate cost separately from human support.
Unknown dispatch retains its maximum reservation and requires explicit recovery.

Pause on extraction facts, generated narrative, and applicable credit review through
real interrupts/checkpoints. Seven source/value/basis checks are explicit; generated
narrative is conservatively mixed-domain in this bounded first live slice, so both
existing RiskManager and ComplianceOfficer support are required. Support has no
credit authority and never dispatches. Analyst continuation is explicit. A changed
request needing token/provider verification pauses before dispatch and exposes an
exact prepared packet, without resetting allowances or causing technical recovery.

Trade-offs: more human clicks for this small educational example, in exchange for
visible support boundaries without an additional semantic judge or model call.
Only E-N01's registered fictional source profile is admitted. General live source
correction, unhandled exceptions/conditions, arbitrary uploads and production
identity/governance remain outside this slice. Provider execution/quality and
LLM-based RAGAS require separate actual evidence; mocked tests prove wiring only.
