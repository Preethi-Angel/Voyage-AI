"""Mock data for travel planning - replaces real API calls."""
from typing import List, Dict
from app.models.responses import FlightOption, HotelOption, ActivityOption


# Mock Flight Database
MOCK_FLIGHTS = {
    "tokyo": [
        FlightOption(
            airline="Japan Airlines",
            departure_time="2025-02-01 10:00",
            arrival_time="2025-02-01 14:30",
            duration="11h 30m",
            price=650.00,
            stops=0
        ),
        FlightOption(
            airline="ANA",
            departure_time="2025-02-01 14:00",
            arrival_time="2025-02-01 18:00",
            duration="10h 00m",
            price=720.00,
            stops=0
        ),
        FlightOption(
            airline="United Airlines",
            departure_time="2025-02-01 08:00",
            arrival_time="2025-02-01 15:00",
            duration="13h 00m",
            price=580.00,
            stops=1
        ),
        FlightOption(
            airline="Premium Business Class - ANA",
            departure_time="2025-02-01 09:00",
            arrival_time="2025-02-01 13:00",
            duration="10h 00m",
            price=1250.00,
            stops=0
        ),
    ],
    "paris": [
        FlightOption(
            airline="Air France",
            departure_time="2025-02-01 18:00",
            arrival_time="2025-02-02 08:00",
            duration="8h 00m",
            price=450.00,
            stops=0
        ),
    ],
    "london": [
        FlightOption(
            airline="British Airways",
            departure_time="2025-02-01 16:00",
            arrival_time="2025-02-02 06:00",
            duration="7h 00m",
            price=380.00,
            stops=0
        ),
    ],
}


# Mock Hotel Database
MOCK_HOTELS = {
    "tokyo": [
        HotelOption(
            name="Shibuya Grand Hotel",
            location="Shibuya, Tokyo",
            price_per_night=120.00,
            total_price=0,  # Will be calculated
            rating=4.2,
            amenities=["WiFi", "Breakfast", "Gym", "City View"]
        ),
        HotelOption(
            name="Shinjuku Budget Inn",
            location="Shinjuku, Tokyo",
            price_per_night=85.00,
            total_price=0,
            rating=3.8,
            amenities=["WiFi", "24/7 Desk"]
        ),
        HotelOption(
            name="Tokyo Luxury Suites",
            location="Ginza, Tokyo",
            price_per_night=250.00,
            total_price=0,
            rating=4.8,
            amenities=["WiFi", "Breakfast", "Spa", "Pool", "Concierge"]
        ),
        HotelOption(
            name="Asakusa Traditional Ryokan",
            location="Asakusa, Tokyo",
            price_per_night=150.00,
            total_price=0,
            rating=4.5,
            amenities=["WiFi", "Traditional Breakfast", "Onsen", "Tea Ceremony"]
        ),
        HotelOption(
            name="Imperial Suite - Ritz-Carlton Tokyo",
            location="Roppongi, Tokyo",
            price_per_night=450.00,
            total_price=0,
            rating=5.0,
            amenities=["WiFi", "Butler Service", "Spa", "Michelin Restaurant", "Panoramic Views", "Private Lounge"]
        ),
    ],
    "paris": [
        HotelOption(
            name="Eiffel View Hotel",
            location="7th Arrondissement, Paris",
            price_per_night=180.00,
            total_price=0,
            rating=4.5,
            amenities=["WiFi", "Breakfast", "Eiffel Tower View"]
        ),
    ],
    "london": [
        HotelOption(
            name="Westminster Inn",
            location="Westminster, London",
            price_per_night=150.00,
            total_price=0,
            rating=4.3,
            amenities=["WiFi", "Breakfast", "Central Location"]
        ),
    ],
}


