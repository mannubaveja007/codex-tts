#!/usr/bin/env python3
import sys
import os
import json
import traceback
import subprocess

def main():
    try:
        # Codex pipes the response JSON object into stdin on turn completion
        payload = json.loads(sys.stdin.read())
    except Exception as e:
        log_error("Failed to parse stdin as JSON payload")
        return

    # Extract response text variations depending on Codex lifecycle versions
    response_text = payload.get("text", payload.get("message", "")).strip()
    if not response_text:
        return

    # Filter out code blocks to maintain clean speech fluidity
    clean_speech_lines = []
    in_code_block = False
    
    for line in response_text.splitlines():
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            clean_speech_lines.append(line)
            
    text_to_stream = "\n".join(clean_speech_lines).strip()
    if not text_to_stream:
        return

    try:
        # Use macOS native 'say' command, running it asynchronously as a background process
        subprocess.Popen(
            ["say", text_to_stream],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        log_error(traceback.format_exc())

def log_error(message):
    try:
        log_dir = os.path.expanduser("~/.codex")
        os.makedirs(log_dir, exist_ok=True)
        with open(os.path.join(log_dir, "tts_hook.log"), "a") as f:
            f.write(f"{message}\n\n")
    except Exception:
        pass

if __name__ == "__main__":
    main()
