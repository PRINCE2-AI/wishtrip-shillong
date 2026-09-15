# Wishtrip · Shillong prototype

Wishtrip is a focused trip-planning prototype for one deeply modeled destination — **Shillong, Meghalaya (Northeast India)** — instead of shallow, broad coverage. It pairs a responsive React/Vite/TypeScript interface with a FastAPI/Pydantic API and a deterministic, explainable planning engine. An optional Claude layer only polishes the explanation copy; it never invents or changes activities, prices, or timings.

## Architecture

```
frontend/  React + Vite + TypeScript, react-leaflet for route maps
   src/main.tsx     UI, state, API calls
   src/styles.css   visual system

backend/   FastAPI + Pydantic
   app/data.py       curated Shillong activity data
   app/models.py     request/response contracts (Pydantic)
   app/planner.py    deterministic scoring and constraint engine
   app/ai.py         optional Claude copy-enhancement layer
   app/main.py       FastAPI routes, CORS
   tests/            planner + API tests
```

Request flow: the frontend posts a `PlanRequest` to `POST /api/plan` → `planner.build_plan()` looks up the destination's curated activity pool, applies hard filters, scores every candidate, and greedily fills morning/afternoon/evening slots per day → the deterministic `PlanResponse` is returned, optionally rewritten (explanation text only) by Claude if `enhance_with_ai` is true and `ANTHROPIC_API_KEY` is set.

## Why a deterministic planner, not an LLM itinerary

An LLM asked to "plan a trip" will happily invent opening hours, prices, and geography it doesn't know. Instead, the itinerary is produced by a rules + scoring engine over **curated, verified data**, so every claim in the output is traceable to a data field. Claude is used only where it's actually good — turning structured facts into 1–2 sentences of warm copy — and is explicitly instructed not to add or change any fact. If the Claude call fails or no key is configured, the app falls back to the deterministic result with no degradation in trip quality.

## Planning approach

