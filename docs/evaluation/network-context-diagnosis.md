# Repeated live-start failure: network context

Observed read-only diagnosis: Nebius GET /v1/models from the restricted command
runtime failed with URLError. The same check outside that sandbox, explicitly
approved by the user, returned HTTP200 and listed the selected
Qwen/Qwen3-30B-A3B-Instruct-2507 model. No generation or embedding calls ran.
This establishes working credentials/model-list access outside the sandbox;
it does not prove a new generation response or complete live recommendation.

Prior local Streamlit servers were launched in the restricted runtime. An
approved fresh server was started outside it at http://127.0.0.1:8506, loopback
only, headless, telemetry disabled. Health check returned HTTP200 ok. Use this
instance, not earlier ports. Do not launch the provider-connected demo from a
network-denied sandbox; repeated isolation alone does not fix connectivity.

Under the user's continuing instruction to clear demo execution blocks, exact
operation 1d478574-1e3d-426c-bfe5-622b75872e79 was isolated using current identity/
version checks and preserved unknown USD0.0007 reservation and records. Replay
remains forbidden. Evidence: var/evaluations/network-blocked-sample-isolation.json.
Ten offline recovery regressions passed. No paid retry, billing reconciliation,
human evidence support or credit decision was performed.

Limitation: the original exception details were not retained by the transport,
so the failed paid request's exact HTTP/network outcome cannot be reconstructed.
Network context is the directly observed environmental defect, not proof of
the processing/billing status of any prior request.
