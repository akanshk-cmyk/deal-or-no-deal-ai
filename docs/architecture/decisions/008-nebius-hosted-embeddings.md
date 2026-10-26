# ADR-008: Nebius-hosted embeddings for the reference corpus

Date: 2026-10-23
Status: Accepted provider and Qwen3-Embedding-8B selection; runtime contract and paid execution pending
Supersedes: ADR-007's local BGE embedding choice only

## Decision and user authority

The user selected “Nebius-hosted embeddings to avoid running a model on computer.” Use Nebius for reference-document and query embeddings. Do not download or load BGE weights, run sentence-transformers/PyTorch for embeddings, or fall back to another provider. The earlier local-library installation and rejected weight-download request remain historical observations, not runtime requirements.

Keep LOCAL_FILE intake, separate source profiles, source/date/corpus isolation, citation-bearing parent/child passages, app-owned SQLite exact cosine storage with at most 500 children, and the DIRECT/KEYWORD/VECTOR/HYBRID comparison. DIRECT remains the loan baseline. No Pinecone, extra agent, reranker, database or deployment is introduced.

The user subsequently approved Qwen/Qwen3-Embedding-8B after reviewing its availability and pricing. The [official Nebius model catalog](https://tokenfactory.nebius.com/api/public/models_info), checked on 2026-10-23, lists it active, with 4096 embedding dimensions, USD0.01 per million input tokens and USD0 output-token charge. These are catalog observations, not measured API compatibility, latency or a guaranteed future rate. Selection requires no repeat approval. Retain this dated rate observation; later actual usage must reconcile against the applicable provider rate.

Input limits need verification: the catalog tags say32K but max_model_len is40960, while the [upstream model card](https://huggingface.co/Qwen/Qwen3-Embedding-8B) states32K. Do not treat either as a verified deployed full-input limit or silently truncate. max_input_tokens and token_count_strategy remain unconfigured, as do the exact request/batch contract, deployment revision, usage accounting and data handling. Do not inherit BGE's384 dimensions,512-token ceiling, tokenizer or query instruction. Embedding execution and indexing stay disabled; catalog selection alone supplies no paid allowance.

## Implementation contract: NEBIUS-EMBEDDING-1.1

The disabled configuration now pins model_id=Qwen/Qwen3-Embedding-8B and catalog dimensions=4096, with catalog-only capability status and dated USD input/output rates. It still rejects activation, arbitrary model swaps, inherited BGE dimensions/token limits and an approved-budget flag. This is model selection metadata, not an executable provider adapter. Existing profile hashes change with this configuration; preserve prior observations without relabeling them.

Before a real request, record an available model/deployment identity, documented request/response contract, input preprocessing and query/document prefixes, tokenizer/counting method, dimensions, normalization, input/batch limits, pricing unit/rate/date, usage reporting, timeout/retry behavior and data handling. If an immutable provider revision is unavailable, record that limitation and actual observed model metadata; do not claim reproducibility that the service cannot guarantee.

Retain SEG-1.0 structural parents and REF-SEG-1.0 original-span/dependency coverage. Approximately 400 body tokens and 50 within-parent overlap remain provisional targets, conditional on the verified hosted tokenizer and full-input allowance. Count headings, prefixes and special tokens; reject overflows instead of truncating. Structural preparation can proceed offline, but fake counts do not establish provider-valid chunks. A tokenizer-only local artifact may be considered if needed and explicitly documented; no local embedding model is required. If exact counting is unavailable, leave final embedding admission blocked rather than assuming a character estimate proves fit.

Implement a lazy, explicitly invoked adapter in the planned embeddings.py module after the model contract is verified. Imports, inspection, refresh, citation viewing and notebook graph rendering make zero requests and do not read secrets. Later credentials use the existing local secret interface; never commit them or print source text, raw queries, headers or response bodies in ordinary diagnostics. Send only selected synthetic or permitted public-reference passages after source admission, never manual-review/gold answers or real confidential borrower material.

Use a separate explicitly approved REFERENCE_EMBEDDING allowance for corpus setup and isolated retrieval benchmarks, with bounded input tokens, requests, retries, wall time and dollars fixed before execution. No numerical budget is invented by this decision. Review-time embedding work must also fit the existing review ledger and unchanged hard caps; two normal generation tasks do not mean only two total provider requests. Reserve/reconcile embedding charges separately from generation, including cache misses, batch failures and uncertain outcomes. Do not auto-retry uncertain paid requests or silently fall back after failure. Offline RAGAS retains its separate allowance.

Reuse vectors only for exact text/preprocessing/model/deployment configuration identity, with independent source provenance and eligibility. Reuse the same query embedding between VECTOR and HYBRID in a paired run. Any model/preprocessing/dimension change requires a separate complete build and document re-embedding; never mix old/new vectors even when dimensions match. Validate vector count, ordering, dimensions, finite values and normalization. Preserve the last complete build and failed-build history on timeout or partial response; no automatic expiry.

## Validation and remaining decisions

Offline configuration/control tests must prove disabled-by-default behavior, rejection of old local-model settings, no network/model/client/database work on inspection/import, and unchanged source isolation. Future adapter tests cover malformed/partial responses, mismatched dimensions, nonfinite/zero vectors, denied budget, rate limits, timeout/uncertain outcomes, cache identity and failed-build activation. These tests do not establish real retrieval quality.

After credentials and a concrete paid allowance are supplied, use a small synthetic smoke test to verify the actual contract and usage, then prepare the selected source and run the same frozen four-arm retrieval benchmark. Record candidate recall/precision, citation/qualification coverage, actual cold/warm latency and embedding tokens/requests/cost separately from generation and RAGAS. No real embeddings, index, benchmark or savings have been measured by this decision.

Trade-off: removes local model-weight setup and inference load, while adding network latency, provider availability, usage charges and external processing. Model choice and dated catalog rates are recorded; the runtime contract, concrete paid allowance and data handling remain open. Do not request the API key during this documentation/configuration change.
