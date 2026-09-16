from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator


Pace = Literal["relaxed", "balanced", "packed"]


class PlanRequest(BaseModel):
    origin_city: str = Field(default="Mumbai", min_length=1, max_length=80)
    destination: str = Field(min_length=1, max_length=80)
    start_date: date
    end_date: date
    travelers: int = Field(default=2, ge=1, le=12)
    budget: float = Field(default=12000, gt=0, le=1000000)
    currency: Literal["INR"] = "INR"
    pace: Pace = "balanced"
    traveller_type: Literal["solo", "couple", "family", "friends", "seniors"] = "couple"
    interests: list[str] = Field(default_factory=list, max_length=8)
    dietary_restrictions: list[str] = Field(default_factory=list, max_length=6)
    accessibility: bool = False
    enhance_with_ai: bool = True
    lodging_area: str = "Police Bazar"

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, value: date, info):
        start = info.data.get("start_date")
        if start and value < start:
            raise ValueError("end_date must be on or after start_date")
        if start and (value - start).days > 13:
            raise ValueError("Trips are limited to 14 days in this prototype")
        return value

    @field_validator("interests", "dietary_restrictions")
    @classmethod
    def normalize_list(cls, values: list[str]):
        return [value.strip().lower() for value in values if value.strip()]


class Activity(BaseModel):
    id: str
    name: str
    category: str
    description: str
    tags: list[str]
    neighborhood: str
    latitude: float
    longitude: float
    duration_hours: float = Field(gt=0)
    price_per_person: float = Field(ge=0)
    opening_hours: str
    open_weekdays: list[int]
    best_time: str
    indoor: bool = False
    accessible: bool = True
    dietary_options: list[str] = Field(default_factory=list)
    popularity: float = Field(ge=0, le=1)
    image: str
    insider_tip: str
    local_story: str
    local_name: str | None = None
    etiquette_note: str | None = None
    myth_fact: str | None = None


class PlannedActivity(BaseModel):
    activity: Activity
    day: int
    date: date
    slot: Literal["morning", "afternoon", "evening"]
    start_time: str
    end_time: str
    travel_minutes_from_previous: int
    score: float
    reasons: list[str]
    alternatives: list[Activity] = Field(default_factory=list)


class DayPlan(BaseModel):
    day: int
    date: date
    theme: str
    activities: list[PlannedActivity]
    estimated_cost: float
    walking_km: float
    total_hours: float


class CostBreakdown(BaseModel):
    category: str
    amount: float


class PlanResponse(BaseModel):
    origin_city: str
    destination: str
    destination_country: str = ""
    start_date: date
    end_date: date
    travelers: int
    traveller_type: str
    currency: str
    budget: float
    estimated_total: float
    cost_breakdown: list[CostBreakdown] = Field(default_factory=list)
    days: list[DayPlan]
    unfilled_days: list[int]
    methodology: list[str]
    seasonal_note: str | None = None
    ai_summary: str | None = None
    ai_enhanced: bool = False
    generated_at: str
