# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`augbot.py` is a single-file Discord bot built on `discord.py` (2.7.1). It watches one specific user and replies whenever that user's messages mention Deus Ex–related keywords. Replies escalate in sass based on how many days have passed since the last mention.

## Architecture

All logic lives in `augbot.py`:

- **Keyword detection** — `on_message` short-circuits on bot authors and on any author other than `WATCHED_USER_ID`, then matches `message.content.lower()` against `DEUS_EX_KEYWORDS`. Requires the **message content** privileged intent (`intents.message_content = True`), which must also be enabled in the Discord Developer Portal.

- **Mention streak tracking** — the date of the last keyword hit is persisted as an ISO date string in `last_mention.txt` (via `read_last_mention` / `write_last_mention`, both tolerant of a missing/empty/corrupt file). On each hit the bot:
  1. Returns early without replying if the last mention was already today (one reply per day max).
  2. Otherwise records today's date and computes the day gap.

- **Tiered responses** — `get_response(days)` picks a random quote from a tier keyed by the gap: `None` (first ever) → 1–3 (`DAY_SHORT`) → 4–7 (`DAY_MID`) → 8–13 (`DAY_HIGH`) → 14+ (`DAY_LEGENDARY`). `{days}` is interpolated only in the higher tiers. The reply is prefixed with `message.author.mention` to ping the watched user.

- **Debug `[kd]` prefix** — a message starting with `[kd]` ("keep date") still triggers a reply but skips `write_last_mention`, so the stored date is preserved. Useful for testing the day tiers without resetting the streak.

## Configuration

Configuration is read from environment variables, loaded from a `.env` file via `python-dotenv` (`load_dotenv()` at startup):

- `DISCORD_TOKEN` — the bot token.
- `WATCHED_USER_ID` — the watched user's ID; read as a string and cast with `int()`.
- `LAST_MENTION_FILE` — optional; path to the streak-state file (defaults to `last_mention.txt`). The Docker image sets this to `/data/last_mention.txt` so state lives on a persisted volume.

`DISCORD_TOKEN` and `WATCHED_USER_ID` are required; the bot raises `KeyError` on startup if either is missing.

## Running

### Local venv

The project uses a local `venv`. Install dependencies from `requirements.txt` (`discord.py==2.7.1`, `python-dotenv==1.2.2`):

```powershell
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe augbot.py
```

### Docker

The bot is containerized via `Dockerfile` (Python 3.13-slim, runs as non-root `appuser`) and `docker-compose.yml`. Streak state is persisted to a `/data` volume, and config is read from `.env` (`env_file: .env`).

Build and run with Compose (recommended — wires up the `.env` file and the `augbot-data` volume automatically):

```powershell
docker compose up -d --build      # build the image and start in the background
docker compose logs -f            # follow logs (stdout/stderr are unbuffered)
docker compose down               # stop and remove the container
```

Or build and run the image directly:

```powershell
docker build -t augbot .
docker run -d --name augbot --restart unless-stopped --env-file .env -v augbot-data:/data augbot
```
