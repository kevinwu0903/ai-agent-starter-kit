from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PricePoint(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class TechnicalIndicators(BaseModel):
    moving_average_5: Optional[float]
    moving_average_20: Optional[float]
    moving_average_60: Optional[float]
    rsi_14: Optional[float]
    macd: Optional[float]
    macd_signal: Optional[float]


class TrendPrediction(BaseModel):
    probability_up: float = Field(..., ge=0.0, le=1.0)
    probability_down: float = Field(..., ge=0.0, le=1.0)
    expected_trend: str
    rationale: str


class NewsArticle(BaseModel):
    title: str
    summary: Optional[str]
    published_at: datetime
    source: Optional[str]
    url: str
    sentiment_score: Optional[float]
    sentiment_label: Optional[str]


class EventInsight(BaseModel):
    category: str
    description: str
    sentiment_label: Optional[str]
    confidence: Optional[float]


class StockAnalysisResponse(BaseModel):
    symbol: str
    exchange_symbol: str
    company_name: Optional[str]
    last_price: Optional[float]
    price_change: Optional[float]
    percent_change: Optional[float]
    history: List[PricePoint]
    indicators: TechnicalIndicators
    prediction: TrendPrediction
    news: List[NewsArticle]
    event_insights: List[EventInsight]
    generated_at: datetime

