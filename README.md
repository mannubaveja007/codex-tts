# Codex TTS: Automated Local Playback for Codex CLI

An automated Text-to-Speech (TTS) pipeline for the OpenAI Codex CLI using the native macOS `say` speech engine.

## Installation
1. Copy the hook script to `/usr/local/bin`:
   ```bash
   sudo cp codex_speech_hook.py /usr/local/bin/codex_speech_hook.py
   sudo chmod +x /usr/local/bin/codex_speech_hook.py
   ```
