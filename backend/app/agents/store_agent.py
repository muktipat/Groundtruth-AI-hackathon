"""Store information agent - handles store hours and location info."""
from typing import Dict, List, Any, Optional
from datetime import datetime
from app.utils.logger import get_logger
from app.models.schemas import LocationData

logger = get_logger(__name__)


class StoreAgent:
    """Manages store information and hours."""
    
    # Mock store database
    STORES = {
        "starbucks_downtown": {
            "name": "Starbucks Downtown",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "hours": {
                "monday": "6:00 AM - 9:00 PM",
                "tuesday": "6:00 AM - 9:00 PM",
                "wednesday": "6:00 AM - 9:00 PM",
                "thursday": "6:00 AM - 9:00 PM",
                "friday": "6:00 AM - 10:00 PM",
                "saturday": "7:00 AM - 10:00 PM",
                "sunday": "7:00 AM - 9:00 PM"
            },
            "phone": "+1-555-0101",
            "address": "123 Main St, New York, NY"
        },
        "starbucks_phoenix": {
            "name": "Starbucks Phoenix",
            "latitude": 33.4484,
            "longitude": -112.0742,
            "hours": {
                "monday": "5:30 AM - 10:00 PM",
                "tuesday": "5:30 AM - 10:00 PM",
                "wednesday": "5:30 AM - 10:00 PM",
                "thursday": "5:30 AM - 10:00 PM",
                "friday": "5:30 AM - 11:00 PM",
                "saturday": "6:00 AM - 11:00 PM",
                "sunday": "6:00 AM - 10:00 PM"
            },
            "phone": "+1-555-0102",
            "address": "456 Central Ave, Phoenix, AZ"
        },
        "starbucks_la": {
            "name": "Starbucks Los Angeles",
            "latitude": 34.0522,
            "longitude": -118.2437,
            "hours": {
                "monday": "5:00 AM - 9:00 PM",
                "tuesday": "5:00 AM - 9:00 PM",
                "wednesday": "5:00 AM - 9:00 PM",
                "thursday": "5:00 AM - 9:00 PM",
                "friday": "5:00 AM - 10:00 PM",
                "saturday": "6:00 AM - 10:00 PM",
                "sunday": "6:00 AM - 9:00 PM"
            },
            "phone": "+1-555-0103",
            "address": "789 Sunset Blvd, Los Angeles, CA"
        }
    }
    
    @staticmethod
    def get_store_hours(store_id: str) -> Optional[Dict[str, str]]:
        """Get store hours for a specific store."""
        store = StoreAgent.STORES.get(store_id)
        if store:
            return {
                "store_name": store["name"],
                "hours": store["hours"],
                "phone": store["phone"],
                "address": store["address"]
            }
        return None
    
    @staticmethod
    def check_if_open(store_id: str) -> Dict[str, Any]:
        """Check if a store is currently open."""
        store = StoreAgent.STORES.get(store_id)
        if not store:
            return {"is_open": False, "error": "Store not found"}
        
        # Mock check - in production, parse actual hours
        current_time = datetime.now()
        current_day = current_time.strftime("%A").lower()
        
        hours = store["hours"].get(current_day, "Closed")
        
        return {
            "store_name": store["name"],
            "is_open": hours != "Closed",
            "hours": hours,
            "phone": store["phone"],
            "address": store["address"]
        }
    
    @staticmethod
    def find_nearby_stores(
        user_location: LocationData,
        max_distance_km: float = 5.0
    ) -> List[Dict[str, Any]]:
        """Find nearby stores within radius."""
        nearby = []
        
        for store_id, store_info in StoreAgent.STORES.items():
            # Simple distance calculation (Haversine formula simplified)
            lat_diff = abs(store_info["latitude"] - user_location.latitude)
            lon_diff = abs(store_info["longitude"] - user_location.longitude)
            distance = ((lat_diff ** 2 + lon_diff ** 2) ** 0.5) * 111  # Rough conversion to km
            
            if distance <= max_distance_km:
                nearby.append({
                    "store_id": store_id,
                    "name": store_info["name"],
                    "distance_km": round(distance, 2),
                    "address": store_info["address"],
                    "phone": store_info["phone"]
                })
        
        return sorted(nearby, key=lambda x: x["distance_km"])
