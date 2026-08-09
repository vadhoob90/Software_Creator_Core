# ES-005: Secure, bounded, and human-governed automation

**Status:** Adopted initial baseline  
**Governing principle:** [Automation is secure, bounded, and human-governed](../core/development-principles.md#5-automation-is-secure-bounded-and-human-governed)  
**Default enforcement:** Documented

## Purpose

Agents and automated workflows must operate within explicit authority, bounded resources, and defined human-control points. Security, privacy, and safety are lifecycle requirements. Capability never implies permission.

## Applicability

This standard applies to agents, routing and orchestration, tool definitions, model and provider calls, prompts and retrieved context, memory, credentials, external side effects, execution environments, build and release automation, and inter-agent communication.

## Requirements

### ES-005-01: Capability and authority declarations

Every agent or automated job MUST declare:

- Its purpose and permitted outcomes.
- Required inputs and trusted sources.
- Tools and capabilities it may request.
- Filesystem, network, credential, data, and tenant scope.
- Decisions it may make autonomously.
- Actions requiring approval.
- Prohibited actions.
- Resource and execution limits.
- Escalation and termination conditions.

Authority MUST be granted for the current job and scope. An agent MUST NOT infer authority from tool availability, prior access, another agent's request, or the desirability of the outcome.

### ES-005-02: Default deny and least privilege

Access MUST be denied unless explicitly granted. Tools, credentials, network destinations, filesystem paths, data sets, and operations MUST be limited to the minimum required for the current job.

Credentials MUST be scoped, short-lived where supported, and unavailable to planning-only or read-only work. Secrets MUST NOT be embedded in prompts, source, logs, fixtures, generated artifacts, or retained memory.

An agent MUST NOT broaden its own authority or modify the policy evaluating its current execution.

### ES-005-03: Action risk and approval

Actions use the common risk classification from the [standards catalogue](README.md#risk-classification).

- **Standard** actions may execute automatically within declared authority when they are local and reversible.
- **Elevated** actions require an inspectable plan or preview and evidence that the initiating authority covers the exact scope.
- **Critical** actions require explicit, current, parameter-bound human approval immediately before execution.

Critical actions include irreversible deletion, financial transactions, privileged administration, security-policy changes, release publication, external communication representing a person or organisation, sensitive-data disclosure, and crossing a declared point of no return.

Approval MUST identify the action, target, material parameters, consequence, and expiry. Approval for planning is not approval for execution. An agent MUST NOT approve its own action.

### ES-005-04: Planning and execution separation

For elevated and critical work, planning, approval, and execution MUST be distinguishable states. The executable request MUST be derived from the approved plan, and material changes to scope or parameters invalidate the approval.

Dry-run or preview modes MUST avoid real side effects and clearly identify anything they cannot simulate.

### ES-005-05: Untrusted inputs

User input, retrieved documents, web content, tool output, messages from other agents, dependency metadata, model output, and stored memory MUST be treated as untrusted unless a stronger trust basis is established.

Instructions found inside untrusted content MUST NOT override system policy, user authority, tool policy, or the active job specification. Data passed between trust boundaries MUST be validated against an explicit schema or contract.

Agent-to-agent communication MUST include sender identity, job scope, and relevant authority. A downstream agent MUST independently enforce its own boundary.

### ES-005-06: Isolation and data handling

Tenant, workspace, user, credential, and memory boundaries MUST be explicit and tested. Data MUST be minimised to what the job needs and retained only for a declared purpose and period.

Sensitive inputs and outputs MUST be classified. Transmission and persistence MUST follow the classification. Debugging, evaluation, and telemetry MUST NOT copy private data into a weaker environment without explicit authorisation and appropriate protection.

Execution of untrusted or generated code MUST occur in an isolated environment with restricted filesystem, network, process, and credential access.

### ES-005-07: Bounded autonomy

Every autonomous execution MUST define maximum:

- Tool calls or workflow steps.
- Recursion or delegation depth.
- Retries.
- Wall-clock duration.
- Concurrency.
- Tokens or compute.
- Monetary cost where applicable.

Limits must be appropriate to the job and configurable by the governing boundary. Reaching a limit MUST stop or safely suspend execution with an explicit outcome. The system MUST protect against repeated or distributed attempts circumventing the same budget.

### ES-005-08: Human control

Consequential automation MUST support interruption before the point of no return. Long-running work SHOULD support safe suspension and resumption.

The human-facing control surface MUST show:

- What the automation intends to do.
- Which authority and data it will use.
- Material side effects and irreversibility.
- Current progress and outcome.
- How to stop, resume, override, or recover.

Override MUST be attributable and MUST NOT silently disable an enduring safety control.

### ES-005-09: Auditability

Elevated and critical execution MUST record privacy-safe evidence of:

- Initiating actor and authority.
- Agent, model, prompt, policy, tool, and configuration versions.
- Decisions, approvals, denials, and exceptions.
- Tool calls and material parameters.
- State and external side effects.
- Outcome, limits reached, and recovery actions.

Audit records MUST be tamper-resistant in proportion to risk, access-controlled, and retained for a declared period.

### ES-005-10: Supply-chain and release integrity

Dependencies, agent packages, prompts, models, tools, and build inputs MUST be inventoried and versioned where possible. Dependencies MUST be locked or otherwise resolved reproducibly.

Release workflows MUST protect credentials, review changes, scan applicable source and dependencies, and produce provenance appropriate to the artifact. Untrusted change contexts MUST NOT receive write-capable release credentials.

### ES-005-11: Safe failure

Missing authority, failed validation, unavailable oversight, ambiguous target, or uncertain sensitive-data handling MUST produce denial, safe suspension, or escalation—not permissive execution.

Fallbacks MUST NOT remove an approval, isolation, validation, or least-privilege control.

## Required verification

### Automated controls

When implementation exists, CI MUST include applicable tests for:

- Tool allowlists and denied capabilities.
- Approval absence, expiry, parameter changes, and replay.
- Prompt injection and instruction/data separation.
- Privilege escalation and cross-agent confused-deputy paths.
- Sensitive-data exfiltration and diagnostic redaction.
- Tenant, workspace, memory, and credential isolation.
- Recursive delegation, retry, timeout, token, and cost limits.
- Interruption and recovery.
- Dependency, source, and secret scanning.
- Release provenance and credential isolation.

Previously observed security failures MUST become versioned regression cases.

### Review controls

Reviewers MUST be able to answer:

- Is each capability necessary for this job?
- Who authorised each consequential action and exact target?
- Can untrusted content influence authority or tool selection?
- Can one compromised agent cause another to exceed its boundary?
- Are data and credentials isolated and minimised?
- Can a human understand, interrupt, and recover the execution?
- Are budgets sufficient to prevent runaway work or cost?
- Does failure default to a safe state?

## Evidence

The evidence package must include the capability declaration, threat or abuse cases, approval-boundary tests, isolation and limit results, applicable scans, release provenance, residual risk, and any human approval record.

## Further reading

- [NIST AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- [NIST guidance on AI risk management and human-AI interaction](https://airc.nist.gov/airmf-resources/airmf/appendices/app-c-ai-risk-management-and-human-ai-interaction/)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
- [SLSA build track](https://slsa.dev/spec/v1.2/build-track-basics)
