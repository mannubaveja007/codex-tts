#!/usr/bin/env python3
import sys
import os
import json
import subprocess

def main():
    try:
        # Codex pipes the response JSON object into stdin on turn completion
        payload = json.loads(sys.stdin.read())
    except Exception:
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
    except Exception:
        pass # Suppress failures to avoid interrupting Codex CLI core processing loops

if __name__ == "__main__":
    main()