# Mock Activities Database
MOCK_ACTIVITIES = {
    "tokyo": {
        "tech": [
            ActivityOption(
                name="Akihabara Tech District Tour",
                description="Explore Tokyo's electronics and anime paradise",
                cost=30.00,
                duration="3 hours",
                category="tech"
            ),
            ActivityOption(
                name="TeamLab Borderless Digital Art Museum",
                description="Immersive digital art experience",
                cost=35.00,
                duration="2 hours",
                category="tech"
            ),
            ActivityOption(
                name="Sony ExploraScience",
                description="Interactive technology exhibition",
                cost=25.00,
                duration="2 hours",
                category="tech"
            ),
        ],
        "food": [
            ActivityOption(
                name="Tsukiji Outer Market Food Tour",
                description="Fresh sushi and street food experience",
                cost=50.00,
                duration="3 hours",
                category="food"
            ),
            ActivityOption(
                name="Ramen Making Class",
                description="Learn to make authentic Japanese ramen",
                cost=65.00,
                duration="2.5 hours",
                category="food"
            ),
            ActivityOption(
                name="Sushi Masterclass at Toyosu Market",
                description="Professional sushi making experience",
                cost=80.00,
                duration="3 hours",
                category="food"
            ),
            ActivityOption(
                name="Private Michelin Star Chef Experience",
                description="Exclusive dining with 3-star Michelin chef",
                cost=250.00,
                duration="4 hours",
                category="food"
            ),
        ],
        "temples": [
            ActivityOption(
                name="Senso-ji Temple Visit",
                description="Tokyo's oldest Buddhist temple in Asakusa",
                cost=0.00,
                duration="2 hours",
                category="temples"
            ),
            ActivityOption(
                name="Meiji Shrine Experience",
                description="Peaceful Shinto shrine in forest setting",
                cost=0.00,
                duration="1.5 hours",
                category="temples"
            ),
            ActivityOption(
                name="Guided Temple Tour (Senso-ji + Meiji + Yasukuni)",
                description="Comprehensive temple tour with expert guide",
                cost=45.00,
                duration="5 hours",
                category="temples"
            ),
        ],
        "nature": [
            ActivityOption(
                name="Mount Fuji Day Trip",
                description="Scenic tour to Japan's iconic mountain",
                cost=120.00,
                duration="10 hours",
                category="nature"
            ),
            ActivityOption(
                name="Shinjuku Gyoen National Garden",
                description="Beautiful traditional Japanese garden",
                cost=5.00,
                duration="2 hours",
                category="nature"
            ),
        ],
        "sightseeing": [
            ActivityOption(
                name="Tokyo Skytree Observation Deck",
                description="Panoramic views from tallest tower",
                cost=28.00,
                duration="1.5 hours",
                category="sightseeing"
            ),
            ActivityOption(
                name="Shibuya Crossing & Harajuku Walking Tour",
                description="Experience Tokyo's most vibrant districts",
                cost=20.00,
                duration="3 hours",
                category="sightseeing"
            ),
            ActivityOption(
                name="Imperial Palace East Gardens",
                description="Historic palace grounds and gardens",
                cost=0.00,
                duration="2 hours",
                category="sightseeing"
            ),
        ],
    },
    "paris": {
        "sightseeing": [
            ActivityOption(
                name="Eiffel Tower Visit",
                description="Iconic Parisian landmark",
                cost=30.00,
                duration="2 hours",
                category="sightseeing"
            ),
        ],
    },
    "london": {
        "sightseeing": [
            ActivityOption(
                name="Big Ben & Westminster Abbey",
                description="Historic London landmarks",
                cost=25.00,
                duration="3 hours",
                category="sightseeing"
            ),
        ],
    },
}


def get_flights(destination: str, budget_preference: str = "mid-range") -> List[FlightOption]:
    """Get mock flight options for destination."""
    dest_key = destination.lower().split(",")[0].strip()
    flights = MOCK_FLIGHTS.get(dest_key, MOCK_FLIGHTS["tokyo"])

    if budget_preference == "budget":
        return sorted(flights, key=lambda f: f.price)[:2]
    elif budget_preference == "luxury":
        return sorted(flights, key=lambda f: f.price, reverse=True)[:2]
    else:
        return flights


def get_hotels(destination: str, nights: int, budget_preference: str = "mid-range") -> List[HotelOption]:
    """Get mock hotel options for destination."""
    dest_key = destination.lower().split(",")[0].strip()
    hotels = MOCK_HOTELS.get(dest_key, MOCK_HOTELS["tokyo"])

    # Calculate total price
    for hotel in hotels:
        hotel.total_price = hotel.price_per_night * nights

    if budget_preference == "budget":
        return sorted(hotels, key=lambda h: h.price_per_night)[:2]
    elif budget_preference == "luxury":
        return sorted(hotels, key=lambda h: h.price_per_night, reverse=True)[:2]
    else:
        return sorted(hotels, key=lambda h: h.price_per_night)[1:3]


def get_activities(destination: str, interests: List[str], max_count: int = 5) -> List[ActivityOption]:
    """Get mock activities based on interests."""
    dest_key = destination.lower().split(",")[0].strip()
    activities_db = MOCK_ACTIVITIES.get(dest_key, MOCK_ACTIVITIES["tokyo"])

    selected_activities = []
    for interest in interests:
        interest_activities = activities_db.get(interest.lower(), [])
        selected_activities.extend(interest_activities[:2])  # Max 2 per interest

    return selected_activities[:max_count]


def calculate_daily_food_budget(duration_days: int, budget_level: str = "mid-range") -> float:
    """Calculate estimated daily food costs."""
    daily_rates = {
        "budget": 30.00,
        "mid-range": 60.00,
        "luxury": 120.00
    }
    daily_rate = daily_rates.get(budget_level, 60.00)
    return daily_rate * duration_days


def calculate_misc_costs(duration_days: int) -> float:
    """Calculate miscellaneous costs (transport, tips, etc.)."""
    return duration_days * 25.00  # $25/day for local transport and misc
