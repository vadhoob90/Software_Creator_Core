# Synthetic example

`job.json` is a versioned input fixture for an isolated example workspace.
It is not a product migration or an agent competence evaluation.

Run the complete scripted demonstration from the repository root:

```sh
uv run --no-sync python scripts/demo.py
```

The demonstration creates a temporary workspace, writes a known synthetic
implementation, really executes its Python checks, records separate scripted
verification and review contributions, and exercises owner commitment and
acceptance. It deletes its own temporary workspace on exit. The output explicitly
identifies the contributors as replay fixtures, not live model agents.

For real host handoffs and retained evidence, follow the
[Core quick start](../docs/core/implementation.md).
