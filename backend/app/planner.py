"""Deterministic, explainable itinerary generator."""

from datetime import date, datetime, timedelta, timezone
from math import cos, radians, sqrt

from .data import get_destination
from .models import Activity, CostBreakdown, DayPlan, PlanRequest, PlanResponse, PlannedActivity

PACE_TARGETS = {"relaxed": (1, 2), "balanced": (2, 3), "packed": (3, 4)}
SLOTS = {"morning": ("09:00", "12:30"), "afternoon": ("13:30", "17:00"), "evening": ("18:00", "21:00")}


def distance_km(a: tuple[float, float], b: tuple[float, float]) -> float:
    lat1, lon1, lat2, lon2 = map(radians, (*a, *b))
    x = (lon2 - lon1) * cos((lat1 + lat2) / 2)
    y = lat2 - lat1
    return sqrt(x * x + y * y) * 6371


def _interest_score(activity: Activity, interests: set[str]) -> float:
    if not interests:
        return 0.7
    return min(1, len(set(activity.tags) & interests) / max(1, min(2, len(interests))))


def _party_fit(activity: Activity, traveller_type: str) -> tuple[float, str | None]:
    """How well an activity suits the traveller party, beyond raw interest match."""
    tags = set(activity.tags)
    if traveller_type == "family":
        if activity.duration_hours > 4 or "adventure" in tags:
            return 0.25, None
        if activity.category in ("Museum", "Workshop") or "nature" in tags:
            return 1.0, "Great pick for a family day"
        return 0.75, None
    if traveller_type == "seniors":
        if activity.duration_hours > 3 or "adventure" in tags or not activity.accessible:
            return 0.2, None
        return 0.9, "Gentle pace, well suited for seniors"
    if traveller_type in ("solo", "friends"):
        if "nightlife" in tags or "adventure" in tags:
            return 1.0, "A favourite for solo/friends trips"
        return 0.75, None
    return 0.8, None  # couple, or unrecognised type: neutral, no strong bias


def _fits_diet(activity: Activity, restrictions: set[str]) -> bool:
    if not restrictions or activity.category != "Food":
        return True
    return restrictions.issubset(set(activity.dietary_options))


def _is_open(activity: Activity, trip_date: date) -> bool:
    return trip_date.weekday() in activity.open_weekdays


def _score(activity: Activity, request: PlanRequest, previous: Activity | None, anchors: dict) -> tuple[float, list[str]]:
    interests = set(request.interests)
    interest = _interest_score(activity, interests)
    budget_fit = max(0, 1 - activity.price_per_person / max(request.budget / request.travelers, 1))
    default_anchor = next(iter(anchors.values()))
    origin = anchors.get(request.lodging_area, default_anchor) if previous is None else (previous.latitude, previous.longitude)
    proximity = max(0, 1 - distance_km(origin, (activity.latitude, activity.longitude)) / 12)
    pace_fit = 1 if activity.duration_hours <= (2.5 if request.pace == "relaxed" else 3.5) else .65
    party_fit, party_reason = _party_fit(activity, request.traveller_type)
    total = .35 * interest + .2 * budget_fit + .2 * proximity + .1 * pace_fit + .1 * activity.popularity + .05 * party_fit
    reasons = []
    if interests and set(activity.tags) & interests:
        reasons.append(f"Matches {', '.join(sorted(set(activity.tags) & interests))}")
    elif not interests:
        reasons.append("Strong local staple")
    if party_reason:
        reasons.append(party_reason)
    if proximity > .7:
        reasons.append("Near your previous stop")
    if activity.price_per_person == 0:
        reasons.append("Free entry protects your budget")
    elif budget_fit > .8:
        reasons.append("Comfortable within your budget")
    if activity.best_time in ("morning", "afternoon", "evening"):
        reasons.append(f"Best experienced in the {activity.best_time}")
    return round(total, 3), reasons[:3]


def _candidate_pool(request: PlanRequest, trip_date: date, used: set[str], activities: list[Activity]) -> list[Activity]:
    candidates = []
    for activity in activities:
        if activity.id in used or not _is_open(activity, trip_date) or not _fits_diet(activity, set(request.dietary_restrictions)):
            continue
        if request.accessibility and not activity.accessible:
            continue
        candidates.append(activity)
    return candidates


