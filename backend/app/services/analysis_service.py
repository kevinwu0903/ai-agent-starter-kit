from __future__ import annotations

from datetime import datetime
from typing import List

from sklearn.linear_model import LogisticRegression

from app.config import get_settings
from app.schemas import (
    EventInsight,
    NewsArticle,
    PricePoint,
    StockAnalysisResponse,
    TechnicalIndicators,
    TrendPrediction,
)

from .news_service import NewsServiceError, classify_event, fetch_company_news
from .stock_service import (
    build_feature_matrix,
    compute_technical_indicators,
    fetch_stock_history,
)


def _history_to_models(history) -> List[PricePoint]:
    return [
        PricePoint(
            date=row["date"],
            open=float(row["open"]),
            high=float(row["high"]),
            low=float(row["low"]),
            close=float(row["close"]),
            volume=float(row["volume"]),
        )
        for _, row in history.iterrows()
    ]


def _news_to_models(news_items: List[dict]) -> List[NewsArticle]:
    articles: List[NewsArticle] = []
    for item in news_items:
        articles.append(
            NewsArticle(
                title=item.get("title"),
                summary=item.get("summary"),
                published_at=item.get("published_at", datetime.utcnow()),
                source=item.get("source"),
                url=item.get("url"),
                sentiment_score=item.get("sentiment_score"),
                sentiment_label=item.get("sentiment_label"),
            )
        )
    return articles


def _generate_prediction(features, targets):
    model = LogisticRegression(max_iter=500, class_weight="balanced")
    model.fit(features, targets)
    latest_features = features.iloc[-1].values.reshape(1, -1)
    probabilities = model.predict_proba(latest_features)[0]

    probability_down = float(probabilities[0])
    probability_up = float(probabilities[1])
    if probability_up >= probability_down:
        expected_trend = "看多"
    else:
        expected_trend = "偏空"

    rationale_parts = [
        f"模型以近 {len(features)} 天的量價與技術指標訓練",
        f"最新特徵顯示上漲機率 {probability_up:.2%}, 下跌機率 {probability_down:.2%}",
    ]

    return TrendPrediction(
        probability_up=probability_up,
        probability_down=probability_down,
        expected_trend=expected_trend,
        rationale="；".join(rationale_parts),
    )


def _build_event_insights(news: List[NewsArticle]) -> List[EventInsight]:
    insights: List[EventInsight] = []
    for article in news:
        category, confidence = classify_event(article.dict())
        insights.append(
            EventInsight(
                category=category,
                description=article.title,
                sentiment_label=article.sentiment_label,
                confidence=confidence,
            )
        )
    return insights


def analyze_stock(symbol: str) -> StockAnalysisResponse:
    settings = get_settings()

    stock_data = fetch_stock_history(symbol)
    indicators = compute_technical_indicators(stock_data.history)
    features, targets = build_feature_matrix(stock_data.history)
    prediction = _generate_prediction(features, targets)

    history_models = _history_to_models(stock_data.history.tail(settings.history_window))

    latest_row = stock_data.history.iloc[-1]
    previous_row = stock_data.history.iloc[-2] if len(stock_data.history) >= 2 else latest_row
    last_price = float(latest_row["close"])
    price_change = float(latest_row["close"] - previous_row["close"])
    percent_change = float(price_change / previous_row["close"] * 100) if previous_row["close"] else None

    try:
        news_items = fetch_company_news(stock_data.symbol, limit=settings.news_limit)
    except NewsServiceError:
        news_items = []
    news_models = _news_to_models(news_items)
    event_insights = _build_event_insights(news_models)

    return StockAnalysisResponse(
        symbol=stock_data.symbol,
        exchange_symbol=stock_data.exchange_symbol,
        company_name=stock_data.company_name,
        last_price=last_price,
        price_change=price_change,
        percent_change=percent_change,
        history=history_models,
        indicators=TechnicalIndicators(**indicators),
        prediction=prediction,
        news=news_models,
        event_insights=event_insights,
        generated_at=datetime.utcnow(),
    )
