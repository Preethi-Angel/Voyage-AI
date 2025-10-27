"""
Real Travel Data Fetcher - Hybrid Approach
Fetches real data from Amadeus API and caches it for demo use.

Usage:
1. Set AMADEUS_API_KEY and AMADEUS_API_SECRET in .env
2. Run: python -m app.services.real_data_fetcher --refresh
3. Cached data will be used for demos (fast + reliable)
4. Refresh weekly or as needed
"""
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from amadeus import Client, ResponseError
    AMADEUS_AVAILABLE = True
except ImportError:
    AMADEUS_AVAILABLE = False
    print("Warning: Amadeus SDK not installed. Install with: pip install amadeus")


class RealDataFetcher:
    """Fetches real travel data from Amadeus API and caches it."""

    def __init__(self):
        self.cache_dir = Path(__file__).parent.parent / "data" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Amadeus client if credentials available
        api_key = os.getenv("AMADEUS_API_KEY")
        api_secret = os.getenv("AMADEUS_API_SECRET")

        if api_key and api_secret and AMADEUS_AVAILABLE:
            self.amadeus = Client(
                client_id=api_key,
                client_secret=api_secret
            )
            self.enabled = True
        else:
            self.amadeus = None
            self.enabled = False
            print("Amadeus API not configured. Using mock data only.")

    def fetch_and_cache_all(self):
        """Fetch real data for all demo destinations and cache it."""
        if not self.enabled:
            print("❌ Amadeus API not configured. Cannot fetch real data.")
            print("Please set AMADEUS_API_KEY and AMADEUS_API_SECRET in .env file")
            return False

        print("🔄 Fetching real travel data from Amadeus TEST API...")
        print("📚 Using Amadeus guaranteed test data cities")
        print("   See: https://developers.amadeus.com/self-service/apis-docs/guides/developer-guides/test-data/\n")

        # Using Amadeus TEST data cities (guaranteed to work in test mode)
        destinations = [
            {"city": "Paris", "iata": "PAR", "cityCode": "PAR", "lat": 48.8566, "lon": 2.3522, "country": "France"},
            {"city": "London", "iata": "LON", "cityCode": "LON", "lat": 51.5074, "lon": -0.1278, "country": "UK"},
            {"city": "New York", "iata": "NYC", "cityCode": "NYC", "lat": 40.7128, "lon": -74.0060, "country": "USA"},
            {"city": "Bangkok", "iata": "BKK", "cityCode": "BKK", "lat": 13.7563, "lon": 100.5018, "country": "Thailand"},
        ]

        cached_data = {
            "last_updated": datetime.now().isoformat(),
            "destinations": {}
        }

        for dest in destinations:
            print(f"\n📍 Fetching data for {dest['city']}...")

            try:
                # Fetch flight offers
                flights = self._fetch_flights(dest["iata"])

                # Fetch hotel offers
                hotels = self._fetch_hotels(dest["city"])

                # Fetch activities/points of interest
                activities = self._fetch_activities(dest["city"])

                cached_data["destinations"][dest["city"].lower()] = {
                    "city": dest["city"],
                    "country": dest["country"],
                    "iata_code": dest["iata"],
                    "flights": flights,
                    "hotels": hotels,
                    "activities": activities
                }

                print(f"✅ {dest['city']}: {len(flights)} flights, {len(hotels)} hotels, {len(activities)} activities")

            except Exception as e:
                print(f"❌ Error fetching {dest['city']}: {str(e)}")
                continue

        # Save to cache
        cache_file = self.cache_dir / "real_travel_data.json"
        with open(cache_file, 'w') as f:
            json.dump(cached_data, f, indent=2)

        print(f"\n✅ Real data cached successfully at: {cache_file}")
        print(f"📅 Last updated: {cached_data['last_updated']}")
        return True

    def _fetch_flights(self, destination_iata: str) -> List[Dict]:
        """Fetch real flight offers from Amadeus."""
        try:
            # Calculate dates (2 weeks from now for outbound)
            departure_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

            # Use Amadeus TEST data guaranteed origin cities
            # See: https://developers.amadeus.com/self-service/apis-docs/guides/developer-guides/test-data/
            origin_airports = ["MAD", "NYC", "PAR"]  # Madrid, New York, Paris - guaranteed in test
            all_flights = []

            for origin in origin_airports:
                try:
                    response = self.amadeus.shopping.flight_offers_search.get(
                        originLocationCode=origin,
                        destinationLocationCode=destination_iata,
                        departureDate=departure_date,
                        adults=1,
                        max=5  # Limit to 5 results per origin
                    )

                    for offer in response.data:
                        # Parse the offer
                        flight = self._parse_flight_offer(offer)
                        if flight:
                            all_flights.append(flight)

                except ResponseError as error:
                    print(f"  ⚠️  Flight search error for {origin}: {error}")
                    continue

            return all_flights[:10]  # Return top 10 flights

        except Exception as e:
            print(f"  ❌ Flight fetch error: {str(e)}")
            return []

    def _parse_flight_offer(self, offer: Dict) -> Optional[Dict]:
        """Parse Amadeus flight offer into our format."""
        try:
            itinerary = offer['itineraries'][0]
            segment = itinerary['segments'][0]

            return {
                "airline": segment['carrierCode'],
                "departure_time": segment['departure']['at'],
                "arrival_time": segment['arrival']['at'],
                "duration": itinerary['duration'],
                "price": float(offer['price']['total']),
                "currency": offer['price']['currency'],
                "stops": len(itinerary['segments']) - 1
            }
        except (KeyError, IndexError) as e:
            return None

    def _fetch_hotels(self, city: str) -> List[Dict]:
        """Fetch real hotel offers from Amadeus."""
        try:
            # First, get city code
            city_response = self.amadeus.reference_data.locations.get(
                keyword=city,
                subType='CITY'
            )

            if not city_response.data:
                return []

            city_code = city_response.data[0]['iataCode']

            # Search for hotels
            check_in = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
            check_out = (datetime.now() + timedelta(days=17)).strftime("%Y-%m-%d")

            hotel_response = self.amadeus.reference_data.locations.hotels.by_city.get(
                cityCode=city_code
            )

            hotels = []
            for hotel in hotel_response.data[:10]:  # Top 10 hotels
                hotels.append({
                    "name": hotel.get('name', 'Hotel'),
                    "location": hotel.get('address', {}).get('cityName', city),
                    "chain_code": hotel.get('chainCode', 'N/A'),
                    "iata_code": hotel.get('iataCode', 'N/A')
                })

            return hotels

        except Exception as e:
            print(f"  ❌ Hotel fetch error: {str(e)}")
            return []

    def _fetch_activities(self, city: str) -> List[Dict]:
        """Fetch real activities/tours from Amadeus."""
        try:
            # Get city coordinates first
            city_response = self.amadeus.reference_data.locations.get(
                keyword=city,
                subType='CITY'
            )

            if not city_response.data:
                return []

            location = city_response.data[0]
            lat = location['geoCode']['latitude']
            lon = location['geoCode']['longitude']

            # Search for activities
            activity_response = self.amadeus.shopping.activities.get(
                latitude=lat,
                longitude=lon,
                radius=10
            )

            activities = []
            for activity in activity_response.data[:15]:  # Top 15 activities
                activities.append({
                    "name": activity.get('name', 'Activity'),
                    "description": activity.get('shortDescription', 'Tour activity'),
                    "price": float(activity.get('price', {}).get('amount', 50.0)),
                    "currency": activity.get('price', {}).get('currencyCode', 'USD'),
                    "rating": activity.get('rating', 4.0),
                    "category": activity.get('category', 'SIGHTSEEING')
                })

            return activities

        except Exception as e:
            print(f"  ❌ Activity fetch error: {str(e)}")
            return []

    def load_cached_data(self) -> Optional[Dict]:
        """Load cached real data."""
        cache_file = self.cache_dir / "real_travel_data.json"

        if cache_file.exists():
            with open(cache_file, 'r') as f:
                data = json.load(f)

            # Check cache age
            last_updated = datetime.fromisoformat(data['last_updated'])
            age_days = (datetime.now() - last_updated).days

            if age_days > 7:
                print(f"⚠️  Cached data is {age_days} days old. Consider refreshing.")

            return data
        else:
            print("❌ No cached data found. Run with --refresh to fetch real data.")
            return None


def main():
    """CLI entry point for refreshing real data."""
    import argparse

    parser = argparse.ArgumentParser(description='Fetch and cache real travel data')
    parser.add_argument('--refresh', action='store_true', help='Refresh cached data from Amadeus API')
    parser.add_argument('--check', action='store_true', help='Check cached data status')

    args = parser.parse_args()

    fetcher = RealDataFetcher()

    if args.refresh:
        success = fetcher.fetch_and_cache_all()
        if success:
            print("\n✅ Real data refresh complete!")
        else:
            print("\n❌ Real data refresh failed. Check your API credentials.")

    elif args.check:
        data = fetcher.load_cached_data()
        if data:
            print(f"\n📊 Cached Data Status:")
            print(f"   Last Updated: {data['last_updated']}")
            print(f"   Destinations: {', '.join(data['destinations'].keys())}")
            for city, info in data['destinations'].items():
                print(f"\n   {city.title()}:")
                print(f"      Flights: {len(info.get('flights', []))}")
                print(f"      Hotels: {len(info.get('hotels', []))}")
                print(f"      Activities: {len(info.get('activities', []))}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
