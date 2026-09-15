"""Optional Claude enhancement layer.

The deterministic planner remains authoritative. Claude may only rewrite the
explanation, so it cannot invent activities, prices, timings, or constraints.
"""

import json
import os

from anthropic import APIError, Anthropic
from dotenv import load_dotenv

from .models import PlanResponse

load_dotenv()


def enhance_plan(plan: PlanResponse) -> PlanResponse:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return plan

    model = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
    client = Anthropic(api_key=api_key)
    facts = json.dumps(plan.model_dump(mode="json"), separators=(",", ":"))
    prompt = (
        "You are the copy editor for a travel itinerary. Rewrite only the "
        "planning explanation in 2 concise sentences. Use only facts present "
        "in the JSON. Do not add, remove, reorder, or modify activities, "
        "prices, timings, dates, or travel claims. Return plain text only.\n\n"
        f"ITINERARY JSON:\n{facts}"
    )
    try:
        message = client.messages.create(
            model=model,
            max_tokens=120,
            temperature=0,
            system="Be accurate, warm, and concise.",
            messages=[{"role": "user", "content": prompt}],
        )
    except APIError:
        # AI copy is optional; the verified deterministic plan is still valid.
        return plan

    text = "".join(block.text for block in message.content if block.type == "text").strip()
    if not text:
        return plan
    plan.ai_summary = text
    plan.ai_enhanced = True
    return plan
