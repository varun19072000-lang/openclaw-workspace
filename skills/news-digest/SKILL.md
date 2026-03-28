---
name: news-digest
description: Fetch and present today's top news headlines across multiple categories. Use this skill whenever the user asks for news, headlines, "what's happening today", "top news", "news digest", "daily briefing", or similar.
---

# News Digest

When the user asks for news, top news, daily briefing, news digest, or similar:

1. Run the news digest script:
   ```bash
   python3 ~/.openclaw/workspace/skills/news-digest/scripts/fetch_news.py
   ```

2. Send the output directly to the user. Do not modify the format.

3. If the user asks for a **specific category** (e.g., "sports news", "crypto news"), run:
   ```bash
   python3 ~/.openclaw/workspace/skills/news-digest/scripts/fetch_news.py sports
   ```
   Valid categories: sports, politics, education, war, tech, business, science, india, crypto, entertainment, climate, startup

**IMPORTANT:** Always run the script. Do NOT try to fetch news yourself. The script combines 4 sources (Google News, GNews.io, NewsAPI.org, TheNewsAPI.com), deduplicates headlines, and formats everything.

**Shorthand:** The user may just say "news" or "digest" — run the full script.
