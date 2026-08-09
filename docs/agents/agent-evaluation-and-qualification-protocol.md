---
id: pdlc-core.agent-evaluation-and-qualification-protocol
kind: governance-protocol
protocol_version: 0.1.0
status: adopted
effective: 2026-08-09
---

# Agent evaluation and qualification protocol

**Governed by:** [Development principles](../core/development-principles.md), [Engineering standards](../standards/README.md), and the [agent qualification gate](agent-qualification-gate.md)

**Applies to:** Every PDLC Core agent build presented as qualified, competent, experienced, recommended, or suitable for a stated product context

## Purpose

An agent must earn competence claims through reproducible evidence. A convincing role definition, an expert persona, or a successful demonstration is not enough.

The interview is a useful metaphor: the candidate must explain, create, diagnose, verify, refuse, escalate, and hand off work under representative conditions. The actual product of the process is not an interview transcript or a single score. It is an attributable evaluation record showing what an exact agent build could do, how reliably it did it, where it failed, and which claims the evidence supports.

This protocol prevents PDLC Core from confusing prompt quality with professional competence or allowing one language model to validate its own unsupported claims.

## Two separate qualification decisions

The [agent qualification gate](agent-qualification-gate.md) decides whether a proposed responsibility deserves to exist as an agent role. This protocol decides whether a particular resolved build has demonstrated the competence required by that role.

Both decisions are required before Core recommends an agent:

```text
Role qualifies as a distinct recurring responsibility
+ exact agent build passes its applicable evaluation suites
= evidence-backed qualified agent build
```

A structurally valid role may have no competent implementation. A capable model may complete useful work without proving that a proposed role definition adds value. Neither result substitutes for the other.

## Unit of evaluation

Scores and qualification results belong to an immutable **evaluated build**, not to a role name or definition in isolation. The build identity includes every component capable of changing observable behaviour:

```text
model and model version
+ Core professional baseline version
+ Core role definition version
+ product or technology specialisation version
+ tool and capability versions
+ authority configuration
+ system and runtime configuration
= evaluated build
```

The evaluation record MUST identify these components or explicitly record that a component was absent. A result MUST NOT be transferred silently to another model, specialisation, tool set, authority level, or materially different configuration.

Definitions-only consumers receive the definition's provenance, not the qualification result of a reference build. A downstream product must evaluate its own resolved build before making a product-specific competence claim.

## Evaluation principles

Every qualification assessment MUST satisfy these principles:

1. **Outcome evidence over performance theatre.** Prefer working artifacts, executable behaviour, and observable decisions to confident explanations.
2. **Representative work over trivia.** Exercise the role's recurring outcome, judgement, boundaries, and failure modes rather than rewarding memorised interview answers.
3. **Predeclared criteria over retrospective scoring.** Freeze the competencies, cases, rubric, thresholds, budgets, and decision rules before qualification runs begin.
4. **Independent evidence over self-assessment.** The candidate may explain its work but cannot be the sole evaluator of that work.
5. **Reliability over best-of-many success.** Report ordinary first-attempt behaviour and repeated-run consistency; do not publish only the best sample.
6. **Diagnostic results over one headline score.** Preserve dimension-level results, blocking failures, limitations, and applicable scope.
7. **Comparative proof over assumed value.** Show whether the role definition and specialisation improve the underlying model rather than merely adding text.
8. **Versioned evidence over permanent reputation.** Results remain attributable to the exact build, suite, protocol, evaluator, and date used.

## Competency contract

Before cases are written, the role owner MUST define a versioned competency contract derived from the role's accountable outcome. Each competency must state:

- the decision or outcome being assessed
- why it is necessary for this role rather than the common professional baseline
- observable evidence of meeting, exceeding, or failing the expectation
- applicable risk classification
- whether failure blocks qualification
- the minimum acceptance threshold
- relevant external and internal sources

The contract SHOULD cover only competencies necessary to the role. Adding impressive but irrelevant topics makes an evaluation less representative.

Common assessment dimensions include:

| Dimension | Evidence sought |
| --- | --- |
| Role-outcome correctness | The owned outcome satisfies its stated acceptance conditions |
| Comprehension | Existing behaviour, constraints, and affected boundaries are understood before action |
| Applied judgement | Decisions and trade-offs are appropriate to the role and evidence available |
| Artifact quality | Outputs are understandable, maintainable, bounded, and usable by their consumers |
| Verification | Claims are supported by relevant, trustworthy checks and retained evidence |
| Failure handling | Invalid inputs, uncertainty, blocked work, and partial failure are made explicit |
| Authority compliance | Prohibited actions are refused and elevated decisions are escalated |
| Handoff quality | Another role can independently understand, verify, and continue the work |

Role-specific competency belongs in the role suite. Behaviour expected from every engineering contributor belongs in the professional-baseline suite. Product, domain, regulatory, or technology competence belongs in a specialisation suite.

## Incorporating external evidence

Job descriptions, public career frameworks, professional standards, incident research, engineering guidance, and observed product failures MAY inform the competency contract. They are inputs, not authorities that replace Core's principles or the role's outcome.

Each material external source MUST have a source record containing:

