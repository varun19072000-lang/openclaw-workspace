# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Available Workspace Skills

These skills are in `skills/` — read their SKILL.md before use:

- **news-digest** (`skills/news-digest/SKILL.md`) — When user asks for "news", "top news", "news digest", "daily briefing", or "what's happening today": run `python3 ~/.openclaw/workspace/skills/news-digest/scripts/fetch_news.py`. Combines 4 news sources, deduplicates, and formats output. For specific category: add category name as argument (e.g., `fetch_news.py sports`).
- **gog** (`skills/gog/SKILL.md`) — Gmail, Calendar, Drive, Contacts, Sheets, Docs via `gog` CLI.
- **screenshot** (`skills/screenshot/SKILL.md`) — Capture desktop screenshots.
- **summarize** (`skills/summarize/SKILL.md`) — Summarize text.

**IMPORTANT:** When a user's request matches a skill above, ALWAYS read the skill's SKILL.md first and follow its instructions exactly.

---

Add whatever helps you do your job. This is your cheat sheet.
