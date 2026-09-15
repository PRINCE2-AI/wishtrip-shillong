import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .ai import enhance_plan
from .data import DESTINATIONS
from .models import PlanRequest, PlanResponse
from .planner import build_plan

load_dotenv()

app = FastAPI(title="Wishtrip API", version="1.0.0", description="Deterministic trip planning prototype")

default_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
extra_origins = [origin.strip() for origin in os.getenv("FRONTEND_ORIGINS", "").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=default_origins + extra_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    total_activities = sum(len(entry["activities"]) for entry in DESTINATIONS.values())
    return {"status": "ok", "destinations": list(DESTINATIONS.keys()), "activities": total_activities}


@app.get("/api/destinations")
def destinations():
    return {
        "destinations": [
            {
                "id": key,
                "name": entry["display_name"],
                "country": entry["country"],
                "currency": entry["currency"],
                "activity_count": len(entry["activities"]),
            }
            for key, entry in DESTINATIONS.items()
        ]
    }


@app.post("/api/plan", response_model=PlanResponse)
def plan_trip(request: PlanRequest):
    try:
        result = build_plan(request)
        return enhance_plan(result) if request.enhance_with_ai else result
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
