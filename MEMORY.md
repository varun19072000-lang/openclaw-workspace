# MEMORY.md — Long-Term Memory

_Curated knowledge about VK and this setup. Updated over time._

---

## About VK

- **Name:** Varun Gandhi — goes by **VK**
- **Timezone:** Asia/Calcutta (IST, UTC+5:30)
- **Channel:** Telegram (primary)
- **Communication style:** Short, abbreviated messages. Doesn't spell everything out. Gets straight to the point.
- **Preferences:** Bullet-point digests, no fluff, concise replies

## Interests & Usage Patterns

- **News** — asks for top news regularly, prefers categorised digest format
- **System status** — checks OpenClaw status periodically
- **AI/tech tools** — curious about how skills and tools work (asked about summarize skill, news-digest skill)
- **Active hours:** Late evening to early morning IST (18:00–03:30+)

## Setup & Config State

- **OpenClaw:** v2026.3.13, model: claude-sonnet-4-6
- **Brave API key:** ❌ Not configured — news-digest skill falls back to Google News RSS
- **news-digest skill:** Exists at `~/.openclaw/workspace/skills/news-digest/` but requires Brave API
- **MEMORY.md:** ✅ Created 2026-03-29
- **memory/2026-03-29.md:** ✅ Created

## Skills Available

- `news-digest` — workspace skill, uses Brave API (not configured), RSS fallback works
- `summarize` — for URLs/PDFs/YouTube links
- `weather` — via wttr.in
- `gog` — Gmail, Calendar, Drive (config status unknown)
- `coding-agent` — delegate coding tasks
- `github` — GitHub operations via gh CLI

## Notes / Lessons

- VK says "yes" to confirm things — treat it as approval to proceed with last proposed action
- When Brave API is unavailable, fetch from Google News RSS across multiple category searches — works well
- Always read startup files after compaction — compactions happen frequently (27+ in one session)

---

_Last updated: 2026-03-29_
