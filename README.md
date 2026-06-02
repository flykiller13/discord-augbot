# augbot

A small Discord bot that watches one specific user and snaps back with a Deus Ex–flavoured quip whenever they mention a Deus Ex keyword (`deus ex`, `jensen`, `illuminati`, `aug`, …).

The sass escalates based on how long they managed to *not* mention it. The longer the streak before they slip, the more dramatic the reply:

- **1–3 days** — short, dismissive.
- **4–7 days** — a respectable attempt, grudgingly acknowledged.
- **8–13 days** — impressed disappointment.
- **14+ days** — legendary betrayal.

The streak is tracked in `last_mention.txt` (the ISO date of the last keyword hit) and the bot replies at most once per day.

## Setup

```powershell
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Then edit `.env` with your values.

## Configuration

Set these in `.env`:

- `DISCORD_TOKEN` — your bot token from the Discord Developer Portal.
- `WATCHED_USER_ID` — the Discord user ID to watch (enable Developer Mode, right-click a user → Copy User ID).

## Running

```powershell
venv\Scripts\python.exe augbot.py
```

The **message content** privileged intent must be enabled for the bot in the Discord Developer Portal (the bot needs to read message text to match keywords).

## Debugging

Prefix a message with `[kd]` ("keep date") to trigger a reply without updating the stored streak date. This lets you exercise the day tiers without resetting `last_mention.txt`.
