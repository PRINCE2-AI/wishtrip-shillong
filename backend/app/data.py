"""Curated seed data for Shillong, Meghalaya.

The prototype intentionally keeps one destination deeply modeled instead of
pretending to have complete national coverage. Prices are per person in INR.

Sources: activity names, neighborhoods, and approximate coordinates are
based on publicly known points of interest (the kind that appear on
OpenStreetMap and general travel references for Shillong and Cherrapunji).
Prices, durations, and opening hours are reasonable synthetic estimates for
prototype purposes, not scraped from a live source.
"""

from .models import Activity


SHILLONG_ACTIVITIES = [
    Activity(
        id="umiam-lake", name="Umiam Lake (Barapani)", category="Outdoors",
        description="A vast reservoir ringed by pine hills, popular for boating and quiet lakeside walks.",
        tags=["outdoors", "nature", "photography", "slow travel"], neighborhood="Umiam",
        latitude=25.6547, longitude=91.8933, duration_hours=2.5, price_per_person=200,
        opening_hours="08:00–17:00", open_weekdays=list(range(7)), best_time="morning",
        popularity=.93, image="https://images.unsplash.com/photo-1506947411487-a56738267384?w=900",
    ),
    Activity(
        id="ward-lake", name="Ward's Lake & Botanical Garden", category="Outdoors",
        description="A colonial-era garden lake in the city centre with a wooden bridge and paddle boats.",
        tags=["outdoors", "nature", "photography", "slow travel"], neighborhood="Shillong City",
        latitude=25.5744, longitude=91.8825, duration_hours=1.5, price_per_person=50,
        opening_hours="08:30–17:00", open_weekdays=[0, 1, 2, 3, 4, 5, 6], best_time="afternoon",
        popularity=.82, image="https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=900",
    ),
    Activity(
        id="elephant-falls", name="Elephant Falls", category="Outdoors",
        description="A three-tiered waterfall reached by short forested steps just outside the city.",
        tags=["outdoors", "nature", "photography"], neighborhood="Upper Shillong",
        latitude=25.5322, longitude=91.8244, duration_hours=1.5, price_per_person=30,
        opening_hours="09:00–17:30", open_weekdays=list(range(7)), best_time="morning",
        popularity=.9, image="https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=900",
    ),
    Activity(
        id="living-root-bridge", name="Double Decker Living Root Bridge, Nongriat", category="Outdoors",
        description="A guided trek through Cherrapunji's jungle to a centuries-old bridge woven from living roots.",
        tags=["outdoors", "nature", "adventure", "photography"], neighborhood="Cherrapunji (Sohra)",
        latitude=25.2450, longitude=91.6970, duration_hours=6, price_per_person=800,
        opening_hours="Daylight hours only, 06:00–17:00", open_weekdays=list(range(7)), best_time="morning",
        indoor=False, accessible=False, popularity=.95,
        image="https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=900",
    ),
    Activity(
        id="mawsmai-cave", name="Mawsmai Limestone Caves", category="Outdoors",
        description="A lit, walkable limestone cave system near Cherrapunji with narrow rock passages.",
        tags=["outdoors", "adventure", "nature"], neighborhood="Cherrapunji (Sohra)",
        latitude=25.2585, longitude=91.7217, duration_hours=1, price_per_person=40,
        opening_hours="09:00–16:30", open_weekdays=list(range(7)), best_time="afternoon",
        indoor=True, accessible=False, popularity=.8,
        image="https://images.unsplash.com/photo-1520962880247-cfaf541c8724?w=900",
    ),
    Activity(
        id="nohkalikai-falls", name="Nohkalikai Falls viewpoint", category="Outdoors",
        description="India's tallest plunge waterfall, viewed from a clifftop park near Cherrapunji.",
        tags=["outdoors", "nature", "photography"], neighborhood="Cherrapunji (Sohra)",
        latitude=25.2833, longitude=91.7167, duration_hours=1, price_per_person=30,
        opening_hours="09:00–17:00", open_weekdays=list(range(7)), best_time="afternoon",
        popularity=.85, image="https://images.unsplash.com/photo-1470770903676-69b98201ea1c?w=900",
    ),
    Activity(
        id="laitlum-canyons", name="Laitlum Canyons viewpoint", category="Outdoors",
        description="A grassy ridge with a dramatic canyon drop into the valley, a favourite sunset spot.",
        tags=["outdoors", "nature", "photography", "slow travel"], neighborhood="Laitlum",
        latitude=25.5075, longitude=91.9494, duration_hours=2, price_per_person=0,
        opening_hours="Open daylight hours", open_weekdays=list(range(7)), best_time="evening",
        popularity=.87, image="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=900",
    ),
    Activity(
        id="police-bazar", name="Police Bazar street food & shopping walk", category="Food",
        description="Shillong's buzzing central market for momos, jadoh, and local craft shopping.",
        tags=["food", "culture", "shopping"], neighborhood="Police Bazar",
        latitude=25.5697, longitude=91.8833, duration_hours=1.5, price_per_person=150,
        opening_hours="11:00–20:30", open_weekdays=list(range(7)), best_time="afternoon",
        dietary_options=["vegetarian"], popularity=.88,
        image="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=900",
    ),
    Activity(
        id="khasi-heritage", name="Don Bosco Centre for Indigenous Cultures", category="Museum",
        description="Seven-storey museum on Northeast India's tribal heritage, crafts, and traditions.",
        tags=["culture", "history", "indoor"], neighborhood="Mawlai",
        latitude=25.6001, longitude=91.8656, duration_hours=2, price_per_person=100,
        opening_hours="09:00–17:00", open_weekdays=[0, 1, 2, 3, 4, 5], best_time="morning",
        indoor=True, popularity=.79, image="https://images.unsplash.com/photo-1503435980610-a51f3ddfee50?w=900",
    ),
    Activity(
        id="cafe-shillong", name="Café Shillong live music evening", category="Food",
        description="A local institution for Khasi-fusion plates and live acoustic sets after dark.",
        tags=["food", "culture", "nightlife"], neighborhood="Laitumkhrah",
        latitude=25.5764, longitude=91.8961, duration_hours=1.5, price_per_person=350,
        opening_hours="12:00–22:00", open_weekdays=list(range(7)), best_time="evening",
        dietary_options=["vegetarian", "vegan"], popularity=.84,
        image="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=900",
    ),
    Activity(
        id="mawlynnong", name="Mawlynnong, Asia's cleanest village", category="Outdoors",
        description="A spotless Khasi village with living root bridges and a bamboo skywalk over the valley.",
        tags=["outdoors", "culture", "nature", "photography"], neighborhood="Mawlynnong",
        latitude=25.2019, longitude=91.8814, duration_hours=3, price_per_person=100,
        opening_hours="08:00–17:00", open_weekdays=list(range(7)), best_time="morning",
        popularity=.86, image="https://images.unsplash.com/photo-1500534623283-312aade485b7?w=900",
    ),
    Activity(
        id="shillong-peak", name="Shillong Peak viewpoint", category="Outdoors",
        description="The city's highest point, with a panoramic lookout over the whole Shillong valley.",
        tags=["outdoors", "photography", "nature"], neighborhood="Upper Shillong",
        latitude=25.5480, longitude=91.8264, duration_hours=1, price_per_person=30,
        opening_hours="09:00–16:00", open_weekdays=[0, 1, 2, 3, 4, 5], best_time="afternoon",
        popularity=.75, image="https://images.unsplash.com/photo-1465101162946-4377e57745c3?w=900",
    ),
    Activity(
        id="wahkaba-falls-picnic", name="Sweet Falls picnic & short trek", category="Outdoors",
        description="A quieter waterfall on the city outskirts with an easy trail, popular for picnics.",
        tags=["outdoors", "nature", "slow travel"], neighborhood="Jhalupara",
        latitude=25.5461, longitude=91.8619, duration_hours=1.5, price_per_person=20,
        opening_hours="08:00–17:00", open_weekdays=list(range(7)), best_time="morning",
        popularity=.7, image="https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=900",
    ),
    Activity(
        id="khasi-craft-workshop", name="Khasi bamboo & cane weaving workshop", category="Workshop",
        description="Hands-on session with a local artisan making traditional bamboo baskets and mats.",
        tags=["craft", "culture", "indoor"], neighborhood="Mawkhar",
        latitude=25.5719, longitude=91.8778, duration_hours=2, price_per_person=250,
        opening_hours="10:00–17:00", open_weekdays=[0, 1, 2, 3, 4, 5], best_time="afternoon",
        indoor=True, popularity=.72, image="https://images.unsplash.com/photo-1528747045269-390fe33c19f2?w=900",
    ),
]

DESTINATIONS: dict[str, dict] = {
    "shillong": {
        "display_name": "Shillong",
        "country": "India",
        "currency": "INR",
        "anchors": {
            "Police Bazar": (25.5697, 91.8833),
            "Laitumkhrah": (25.5764, 91.8961),
            "Cherrapunji": (25.2585, 91.7217),
        },
        "default_lodging_area": "Police Bazar",
        "activities": SHILLONG_ACTIVITIES,
        "seasonal_notes": {
            3: "Spring — clear skies and blooming rhododendrons make viewpoints especially scenic.",
            6: "Monsoon begins — Cherrapunji waterfalls are at their most dramatic, but trails get slippery.",
            7: "Peak monsoon — heavy rain likely most days; plan indoor backups and flexible timings.",
            8: "Still monsoon season — waterfalls remain spectacular; carry rain gear for outdoor stops.",
            11: "Post-monsoon and clear — one of the best months for the Laitlum Canyons and root bridge trek.",
            12: "Cool, dry, and clear — comfortable trekking weather with long-range valley views.",
        },
    },
}


def get_destination(name: str) -> dict | None:
    return DESTINATIONS.get(name.strip().casefold())
