# Live token-fit proposal â€” approved live-only profile

Measured with Qwen/Qwen3-30B-A3B-Instruct-2507 tokenizer revision
0d7cf23991f47feeb3a57ecb4c9cee8ea4a17bfe; provider chat/schema overhead is not yet
verified. These are actual local component counts, not billed provider usage.

| Packet | Existing cap | Original components | Proposed compact components |
|---|---:|---:|---:|
| Extraction | 3000 input |6791|3699|
| Synthesis |1500 input|8118|2282|

Both existing packets exceed limits. Even proposed packets exceed the existing
stage allocations. User approved the compact live profile. Its separate runtime prompts and stage allocations are implemented; no paid dispatch has run.

Concrete proposal:
- Live-only extraction input4000/output1000; synthesis input2500/output650.
- Normal maximum6500 input/1650 output plus protected correction1500/350 fits the
  unchanged aggregate8000/2000. Other20-node/12-tool/5-attempt/180-second/45-second/
  USD0.25 review limits and shared USD0.10 approved spend remain unchanged.
- Shorter, separately versioned Live prompts, not changes to historical Fixture
  prompts/registrations. Exact approved text: docs/agents/live-extractor.md and live-synthesizer.md; builder: src/deal_or_no_deal_ai/live_context.py.
- Preserve every original page text/handle; original source metadata stays in the
  local source dictionary. Retain financial/policy rows with shared column headers
  and exact refs; remove duplicated reference lists. Full applicability/results stay.
- Strip schema annotations and alias internal $defs names, preserving wire field
  names and validation constraints. Python still validates the full original schema.
- Retained candidates: var/evaluations/live-compaction-proposal/packets.json and
  measurement.json. These are approved offline packets, not dispatched provider requests.

Local components leave301 extraction and218 synthesis tokens for rendering overhead.
This is not a guarantee: verify selected hosted model, structured-output behavior,
whole-request accounting, current rates and actual response usage before a full
paid journey. Stop on overflow/truncation/unknown usage, no hidden fallback/retry.
Prompt semantic equivalence and live quality remain unverified. Critical fact and
narrative human support still precede trusted calculation/report; budget approval
does not bypass them or complete general uploaded-deal admission.

## Executed verification

After applying the approved profile, 27 focused tests and 3 subtests passed, covering provider limits, compact schema constraints, source preservation, allowance handling, readiness UI, retrieval/native RAGAS ID metrics and normal Fixture graph. Four RAGAS public-API deprecation warnings remain under the pinned version. Earlier dependency regression: 246 tests and 269 subtests passed; a separate readiness UI test also passed. These tests do not represent paid calls or live model-quality results.
