from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.schemas import StockAnalysisResponse
from app.services.analysis_service import analyze_stock
from app.services.stock_service import StockDataError

settings = get_settings()

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/analysis/{symbol}", response_model=StockAnalysisResponse)
def stock_analysis(symbol: str) -> StockAnalysisResponse:
    try:
        return analyze_stock(symbol)
    except StockDataError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - fallback guard
        raise HTTPException(status_code=500, detail="Unexpected server error") from exc
