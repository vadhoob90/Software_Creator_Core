# Local Software Change Engineer suite 0.2.0

This in-progress suite expands the initial five-task comparison into twenty matched tasks. It keeps objective qualification gates while adding a blinded, anchored quality profile and independent cost reporting.

## Current implementation slice

- [`task-matrix-v0.2.0.json`](task-matrix-v0.2.0.json) defines the complete portfolio and planned deterministic evidence.
- [`reviewer-guidance-v0.2.0.md`](reviewer-guidance-v0.2.0.md) defines blinded review and the 0–2 anchors.
- [`schemas/run-record.schema.json`](schemas/run-record.schema.json) defines an individual attempt record.
- [`schemas/aggregate-result.schema.json`](schemas/aggregate-result.schema.json) defines a matched comparison record.
- [`validate_records.py`](validate_records.py) enforces cross-field rules that JSON Schema alone does not express clearly.

Validate the matrix, schemas, and example records with:

```bash
python3 -m unittest discover -s tests -v
python3 validate_records.py matrix task-matrix-v0.2.0.json
```

## Deliberate stopping point

This slice does not yet include the twenty seed repositories or execute the forty model runs. That ordering allows the task portfolio, scoring anchors, and record contract to be reviewed before the expensive part of the experiment is built or run.

See the [0.2.0 protocol](../local-evaluation-protocol-v0.2.0.md) and tracking [issue #3](https://github.com/vadhoob90/PDLC_Core/issues/3).
