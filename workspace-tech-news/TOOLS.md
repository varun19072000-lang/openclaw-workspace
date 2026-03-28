# TOOLS.md - Tech News Agent Tools

## News Fetching

When asked for tech news, run this command:
```bash
python3 /Users/varun_ssd/.openclaw/workspace/skills/news-digest/scripts/fetch_news.py tech
```

For startup-specific news, also run:
```bash
python3 /Users/varun_ssd/.openclaw/workspace/skills/news-digest/scripts/fetch_news.py startup
```

This fetches from 4 sources (Google News RSS, GNews.io, NewsAPI.org, TheNewsAPI.com), deduplicates, and outputs formatted results.

**IMPORTANT:** ALWAYS run this command when asked for news. Don't make up headlines.

## Deep Dive Research

For follow-up questions or detailed info, use the `researcher` subagent:
- Ask it to web_search for specific product details, company info, funding rounds
- It has access to web_search and web_fetch tools

## Response Format

When presenting news:
1. Lead with the biggest story
2. Tag each: [AI] [Startup] [Gadget] [Security] [Cloud]
3. Each headline: **bold title** — source — 1-line summary
4. Offer: "Want me to dig deeper on any of these?"

When answering follow-ups:
- Explain technical concepts simply
- Highlight what matters for builders and founders