- publisher and title
- stable location where available
- published version or retrieval date
- applicable licence or usage constraint when relevant
- competency or risk it informed
- the Core interpretation derived from it
- rationale for including, adapting, or rejecting the source's expectation

Employer job descriptions are market signals, not proof that a competency is necessary or measurable. Market-derived competencies SHOULD be triangulated across independent sources and MUST be translated into observable role behaviour. Core SHOULD derive criteria rather than copying proprietary wording.

Changes to a source do not silently change a competency contract. Updating a derived criterion is a versioned Core decision with an impact assessment under [ES-004](../standards/ES-004-deliberate-compatible-reversible-evolution.md).

## Evaluation suite structure

An applicable evaluation is composed from independently versioned suites:

```text
professional-baseline suite
+ role suite
+ selected specialisation suites
+ product-owned acceptance suite
= evaluation portfolio for the resolved build
```

Core owns the baseline and Core-role suites. A product owns evaluation of its local specialisation, policies, architecture, and risks. Passing a Core suite MUST NOT be represented as product acceptance.

Each suite contains three partitions:

- **Public development cases** — examples that explain expectations and support iteration.
- **Restricted qualification cases** — unseen cases used for formal qualification.
- **Retired cases** — previously restricted cases available for diagnosis and regression once they no longer protect a holdout.

The suite manifest and competency coverage MAY be public. Restricted prompts, fixtures, oracles, and rubric details MUST NOT be available to the candidate during execution. If they are disclosed or become accessible to the candidate, the affected qualification result is invalidated and the cases must be retired or replaced.

## Case portfolio

The number of cases follows competency and risk coverage, not an arbitrary interview-question target. A useful initial portfolio may contain twenty to thirty cases, but case count alone is not evidence of adequacy.

The portfolio MUST include representative cases for:

- expected successful work
- incomplete, contradictory, or invalid inputs
- unfamiliar existing artifacts that must be understood before modification
- implementation or artifact production where the role creates outputs
- diagnosis and recovery from failure
- verification and evidence selection
- ambiguous evidence and explicit uncertainty
- pressure to exceed authority or bypass a control
- refusal, escalation, and human-decision boundaries
- downstream handoff and independent review

At least one case MUST exercise every blocking competency and every critical boundary. Similar questions with superficial wording changes count as one scenario family, not independent coverage.

Explanation-only questions MAY assess mental models or judgement but MUST NOT be the sole evidence for a competency that can be exercised through actual work. For engineering roles, qualification SHOULD use executable repositories, tests, defects, change requests, and review artifacts wherever practicable.

## Case contract

Every case MUST have a stable identifier and versioned contract containing:

```yaml
case:
  id: <stable-case-id>
  version: <case-version>
  status: public-development | restricted-qualification | retired
  scenario_family: <family-id>
  competencies: [<competency-id>]
  risk: standard | elevated | critical

  candidate_material:
    brief: <task-visible-to-candidate>
    fixture: <isolated-fixture-reference>
    authority: <granted-and-prohibited-actions>
    resources: <time-tool-and-token-budget>

  evaluator_material:
    expected_outcomes: [<observable-outcome>]
    deterministic_checks: [<check-reference>]
    rubric: <rubric-reference>
    blocking_failures: [<failure-condition>]
    required_evidence: [<evidence-type>]
```

Candidate material MUST be separable from evaluator material so that the execution environment can expose only what the candidate is authorised to see.

## Execution protocol

Formal qualification runs MUST follow a recorded execution plan:

1. Freeze the evaluated build, suite versions, rubric, thresholds, budgets, and comparison builds.
2. Create a fresh, isolated context for each case; do not carry reasoning, solutions, or feedback between cases.
3. Expose only candidate material and the tools, data, network access, and authority declared by the case.
4. Capture inputs, outputs, tool calls, side effects, timings, failures, and material environment metadata.
5. Apply deterministic checks before judgement-based scoring.
6. Repeat stochastic cases at least three independent times unless the evaluator records why the execution is deterministic.
7. Score every valid run, including incomplete work and explicit refusal; do not discard an unfavourable run.
8. Classify infrastructure failures separately and rerun them only after recording why the attempt was invalid.
9. Preserve the immutable raw evidence and produce an attributable result record.

Qualification MUST measure first-attempt behaviour. Retries initiated by the candidate within its declared job protocol count as part of that attempt; external selection of the best result from multiple attempts does not.

## Independent evaluation

Evaluation uses the strongest available evidence in this order:

1. executable and deterministic outcome checks
2. mechanically measured properties and policy checks
3. blinded rubric-based assessment
4. human review for ambiguous or high-consequence judgement

An LLM judge MAY apply a rubric, but it MUST NOT be the sole evidence for a critical subjective decision or score its own execution instance. The evaluator record must disclose its model, prompt, tools, calibration set, and known relationship to the candidate model.

Using the same model family for candidate and evaluator creates correlated error and MUST be recorded as a limitation. Such an evaluator requires corroboration through deterministic evidence, a separately calibrated evaluator, or human review for material judgement.

Judgement-based evaluators MUST be calibrated against a versioned set of independently reviewed examples before qualification. Material evaluator disagreement is an evaluation result to investigate, not noise to conceal through averaging.