def build_plan(request: PlanRequest) -> PlanResponse:
    destination = get_destination(request.destination)
    if destination is None:
        raise ValueError(
            "This prototype currently supports Shillong. More destinations are on the roadmap."
        )
    activities = destination["activities"]
    anchors = destination["anchors"]

    days: list[DayPlan] = []
    used: set[str] = set()
    running_cost = 0.0
    category_cost: dict[str, float] = {}
    current = request.start_date
    day_number = 1
    while current <= request.end_date:
        target_min, target_max = PACE_TARGETS[request.pace]
        chosen: list[PlannedActivity] = []
        previous: Activity | None = None
        hours = 0.0
        walking = 0.0
        cost = 0.0
        pool = _candidate_pool(request, current, used, activities)
        for slot in ("morning", "afternoon", "evening"):
            if len(chosen) >= target_max:
                break
            options = []
            for activity in pool:
                if activity.id in used or activity.best_time != slot:
                    continue
                if hours + activity.duration_hours > (7.5 if request.pace == "relaxed" else 9):
                    continue
                # Keep the trip spend deterministic and avoid using the entire budget early.
                projected = running_cost + (cost + activity.price_per_person) * request.travelers
                if projected > request.budget * 1.08 and len(chosen) >= target_min:
                    continue
                score, reasons = _score(activity, request, previous, anchors)
                options.append((score, activity, reasons))
            if not options:
                continue
            options.sort(key=lambda row: (-row[0], row[1].id))
            score, activity, reasons = options[0]
            # Next-best options in this slot become client-side swap suggestions.
            alternatives = [row[1] for row in options[1:3]]
            start_time, end_time = SLOTS[slot]
            travel = 0 if previous is None else round(distance_km((previous.latitude, previous.longitude), (activity.latitude, activity.longitude)) * 12)
            walking += 0 if previous is None else distance_km((previous.latitude, previous.longitude), (activity.latitude, activity.longitude))
            chosen.append(PlannedActivity(
                activity=activity, day=day_number, date=current, slot=slot,
                start_time=start_time, end_time=end_time, travel_minutes_from_previous=travel,
                score=score, reasons=reasons, alternatives=alternatives,
            ))
            used.add(activity.id)
            category_cost[activity.category] = category_cost.get(activity.category, 0) + activity.price_per_person * request.travelers
            previous, hours, cost = activity, hours + activity.duration_hours, cost + activity.price_per_person
        if chosen:
            theme = " + ".join(dict.fromkeys(item.activity.category for item in chosen))
            days.append(DayPlan(day=day_number, date=current, theme=theme, activities=chosen,
                                estimated_cost=round(cost * request.travelers, 2),
                                walking_km=round(walking, 1), total_hours=round(hours, 1)))
            running_cost += cost * request.travelers
        day_number += 1
        current += timedelta(days=1)
    expected_days = (request.end_date - request.start_date).days + 1
    planned_day_numbers = {day.day for day in days}
    unfilled = [number for number in range(1, expected_days + 1) if number not in planned_day_numbers]
    cost_breakdown = [
        CostBreakdown(category=category, amount=round(amount, 2))
        for category, amount in sorted(category_cost.items(), key=lambda row: -row[1])
    ]
    seasonal_note = destination["seasonal_notes"].get(request.start_date.month)
    return PlanResponse(
        origin_city=request.origin_city, destination=destination["display_name"],
        destination_country=destination["country"], start_date=request.start_date,
        end_date=request.end_date, travelers=request.travelers, traveller_type=request.traveller_type,
        currency=request.currency, budget=request.budget,
        estimated_total=round(running_cost, 2), cost_breakdown=cost_breakdown,
        days=days, unfilled_days=unfilled,
        methodology=[
            "Hard filters: opening weekday, dietary/accessibility needs, no duplicate stops.",
            "Ranking: 35% interest match, 20% proximity, 20% budget fit, 10% pace, 10% popularity, 5% party fit.",
            "Party fit downweights long/adventurous stops for family & seniors trips, and favours them for solo/friends trips.",
            "Time blocks prevent overlap; daily activity hours stay under the selected pace limit.",
            f"Travel time uses straight-line {destination['display_name']} coordinates × 12 and is a planning estimate.",
            f"Plan shaped for a {request.traveller_type} trip departing from {request.origin_city}.",
        ],
        seasonal_note=seasonal_note,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )
