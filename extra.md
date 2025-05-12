Route 1 – Executive Summarizer
Step	What happens in this step
1. Receive request	Client calls /executive-summary with an xor_id. This ID is the only input and triggers the flow.
2. Retrieve incident data	Use the xor_id to call your internal Incident-Data API and pull the full raw incident record. Handle timeouts / retries here.
3. Format data for the model	• Strip fields the model doesn’t need.
• Normalize dates, redact sensitive items, and convert codes to human-readable text.
• Assemble the cleaned information into a prompt-ready block.
4. Generate executive summary	Insert the cleaned block into the Executive-level prompt template and send it to the LLM. Wait for the model to return its summary.
5. Return response	Wrap the model’s text in the standard JSON schema—e.g., `{ "summary": "…"} — and send the HTTP 200 response back to the caller.

Route 2 – Stream File Summarizer
Step	What happens in this step
1. Receive request	Client calls /stream-summary with a case_id. This starts the stream-file flow.
2. Retrieve case metadata	Call the Case-Metadata API with case_id to learn which artefact type is attached (email or stream file).
3. Classify and route	• If type = email → hand off to the (future) Email Summarizer module (placeholder).
• If type = stream file → continue to Step 4.
4.1 Download file	Fetch the artefact via /original-message/{case_id} and store it in a temp location.
4.2 Check archive status	Inspect the file header to decide whether it is readable & unzipped or a ZIP archive.
4.3 If readable & unzipped	• Parse headers, body, and any embedded items.
• Run the existing content-analysis workflow.
• Produce a text summary block.
• Proceed to Step 5.
4.4 If ZIP archive	Follow the numbered sub-steps below:
** 4.4.1 Unzip contents**	Extract every entry into a temp directory.
** 4.4.2 Iterate entries**	For each file inside the ZIP, read its contents to text.
** 4.4.3 Aggregate text**	Build a single document that pairs each filename with its content, line by line.
** 4.4.4 Build prompt**	Embed the aggregated text into the Stream-file prompt template.
** 4.4.5 Generate summary**	Send the prompt to the LLM and capture its output.
** 4.4.6 Clean up**	Delete temp files and close the ZIP branch.
5. Return response	Whether from 4.3 or 4.4.5, wrap the model output as { "stream_summary": "…"} and return it to the caller.


“Must-have” unit-test checklist for the entire project

This list trims each module down to the single most critical test you need to guarantee that the whole service behaves, stays secure, and doesn’t blow up resources. If these pass, the API can function; everything else is “nice to have.”
Module / Function	Essential test	What it proves
1. ID validators (xor_id, case_id)	Valid input accepted, missing / malformed rejected	No bad request reaches downstream code.
2. Incident-data fetcher	200 → payload OK, 404 → raises “not found”	Core happy path works and the service fails fast on an unknown incident.
3. Incident-data transformer	Given the sample raw payload, returns only the whitelisted, normalised fields	Model never sees junk or un-normalised data.
4. Executive-prompt builder	Fills every placeholder in the template when all fields are present	Guarantees your executive prompt is syntactically correct.
5. LLM client wrapper (shared)	On success returns text; on 429 error converts to clean application error	One test covers model success and model failure for both routes.
6. Case-metadata fetcher	type="stream" returns correct dict; HTTP error raises “case not found”	Stream path can be taken or rejected cleanly.
7. Stream-file downloader	On HTTP 200 saves file; on 500 raises “download failed”	Protects the heavy file-handling pipeline.
8. ZIP / non-ZIP discriminator	Correctly returns True for a real ZIP and False for a plain log	Downstream logic branches correctly.
9. Unzip → iterate → aggregate (see previous answer)	Happy-path aggregation with two small text files returns the expected --- filename --- block	Confirms the most complex inner function actually works.
10. Stream-prompt builder	Embeds the aggregated text and produces a prompt under the model’s token limit	Ensures you never send an over-sized or malformed prompt.
11. Response formatter (shared)	Given "OK" text, returns HTTP-ready JSON { "summary": "OK" } or { "stream_summary": "OK" }	Final API output is always valid JSON.
12. Temp-directory cleanup	After any successful aggregation call, the request’s temp directory is deleted	Prevents disk leaks across many requests.

Architectural considerations to round out the design
Area	Why it matters	Key questions & options
1. Scalability & workload isolation	Both endpoints can be CPU-/I/O-heavy (large ZIPs, LLM latency).	• Async worker pool vs. blocking HTTP thread.
• Separate background queue for ZIP flows; return a job-ID if SLA is tight.
• Horizontally scale workers behind a load balancer; pin long-running jobs to dedicated nodes.
2. Token & cost budgeting	LLM charges and context limits are hard ceilings.	• Impose a token budget per request; hierarchically summarise or chunk when over budget.
• Cache summaries keyed by xor_id/case_id to avoid repeat calls.
3. Temp-file management & storage tiering	Large archives can flood /tmp.	• Mount a fast ephemeral volume (tmpfs or SSD) with a strict quota.
• Auto-purge on shutdown; add periodic janitor job.
4. Security hardening	Handling untrusted files and PII.	• Run extraction in a sandbox (container or chroot) with no network and least privileges.
• Pass files through AV/malware scan before reading.
• Encrypt temp disks if incident data is sensitive.
5. Authentication & authorization	Prevent open endpoints from being abused.	• Front the API with an API gateway or service mesh (JWT/OAuth).
• Rate-limit by client ID.
• Log every request & summary for audit.
6. Observability & SLOs	You’ll need insight when things go slow or fail.	• Expose metrics: total requests, average LLM latency, ZIP bytes processed, error counts.
• Distributed tracing: attach a trace-ID through every downstream call.
7. Error handling & fallbacks	External services (LLM, data APIs) will fail.	• Tiered retry with exponential back-off.
• Configurable circuit breaker around the LLM.
• Optional fallback to a smaller local model for “good-enough” summaries.
8. Prompt-template versioning	Prompt tweaks can break output format.	• Store templates in git with explicit version tags; include version in every prompt so you can correlate failures.
9. Compliance & data retention	Especially critical in a cybersecurity context.	• Define a max retention window for raw artefacts and summaries.
• Mask or hash personal identifiers before logging.
• Document a GDPR/CCPA deletion workflow.
10. CI/CD & environment parity	Reduce “works on my machine” surprises.	• Containerise workers with pinned library versions.
• Use IaC (Terraform, Helm) to spin identical dev/stage/prod stacks.
• Run unit + integration tests in the pipeline; block merges on coverage regressions.
11. Cost management	LLM usage and storage grow quickly.	• Monitor per-endpoint cost (tokens × price).
• Auto-scale down after hours; queue low-priority jobs.
12. Future extensibility	Email path, new artefact types, or new LLMs.	• Keep summariser modules plug-in based (strategy pattern).
• Abstract LLM client so you can swap OpenAI ↔ Anthropic ↔ local model.



Zip file consideration

1 . oversize content	Attackers can craft archives whose uncompressed size is gigabytes even though the ZIP is only a few KB (“compression bombs”). Legitimate cases can also include thousands of log shards. Both blow up memory, disk, and LLM-token budgets.	• Check the compressed and projected uncompressed size before extraction.
• Impose a hard limit on total bytes and file-count; refuse or truncate above the threshold.
• Stream or chunk large text into incremental summaries instead of one huge prompt.
2 . Path-traversal (“Zip-Slip”)	Malicious filenames such as ../../../etc/passwd can overwrite files outside your temp directory.	• Strip directory components or use safe extract libraries that normalize paths.
• Extract into a sandbox directory mounted with least privileges.
3 . Binary & non-text files	Many attachments are PDFs, images, docs, or proprietary binaries. Dumping them as raw bytes pollutes the prompt and wastes tokens.	• Detect MIME type / magic bytes.
• Skip non-text, or run OCR/text-extraction for types you truly need (e.g., PDF → text).
• Insert placeholders like [binary attachment <name> skipped] so the summary still notes their presence.
4 . Encoding mess	Different files may use UTF-8, UTF-16, ISO-8859-1, etc. Naïve .read() calls can crash or mangle text.	• Detect encoding (chardet/charset-normalizer).
• Decode gracefully with fallback and flag undecodable files.
5 . Nested archives	ZIPs inside ZIPs (or tar.gz) create infinite loops or explode file counts.	• Recursion depth limit (e.g., max 1 nested level).
• Apply the same size caps at each recursion.
6 . Malware execution risk	Merely reading a file is usually safe, but some libraries auto-process (e.g., image metadata parsing) and have CVEs.	• Use minimal safe file-read APIs.
• Ensure no external helpers (LibreOffice, ImageMagick) are invoked without sandboxing.
7 . Temp-file cleanup & concurrency	High-throughput workers can leave GBs of temp data or collide on directory names.	• Generate unique per-request temp dirs.
• try/finally cleanup or OS-level tmpdir auto-delete.
• Monitor disk usage & set retention policies.
8 . Prompt-size explosion	Even after filtering, text may exceed the LLM context window.	• Pre-summarize each file to a fixed token budget before concatenation.
• Use hierarchical summarization (file-level ⟶ bundle-level).
9 . PII / sensitive leakage	Raw files might hold credentials, client names, etc.	• Run redaction or classification passes before feeding to the model.
• Mask obvious patterns (e-mail, credit-card, SIN) with [REDACTED].
10 . Performance & SLA impact	Large archives can make a single API call run for minutes, breaking your latency guarantees.	• Enforce timeouts on each phase (download, unzip, read, LLM).
• Off-load heavy jobs to an async/background worker and return a job-ID to the caller if real-time isn’t feasible.
