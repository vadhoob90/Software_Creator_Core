# ES-006: Secure and respectful software

**Status:** Adopted initial baseline

**Governing principle:** [P-007: Secure and respectful software](../core/development-principles.md#p-007-we-will-create-software-that-is-secure-and-respects-the-people-it-serves)

**Default enforcement:** Documented

## Purpose

Software created or governed through PDLC must protect the people,
information, systems, and relationships entrusted to it. Security, privacy,
safety, and respectful treatment are product requirements throughout design,
implementation, verification, release, and retirement.

This standard complements
[ES-005](ES-005-secure-bounded-human-governed-automation.md). ES-005 secures
agents and automation performing development work; ES-006 governs the software
that work creates.

## Applicability

This standard applies to source, configuration, data handling, interfaces,
dependencies, generated product artifacts, deployment definitions, and
operational or retirement plans for which a PDLC-governed job claims product
security evidence.

Product repositories own their domain, jurisdiction, deployment environment,
risk acceptance, and policies that specialise or tighten this baseline. Using
a PDLC definition without applying and evidencing this standard does not create
a product-security conformance claim.

## Requirements

### ES-006-01: Product security context

Before selecting controls, the product MUST identify:

- The people and organisations affected by the product.
- Intended use, foreseeable misuse, and material harm.
- Deployment and operational environment.
- Data categories, sensitivity, ownership, and movement.
- External services, identities, dependencies, and trust boundaries.
- Applicable product, contractual, legal, regulatory, and accessibility
  obligations.
- Accountable security and risk owners.

Missing context MUST remain an explicit uncertainty. A generic checklist MUST
NOT be represented as a product-specific threat assessment.

### ES-006-02: Threat and abuse analysis

Elevated and critical products or changes MUST maintain a threat model covering
assets, actors, entry points, trust boundaries, threats, abuse cases, existing
controls, and residual risk. Standard-risk work MAY use a smaller recorded
analysis.

The analysis MUST include relevant malicious use, accidental misuse,
dependency compromise, privilege escalation, data disclosure, integrity loss,
denial of service, unsafe failure, and recovery paths. Material changes to
architecture, authority, data, exposure, or deployment invalidate the affected
part of the analysis until reviewed.

### ES-006-03: Least exposure and secure design

The product MUST minimise exposed interfaces, authority, retained data,
privileged components, and trusted dependencies to what the intended outcome
requires.

Security boundaries MUST be enforced by the trusted component that owns the
decision. Client visibility, interface hiding, prompt instructions, or caller
claims MUST NOT substitute for authentication, authorisation, or server-side
validation.

Default configuration MUST be safe for its documented context. Development,
debug, test, or example settings that weaken protection MUST be visibly
separated and MUST NOT silently become production defaults.

### ES-006-04: Identity and authority

Authentication and authorisation MUST be explicit at every protected boundary.
Identity, tenant, role, and resource scope MUST be validated independently of
untrusted request parameters.

Privileges MUST be least-authority and time-bounded where practical. Sensitive
or destructive actions MUST require protection proportionate to their
consequence, including re-authentication, approval, separation of duties, or
step-up controls where applicable.

Denial MUST fail safely and MUST NOT reveal sensitive existence, identity, or
policy information unnecessarily.

### ES-006-05: Data and privacy

Every collected or generated data category MUST have a declared purpose,
access policy, retention expectation, and disposition path. The product MUST
minimise collection, access, replication, and retention.

Sensitive data MUST be protected in transit and at rest where the risk requires
it. Secrets MUST NOT be stored in source, prompts, logs, fixtures, examples,
generated artifacts, or client-delivered code.

Logging, analytics, evaluation, support, and debugging MUST respect the same
classification and purpose boundaries as primary product behaviour. Retirement
MUST account for legal holds, contractual retention, archival duties, deletion,
anonymisation, and restoration needs rather than applying one universal data
action.

### ES-006-06: Untrusted input, output, and failure

External input, uploaded or retrieved content, model output, dependency data,
and cross-system messages MUST be treated as untrusted unless a stronger basis
is established.

Inputs MUST be validated at the boundary that consumes them. Outputs MUST be
encoded or constrained for their destination. Parsers, deserializers, file
handling, command construction, rendering, and generated code MUST defend
against injection and boundary confusion appropriate to the technology.

Failures MUST preserve security invariants. Errors and diagnostics MUST be
actionable without disclosing credentials, private content, internal policy,
or exploitable implementation detail.

### ES-006-07: Dependency and release integrity

Source, dependencies, build inputs, generated code, deployment definitions,
and release workflows MUST be inventoried and attributable where material.
Dependencies MUST be pinned or resolved reproducibly where supported and
reviewed for known risk.

Release paths MUST isolate credentials, prevent unreviewed changes from gaining
publication authority, and produce provenance appropriate to the artifact.
Unsupported or vulnerable dependencies require remediation or an explicit,
time-bounded exception with compensating controls.

### ES-006-08: Respectful interaction and meaningful control

The product MUST NOT obtain agreement, disclosure, or consequential action by
deception, obscured defaults, or avoidable coercion. Material choices,
consequences, and irreversible boundaries must be understandable to the people
affected.

People MUST have proportionate ways to correct errors, withdraw from optional
processing, challenge consequential outcomes, or obtain support when the
product context requires them. Accessibility and exclusion risks MUST be
considered alongside security rather than treated as reasons to deny a usable
service without investigation.

### ES-006-09: Vulnerability, incident, and recovery readiness

Released software MUST identify how material vulnerabilities and security
reports are received, assessed, remediated, communicated, and verified.
Operational products MUST declare security-relevant signals and an accountable
response path proportionate to risk.

Recovery, credential rotation, access revocation, safe disablement, data
restoration, and integrity verification MUST be planned and tested where their
failure would be elevated or critical. PDLC may validate these artifacts when
invoked; it does not become the product's continuous incident-management
system.

### ES-006-10: Risk acceptance and evidence scope

Residual elevated or critical risk requires an accountable human decision that
identifies the affected scope, evidence, consequence, compensating controls,
review date, and remediation or retirement condition.

Security evidence MUST declare the exact product version, configuration,
environment assumptions, data scope, and assessment method. Evidence from a
different version or context MUST NOT be silently reused as current assurance.

## Required verification

### Automated controls

When implementation exists, CI and applicable product verification MUST
include proportionate:

- Static analysis, dependency, secret, and infrastructure scanning.
- Authentication, authorisation, tenant-isolation, and denied-access tests.
- Input-validation, injection, unsafe-file, and output-encoding tests.
- Sensitive-data and diagnostic-redaction tests.
- Build and release-integrity checks.
- Security regression cases for previously observed failures.
- Recovery, revocation, and safe-disablement tests for critical paths.

Tool output is evidence to review, not proof that every relevant threat was
considered. A scanner with no findings MUST NOT be treated as a complete
security assessment.

### Review controls

Reviewers MUST be able to answer:

- Does the security context describe this product and deployment rather than a
  generic system?
- Which people, assets, data, and trust boundaries can be harmed?
- Are authority and sensitive data minimised and enforced at trusted
  boundaries?
- Can untrusted input cross into code, commands, files, rendering, models, or
  privileged decisions?
- Are dependencies and the release path attributable and protected?
- Can affected people understand and challenge consequential behaviour where
  appropriate?
- Can vulnerabilities and incidents be reported, contained, recovered, and
  verified?
- Who accepted each residual elevated or critical risk, and when is it
  reviewed?

## Evidence

The evidence package must include the product security context, applicable
threat and abuse analysis, control and test results, dependency and release
evidence, unresolved findings, residual-risk decisions, recovery evidence, and
the exact scope in which the assessment is valid.

## Further reading

- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Software Assurance Maturity Model](https://owaspsamm.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
