# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`augbot.py` is a single-file Discord bot built on `discord.py` (2.7.1). It watches one specific user and replies "I never asked for this." whenever that user's messages mention Deus Ex–related keywords.

## Architecture

- **`augbot.py`** — the entire bot. Key elements:
  - `on_message` short-circuits on bot authors and on any author other than `WATCHED_USER_ID`, then matches `message.content.lower()` against `DEUS_EX_KEYWORDS`.
  - Requires the **message content** privileged intent (`intents.message_content = True`), which must also be enabled in the Discord Developer Portal for the bot.

## Configuration

Configuration is read from environment variables, loaded from a `.env` file via `python-dotenv` (`load_dotenv()` at startup):

- `DISCORD_TOKEN` — the bot token.
- `WATCHED_USER_ID` — the watched user's ID; read as a string and cast with `int()`.

Both are required; the bot raises `KeyError` on startup if either is missing.

## Running

The project uses a local `venv`. Install dependencies from `requirements.txt` (`discord.py==2.7.1`, `python-dotenv==1.2.2`):

```powershell
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe augbot.py
```
