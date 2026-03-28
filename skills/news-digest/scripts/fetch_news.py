#!/usr/bin/env python3
"""
News Digest — Fetches from 4 sources, deduplicates, and outputs clean results.
Sources: Google News RSS, GNews.io, NewsAPI.org, TheNewsAPI.com
"""

import json
import os
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher

# API Keys
GNEWS_KEY = os.environ.get("GNEWS_API_KEY", "13091aff49eacd9721f60c5a967e92d0")
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY", "6db3fdb9d4514e50949b6bc6e24d32fd")
THENEWSAPI_KEY = os.environ.get("THENEWSAPI_KEY", "uJNevPFM9tZ3kfxA0uWh5qz39mVK7zhbQrjuY5wS")

CATEGORIES = {
    "sports": {"emoji": "🏏", "label": "SPORTS", "gnews": "sports", "newsapi": "sports", "thenews": "sports", "goog": "sports+news+today"},
    "politics": {"emoji": "🏛️", "label": "POLITICS", "gnews": "nation", "newsapi": "general", "thenews": "politics", "goog": "politics+news+today"},
    "education": {"emoji": "📚", "label": "EDUCATION", "gnews": None, "newsapi": None, "thenews": None, "goog": "education+news+today+India"},
    "war": {"emoji": "⚔️", "label": "WAR/CONFLICT", "gnews": "world", "newsapi": None, "thenews": None, "goog": "war+conflict+news+today"},
    "tech": {"emoji": "💻", "label": "TECHNOLOGY/AI", "gnews": "technology", "newsapi": "technology", "thenews": "tech", "goog": "technology+AI+news+today"},
    "business": {"emoji": "📈", "label": "BUSINESS/MARKETS", "gnews": "business", "newsapi": "business", "thenews": "business", "goog": "stock+market+business+news+today"},
    "science": {"emoji": "🔬", "label": "SCIENCE", "gnews": "science", "newsapi": "science", "thenews": "science", "goog": "science+news+today"},
    "india": {"emoji": "🇮🇳", "label": "INDIA", "gnews": "nation", "newsapi": None, "thenews": None, "goog": "India+news+today"},
    "crypto": {"emoji": "🪙", "label": "CRYPTO/WEB3", "gnews": None, "newsapi": None, "thenews": None, "goog": "crypto+web3+bitcoin+news+today"},
    "entertainment": {"emoji": "🎬", "label": "ENTERTAINMENT", "gnews": "entertainment", "newsapi": "entertainment", "thenews": "entertainment", "goog": "entertainment+movies+news+today"},
    "climate": {"emoji": "🌍", "label": "CLIMATE/ENVIRONMENT", "gnews": None, "newsapi": None, "thenews": None, "goog": "climate+environment+news+today"},
    "startup": {"emoji": "🚀", "label": "STARTUP/FUNDING", "gnews": None, "newsapi": None, "thenews": None, "goog": "startup+funding+VC+news+today"},
}


