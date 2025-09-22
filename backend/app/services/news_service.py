from __future__ import annotations

import html
import re
from datetime import datetime
from typing import List, Tuple
from urllib.parse import quote_plus

import feedparser
from cachetools import TTLCache, cached

try:  # SnowNLP is optional but provides Chinese sentiment analysis
    from snownlp import SnowNLP  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    SnowNLP = None

_CACHE = TTLCache(maxsize=64, ttl=600)


class NewsServiceError(Exception):
    """Raised when news could not be loaded."""


def _clean_text(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _compute_sentiment(text: str) -> Tuple[float | None, str | None]:
    if not text:
        return None, None

    if SnowNLP is None:
        return None, None

    try:
        score = SnowNLP(text).sentiments
    except Exception:  # pragma: no cover - SnowNLP failure
        return None, None

    if score >= 0.65:
        label = "positive"
    elif score <= 0.35:
        label = "negative"
    else:
        label = "neutral"
    return float(score), label


@cached(_CACHE)
def fetch_company_news(keyword: str, limit: int = 8) -> List[dict]:
    query = quote_plus(f"{keyword} 台股")
    url = (
        "https://news.google.com/rss/search?q="
        f"{query}&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant"
    )
    parsed = feedparser.parse(url)
    if parsed.bozo:  # pragma: no cover - feedparser attribute when parsing fails
        raise NewsServiceError(f"Unable to parse news feed for {keyword}")

    articles: List[dict] = []
    for entry in parsed.entries[:limit]:
        summary = _clean_text(entry.get("summary", ""))
        title = _clean_text(entry.get("title", ""))
        score, label = _compute_sentiment(f"{title} {summary}")
        published = entry.get("published") or entry.get("updated")
        published_dt = (
            datetime(*entry.published_parsed[:6]) if getattr(entry, "published_parsed", None) else datetime.utcnow()
        )
        articles.append(
            {
                "title": title,
                "summary": summary,
                "published_at": published_dt,
                "source": entry.get("source", {}).get("title") if entry.get("source") else entry.get("author"),
                "url": entry.get("link"),
                "sentiment_score": score,
                "sentiment_label": label,
            }
        )
    return articles


def classify_event(article: dict) -> Tuple[str, float | None]:
    text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
    if any(keyword in text for keyword in ["earnings", "financial", "財報", "營收"]):
        return "財務表現", 0.8
    if any(keyword in text for keyword in ["政策", "政府", "regulation", "法規", "政策"]):
        return "政策監管", 0.6
    if any(keyword in text for keyword in ["supply", "供應", "缺料", "supply chain"]):
        return "供應鏈", 0.5
    if any(keyword in text for keyword in ["經濟", "inflation", "通膨", "gdp", "利率", "利息"]):
        return "總體經濟", 0.6
    return "一般新聞", None
