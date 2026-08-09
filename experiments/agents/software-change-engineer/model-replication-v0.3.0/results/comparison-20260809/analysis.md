# Cross-model replication result

## Outcome

| Model | Concise A | Detailed B | Detailed − concise | Strict passes A/B |
|---|---:|---:|---:|---:|
| `gpt-5.6-terra` | 65/70 | 65/70 | +0 | 5/10 · 5/10 |
| `gpt-5.6-sol` | 64/70 | 68/70 | +4 | 5/10 · 8/10 |

The model-definition interaction is **+4 points**. Terra shows no aggregate definition effect; Sol favors the detailed definition.

Within Sol, detailed B wins 4 task pairs, loses 0, and ties 6. The exact two-sided sign-test p-value is 0.125; with ten tasks this is directional evidence, not a conclusive estimate.

## Task-level scores

| Task | Terra A | Terra B | Sol A | Sol B | Interaction |
|---|---:|---:|---:|---:|---:|
| LSE-120 | 7 | 7 | 7 | 7 | +0 |
| LSE-121 | 7 | 7 | 7 | 7 | +0 |
| LSE-122 | 6 | 6 | 6 | 6 | +0 |
| LSE-123 | 6 | 6 | 7 | 7 | +0 |
| LSE-124 | 7 | 7 | 6 | 7 | +1 |
| LSE-125 | 6 | 7 | 7 | 7 | -1 |
| LSE-126 | 6 | 6 | 6 | 7 | +1 |
| LSE-127 | 6 | 6 | 5 | 6 | +1 |
| LSE-128 | 7 | 6 | 6 | 7 | +2 |
| LSE-129 | 7 | 7 | 7 | 7 | +0 |

## Criterion results

| Criterion | Terra A | Terra B | Sol A | Sol B |
|---|---:|---:|---:|---:|
| Bounded Scope | 10/10 | 10/10 | 10/10 | 10/10 |
| Candidate Authored Tests | 10/10 | 10/10 | 10/10 | 10/10 |
| Dependency Integrity | 10/10 | 10/10 | 10/10 | 10/10 |
| Focused Upstream Regressions | 8/10 | 7/10 | 7/10 | 10/10 |
| Handoff Evidence Integrity | 10/10 | 10/10 | 10/10 | 10/10 |
| Hidden Acceptance Tests | 8/10 | 8/10 | 7/10 | 8/10 |
| Repository Quality Checks | 9/10 | 10/10 | 10/10 | 10/10 |

## Sol resource effect of detail

| Measure | Concise A | Detailed B | Change |
|---|---:|---:|---:|
| Candidate time | 1099.5s | 1149.1s | +4.5% |
| Average per task | 109.9s | 114.9s | +4.5% |
| Input tokens | 2,856,628 | 2,949,142 | +3.2% |
| Output tokens | 36,311 | 38,404 | +5.8% |
| Tool calls | 116 | 113 | -2.6% |
| Changed lines | 520 | 466 | -10.4% |

Detailed B used +3.2% input tokens and +5.8% output tokens, took +4.5% elapsed time, made -2.6% tool calls, and changed -10.4% lines relative to concise A. It produced three additional strict task passes; the exact paired strict-pass p-value is 0.25.

## Interpretation

The result does not support treating the answer to “does more definition detail help?” as model-independent. Detail did not help Terra on aggregate, but it aligned with fewer Sol regressions and a four-point Sol advantage. Because there was one stochastic run per task and condition, replication across repeated runs or a new task block is needed before treating the Sol effect as stable.
