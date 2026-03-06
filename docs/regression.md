# Regression Keywords

Keywords for asserting that LLM response behavior has not regressed from saved baselines.

## Keywords

### Response Should Match Baseline Semantically
**Arguments:** `response`, `baseline`, `threshold=0.8`

Asserts that the response semantically matches a baseline response above the given threshold.

```robot
Response Should Match Baseline Semantically    ${response}    ${expected_baseline}
Response Should Match Baseline Semantically    ${response}    ${expected_baseline}    threshold=0.9
```

### Save Response As Baseline
**Arguments:** `response`, `baseline_id`

Saves a response as a baseline for future regression checks. Baselines are stored as local JSON files in `.roboassay_baselines/`.

```robot
Save Response As Baseline    ${response}    my-feature-baseline
```

### Response Behavior Should Not Have Changed
**Arguments:** `response`, `baseline_id`

Asserts that the response behavior has not changed from a previously saved baseline.

```robot
Response Behavior Should Not Have Changed    ${response}    my-feature-baseline
```