The role-definition author may create cases and explain intended behaviour but MUST NOT be the sole person or agent deciding qualification.

## Comparative and ablation evaluation

The first qualification of a role, and any material behavioural revision, MUST compare controlled builds where the available components permit it:

```text
A. underlying model and tools
B. A + professional baseline
C. B + role definition
D. C + applicable specialisation
```

All comparison builds receive the same candidate-visible cases, budgets, authority, tools, and scoring rules. The evaluation charter must define in advance what constitutes a meaningful improvement.

The role definition does not demonstrate value merely because build C passes. It must improve the role-specific result or reliability relative to build B without causing a material regression in blocking competencies. A specialisation claim similarly requires build D to improve the applicable product or technology competencies relative to build C.

If a layer produces no meaningful benefit, the outcome is not hidden. The layer must be reshaped, removed, or retained only with a recorded non-performance rationale such as standardised portability or clearer governance.

## Scoring and decision rules

Each valid run receives a case outcome of **pass** or **fail** plus its dimension-level rubric results. An execution that cannot be assessed because the evaluation infrastructure failed receives **invalid** and does not count as a candidate success or failure.

The published record MUST report:

- valid runs passed and attempted
- cases passed consistently across all required runs
- dimension-level results
- blocking and critical failures
- comparison-build results and measured contribution from each layer
- evaluator disagreement and invalid runs
- observed limitations and applicable contexts

Qualification is **passed** only when:

- every predeclared blocking threshold is satisfied
- no valid run contains an unauthorised critical action, concealed material failure, fabricated evidence, or prohibited self-approval
- the required repeated-run reliability is met
- the result is supported by the required independent evidence
- the role layer meets its predeclared comparative-improvement requirement

Otherwise the result is **failed**, **inconclusive**, or **invalidated**. An inconclusive result is not a pass. Scores from unrelated dimensions MUST NOT compensate for a blocking failure.

A single aggregate score MAY be displayed for navigation only when its weighting is published. It MUST NOT replace the qualification outcome or dimension-level evidence.

## Published qualification card

A definition may display a qualification card only for an evaluated build with a discoverable evidence record. The card MUST identify scope and limitations near the score so that readers cannot mistake reference evidence for a universal capability claim.

Illustrative shape:

```yaml
agent_qualification:
  outcome: passed
  role: <role-id@version>
  evaluated_build_id: <immutable-build-id>
  protocol: pdlc-core.agent-evaluation-and-qualification-protocol@0.1.0
  evaluation_portfolio: [<suite-id@version>]
  evaluated_at: <ISO-8601-timestamp>

  build:
    model: <provider-model-and-version>
    professional_baseline: <baseline-id@version-or-none>
    role_definition: <role-id@version>
    specialisations: [<profile-id@version>]
    tools: [<tool-id@version>]
    authority_profile: <authority-id@version>
    runtime: <material-runtime-configuration>

  results:
    valid_runs: <passed>/<attempted>
    consistently_passed_cases: <passed>/<attempted>
    dimensions:
      <competency-id>: <result-and-threshold>
    blocking_failures: []
    critical_failures: []

  comparison:
    underlying_model: <result-reference>
    with_professional_baseline: <result-reference>
    with_role_definition: <result-reference>
    with_specialisation: <result-reference-or-not-applicable>
    demonstrated_role_contribution: <predeclared-measure>

  evidence: <immutable-evidence-record>
  limitations: [<known-limitation>]
  applicable_contexts: [<supported-context>]
  reassessment_triggers: [<trigger>]
```

Placeholder values, self-awarded labels, unavailable evidence, selectively omitted runs, or an unscoped number MUST NOT be presented as qualification.

## Lifecycle and reassessment

Evaluation suites, evaluated builds, raw evidence, derived results, and qualification decisions are immutable versioned artifacts. Corrections create a successor and retain a link to the superseded record.

Reassessment is required when a change can materially affect behaviour or the validity of evidence, including:

- model or material model-version change
- baseline, role, specialisation, tool, authority, or runtime change
- role outcome, boundary, competency, rubric, or threshold change
- discovery of contamination, evaluator bias, fixture defect, or score calculation error
- new failure evidence that contradicts a published competence claim
- expiry or change in a product, regulatory, security, or technology context

Editorial changes that cannot affect execution MAY retain the result with a recorded impact decision. A newer model name or higher score elsewhere is not evidence of continued qualification.

When evidence is invalidated, the visible card MUST stop showing **passed**. Historical results remain available with their invalidation reason so that consumers can reconstruct what was known at the time.

## Initial implementation boundary

This version defines the protocol and evidence contract. It does not yet claim that PDLC Core has:

- selected the first replacement role for `implementer`
- created a competency contract or evaluation suite for that role
- built an evaluation runner or restricted-case store
- qualified any agent build
- standardised one scoring library or LLM evaluator

The next role candidate must use this protocol rather than inventing its evidence model inside the definition. The smallest valid implementation is one role-specific competency contract, a representative case portfolio, controlled comparison builds, retained results, and an independently reviewed qualification card.
