"""Curated seed data for Shillong, Meghalaya.

The prototype intentionally keeps one destination deeply modeled instead of
pretending to have complete national coverage. Prices are per person in INR.

Sources: activity names, neighborhoods, and approximate coordinates are
based on publicly known points of interest (the kind that appear on
OpenStreetMap and general travel references for Shillong and Cherrapunji).
Prices, durations, and opening hours are reasonable synthetic estimates for
prototype purposes, not scraped from a live source. Local names, legends,
and etiquette notes reflect commonly documented Khasi cultural context and
general travel-writing knowledge about the region, not a single verified
source — treat them as reasonable background, not an authoritative record.
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
        insider_tip="Arrive by 8 AM for calm, mirror-still water and soft light — by mid-morning boat traffic and wind ripple the surface.",
        local_story="\"Umiam\" roughly means \"tears of water\" in Khasi. The lake itself is artificial, formed in the 1960s when the Umiam river was dammed for hydropower, submerging a valley Khasi families once farmed.",
        local_name="Also called Barapani (\"big water\").",
    ),
    Activity(
        id="ward-lake", name="Ward's Lake & Botanical Garden", category="Outdoors",
        description="A colonial-era garden lake in the city centre with a wooden bridge and paddle boats.",
        tags=["outdoors", "nature", "photography", "slow travel"], neighborhood="Shillong City",
        latitude=25.5744, longitude=91.8825, duration_hours=1.5, price_per_person=50,
        opening_hours="08:30–17:00", open_weekdays=[0, 1, 2, 3, 4, 5, 6], best_time="afternoon",
        popularity=.82, image="https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=900",
        insider_tip="Visit right at opening (8:30 AM) to have the wooden bridge and paddle boats to yourself before local families arrive in the afternoon.",
        local_story="Laid out in the early 1900s under British administration, the lake and garden are older than most of Shillong's colonial buildings that still stand today.",
    ),
    Activity(
        id="elephant-falls", name="Elephant Falls", category="Outdoors",
        description="A three-tiered waterfall reached by short forested steps just outside the city.",
        tags=["outdoors", "nature", "photography"], neighborhood="Upper Shillong",
        latitude=25.5322, longitude=91.8244, duration_hours=1.5, price_per_person=30,
        opening_hours="09:00–17:30", open_weekdays=list(range(7)), best_time="morning",
        popularity=.9, image="https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=900",
        insider_tip="The lowest, most photogenic tier gets crowded with tour groups by 11 AM — arrive by 9 AM for clear photos and easier footing on the stone steps.",
        local_story="Its Khasi name describes what the British missed when they renamed it: the elephant-shaped boulder that first gave the falls their English name later collapsed in an earthquake, long before most visitors today ever saw it.",
        local_name="Ka Kshaid Lai Pateng Khohsiew (\"the three-step waterfall\")",
    ),
    Activity(
        id="living-root-bridge", name="Double Decker Living Root Bridge, Nongriat", category="Outdoors",
        description="A guided trek through Cherrapunji's jungle to a centuries-old bridge woven from living roots.",
        tags=["outdoors", "nature", "adventure", "photography"], neighborhood="Cherrapunji (Sohra)",
        latitude=25.2450, longitude=91.6970, duration_hours=6, price_per_person=800,
        opening_hours="Daylight hours only, 06:00–17:00", open_weekdays=list(range(7)), best_time="morning",
        indoor=False, accessible=False, popularity=.95,
        image="https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=900",
        insider_tip="Start the descent by 7 AM — it's roughly 3,500 steps down (and back up), and afternoon heat plus returning trekkers make the climb back noticeably harder after noon.",
        local_story="Khasi communities have trained the roots of rubber fig trees across rivers for generations — a living structure that grows stronger with age instead of decaying like a wooden bridge would.",
        local_name="Jingkieng jri (\"living root bridge\")",
        etiquette_note="Some stretches cross land the local village maintains; a small entry or maintenance fee is often collected on the trail, and it goes directly toward bridge upkeep — pay it without haggling.",
        myth_fact="Cherrapunji (Sohra) is famous as the \"wettest place on Earth\", but that record now technically belongs to nearby Mawsynram, about 15 km away, which records slightly higher average rainfall.",
    ),
    Activity(
        id="mawsmai-cave", name="Mawsmai Limestone Caves", category="Outdoors",
        description="A lit, walkable limestone cave system near Cherrapunji with narrow rock passages.",
        tags=["outdoors", "adventure", "nature"], neighborhood="Cherrapunji (Sohra)",
        latitude=25.2585, longitude=91.7217, duration_hours=1, price_per_person=40,
        opening_hours="09:00–16:30", open_weekdays=list(range(7)), best_time="afternoon",
        indoor=True, accessible=False, popularity=.8,
        image="https://images.unsplash.com/photo-1520962880247-cfaf541c8724?w=900",
        insider_tip="Go on a weekday morning — the lit walkway narrows in places, and weekend afternoons can mean queuing to pass through the tightest section.",
        local_story="The cave sits in Sohra, the original Khasi name for the area the British recorded as \"Cherrapunji\" — its limestone hills have been slowly carved out by some of the heaviest rainfall on the planet.",
    ),
    Activity(
        id="nohkalikai-falls", name="Nohkalikai Falls viewpoint", category="Outdoors",
        description="India's tallest plunge waterfall, viewed from a clifftop park near Cherrapunji.",
        tags=["outdoors", "nature", "photography"], neighborhood="Cherrapunji (Sohra)",
        latitude=25.2833, longitude=91.7167, duration_hours=1, price_per_person=30,
        opening_hours="09:00–17:00", open_weekdays=list(range(7)), best_time="afternoon",
        popularity=.85, image="https://images.unsplash.com/photo-1470770903676-69b98201ea1c?w=900",
        insider_tip="Come in early afternoon when the sun lights up the plunge pool's blue-green water — mornings here are often misty and can hide the base of the falls entirely.",
        local_story="The name means \"jump of Ka Likai\" — a Khasi legend about a grieving mother named Likai who, after a jealous second husband tricked her into a horrific act, ran to this cliff and leapt. The falls have carried her name ever since.",
    ),
    Activity(
        id="laitlum-canyons", name="Laitlum Canyons viewpoint", category="Outdoors",
        description="A grassy ridge with a dramatic canyon drop into the valley, a favourite sunset spot.",
        tags=["outdoors", "nature", "photography", "slow travel"], neighborhood="Laitlum",
        latitude=25.5075, longitude=91.9494, duration_hours=2, price_per_person=0,
        opening_hours="Open daylight hours", open_weekdays=list(range(7)), best_time="evening",
        popularity=.87, image="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=900",
        insider_tip="Time it for about an hour before sunset — the canyon light turns gold right as the sun drops toward the valley, then fades fast once it's below the ridge.",
        local_story="Unlike many of Meghalaya's named waterfalls, Laitlum carries no single legend — locals simply treat the ridge as a place to sit and watch the plateau fall away toward the Bangladesh plains in the distance.",
        local_name="Laitlum (\"end of the hills\")",
    ),
    Activity(
        id="police-bazar", name="Police Bazar street food & shopping walk", category="Food",
        description="Shillong's buzzing central market for momos, jadoh, and local craft shopping.",
        tags=["food", "culture", "shopping"], neighborhood="Police Bazar",
        latitude=25.5697, longitude=91.8833, duration_hours=1.5, price_per_person=150,
        opening_hours="11:00–20:30", open_weekdays=list(range(7)), best_time="afternoon",
        dietary_options=["vegetarian"], popularity=.88,
        image="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=900",
        insider_tip="Go around 5–6 PM, once stalls are fully set up and lit, but before the after-dinner rush makes the lanes hard to walk through.",
        local_story="Named for a colonial-era police post that once stood here, this market has been Shillong's commercial heart for over a century, mixing old Khasi produce sellers with newer cafes and clothing stalls side by side.",
    ),
    Activity(
        id="khasi-heritage", name="Don Bosco Centre for Indigenous Cultures", category="Museum",
        description="Seven-storey museum on Northeast India's tribal heritage, crafts, and traditions.",
        tags=["culture", "history", "indoor"], neighborhood="Mawlai",
        latitude=25.6001, longitude=91.8656, duration_hours=2, price_per_person=100,
        opening_hours="09:00–17:00", open_weekdays=[0, 1, 2, 3, 4, 5], best_time="morning",
        indoor=True, popularity=.79, image="https://images.unsplash.com/photo-1503435980610-a51f3ddfee50?w=900",
        insider_tip="Arrive at opening (9 AM) on a weekday — the seven-storey walk takes about 90 minutes done properly, and tour groups later in the day can back up the single spiral staircase.",
        local_story="Built specifically to document and preserve the oral histories, textiles, and rituals of Northeast India's many indigenous communities, it's considered one of the largest tribal museums in Asia.",
        etiquette_note="Photography is generally allowed, but a few galleries with sacred or ritual objects ask visitors not to shoot — in-gallery signage makes this clear, so it's worth checking before you do.",
    ),
    Activity(
        id="cafe-shillong", name="Café Shillong live music evening", category="Food",
        description="A local institution for Khasi-fusion plates and live acoustic sets after dark.",
        tags=["food", "culture", "nightlife"], neighborhood="Laitumkhrah",
        latitude=25.5764, longitude=91.8961, duration_hours=1.5, price_per_person=350,
        opening_hours="12:00–22:00", open_weekdays=list(range(7)), best_time="evening",
        dietary_options=["vegetarian", "vegan"], popularity=.84,
        image="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=900",
        insider_tip="Arrive by 7 PM on weekends — live-music nights fill up fast, and later arrivals often end up standing at the back.",
        local_story="Shillong has an outsized reputation for rock and acoustic music in India — often nicknamed the \"Rock Capital of India\" — and venues like this one belong to a live-music scene that's been active since the 1960s.",
    ),
    Activity(
        id="mawlynnong", name="Mawlynnong, Asia's cleanest village", category="Outdoors",
        description="A spotless Khasi village with living root bridges and a bamboo skywalk over the valley.",
        tags=["outdoors", "culture", "nature", "photography"], neighborhood="Mawlynnong",
        latitude=25.2019, longitude=91.8814, duration_hours=3, price_per_person=100,
        opening_hours="08:00–17:00", open_weekdays=list(range(7)), best_time="morning",
        popularity=.86, image="https://images.unsplash.com/photo-1500534623283-312aade485b7?w=900",
        insider_tip="Go on a weekday morning — the \"cleanest village\" title draws heavy weekend tour-bus traffic that can crowd the narrow lanes and skywalk.",
        local_story="The village's cleanliness isn't for tourists — it comes from a long-standing Khasi community practice of daily collective cleaning, organised locally long before any outside recognition brought visitors here.",
        etiquette_note="This is a living village, not an attraction built for visitors — ask before photographing residents or stepping into family compounds, and use the public dustbins provided rather than assuming any spot is fair game.",
    ),
    Activity(
        id="shillong-peak", name="Shillong Peak viewpoint", category="Outdoors",
        description="The city's highest point, with a panoramic lookout over the whole Shillong valley.",
        tags=["outdoors", "photography", "nature"], neighborhood="Upper Shillong",
        latitude=25.5480, longitude=91.8264, duration_hours=1, price_per_person=30,
        opening_hours="09:00–16:00", open_weekdays=[0, 1, 2, 3, 4, 5], best_time="afternoon",
        popularity=.75, image="https://images.unsplash.com/photo-1465101162946-4377e57745c3?w=900",
        insider_tip="Go around 4 PM for the clearest valley views before evening haze sets in — this is an Air Force-managed area, so opening hours can shift without much notice.",
        local_story="Locally called Lum Shillong, the peak is considered the seat of the city's guardian deity in Khasi tradition — Shillong is said to take its name from this hill.",
        local_name="Lum Shillong",
    ),
    Activity(
        id="wahkaba-falls-picnic", name="Sweet Falls picnic & short trek", category="Outdoors",
        description="A quieter waterfall on the city outskirts with an easy trail, popular for picnics.",
        tags=["outdoors", "nature", "slow travel"], neighborhood="Jhalupara",
        latitude=25.5461, longitude=91.8619, duration_hours=1.5, price_per_person=20,
        opening_hours="08:00–17:00", open_weekdays=list(range(7)), best_time="morning",
        popularity=.7, image="https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=900",
        insider_tip="Weekday mornings are quietest — this spot is popular with local families for weekend picnics, so the trail and falls get busy from midday on Saturdays and Sundays.",
        local_story="Known locally as Wah Kaba, this is a low-key spot favoured by Shillong residents rather than a big-ticket tourist stop — a good look at what a local Sunday actually looks like here.",
        local_name="Wah Kaba",
    ),
    Activity(
        id="khasi-craft-workshop", name="Khasi bamboo & cane weaving workshop", category="Workshop",
        description="Hands-on session with a local artisan making traditional bamboo baskets and mats.",
        tags=["craft", "culture", "indoor"], neighborhood="Mawkhar",
        latitude=25.5719, longitude=91.8778, duration_hours=2, price_per_person=250,
        opening_hours="10:00–17:00", open_weekdays=[0, 1, 2, 3, 4, 5], best_time="afternoon",
        indoor=True, popularity=.72, image="https://images.unsplash.com/photo-1528747045269-390fe33c19f2?w=900",
        insider_tip="Book the morning slot — artisans are freshest early in the day, and afternoon sessions sometimes run shorter once the day's market orders are done.",
        local_story="Bamboo and cane weaving is a skill passed down within Khasi families for generations, traditionally used for everything from the conical \"knup\" rain-shields farmers still wear to baskets for harvested betel nut.",
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
