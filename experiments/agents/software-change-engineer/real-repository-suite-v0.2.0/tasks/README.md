# Task reproduction catalogue

This catalogue adds navigable reproduction references for the ten locked task
inputs. The `LSE-*.md` files are intentionally unchanged because their exact
contents are hashed in the [experiment lock](../experiment.lock.json) and were
shown to both conditions during the scored run.

The tasks are synthetic PDLC Core evaluation scenarios. They are not reports of
accepted upstream bugs and are not associated with upstream issues or pull
requests. Reproduce them in disposable local checkouts; do not submit the
experimental patches or contact upstream maintainers unless they independently
request that work.

Shared references:

- [Experiment method and runner](../README.md)
- [Content-addressed experiment lock](../experiment.lock.json)
- [PDLC Core tracking issue #3](https://github.com/vadhoob90/PDLC_Core/issues/3)
- [Scored run summary](../results/run-20260809T155111Z/result.md)
- [Post-run validity review](../results/run-20260809T155111Z/validity-review.md)

## LSE-120 — Atomic case-insensitive dictionary updates

- [Task](LSE-120.md)
- Repository: [`psf/requests`](https://github.com/psf/requests)
- Baseline: [`1f6589e`](https://github.com/psf/requests/tree/1f6589ec3a1ee910f9a65cc3ceac60b26677bc0e)
- Relevant code: [`src/requests/structures.py`](https://github.com/psf/requests/blob/1f6589ec3a1ee910f9a65cc3ceac60b26677bc0e/src/requests/structures.py)
- Upstream tests: [`tests/test_structures.py`](https://github.com/psf/requests/blob/1f6589ec3a1ee910f9a65cc3ceac60b26677bc0e/tests/test_structures.py)
- Independent check: [`hidden_tests/LSE-120.py`](../hidden_tests/LSE-120.py)
- Recorded evidence: [concise A](../results/run-20260809T155111Z/LSE-120/condition-a) · [detailed B](../results/run-20260809T155111Z/LSE-120/condition-b)

## LSE-121 — Prevalidate response hooks

- [Task](LSE-121.md)
- Repository: [`psf/requests`](https://github.com/psf/requests)
- Baseline: [`1f6589e`](https://github.com/psf/requests/tree/1f6589ec3a1ee910f9a65cc3ceac60b26677bc0e)
- Relevant code: [`src/requests/hooks.py`](https://github.com/psf/requests/blob/1f6589ec3a1ee910f9a65cc3ceac60b26677bc0e/src/requests/hooks.py)
- Upstream tests: [`tests/test_hooks.py`](https://github.com/psf/requests/blob/1f6589ec3a1ee910f9a65cc3ceac60b26677bc0e/tests/test_hooks.py)
- Independent check: [`hidden_tests/LSE-121.py`](../hidden_tests/LSE-121.py)
- Recorded evidence: [concise A](../results/run-20260809T155111Z/LSE-121/condition-a) · [detailed B](../results/run-20260809T155111Z/LSE-121/condition-b)

## LSE-122 — ANSI-aware short-help width

- [Task](LSE-122.md)
- Repository: [`pallets/click`](https://github.com/pallets/click)
- Baseline: [`00e592c`](https://github.com/pallets/click/tree/00e592cea702e0b2caa0dee42489fdb1c22cd845)
- Relevant code: [`src/click/utils.py`](https://github.com/pallets/click/blob/00e592cea702e0b2caa0dee42489fdb1c22cd845/src/click/utils.py)
- Upstream tests: [`tests/test_utils/test_make_default_short_help.py`](https://github.com/pallets/click/blob/00e592cea702e0b2caa0dee42489fdb1c22cd845/tests/test_utils/test_make_default_short_help.py)
- Independent check: [`hidden_tests/LSE-122.py`](../hidden_tests/LSE-122.py)
- Recorded evidence: [concise A](../results/run-20260809T155111Z/LSE-122/condition-a) · [detailed B](../results/run-20260809T155111Z/LSE-122/condition-b)

## LSE-123 — Complete pending progress updates

- [Task](LSE-123.md)
- Repository: [`pallets/click`](https://github.com/pallets/click)
- Baseline: [`00e592c`](https://github.com/pallets/click/tree/00e592cea702e0b2caa0dee42489fdb1c22cd845)
- Relevant code: [`src/click/_termui_impl.py`](https://github.com/pallets/click/blob/00e592cea702e0b2caa0dee42489fdb1c22cd845/src/click/_termui_impl.py)
- Upstream tests: [`tests/test_termui.py`](https://github.com/pallets/click/blob/00e592cea702e0b2caa0dee42489fdb1c22cd845/tests/test_termui.py)
- Independent check: [`hidden_tests/LSE-123.py`](../hidden_tests/LSE-123.py)
- Recorded evidence: [concise A](../results/run-20260809T155111Z/LSE-123/condition-a) · [detailed B](../results/run-20260809T155111Z/LSE-123/condition-b)

## LSE-124 — Binary file-size formatting

- [Task](LSE-124.md)
- Repository: [`Textualize/rich`](https://github.com/Textualize/rich)
- Baseline: [`9d8f9a3`](https://github.com/Textualize/rich/tree/9d8f9a372cc5916fd4781fec207ced7ddac2f08f)
- Relevant code: [`rich/filesize.py`](https://github.com/Textualize/rich/blob/9d8f9a372cc5916fd4781fec207ced7ddac2f08f/rich/filesize.py)
- Upstream tests: [`tests/test_filesize.py`](https://github.com/Textualize/rich/blob/9d8f9a372cc5916fd4781fec207ced7ddac2f08f/tests/test_filesize.py)
- Independent check: [`hidden_tests/LSE-124.py`](../hidden_tests/LSE-124.py)
- Recorded evidence: [concise A](../results/run-20260809T155111Z/LSE-124/condition-a) · [detailed B](../results/run-20260809T155111Z/LSE-124/condition-b)

## LSE-125 — Reject contradictory measurement bounds

- [Task](LSE-125.md)
- Repository: [`Textualize/rich`](https://github.com/Textualize/rich)
- Baseline: [`9d8f9a3`](https://github.com/Textualize/rich/tree/9d8f9a372cc5916fd4781fec207ced7ddac2f08f)
- Relevant code: [`rich/measure.py`](https://github.com/Textualize/rich/blob/9d8f9a372cc5916fd4781fec207ced7ddac2f08f/rich/measure.py)
- Upstream tests: [`tests/test_measure.py`](https://github.com/Textualize/rich/blob/9d8f9a372cc5916fd4781fec207ced7ddac2f08f/tests/test_measure.py)
- Independent check: [`hidden_tests/LSE-125.py`](../hidden_tests/LSE-125.py)
- Recorded evidence: [concise A](../results/run-20260809T155111Z/LSE-125/condition-a) · [detailed B](../results/run-20260809T155111Z/LSE-125/condition-b)

## LSE-126 — Redact API-key headers

- [Task](LSE-126.md)
- Repository: [`encode/httpx`](https://github.com/encode/httpx)
- Baseline: [`b5addb6`](https://github.com/encode/httpx/tree/b5addb64f0161ff6bfe94c124ef76f6a1fba5254)
- Relevant code: [`httpx/_models.py`](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_models.py)
- Upstream tests: [`tests/models/test_headers.py`](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/tests/models/test_headers.py)
- Independent check: [`hidden_tests/LSE-126.py`](../hidden_tests/LSE-126.py)
- Recorded evidence: [concise A](../results/run-20260809T155111Z/LSE-126/condition-a) · [detailed B](../results/run-20260809T155111Z/LSE-126/condition-b)

## LSE-127 — Immutable query-parameter removal

- [Task](LSE-127.md)
- Repository: [`encode/httpx`](https://github.com/encode/httpx)
- Baseline: [`b5addb6`](https://github.com/encode/httpx/tree/b5addb64f0161ff6bfe94c124ef76f6a1fba5254)
- Relevant code: [`httpx/_urls.py`](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_urls.py)
- Upstream tests: [`tests/models/test_queryparams.py`](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/tests/models/test_queryparams.py)
- Independent check: [`hidden_tests/LSE-127.py`](../hidden_tests/LSE-127.py)
- Recorded evidence: [concise A](../results/run-20260809T155111Z/LSE-127/condition-a) · [detailed B](../results/run-20260809T155111Z/LSE-127/condition-b)

## LSE-128 — Type-safe destructive Stash read

- [Task](LSE-128.md)
- Repository: [`pytest-dev/pytest`](https://github.com/pytest-dev/pytest)
- Baseline: [`006884b`](https://github.com/pytest-dev/pytest/tree/006884bac1cff49d2e2908c20fbbb0f0bc8e671b)
- Relevant code: [`src/_pytest/stash.py`](https://github.com/pytest-dev/pytest/blob/006884bac1cff49d2e2908c20fbbb0f0bc8e671b/src/_pytest/stash.py)
- Upstream tests: [`testing/test_stash.py`](https://github.com/pytest-dev/pytest/blob/006884bac1cff49d2e2908c20fbbb0f0bc8e671b/testing/test_stash.py)
- Independent check: [`hidden_tests/LSE-128.py`](../hidden_tests/LSE-128.py)
- Recorded evidence: [concise A](../results/run-20260809T155111Z/LSE-128/condition-a) · [detailed B](../results/run-20260809T155111Z/LSE-128/condition-b)

## LSE-129 — Reject invalid mock sleep durations

- [Task](LSE-129.md)
- Repository: [`pytest-dev/pytest`](https://github.com/pytest-dev/pytest)
- Baseline: [`006884b`](https://github.com/pytest-dev/pytest/tree/006884bac1cff49d2e2908c20fbbb0f0bc8e671b)
- Relevant code: [`src/_pytest/timing.py`](https://github.com/pytest-dev/pytest/blob/006884bac1cff49d2e2908c20fbbb0f0bc8e671b/src/_pytest/timing.py)
- Related upstream use: [`testing/test_junitxml.py`](https://github.com/pytest-dev/pytest/blob/006884bac1cff49d2e2908c20fbbb0f0bc8e671b/testing/test_junitxml.py)
- Independent check: [`hidden_tests/LSE-129.py`](../hidden_tests/LSE-129.py)
- Recorded evidence: [concise A](../results/run-20260809T155111Z/LSE-129/condition-a) · [detailed B](../results/run-20260809T155111Z/LSE-129/condition-b)
