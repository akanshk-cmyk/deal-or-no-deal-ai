# Uploaded financial evidence review — UPLOAD-FACT-1.0

Authorized next step after UPLOAD-1.0. Implements the existing FACT-SUPPORT-1.0
human evidence-check pattern for uploaded candidates, without enabling Live or
financial case registration. Reuse one SQLite/admission, existing money/FIN-1.0
arithmetic, native UI forms and exact retained page citations. No new dependency.

Bounded initial fields: annual CFADS, annual principal and annual interest, the
existing CALC-004 inputs. Analyst proposes a value with exact original quote/span,
raw numeric token/label, USD/source scale, subject/facility, annual period and
actual/projection basis, source unit label, and reason. Source numeric normalization
uses Decimal and explicit1/1000/1000000 scale. Reference/quote/token/label/unit
presence is mechanical only, never semantic approval. Dates/subject/facility may
need human interpretation; do not require naive exact string matching for them.

RiskManager alone records HUMAN_SUPPORTED, UNSUPPORTED or WITHHELD against the
exact current candidate digest and package/page/basis. Required independent checks:
reference, row/label, normalized value, units/scale, period, subject/facility and
debt-service scope. Support requires all checks and nonblank reason. Names are
simulated; this is not independent authenticated banking validation. No model result
is created: candidates are REVIEWER_PROVIDED, purpose UPLOAD_CANDIDATE_ONLY.

Append immutable application event records (local SQLite is not tamper-proof),
with role/reason/UTC/operation and current-version concurrency/idempotency guards.
Revisions preserve original proposals/assessments. Replacing any candidate makes
previous support ineligible; old receipt cannot support a new value/source/basis.
Read revalidates retained sources, exact span/normalization and current receipts.
No automatic expiration, deletion or policy change.

Read-only annual DSCR preview is Unknown until all three latest candidates are
HUMAN_SUPPORTED and subject/facility/annual dates/actual-vs-projection/currency match.
Use existing CALC-004 Decimal calculation; zero/negative service denominator remains
Not meaningful, not zero risk. Preview reflects only supplied annual inputs, not
full-term repayment adequacy. Recompute locally from current supported records;
no cached stale ratio, score, policy result, AI decision or credit approval.

UI remains on New Deal/Upload, beside original page evidence: proposals, RiskManager
review controls, per-field state, missing/incompatible blockers and preserved
history. Financial Run stays disabled. General extraction, all other critical
facts, complete source-authority/subject registry, source amendments/currentness,
new-fact graph admission, factor onboarding and Nebius remain separate next work.

Tests: proposal normalization/citation guards; wrong roles/scope, missing checks,
stale/duplicate/competing commands; new proposal invalidates support/preview; missing,
withheld, incompatible basis/subjects, zero service; changed source; exact event
lineage and UI handoff. Synthetic only. No fixture-value borrowing or paid calls.
