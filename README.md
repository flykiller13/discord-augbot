# augbot

A small Discord bot that watches one specific user and replies **"I never asked for this."** whenever they mention a Deus Ex keyword.

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
