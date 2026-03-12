# Installation

## Requirements

- Python **3.8** or newer
- Robot Framework **4.0** or newer
- An **Anthropic API key** (RoboAssay uses Claude as its judge)

---

## Install from PyPI

```bash
pip install robotframework-roboassay
```

## Install from Source

```bash
git clone https://github.com/xleetsuperhax/RoboAssay.git
cd RoboAssay
pip install -e .
```

---

## Set Your API Key

RoboAssay calls the Anthropic API to evaluate responses. You must provide your API key via the `ANTHROPIC_API_KEY` environment variable.

=== "Linux / macOS"

    ```bash
    export ANTHROPIC_API_KEY=your-api-key-here
    ```

    To persist across sessions, add this to your `~/.bashrc` or `~/.zshrc`.

=== "Windows (PowerShell)"

    ```powershell
    $env:ANTHROPIC_API_KEY = "your-api-key-here"
    ```

=== "Windows (CMD)"

    ```cmd
    set ANTHROPIC_API_KEY=your-api-key-here
    ```

=== ".env file"

    If your project uses `python-dotenv`, add this to your `.env` file:

    ```
    ANTHROPIC_API_KEY=your-api-key-here
    ```

!!! tip "Getting an API Key"
    You can get an Anthropic API key from [console.anthropic.com](https://console.anthropic.com).

---

## Verify the Installation

```bash
python -c "import RoboAssay; print('RoboAssay installed successfully')"
```

---

## Optional Configuration

RoboAssay supports a few environment variables for advanced configuration:

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | *(required)* | Your Anthropic API key |
| `ROBOASSAY_JUDGE_MODEL` | `claude-sonnet-4-20250514` | Override the judge model |
| `ROBOASSAY_BASELINE_DIR` | `.roboassay_baselines/` (relative to cwd at runtime) | Directory for regression baselines. **Tip:** set this explicitly in CI to ensure a stable path regardless of working directory. |
| `ROBOASSAY_REQUEST_TIMEOUT` | `30` | HTTP request timeout in seconds |
| `ROBOASSAY_MAX_RETRIES` | `3` | Max retries for transient API errors (429, 5xx) |
| `ROBOASSAY_ANTHROPIC_VERSION` | `2023-06-01` | Anthropic API version header |

---

## Dependencies

RoboAssay has minimal dependencies:

```
robotframework>=4.0.0
requests>=2.25.0
```

These are installed automatically when you install via pip.
