#!/usr/bin/env python3
import sys
import os
import json
import traceback
import subprocess

def find_voice(voice_name):
    if not voice_name:
        return None
    try:
        # Run say -v "?" to list all available voices
        res = subprocess.run(["say", "-v", "?"], capture_output=True, text=True, check=True)
        for line in res.stdout.splitlines():
            parts = line.split()
            if parts:
                name = parts[0]
                # Case-insensitive comparison
                if name.lower() == voice_name.strip().lower():
                    return name
    except Exception:
        pass
    return voice_name  # fallback to whatever user passed

def main():
    raw_input = ""
    try:
        raw_input = sys.stdin.read()
        payload = json.loads(raw_input)
    except Exception as e:
        log_error(f"Failed to parse stdin as JSON payload. Raw input was: {repr(raw_input)}\nError: {traceback.format_exc()}")
        return

    # Extract response text variations depending on Codex lifecycle versions (Stop hook vs Response hook)
    response_text = ""
    last_msg = payload.get("last_assistant_message")
    if last_msg:
        if isinstance(last_msg, dict):
            response_text = last_msg.get("content", "")
        else:
            response_text = str(last_msg)
            
    if not response_text:
        response_text = payload.get("text", payload.get("message", ""))

    response_text = response_text.strip()
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
        # Get speech rate configuration (default to 185 words per minute)
        rate = os.environ.get("TTS_SPEED", "185")
        
        # Get custom voice configuration (if set, e.g. "Samantha" or "Daniel")
        # Match it case-insensitively with the system voices
        voice = find_voice(os.environ.get("TTS_VOICE"))
        
        cmd = ["say", "-r", rate]
        if voice:
            cmd.extend(["-v", voice])
        cmd.append(text_to_stream)
        
        # Use macOS native 'say' command, spawning it in the background
        # so the Codex CLI returns control to you immediately without waiting.
        subprocess.Popen(
            cmd,
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
            f.write(f"--- ERROR ---\n{message}\n\n")
    except Exception:
        pass

if __name__ == "__main__":
    main()