def fetch_url(url, timeout=10):
    """Fetch URL and return response text."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-NewsDigest/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None


def fetch_google_rss(category):
    """Fetch from Google News RSS."""
    query = CATEGORIES[category]["goog"]
    url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    xml_data = fetch_url(url)
    if not xml_data:
        return []

    results = []
    try:
        root = ET.fromstring(xml_data)
        for item in root.findall(".//item")[:8]:
            title = item.findtext("title", "")
            source = item.findtext("source", "")
            pub_date = item.findtext("pubDate", "")
            if title:
                # Google RSS titles often have " - Source" at end
                if " - " in title and not source:
                    parts = title.rsplit(" - ", 1)
                    title = parts[0]
                    source = parts[1] if len(parts) > 1 else ""
                results.append({
                    "title": title.strip(),
                    "source": source.strip(),
                    "origin": "google_rss",
                    "category": category,
                    "date": pub_date,
                })
    except ET.ParseError:
        pass
    return results


def fetch_gnews(category):
    """Fetch from GNews.io API."""
    cat = CATEGORIES[category].get("gnews")
    if not cat or not GNEWS_KEY:
        return []

    url = f"https://gnews.io/api/v4/top-headlines?category={cat}&lang=en&country=in&max=5&apikey={GNEWS_KEY}"
    data = fetch_url(url)
    if not data:
        return []

    results = []
    try:
        j = json.loads(data)
        for article in j.get("articles", [])[:5]:
            results.append({
                "title": article.get("title", "").strip(),
                "source": article.get("source", {}).get("name", ""),
                "origin": "gnews",
                "category": category,
                "date": article.get("publishedAt", ""),
                "description": article.get("description", ""),
            })
    except json.JSONDecodeError:
        pass
    return results


def fetch_newsapi(category):
    """Fetch from NewsAPI.org."""
    cat = CATEGORIES[category].get("newsapi")
    if not cat or not NEWSAPI_KEY:
        return []

    url = f"https://newsapi.org/v2/top-headlines?category={cat}&country=in&pageSize=5&apiKey={NEWSAPI_KEY}"
    data = fetch_url(url)
    if not data:
        return []

    results = []
    try:
        j = json.loads(data)
        for article in j.get("articles", [])[:5]:
            title = article.get("title", "")
            if title and title != "[Removed]":
                results.append({
                    "title": title.strip(),
                    "source": article.get("source", {}).get("name", ""),
                    "origin": "newsapi",
                    "category": category,
                    "date": article.get("publishedAt", ""),
                    "description": article.get("description", ""),
                })
    except json.JSONDecodeError:
        pass
    return results


def fetch_thenewsapi(category):
    """Fetch from TheNewsAPI.com."""
    cat = CATEGORIES[category].get("thenews")
    if not cat or not THENEWSAPI_KEY:
        return []

    url = f"https://api.thenewsapi.com/v1/news/top?api_token={THENEWSAPI_KEY}&categories={cat}&locale=in&language=en&limit=5"
    data = fetch_url(url)
    if not data:
        return []

    results = []
    try:
        j = json.loads(data)
        for article in j.get("data", [])[:5]:
            results.append({
                "title": article.get("title", "").strip(),
                "source": article.get("source", ""),
                "origin": "thenewsapi",
                "category": category,
                "date": article.get("published_at", ""),
                "description": article.get("description", ""),
            })
    except json.JSONDecodeError:
        pass
    return results


def similarity(a, b):
    """Check title similarity to detect duplicates."""
    a_clean = a.lower().strip()
    b_clean = b.lower().strip()
    # Quick check for substring
    if a_clean in b_clean or b_clean in a_clean:
        return 1.0
    return SequenceMatcher(None, a_clean, b_clean).ratio()


def deduplicate(articles):
    """Remove duplicate articles based on title similarity."""
    unique = []
    for article in articles:
        is_dup = False
        for existing in unique:
            if similarity(article["title"], existing["title"]) > 0.6:
                is_dup = True
                # Keep the one with more info (description)
                if article.get("description") and not existing.get("description"):
                    unique.remove(existing)
                    unique.append(article)
                break
        if not is_dup:
            unique.append(article)
    return unique


def fetch_category(category):
    """Fetch from all 4 sources for a single category."""
    all_articles = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(fetch_google_rss, category): "google",
            executor.submit(fetch_gnews, category): "gnews",
            executor.submit(fetch_newsapi, category): "newsapi",
            executor.submit(fetch_thenewsapi, category): "thenews",
        }
        for future in as_completed(futures):
            try:
                results = future.result()
                if results:
                    all_articles.extend(results)
            except Exception:
                pass

    # Deduplicate
    unique = deduplicate(all_articles)
    return unique[:5]  # Top 5 per category


def main():
    """Main entry point."""
    today = datetime.now().strftime("%A, %d %B %Y")

    # Check for specific category argument
    requested = sys.argv[1] if len(sys.argv) > 1 else None

    if requested and requested in CATEGORIES:
        cats = {requested: CATEGORIES[requested]}
        max_per_cat = 8
    else:
        cats = CATEGORIES
        max_per_cat = 4

    # Fetch all categories in parallel
    all_results = {}
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(fetch_category, cat): cat for cat in cats}
        for future in as_completed(futures):
            cat = futures[future]
            try:
                articles = future.result()
                all_results[cat] = articles[:max_per_cat]
            except Exception:
                all_results[cat] = []

    # Output formatted digest
    print(f"📰 Daily News Digest — {today}")
    print()

    for cat_key in cats:
        cat_info = CATEGORIES[cat_key]
        articles = all_results.get(cat_key, [])

        print(f"{cat_info['emoji']} {cat_info['label']}")

        if not articles:
            print("• No headlines found")
        else:
            for i, article in enumerate(articles):
                source = f" ({article['source']})" if article.get("source") else ""
                bullet = "•"
                title = article["title"]
                # Bold first headline (most important)
                if i == 0:
                    title = f"**{title}**"
                print(f"{bullet} {title}{source}")
        print()

    # Sources summary
    sources_used = set()
    for articles in all_results.values():
        for a in articles:
            sources_used.add(a.get("origin", ""))

    source_names = {
        "google_rss": "Google News",
        "gnews": "GNews.io",
        "newsapi": "NewsAPI.org",
        "thenewsapi": "TheNewsAPI.com"
    }
    active = [source_names.get(s, s) for s in sources_used if s]
    if active:
        print(f"📡 Sources: {', '.join(sorted(active))}")

    print("\nReply with a category name for more details.")


if __name__ == "__main__":
    main()
