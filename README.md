# Codex TTS: Local Automated Voice Playback for Codex CLI

An automated, zero-latency, local Text-to-Speech (TTS) pipeline for the OpenAI Codex CLI. It intercepts Codex responses, filters out code blocks/formatting, and reads conversational explanations out loud in the background using the native macOS `say` engine.

## Features

- 🏎️ **Zero Network Latency**: Works 100% offline using macOS's built-in speech engine.
- ⚡ **Asynchronous & Non-Blocking**: Spawns speech tasks in background processes, allowing you to read and type while it talks.
- 🧹 **Smart Text Filtering**: Automatically strips out markdown code blocks (e.g. ` ```python ... ``` `) and syntax formatting so only conversational text and reasoning are spoken.
- 🗣️ **Customizable Voice & Speed**: Swap voices (e.g. `Samantha`, `Rishi`, `Daniel`) and control words-per-minute speed via shell environment variables.
- ⏹️ **Instant Silence**: Stop long playbacks immediately with a simple terminal command.

---

## Installation

### Step 1: Clone and Set Up the Script
Copy the hook script to your local bin directory and make it executable:
```bash
sudo cp codex_speech_hook.py /usr/local/bin/codex_speech_hook.py
sudo chmod +x /usr/local/bin/codex_speech_hook.py
```

### Step 2: Register the Hook in Codex
Add the hook command to your user-level Codex lifecycle configuration in `~/.codex/hooks.json` under the `"Stop"` event.

Open `~/.codex/hooks.json` and add `/usr/local/bin/codex_speech_hook.py` under the `"Stop"` hooks array:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/usr/local/bin/codex_speech_hook.py"
          }
        ]
      }
    ]
  }
}
```

Ensure hooks are enabled in your `~/.codex/config.toml` file:
```toml
[features]
hooks = true
```

---

## Usage & Configuration

### Environment Variables
Configure these variables in your shell profile (e.g. `~/.zshrc` or `~/.bashrc`) to customize the speech:

```bash
# Choose your preferred macOS voice (run `say -v "?"` to list all available voices)
export TTS_VOICE="Samantha"

# Adjust speaking rate in words-per-minute (default: 185)
export TTS_SPEED="200"

# Optional: Add a quick alias to silence the voice instantly
alias shutup="killall say"
```

Save your profile and reload it:
```bash
source ~/.zshrc
```

### Launch Codex
Start your Codex CLI session:
```bash
codex
```
Prompt Codex as usual. The text response will be spoken immediately in the background while keeping your terminal active for your next input.

---

## License

MIT License. Feel free to customize and share!
