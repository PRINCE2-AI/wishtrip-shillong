"""Curated seed data for two deeply modeled destinations.

The prototype intentionally keeps a small number of destinations deeply
modeled instead of pretending to have complete global coverage. Prices are
per person in the destination's local pricing (USD for Kyoto, INR for
Shillong) — the planner converts using request.currency at read time via the
frontend display layer; costs stored here are already in the unit the
destination is priced in.

Sources: activity names, neighborhoods, and approximate coordinates are
based on publicly known points of interest (temple/market/viewpoint names
that appear on OpenStreetMap and general travel references for Kyoto and
Shillong). Prices, durations, and opening hours are reasonable synthetic
estimates for prototype purposes, not scraped from a live source.
"""

from .models import Activity


KYOTO_ACTIVITIES = [
    Activity(
        id="fushimi-inari", name="Fushimi Inari Taisha", category="Temple",
        description="Walk through thousands of vermilion torii gates on a forested hillside.",
        tags=["culture", "history", "outdoors", "photography"], neighborhood="Fushimi",
        latitude=34.9671, longitude=135.7727, duration_hours=2.5, price_per_person=0,
        opening_hours="Open 24 hours", open_weekdays=list(range(7)), best_time="morning",
        popularity=.98, image="https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=900",
    ),
    Activity(
        id="kiyomizu-dera", name="Kiyomizu-dera Temple", category="Temple",
        description="A UNESCO-listed temple with a sweeping wooden stage and city views.",
        tags=["culture", "history", "photography"], neighborhood="Higashiyama",
        latitude=34.9949, longitude=135.7850, duration_hours=2, price_per_person=3,
        opening_hours="06:00–18:00", open_weekdays=list(range(7)), best_time="morning",
        popularity=.96, image="https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=900",
    ),
    Activity(
        id="gion-walk", name="Gion & Shirakawa evening walk", category="Neighborhood",
        description="A self-guided stroll through lantern-lit lanes beside the Shirakawa canal.",
        tags=["culture", "photography", "slow travel", "nightlife"], neighborhood="Gion",
        latitude=35.0037, longitude=135.7788, duration_hours=1.5, price_per_person=0,
        opening_hours="Best after 17:00", open_weekdays=list(range(7)), best_time="evening",
        popularity=.91, image="https://images.unsplash.com/photo-1492571350019-22de08371fd3?w=900",
    ),
    Activity(
        id="nishiki-market", name="Nishiki Market tasting crawl", category="Food",
        description="Sample Kyoto specialties in a covered five-block market.",
        tags=["food", "culture", "shopping"], neighborhood="Central Kyoto",
        latitude=35.0050, longitude=135.7648, duration_hours=2, price_per_person=22,
        opening_hours="10:00–18:00", open_weekdays=[0, 1, 2, 3, 4, 5], best_time="afternoon",
        dietary_options=["vegetarian", "vegan"], popularity=.9,
        image="https://images.unsplash.com/photo-1554797589-7241bb691973?w=900",
    ),
    Activity(
        id="tea-ceremony", name="Camellia Garden tea ceremony", category="Workshop",
        description="Learn the quiet choreography of matcha preparation with a local host.",
        tags=["food", "culture", "slow travel", "wellness"], neighborhood="Higashiyama",
        latitude=34.9978, longitude=135.7805, duration_hours=1.5, price_per_person=42,
        opening_hours="09:30–17:00", open_weekdays=list(range(7)), best_time="afternoon",
        dietary_options=["vegetarian", "vegan"], popularity=.88,
        image="https://images.unsplash.com/photo-1545048702-79362596cdc9?w=900",
    ),
    Activity(
        id="arashiyama-bamboo", name="Arashiyama bamboo grove & Tenryu-ji", category="Outdoors",
        description="Pair the famous bamboo lane with a tranquil Zen garden and mountain foothills.",
        tags=["outdoors", "culture", "photography", "wellness"], neighborhood="Arashiyama",
        latitude=35.0170, longitude=135.6713, duration_hours=3.5, price_per_person=5,
        opening_hours="08:30–17:00", open_weekdays=list(range(7)), best_time="morning",
        popularity=.97, image="https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=900",
    ),
    Activity(
        id="philosopher-path", name="Philosopher's Path", category="Outdoors",
        description="A leafy canal-side path connecting small temples in northern Higashiyama.",
        tags=["outdoors", "wellness", "photography", "slow travel"], neighborhood="Higashiyama",
        latitude=35.0270, longitude=135.7935, duration_hours=2, price_per_person=0,
        opening_hours="Open 24 hours", open_weekdays=list(range(7)), best_time="afternoon",
        popularity=.84, image="https://images.unsplash.com/photo-1493780474015-ba834fd0ce2f?w=900",
    ),
    Activity(
        id="nijo-castle", name="Nijo Castle", category="History",
        description="Explore shogun-era rooms, nightingale floors, and landscaped gardens.",
        tags=["culture", "history", "architecture"], neighborhood="Central Kyoto",
        latitude=35.0142, longitude=135.7481, duration_hours=2.5, price_per_person=8,
        opening_hours="08:45–17:00", open_weekdays=[0, 1, 2, 3, 4, 6], best_time="morning",
        popularity=.89, image="https://images.unsplash.com/photo-1478436127897-769e1b3f0f36?w=900",
    ),
    Activity(
        id="kyoto-railway", name="Kyoto Railway Museum", category="Museum",
        description="Hands-on railway history with restored locomotives and a working steam train.",
        tags=["history", "family", "indoor", "engineering"], neighborhood="Shimogyo",
        latitude=34.9875, longitude=135.7414, duration_hours=2.5, price_per_person=12,
        opening_hours="10:00–17:30", open_weekdays=[0, 1, 3, 4, 5, 6], best_time="afternoon",
        indoor=True, popularity=.78, image="https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=900",
    ),
    Activity(
        id="northern-mountains", name="Kurama mountain & onsen day", category="Wellness",
        description="A gentle cedar-forest hike followed by a restorative mountain bath.",
        tags=["outdoors", "wellness", "slow travel", "nature"], neighborhood="Kurama",
        latitude=35.1160, longitude=135.7700, duration_hours=5, price_per_person=28,
        opening_hours="09:00–17:00", open_weekdays=list(range(7)), best_time="morning",
        popularity=.8, image="https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=900",
    ),
    Activity(
        id="tofu-dinner", name="Shigetsu Buddhist cuisine dinner", category="Food",
        description="A seasonal shojin ryori meal focused on tofu, vegetables, and mindful presentation.",
        tags=["food", "culture", "wellness"], neighborhood="Arashiyama",
        latitude=35.0157, longitude=135.6718, duration_hours=1.5, price_per_person=55,
        opening_hours="17:00–20:00", open_weekdays=[0, 1, 2, 3, 4, 5, 6], best_time="evening",
        dietary_options=["vegetarian", "vegan", "gluten-free"], popularity=.86,
        image="https://images.unsplash.com/photo-1547592180-85f173990554?w=900",
    ),
    Activity(
        id="pontocho-dinner", name="Pontocho lantern-lit dinner", category="Food",
        description="Choose a small counter in one of Kyoto's atmospheric dining alleys.",
        tags=["food", "nightlife", "culture"], neighborhood="Pontocho",
        latitude=35.0050, longitude=135.7715, duration_hours=1.5, price_per_person=48,
        opening_hours="17:30–22:00", open_weekdays=list(range(7)), best_time="evening",
        dietary_options=["vegetarian"], popularity=.92,
        image="https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?w=900",
    ),
    Activity(
        id="sake-brewery", name="Fushimi sake brewery tasting", category="Food",
        description="Discover Fushimi's soft-water brewing tradition with a guided tasting.",
        tags=["food", "culture", "history"], neighborhood="Fushimi",
        latitude=34.9320, longitude=135.7620, duration_hours=2, price_per_person=30,
        opening_hours="10:00–17:00", open_weekdays=[0, 1, 2, 3, 4, 5, 6], best_time="afternoon",
        dietary_options=["vegetarian"], popularity=.82,
        image="https://images.unsplash.com/photo-1569529465841-dfecdab7503b?w=900",
    ),
    Activity(
        id="kyoto-craft", name="Kintsugi & ceramics studio", category="Workshop",
        description="Repair a small ceramic piece with gold and take home a thoughtful souvenir.",
        tags=["craft", "culture", "shopping", "indoor"], neighborhood="Gojo",
        latitude=34.9921, longitude=135.7653, duration_hours=2.5, price_per_person=68,
        opening_hours="10:00–18:00", open_weekdays=[0, 2, 3, 4, 5, 6], best_time="afternoon",
        indoor=True, popularity=.76, image="https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=900",
    ),
]

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
    "kyoto": {
        "display_name": "Kyoto",
        "country": "Japan",
        "currency": "USD",
        "anchors": {"Gion": (35.0037, 135.7788), "Kyoto Station": (34.9858, 135.7588), "Arashiyama": (35.0170, 135.6713)},
        "default_lodging_area": "Gion",
        "activities": KYOTO_ACTIVITIES,
        "seasonal_notes": {
            3: "Late March starts cherry blossom season — expect larger crowds at Higashiyama temples.",
            4: "Peak cherry blossom month — book popular spots early in the day to beat crowds.",
            6: "Rainy season (tsuyu) — pack for showers; indoor workshops and museums are good backups.",
            7: "Hot and humid — mornings are the most comfortable time for outdoor walking activities.",
            11: "Peak autumn foliage — Arashiyama and the Philosopher's Path are especially striking.",
            12: "Cold and quiet — fewer crowds, some outdoor gardens close earlier.",
        },
    },
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
