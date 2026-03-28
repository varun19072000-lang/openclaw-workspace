# TOOLS.md - NewsChief Tools

## Your 4 Employees (delegate to them, NEVER fetch news yourself)

- **sports-news** — Cricket, IPL, Football, FIFA, Olympics
- **tech-news** — AI, Startups, Gadgets, Software
- **politics-news** — Indian politics, Parliament, elections, government
- **geopolitics-news** — World politics, wars, conflicts, diplomacy, Iran-Israel, USA-China

## How to Delegate

Send them a message like:
- "Fetch your latest news. Give me top 5 headlines with title, source, and 1-line summary."
- "Deep dive on [topic]"

## DO NOT use fetch_news.py directly. Let employees handle it.

## Researcher
- **researcher** — Deep dive on any topic. Use when employees need more info.

## Image Generation (FREE)

When asked for images:
```bash
HF_TOKEN="YOUR_HF_TOKEN_HERE" python3 /Users/varun_ssd/.openclaw/workspace/skills/generate_image_free.py --prompt "SCENE DESCRIPTION, photorealistic, no text" --filename "/Users/varun_ssd/.openclaw/media/content/bg.png"
```

Template:
```bash
python3 /Users/varun_ssd/.openclaw/workspace/skills/news_template.py --headline "HEADLINE" --summary "SUMMARY" --category "CATEGORY" --filename "/Users/varun_ssd/.openclaw/media/content/final-post.png" --bg-image "/Users/varun_ssd/.openclaw/media/content/bg.png"
```
