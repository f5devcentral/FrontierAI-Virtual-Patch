# Changelog

All notable changes to virtual-patch-copilot are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project aims to follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] — 2026-09-08

The hybrid-fabric release: the band-aid stops being an F5 Distributed Cloud feature and becomes a
property of the finding. The same declarative policy now applies, validates and retires on
**BIG-IP Advanced WAF** and **F5 WAF for NGINX (App Protect)** as well as XC — three enforcement
points, every form proven against a real exploit on real appliances.

### Added
- **BIG-IP Advanced WAF as a live enforcement point.** Apply and retire a band-aid on your own
  appliance behind the same human gate, with all three forms proven on a live BIG-IP:
  `service_policy` (value constraint), `waf_data_guard` (response masking) and `api_schema`
  (API contract). The reconcile loop auto-retires an AWAF band-aid once the cure lands, and the
  console routes both Mitigate and Retire to the appliance.
- **F5 WAF for NGINX (App Protect) as a third enforcement point** — the same apply / validate /
  retire spine, the same three forms, all live-proven, wired through the CLI, the console, the
  report and reconcile. `vpcopilot nginx-lab create` stands up the guarded vhost.
- **Named sessions** in the console: an explicit, switchable scan workspace instead of one
  implicit output directory, reachable by agents as well as by the UI.
- **A global live-band-aid inventory**, keyed by load balancer and finding id, separate from
  per-session scan artifacts — so reconcile and retire read infrastructure state rather than
  whichever scan happened to run last, and a reused slug can no longer orphan a live band-aid.
- **NGINX connection fields in ⚙ Setup**, which the console had been missing.
- **Generated flow diagrams** (`docs/images/flow-*.svg`, sources in `docs/images/src/`) covering
  the agent pipeline, the four-act story, and the control-plane / data-plane view.

### Changed
- **The F5 logo is gone from every UI surface** — the console header and the standalone HTML
  report now carry a neutral product mark instead. The report stays a single self-contained file
  with no external resource loads; the mark is inline SVG rather than an embedded PNG.
- Honest declines are surfaced, not hidden: where a control has no declarative-WAF equivalent
  (`rate_limit`, `malicious_user`, `bot_defense`) or cannot work as a virtual patch (`waf` — ASM
  and App Protect both hold freshly-imported signatures in staging), the console and the report
  say so and say why, per enforcement point.
- The console hero band reflects the operator's own scan rather than a tenant-wide dashboard.
- Docs: `docs/NGINX.md` is new, `docs/BIGIP.md` covers all three forms, and `README` / `TRY_IT`
  describe the hybrid fabric.

### Fixed
- A leak-only probe now passes through validation, so `waf_data_guard` can auto-retire.
- A rejected NGINX config is reported as a box error instead of a fake successful dry-run.
- Live-spike hardening on BIG-IP: clean-slate-first apply, an honest `auth_failed` outcome, and
  a declined staged-signature policy instead of one that looks applied and blocks nothing.

### Security
- Scrubbed live-estate identifiers and PII from the repository ahead of public release.

## [0.2.0] — 2026-08-18

The scan-everything / mitigate-everywhere release: three new discovery inputs, the reconcile
and drift loops, an evidence/audit spine, MCP + CI surfaces, a declarative-WAF emitter, and a
full ops console — hardened by a security- and correctness-focused quality pass.

### Added
- **Discovery inputs beyond a repo:** a CVE / advisory id (H1, via OSV.dev), dependency
  manifests (H2 — `requirements.txt`, `package-lock.json`, `pom.xml`, …), and an OpenAPI/Swagger
  spec (H3, which also reports spec-vs-code drift alongside a repo scan).
- **Reconcile & drift:** patch-expiry and the reconcile loop that retires a band-aid once the
  code fix lands (I1), and pre-apply drift/conflict detection (I2).
- **Evidence & audit:** every LB change is attributed and exportable as evidence (F3); an
  optional off-box audit event sink (J3); attribution backfill (J4); an optional detached
  minisign signature over the evidence bundle (J1) with `export --verify` (J2); and CWE/OWASP
  weakness mapping stamped by code, never by a model (J5).
- **New surfaces:** an MCP server mode (K1) and a CI action that scans a pull request's diff and
  comments the band-aid (K2).
- **Enforcement reach:** a declarative WAF policy emitter — one finding, every enforcement point,
  consumed by both BIG-IP Advanced WAF and NGINX App Protect (L1) — and `vpcopilot bigip-lab`
  create/teardown with the Larkspur origin for validation (L2).
- **Quality of mitigation:** shadow simulation of a band-aid's blast radius before it is applied
  (G2), a refine loop that gates on blast radius (G3), a four-way model scorecard, and a Gemini
  provider config (G4).
- **Authenticated probing** for auth-protected apps — a flagged 401 baseline and an `auth_failed`
  outcome instead of a false "unprotected" reading.
- **Ops console:** full scan transcript, the HTML report on Review and the audit trail on Retire
  (F1–F3), a benchmark dashboard, and an official **F5 brand reskin** (logo, colors, Aptos type).

### Changed
- **Simpler everyday console:** progressive disclosure across Scan, Run settings, Setup, and
  Review; the ⑦ Benchmark step and the header model switcher are model-evaluation tools now gated
  behind advanced mode (`VPCOPILOT_ADVANCED`, or more than one `config/agents*.yaml`).
- **Packaging:** the sdist ships only `src/`, `config/`, `docs/`, and metadata — never the
  benchmark/infra/lab/demo scaffolding; `config/agents.yaml` is bundled in the wheel with a
  package-relative fallback so a pip install has its per-agent model registry.

### Fixed
- Everyday-user crashes and silent failures: a malformed OpenAPI spec or an unknown/offline CVE
  now returns a clean error, not a traceback; a total discover/provider failure hard-fails instead
  of writing a clean exit-0 "0 findings" summary; `apply-waf` explains a missing `--template`
  instead of crashing on a real tenant; `lab-create` validates the origin `host:port`.
- Reconcile can retire an auth-protected origin (its health check no longer rejects the 401 a real
  app returns) and treats 5xx as unhealthy.
- Console: the results page no longer 500s on a mid-write read and no longer hangs on a stuck job;
  a concurrent scan can't repoint an in-flight job's run directory.
- Reporting honesty (numbers that told the operator something untrue), five console/worker
  concurrency races, spec-vs-code comparison, and normalization that widened an exact-path DENY.

### Security
- Closed a protected-LB / protected-policy **guard bypass** on the default apply/Mitigate path —
  the check now runs through the hardened `guard_lb` with name validation and a case-insensitive
  compare, and an override is audited.
- Guarded the MCP `drift` tool against a caller-supplied **path traversal**.
- Neutralized **spreadsheet formula injection** in the audit CSV export.
- Dropped the `lab.example.com` **default `--url`** (an estate leak and a footgun that pointed
  a customer's probes at a third-party host) — driven from `VPCOPILOT_DEFAULT_URL` instead.
- Credential-redaction hardening, and a broader `.gitignore` for `.env*` and scratch files.

## [0.1.0] — 2026-07-12

First public release.

[0.3.0]: https://github.com/henleda/virtual-patch-copilot/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/henleda/virtual-patch-copilot/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/henleda/virtual-patch-copilot/releases/tag/v0.1.0
