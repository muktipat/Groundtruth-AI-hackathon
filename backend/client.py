"""Test client for AuraCX API."""
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


class AuraCXClient:
    """Client for interacting with AuraCX API."""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health."""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def chat(
        self,
        message: str,
        customer_id: str,
        latitude: float,
        longitude: float,
        address: str = None,
        weather_context: str = None
    ) -> Dict[str, Any]:
        """Send a message to AuraCX."""
        payload = {
            "message": message,
            "customer_id": customer_id,
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "address": address or f"{latitude}, {longitude}"
            },
            "customer_profile": {
                "customer_id": customer_id,
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "weather_context": weather_context
            }
        }
        
        response = requests.post(
            f"{self.base_url}/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        return response.json()


def main():
    """Run example interactions."""
    client = AuraCXClient()
    
    print("=" * 60)
    print("AuraCX - Hyper-Personalized Customer Experience")
    print("=" * 60)
    
    # Health check
    print("\n1. Health Check:")
    health = client.health_check()
    print(json.dumps(health, indent=2, default=str))
    
    # Test 1: Store hours query
    print("\n2. Store Hours Query:")
    response = client.chat(
        message="Is your store open right now?",
        customer_id="cust_001",
        latitude=40.7128,
        longitude=-74.0060,
        address="New York, NY"
    )
    print(json.dumps({
        "message": response.get("message"),
        "intent": response.get("intent"),
        "emotion": response.get("emotion"),
        "confidence": response.get("confidence")
    }, indent=2))
    
    # Test 2: Stock check with weather context
    print("\n3. Product Recommendation (Cold Weather):")
    response = client.chat(
        message="I'm cold, what should I get?",
        customer_id="cust_002",
        latitude=40.7128,
        longitude=-74.0060,
        address="New York, NY",
        weather_context="cold"
    )
    print(json.dumps({
        "message": response.get("message"),
        "intent": response.get("intent"),
        "emotion": response.get("emotion"),
        "confidence": response.get("confidence")
    }, indent=2))
    
    # Test 3: Order tracking
    print("\n4. Order Status Query:")
    response = client.chat(
        message="Where is order 1234?",
        customer_id="cust_001",
        latitude=40.7128,
        longitude=-74.0060,
        address="Phoenix, AZ"
    )
    print(json.dumps({
        "message": response.get("message"),
        "intent": response.get("intent"),
        "confidence": response.get("confidence")
    }, indent=2))
    
    # Test 4: Nearby stores
    print("\n5. Location Recommendation:")
    response = client.chat(
        message="Find me a Starbucks nearby",
        customer_id="cust_003",
        latitude=34.0522,
        longitude=-118.2437,
        address="Los Angeles, CA"
    )
    print(json.dumps({
        "message": response.get("message"),
        "intent": response.get("intent"),
        "confidence": response.get("confidence")
    }, indent=2))
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
