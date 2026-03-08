# Regression Keywords

Detect behavioral drift in LLM responses by comparing against saved baselines.

As LLMs evolve — through model updates, prompt changes, or configuration drift — their responses can change in subtle ways. Regression keywords let you capture a "known good" response as a baseline, then assert in future test runs that behavior hasn't changed.

---

## Save Response As Baseline

**Arguments:** `response`, `baseline_id`

Saves a response as a named baseline for future regression checks. Baselines are stored as JSON files in `.roboassay_baselines/` (relative to the current working directory). The directory is created automatically.

```robot
Save Response As Baseline    ${response}    refund-policy-v1
Save Response As Baseline    ${response}    support-bot-greeting
```

The `baseline_id` is a string identifier you choose — use something descriptive. Running this keyword again with the same ID will overwrite the existing baseline.

**Baseline storage location:** Configurable via the `ROBOASSAY_BASELINE_DIR` environment variable (default: `.roboassay_baselines/`).

---

## Response Behavior Should Not Have Changed

**Arguments:** `response`, `baseline_id`

Asserts that the response behavior has not changed from a previously saved baseline. Uses semantic comparison — not exact string matching — so minor rewording won't cause failures, but meaningful behavioral changes will.

```robot
Response Behavior Should Not Have Changed    ${response}    refund-policy-v1
Response Behavior Should Not Have Changed    ${response}    support-bot-greeting
```

**Fails when:** The response meaningfully differs from the saved baseline in content, stance, or behavior.

!!! warning "Baseline must exist"
    This keyword will fail if no baseline has been saved with the given `baseline_id`. Always save a baseline first.

---

## Response Should Match Baseline Semantically

**Arguments:** `response`, `baseline`, `threshold=0.8`

Asserts that the response semantically matches a provided baseline string above a given similarity threshold (0.0–1.0). Unlike `Response Behavior Should Not Have Changed`, the baseline is passed directly as a string rather than loaded from a file.

```robot
${expected}=    Set Variable    Refunds are processed within 5 business days.
Response Should Match Baseline Semantically    ${response}    ${expected}

# Stricter threshold (90% similarity required)
Response Should Match Baseline Semantically    ${response}    ${expected}    threshold=0.9

# More lenient threshold
Response Should Match Baseline Semantically    ${response}    ${expected}    threshold=0.7
```

**Fails when:** The semantic similarity score between the response and baseline falls below the threshold.

---

## Regression Testing Workflow

A typical regression workflow has two phases:

### Phase 1 — Establish Baselines

Run this once when you're happy with your LLM's current behavior:

```robot
*** Settings ***
Library    RoboAssay

*** Test Cases ***
Save Baselines
    ${response}=    Call My LLM    What is the refund policy?
    Save Response As Baseline    ${response}    refund-policy

    ${response}=    Call My LLM    How do I contact support?
    Save Response As Baseline    ${response}    contact-support
```

### Phase 2 — Run Regression Checks

Run this in CI on every deployment or model update:

```robot
*** Settings ***
Library    RoboAssay

*** Test Cases ***
Refund Policy Has Not Regressed
    ${response}=    Call My LLM    What is the refund policy?
    Response Behavior Should Not Have Changed    ${response}    refund-policy

Contact Support Has Not Regressed
    ${response}=    Call My LLM    How do I contact support?
    Response Behavior Should Not Have Changed    ${response}    contact-support
```

---

## Full Example

```robot
*** Settings ***
Library    RoboAssay

*** Variables ***
${V1_RESPONSE}    Refunds are processed within 5 business days of receiving the return.
${V2_RESPONSE}    We process refunds in 5 business days after we receive your returned item.
${CHANGED}        Returns take about two weeks to process and may incur a restocking fee.

*** Test Cases ***
Save A Baseline
    Save Response As Baseline    ${V1_RESPONSE}    refund-timing

Semantically Similar Response Passes
    Response Should Match Baseline Semantically    ${V2_RESPONSE}    ${V1_RESPONSE}

Changed Behavior Is Caught
    [Documentation]    This test is expected to fail — behavior has changed.
    [Tags]    expected-fail
    Response Behavior Should Not Have Changed    ${CHANGED}    refund-timing
```

---

## Tips

!!! tip "Committing Baselines"
    Commit your `.roboassay_baselines/` directory to version control. This lets your team share baselines and track how LLM behavior evolves over time.

!!! tip "Threshold Tuning"
    Start with the default threshold of `0.8` for `Response Should Match Baseline Semantically`. If you're getting too many false positives (tests failing on minor rewording), lower the threshold. If important changes are slipping through, raise it.