1. **Hard filters** per candidate day: activity must open on that weekday, satisfy dietary restrictions (for `Food` category activities), and satisfy accessibility if requested. Already-used activities are excluded (no duplicates across the whole trip).
2. **Scoring** (0–1, weighted): 35% interest-tag match, 20% proximity to the previous stop (or to the chosen lodging area for the day's first stop), 20% budget fit, 15% pace fit (duration vs. selected pace), 10% popularity.
3. **Slot filling**: each day fills morning → afternoon → evening from the highest-scoring open candidate for that slot, subject to a daily hour cap (7.5h relaxed / 9h balanced & packed) and a soft budget guardrail (once the minimum activities-per-pace target is met, additional stops that would push spend past 108% of budget are skipped).
4. **Alternatives**: the next 1–2 best-scoring candidates per slot are returned alongside the chosen activity, powering the "Swap for…" button in the UI — a low-risk way to show planning intelligence beyond a single fixed answer, without a second API round-trip.
5. **Cost breakdown**: spend is summed by activity category (Food, Outdoors, Workshop, …) so a traveller can see where their budget goes, not just a single total.
6. **Seasonal notes**: a short, month-specific note (e.g. monsoon trail conditions in July, clear post-monsoon trekking weather in November) is attached based on the trip's start month.
7. **Travel time**: estimated as straight-line distance between coordinates × 12 minutes/km — a deliberate simplification, surfaced in the UI as an estimate rather than presented as routed, road-accurate time. This is a bigger approximation in Shillong's hill terrain than on flat ground, and is called out explicitly rather than presented as fact.

## Data model and sources

Each `Activity` (see `backend/app/models.py`) has: id, name, category, description, tags, neighborhood, coordinates, duration, price per person (INR), opening hours/weekdays, best time of day, indoor/accessible flags, dietary options, a popularity score, and an image.

**Shillong** (14 activities): well-known Meghalaya points of interest — Umiam Lake, Ward's Lake, Elephant Falls, the Nongriat double-decker living root bridge, Mawsmai Caves, Nohkalikai Falls, Laitlum Canyons, Police Bazar, Don Bosco Centre for Indigenous Cultures, Mawlynnong, Shillong Peak, and local food/craft experiences.

Place names, neighborhoods, and approximate coordinates are based on publicly known points of interest (the kind that appear on OpenStreetMap and general travel references for Shillong and Cherrapunji). **Prices, durations, opening hours, and popularity scores are reasonable synthetic estimates for prototype purposes** — they are not scraped from a live booking source, and should not be treated as current, bookable prices. This is stated here rather than presented as fact.

## Constraints, assumptions, and known limitations

- **One destination, deeply modeled** with 14 hand-curated activities, rather than broad-but-shallow national coverage. The data layer is destination-keyed, so adding a second city is a data-only change, not an architecture change.
- **Travel time is a straight-line estimate** (× 12 min/km), not a routed, road- or terrain-aware calculation — it understates travel time in Shillong's hill terrain, where roads wind around ridges and valleys.
- **Prices are synthetic estimates**, not live rates; the app never claims a booking is available.
- **No booking or persistence layer** — this is a planning prototype; itineraries are not saved server-side or shareable via a link yet.
- **Weather is not live** — seasonal notes are static, month-based generalizations, not a live forecast.
- **Claude enhancement only rewrites the explanation text** (max 2 sentences); it cannot alter activities, order, timings, or costs, and the app works fully without an API key.
- **Trips are capped at 14 days** to keep the deterministic search space and UI reasonable.
- If a day can't be filled (e.g. very restrictive filters), it's returned in `unfilled_days` rather than silently faked.

## Run locally

### Backend (Python 3.11+)

```powershell
cd backend
py -m venv .venv # optional; the workspace .venv also works
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Copy `.env.example` to `.env` at the project root and put your own Anthropic key in `.env` if you want AI-enhanced copy — this is entirely optional. The backend loads it automatically via `python-dotenv`. **Never commit a real `.env` file or API key.** If `ANTHROPIC_API_KEY` is absent, the app automatically uses the deterministic planner with no API call.

API docs: `http://localhost:8000/docs`

### Frontend (Node 18+)

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. To point at another API origin (e.g. a deployed backend), set `VITE_API_URL`.

### Tests

```powershell
cd backend
pytest

cd ..\frontend
npm run build
```

## Deploying for free

**Backend (FastAPI) → Render.com free web service**
1. Push this repo to GitHub.
2. On Render: New → Web Service → connect the repo, root directory `backend` (this repo includes a `render.yaml` blueprint, so Render can pick up the build/start commands automatically).
3. Build command: `pip install -r requirements.txt`. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Add an environment variable `FRONTEND_ORIGINS` set to your deployed frontend's URL (comma-separated if more than one) so CORS allows it. Optionally add `ANTHROPIC_API_KEY` / `ANTHROPIC_MODEL` for AI-enhanced copy.
5. Note the free tier spins down after inactivity, so the first request after idling takes a few seconds to wake up.

**Frontend (Vite/React) → Vercel (or Netlify)**
1. On Vercel: New Project → import the same repo, root directory `frontend`.
2. Framework preset: Vite. Build command `npm run build`, output directory `dist` (Vercel usually detects this automatically).
3. Add an environment variable `VITE_API_URL` set to your Render backend's URL.
4. Deploy — you get a free `*.vercel.app` URL to share.

Deploy the backend first so you have its URL for the frontend's `VITE_API_URL`, then redeploy the backend once with the frontend's final URL in `FRONTEND_ORIGINS`.

## API example

`POST /api/plan`

```json
{
  "origin_city": "Guwahati",
  "destination": "Shillong",
  "start_date": "2026-11-10",
  "end_date": "2026-11-14",
  "travelers": 2,
  "traveller_type": "couple",
  "budget": 12000,
  "currency": "INR",
  "pace": "balanced",
  "interests": ["outdoors", "culture"],
  "dietary_restrictions": [],
  "accessibility": false
}
```

## Example trip requests (showing how inputs change the output)

**1. Couple, culture + outdoors, balanced pace, ₹12,000**
`origin_city: Guwahati, interests: [outdoors, culture], pace: balanced, budget: 12000, travelers: 2`
→ Days mix Don Bosco Centre, Police Bazar, and Café Shillong with Mawlynnong and Laitlum Canyons; cost breakdown spreads across Food, Outdoors, Museum, and Workshop.

**2. Same dates, adventure-leaning friends group, packed pace, ₹18,000**
`traveller_type: friends, interests: [outdoors, adventure], pace: packed, budget: 18000`
→ Prioritizes the Nongriat Living Root Bridge trek, Mawsmai Caves, and Nohkalikai Falls; packed pace allows more stops per day, and the higher budget lets the guardrail admit the pricier trek instead of excluding it.

**3. November vs. July, same everything else**
`start_date: 2026-11-10` → surfaces the "clear, dry trekking weather" seasonal note.
`start_date: 2026-07-10` → surfaces the "peak monsoon, carry rain gear" seasonal note instead, for the exact same inputs otherwise.

These requests use the same engine and data but produce meaningfully different day-by-day plans because every input (interests, pace, budget, party type, and even trip month) directly changes the filtering, scoring, or seasonal messaging — not just cosmetic text.

## What I'd improve with more time and better data

- Route travel time with a real routing engine (e.g. self-hosted OSRM) instead of straight-line distance — this matters more here than most places, given Shillong's hill terrain.
- Expand the activity count and source prices from a maintained public dataset rather than synthetic estimates.
- Persist generated itineraries (e.g. SQLite) behind a shareable link.
- Live weather/seasonal data instead of static month-based notes.
- A second or third Northeast India destination (e.g. Gangtok, Tawang) reusing the same destination-keyed data layer.
- Auto-generate frontend TypeScript types from the FastAPI OpenAPI schema to remove manual type duplication.
