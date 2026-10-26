# Review-mode layout consistency — 2026-10-25

Current unified experience (2026-10-25): [approved contract](../specs/unified-review-experience.md).
One Run AI Deal Review action uses config/app.toml mode; saved and live records
share the existing saved UI. Earlier sidebar mode and separate layout descriptions
are historical. Live interrupts, source labels and backend authority remain intact.

Scope: a presentation improvement over existing saved and live workflows. No
business rules, provider calls, graph edges, permissions, data migrations or
dependencies are added by this change.

Both modes use the existing six destinations, shared deal context card and
workspace tab names: Overview, Extracted Terms, Financial Analysis, Compliance,
Risk Assessment and Human Review. The answer-source badge identifies saved
answers or Live AI response / Nebius. Source text, original page and version
remain available while live facts and conclusions are reviewed.

Live review checkpoints appear under Human Review; Overview states the next
required role and action. Missing upstream results have explicit empty states.
The workspace uses the existing analysis / evidence two-column proportions.
Risk, policy exceptions and evidence checks remain separate assessments.

The bounded live mode currently supports only Standard Deal. It shows one deal
with earlier execution attempts under Review History, defaulting to the latest
when there is no explicit selection. Saved/live selections use separate session
keys. The live dashboard groups attempts by deal and shows recorded status and
next action. Credit memos reuse the bordered memo presentation and download label.

Mode-specific capabilities remain explicit: saved mode supports its registered
examples and upload inspection; live mode supports its bounded registered
Standard Deal, actual generation, fact review and narrative review. This change
does not claim that every supported action is identical in both modes.

New Deal follow-up: both modes now expose Sample Deal / Upload New Deal, a
scenario selector, the same shared three-step registered package preview and
document checklist, an explicit Run action and a separate-run action. Live mode
offers only its supported Standard Deal; uploads reuse existing inspection and
cannot start unregistered live analysis. Preparation and browsing make no model
calls. Start results distinguish completed (success), paused (warning), and
recovery/invalid output (error); a recovery state never receives a success notice.
After an explicit attempt, both modes provide workspace, memo and activity links.

The additional offline AppTest verifies matching preview cards, both live intake
choices, zero requests while browsing, one mocked request on explicit start,
paused-state warnings, recovery errors and absence of false success messages.

Viewing, navigation and mode switching must not dispatch model requests, support
evidence or resume a graph. Existing role checks, required quotations, comments,
approval readiness and explicit Continue buttons remain authoritative.

Validation uses offline Streamlit AppTest and mocked provider transport. Check
all six live pages, mode switching, fact-review submission, narrative pause,
completed memo and existing saved-mode presentation regressions. No paid or SEC
requests are needed. AppTest checks do not establish pixel-level browser fidelity.

Observed validation: 27 existing focused live-graph, command-center and
recommendation tests passed; both new layout/history regression tests passed.
The extended existing live UI navigation/evidence test also passed separately
after the final presentation edits. All provider responses in these checks were
mocked. No actual model call or personal review record was changed by validation.
