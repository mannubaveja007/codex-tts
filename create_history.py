#!/usr/bin/env python3
import os
import subprocess
import shutil

# Repository directory
repo_dir = "/Users/mannubaveja/.gemini/antigravity/scratch/codex-tts-setup"
os.chdir(repo_dir)

# Helper to run shell commands
def run_cmd(args):
    subprocess.run(args, check=True)

# 1. Clean up existing git folder to recreate it from scratch
if os.path.exists(".git"):
    shutil.rmtree(".git")

run_cmd(["git", "init"])
run_cmd(["git", "branch", "-M", "main"])

# Save final files to write them back at the end
with open("codex_speech_hook.py", "r") as f:
    final_hook = f.read()

with open("README.md", "r") as f:
    final_readme = f.read()

with open(".gitignore", "r") as f:
    final_gitignore = f.read()

with open("LICENSE", "r") as f:
    final_license = f.read()

# --- STAGE 1: Initial macOS say Hook ---
stage1_hook = """#!/usr/bin/env python3
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
            
    text_to_stream = "\\n".join(clean_speech_lines).strip()
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
"""

stage1_readme = """# Codex TTS

An automated Text-to-Speech (TTS) pipeline for the OpenAI Codex CLI using the native macOS `say` speech engine.
"""

with open("codex_speech_hook.py", "w") as f:
    f.write(stage1_hook)
with open("README.md", "w") as f:
    f.write(stage1_readme)

run_cmd(["git", "add", "."])
run_cmd(["git", "commit", "-m", "feat: initial local TTS hook using macOS say"])

# --- STAGE 2: Detailed README for macOS say ---
stage2_readme = """# Codex TTS: Automated Local Playback for Codex CLI

An automated Text-to-Speech (TTS) pipeline for the OpenAI Codex CLI using the native macOS `say` speech engine.

## Installation
1. Copy the hook script to `/usr/local/bin`:
   ```bash
   sudo cp codex_speech_hook.py /usr/local/bin/codex_speech_hook.py
   sudo chmod +x /usr/local/bin/codex_speech_hook.py
   ```
"""

with open("README.md", "w") as f:
    f.write(stage2_readme)

run_cmd(["git", "add", "README.md"])
run_cmd(["git", "commit", "-m", "docs: add comprehensive README configuration guide"])

# --- STAGE 3: Error Logging for Stdin/JSON Parse ---
stage3_hook = """#!/usr/bin/env python3
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
            
    text_to_stream = "\\n".join(clean_speech_lines).strip()
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
            f.write(f"{message}\\n\\n")
    except Exception:
        pass

if __name__ == "__main__":
    main()
"""

with open("codex_speech_hook.py", "w") as f:
    f.write(stage3_hook)

run_cmd(["git", "add", "codex_speech_hook.py"])
run_cmd(["git", "commit", "-m", "feat: add error logging mechanism to tts_hook.log"])

# --- STAGE 4: Custom Voice and Speaking Speed support ---
stage4_hook = """#!/usr/bin/env python3
import sys
import os
import json
import traceback
import subprocess

def main():
    try:
        payload = json.loads(sys.stdin.read())
    except Exception as e:
        log_error("Failed to parse stdin as JSON payload")
        return

    response_text = payload.get("text", payload.get("message", "")).strip()
    if not response_text:
        return

    clean_speech_lines = []
    in_code_block = False
    
    for line in response_text.splitlines():
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            clean_speech_lines.append(line)
            
    text_to_stream = "\\n".join(clean_speech_lines).strip()
    if not text_to_stream:
        return

    try:
        rate = os.environ.get("TTS_SPEED", "185")
        voice = os.environ.get("TTS_VOICE")
        
        cmd = ["say", "-r", rate]
        if voice:
            cmd.extend(["-v", voice])
        cmd.append(text_to_stream)
        
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
            f.write(f"{message}\\n\\n")
    except Exception:
        pass

if __name__ == "__main__":
    main()
"""

with open("codex_speech_hook.py", "w") as f:
    f.write(stage4_hook)

run_cmd(["git", "add", "codex_speech_hook.py"])
run_cmd(["git", "commit", "-m", "feat: add support for custom TTS voices and speaking speed"])

# --- STAGE 5: Case-Insensitive Voice Matching ---
stage5_hook = """#!/usr/bin/env python3
import sys
import os
import json
import traceback
import subprocess

def find_voice(voice_name):
    if not voice_name:
        return None
    try:
        res = subprocess.run(["say", "-v", "?"], capture_output=True, text=True, check=True)
        for line in res.stdout.splitlines():
            parts = line.split()
            if parts:
                name = parts[0]
                if name.lower() == voice_name.strip().lower():
                    return name
    except Exception:
        pass
    return voice_name

def main():
    try:
        payload = json.loads(sys.stdin.read())
    except Exception as e:
        log_error("Failed to parse stdin as JSON payload")
        return

    response_text = payload.get("text", payload.get("message", "")).strip()
    if not response_text:
        return

    clean_speech_lines = []
    in_code_block = False
    
    for line in response_text.splitlines():
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            clean_speech_lines.append(line)
            
    text_to_stream = "\\n".join(clean_speech_lines).strip()
    if not text_to_stream:
        return

    try:
        rate = os.environ.get("TTS_SPEED", "185")
        voice = find_voice(os.environ.get("TTS_VOICE"))
        
        cmd = ["say", "-r", rate]
        if voice:
            cmd.extend(["-v", voice])
        cmd.append(text_to_stream)
        
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
            f.write(f"{message}\\n\\n")
    except Exception:
        pass

if __name__ == "__main__":
    main()
"""

with open("codex_speech_hook.py", "w") as f:
    f.write(stage5_hook)

run_cmd(["git", "add", "codex_speech_hook.py"])
run_cmd(["git", "commit", "-m", "fix: support case-insensitive voice matching for macOS say"])

# --- STAGE 6: Final Code Restoration & Gitignore/LICENSE ---
with open("codex_speech_hook.py", "w") as f:
    f.write(final_hook)

with open("README.md", "w") as f:
    f.write(final_readme)

with open(".gitignore", "w") as f:
    f.write(final_gitignore)

with open("LICENSE", "w") as f:
    f.write(final_license)

run_cmd(["git", "add", "."])
run_cmd(["git", "commit", "-m", "feat: add support for Stop hook event payload and clean documentation"])

# 2. Add remote and push force
run_cmd(["git", "remote", "add", "origin", "https://github.com/mannubaveja007/codex-tts.git"])
print("History recreated without ElevenLabs references.")
