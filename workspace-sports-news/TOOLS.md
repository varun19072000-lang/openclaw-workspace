# TOOLS.md - Sports News Agent Tools

## News Fetching

When asked for sports news, run this command:
```bash
python3 /Users/varun_ssd/.openclaw/workspace/skills/news-digest/scripts/fetch_news.py sports
```

This fetches from 4 sources (Google News RSS, GNews.io, NewsAPI.org, TheNewsAPI.com), deduplicates, and outputs formatted results.

**IMPORTANT:** ALWAYS run this command when asked for news. Don't make up headlines.

## Deep Dive Research

For follow-up questions or detailed info, use the `researcher` subagent:
- Ask it to web_search for specific match scores, player stats, tournament details
- It has access to web_search and web_fetch tools

## Response Format

When presenting news:
1. Lead with the biggest story
2. Each headline: **bold title** — source — 1-line summary
3. Offer: "Want me to dig deeper on any of these?"

When answering follow-ups:
- Give specific details: scores, stats, player names, dates
- Cite sources when possible
