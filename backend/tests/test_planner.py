from datetime import date

import pytest

from app.models import PlanRequest
from app.planner import build_plan


def request(**overrides):
    values = {
        "origin_city": "Guwahati", "destination": "Shillong", "start_date": date(2026, 11, 10),
        "end_date": date(2026, 11, 12), "travelers": 2, "budget": 12000, "currency": "INR", "pace": "balanced",
        "traveller_type": "couple", "interests": ["outdoors", "food"], "dietary_restrictions": [],
        "enhance_with_ai": False,
    }
    values.update(overrides)
    return PlanRequest(**values)


def test_plan_is_deterministic_and_has_no_duplicates():
    first = build_plan(request())
    second = build_plan(request())
    assert first.days == second.days
    assert first.estimated_total == second.estimated_total
    ids = [item.activity.id for day in first.days for item in day.activities]
    assert len(ids) == len(set(ids))


def test_interest_and_dietary_constraints_are_explainable():
    plan = build_plan(request(interests=["food"], dietary_restrictions=["vegan"]))
    food = [item.activity for day in plan.days for item in day.activities if item.activity.category == "Food"]
    assert all("vegan" in item.dietary_options for item in food)
    assert any(item.reasons for day in plan.days for item in day.activities)


def test_invalid_destination_is_rejected():
    with pytest.raises(ValueError, match="supports Shillong"):
        build_plan(request(destination="Goa"))


def test_date_range_is_validated():
    with pytest.raises(ValueError):
        request(end_date=date(2026, 11, 1))


def test_shillong_plan_uses_its_own_curated_data():
    plan = build_plan(request(interests=["outdoors", "nature"]))
    assert plan.destination == "Shillong"
    assert plan.destination_country == "India"
    assert plan.currency == "INR"
    ids = [item.activity.id for day in plan.days for item in day.activities]
    assert all(activity_id.startswith((
        "umiam", "ward", "elephant", "living-root", "mawsmai", "nohkalikai", "laitlum",
        "police-bazar", "khasi", "cafe-shillong", "mawlynnong", "shillong-peak", "wahkaba",
    )) for activity_id in ids)
    assert plan.seasonal_note is not None


def test_stay_suggestions_are_included():
    plan = build_plan(request())
    assert len(plan.stay_suggestions) == 3
    assert all(stay.price_per_night > 0 for stay in plan.stay_suggestions)


def test_cost_breakdown_matches_estimated_total():
    plan = build_plan(request())
    assert round(sum(row.amount for row in plan.cost_breakdown), 2) == plan.estimated_total


def test_traveller_type_changes_which_activities_are_chosen():
    shared = dict(
        start_date=date(2026, 11, 10), end_date=date(2026, 11, 11), budget=8000, pace="balanced",
        interests=["outdoors", "adventure"],
    )
    family_ids = {item.activity.id for day in build_plan(request(traveller_type="family", **shared)).days for item in day.activities}
    friends_ids = {item.activity.id for day in build_plan(request(traveller_type="friends", **shared)).days for item in day.activities}
    # The 6-hour adventure trek is penalised for a family trip and boosted for a friends trip.
    assert "living-root-bridge" not in family_ids
    assert "living-root-bridge" in friends_ids


def test_alternatives_never_include_the_chosen_activity():
    plan = build_plan(request())
    for day in plan.days:
        for item in day.activities:
            assert item.activity.id not in {alt.id for alt in item.alternatives}
