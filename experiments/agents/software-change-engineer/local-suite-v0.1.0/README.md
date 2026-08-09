# Local Software Change Engineer suite 0.1.0

This suite contains five small synthetic Python repositories and evaluator-owned hidden tests. It tests the detailed role specification against a credible basic definition without importing code or knowledge from a downstream product.

Each `public/` directory is copied into a fresh temporary Git repository for an attempt. The candidate sees only that repository, its `AGENTS.md`, and its `TASK.md`. After the attempt, `evaluate.py` runs the public tests and the corresponding hidden test from outside the candidate workspace.

Run an evaluation check with:

```bash
python3 evaluate.py \
  --task LSE-001 \
  --candidate-dir /path/to/completed/repository \
  --condition basic \
  --last-message /path/to/last-message.txt \
  --output /path/to/result.json
```

The evaluator uses only the Python standard library. It does not execute network, publishing, or downstream repository actions.

The executed suite's [per-attempt results](evidence/results/) and [replayable patches](evidence/patches/) support the [published comparison](../local-evaluation-result-v0.1.0.md). Evidence records are model- and runtime-specific; they are not universal agent scores.
