"""
Hybrid Data Service - Uses Cached Real Data with Mock Fallback

This service provides a hybrid approach:
1. First, tries to load cached real data from Amadeus API
2. Falls back to mock data if cache is unavailable
3. Agents work with real data for demos (fast + reliable)
"""
import json
from pathlib import Path
from typing import List, Optional
from app.models.responses import FlightOption, HotelOption, ActivityOption

# Import original mock data as fallback
from app.services import mock_data


class HybridDataService:
    """Provides travel data from cached real API responses with mock fallback."""

    def __init__(self):
        self.cache_file = Path(__file__).parent.parent / "data" / "cache" / "real_travel_data.json"
        self.cached_data = self._load_cache()
        self.using_real_data = self.cached_data is not None

        if self.using_real_data:
            print("✅ Using cached REAL travel data from Amadeus API")
        else:
            print("⚠️  Using MOCK travel data (real data not cached)")

    def _load_cache(self) -> Optional[dict]:
        """Load cached real data if available."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"❌ Error loading cached data: {e}")
                return None
        return None

    def get_flights(self, destination: str, preference: str = "economy") -> List[FlightOption]:
        """
        Get flight options (from real cached data or mock data).

        Args:
            destination: City name (e.g., "Tokyo", "Paris")
            preference: "economy", "business", or "luxury"

        Returns:
            List of FlightOption objects
        """
        city_key = destination.lower().split(',')[0].strip()

        # Try real cached data first
        if self.using_real_data and city_key in self.cached_data.get('destinations', {}):
            real_flights = self.cached_data['destinations'][city_key].get('flights', [])
            if real_flights:
                # Convert cached real data to FlightOption objects
                flights = []
                for flight in real_flights:
                    flights.append(FlightOption(
                        airline=flight.get('airline', 'Airline'),
                        departure_time=flight.get('departure_time', '2025-02-01 10:00'),
                        arrival_time=flight.get('arrival_time', '2025-02-01 22:00'),
                        duration=flight.get('duration', '12h 00m'),
                        price=float(flight.get('price', 500.0)),
                        stops=int(flight.get('stops', 0))
                    ))

                # Filter by preference if needed
                if preference == "luxury":
                    flights = [f for f in flights if f.price > 1000]
                elif preference == "budget":
                    flights = sorted(flights, key=lambda x: x.price)[:3]

                return flights

        # Fallback to mock data
        return mock_data.get_flights(destination, preference)

    def get_hotels(
        self,
        destination: str,
        duration_days: int,
        preference: str = "mid-range"
    ) -> List[HotelOption]:
        """
        Get hotel options (from real cached data or mock data).

        Args:
            destination: City name
            duration_days: Number of nights
            preference: "budget", "mid-range", or "luxury"

        Returns:
            List of HotelOption objects
        """
        city_key = destination.lower().split(',')[0].strip()

        # Try real cached data first
        if self.using_real_data and city_key in self.cached_data.get('destinations', {}):
            real_hotels = self.cached_data['destinations'][city_key].get('hotels', [])
            if real_hotels:
                hotels = []
                for hotel in real_hotels:
                    # Estimate pricing based on preference
                    base_price = self._estimate_hotel_price(hotel.get('chain_code', 'N/A'), preference)

                    hotels.append(HotelOption(
                        name=hotel.get('name', 'Hotel'),
                        location=hotel.get('location', destination),
                        price_per_night=base_price,
                        total_price=base_price * duration_days,
                        rating=4.0,  # Default rating (Amadeus doesn't always provide this)
                        amenities=self._get_amenities_for_tier(preference)
                    ))

                # Filter by preference
                if preference == "budget":
                    hotels = sorted(hotels, key=lambda x: x.price_per_night)[:3]
                elif preference == "luxury":
                    hotels = sorted(hotels, key=lambda x: x.price_per_night, reverse=True)[:3]
                else:  # mid-range
                    hotels = sorted(hotels, key=lambda x: x.price_per_night)[2:5]

                return hotels

        # Fallback to mock data
        return mock_data.get_hotels(destination, duration_days, preference)

    def get_activities(
        self,
        destination: str,
        interests: List[str],
        max_count: int = 5
    ) -> List[ActivityOption]:
        """
        Get activity options (from real cached data or mock data).

        Args:
            destination: City name
            interests: List of interest categories
            max_count: Maximum number of activities

        Returns:
            List of ActivityOption objects
        """
        city_key = destination.lower().split(',')[0].strip()

        # Try real cached data first
        if self.using_real_data and city_key in self.cached_data.get('destinations', {}):
            real_activities = self.cached_data['destinations'][city_key].get('activities', [])
            if real_activities:
                activities = []
                for activity in real_activities[:max_count]:
                    activities.append(ActivityOption(
                        name=activity.get('name', 'Activity'),
                        description=activity.get('description', 'Tour activity'),
                        cost=float(activity.get('price', 50.0)),
                        duration="2-3 hours",
                        category=activity.get('category', 'SIGHTSEEING').lower()
                    ))
                return activities

        # Fallback to mock data
        return mock_data.get_activities(destination, interests, max_count)

    def _estimate_hotel_price(self, chain_code: str, preference: str) -> float:
        """Estimate hotel price per night based on chain and preference."""
        # Premium chains
        premium_chains = ['HY', 'IH', 'MC', 'RT', 'SH', 'WI']

        if preference == "luxury":
            return 300.0 if chain_code in premium_chains else 250.0
        elif preference == "budget":
            return 80.0 if chain_code not in premium_chains else 120.0
        else:  # mid-range
            return 150.0 if chain_code in premium_chains else 120.0

    def _get_amenities_for_tier(self, preference: str) -> List[str]:
        """Get typical amenities for hotel tier."""
        if preference == "luxury":
            return ["WiFi", "Breakfast", "Spa", "Pool", "Concierge", "Room Service"]
        elif preference == "budget":
            return ["WiFi", "24/7 Desk"]
        else:  # mid-range
            return ["WiFi", "Breakfast", "Gym", "Business Center"]

    def is_using_real_data(self) -> bool:
        """Check if service is using cached real data."""
        return self.using_real_data

    def get_data_source_info(self) -> dict:
        """Get information about current data source."""
        if self.using_real_data:
            return {
                "source": "Cached Real Data (Amadeus API)",
                "last_updated": self.cached_data.get('last_updated', 'Unknown'),
                "destinations": list(self.cached_data.get('destinations', {}).keys())
            }
        else:
            return {
                "source": "Mock Data",
                "last_updated": "N/A",
                "destinations": ["tokyo", "paris", "london", "new york"]
            }


# Global instance
_hybrid_service = None


def get_hybrid_service() -> HybridDataService:
    """Get singleton instance of HybridDataService."""
    global _hybrid_service
    if _hybrid_service is None:
        _hybrid_service = HybridDataService()
    return _hybrid_service


# Convenience functions that use hybrid service
def get_flights(destination: str, preference: str = "economy") -> List[FlightOption]:
    """Get flights from hybrid data source."""
    return get_hybrid_service().get_flights(destination, preference)


def get_hotels(destination: str, duration_days: int, preference: str = "mid-range") -> List[HotelOption]:
    """Get hotels from hybrid data source."""
    return get_hybrid_service().get_hotels(destination, duration_days, preference)


def get_activities(destination: str, interests: List[str], max_count: int = 5) -> List[ActivityOption]:
    """Get activities from hybrid data source."""
    return get_hybrid_service().get_activities(destination, interests, max_count)


# Keep compatibility with existing mock_data functions
calculate_daily_food_budget = mock_data.calculate_daily_food_budget
calculate_misc_costs = mock_data.calculate_misc_costs
