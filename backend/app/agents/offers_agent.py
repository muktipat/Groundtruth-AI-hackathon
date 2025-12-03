"""Offers and coupons agent."""
from typing import Dict, List, Any, Optional
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OffersAgent:
    """Manages customer offers and coupons."""
    
    # Mock offers database
    OFFERS = [
        {
            "id": "WELCOME10",
            "code": "WELCOME10",
            "description": "10% off first order",
            "discount": 10,
            "type": "percentage",
            "min_purchase": 5.0,
            "valid_until": "2025-12-31",
            "categories": ["all"]
        },
        {
            "id": "HOT_COCOA_COUPON",
            "code": "HOT10",
            "description": "Hot Cocoa 10% coupon",
            "discount": 10,
            "type": "percentage",
            "min_purchase": 0.0,
            "valid_until": "2025-12-31",
            "categories": ["hot_drinks"]
        },
        {
            "id": "SUMMER_COLD",
            "code": "COLD15",
            "description": "15% off cold beverages",
            "discount": 15,
            "type": "percentage",
            "min_purchase": 3.0,
            "valid_until": "2025-12-31",
            "categories": ["cold_drinks"]
        },
        {
            "id": "PASTRY_DEAL",
            "code": "PASTRY20",
            "description": "$2 off any pastry",
            "discount": 2.0,
            "type": "fixed",
            "min_purchase": 0.0,
            "valid_until": "2025-12-31",
            "categories": ["pastries"]
        },
        {
            "id": "LOYALTY_REWARD",
            "code": "LOYALTY15",
            "description": "15% loyalty reward for frequent visitors",
            "discount": 15,
            "type": "percentage",
            "min_purchase": 10.0,
            "valid_until": "2025-12-31",
            "categories": ["all"]
        }
    ]
    
    @staticmethod
    def get_personalized_offers(
        customer_id: str,
        weather_context: Optional[str] = None,
        recent_purchases: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get personalized offers for a customer based on weather and preferences."""
        recommended_offers = []
        
        # Weather-based recommendations
        if weather_context:
            weather_lower = weather_context.lower()
            if "cold" in weather_lower or "winter" in weather_lower:
                # Recommend hot drinks
                for offer in OffersAgent.OFFERS:
                    if "hot_drinks" in offer.get("categories", []) or "all" in offer.get("categories", []):
                        recommended_offers.append(offer)
            elif "hot" in weather_lower or "summer" in weather_lower:
                # Recommend cold drinks
                for offer in OffersAgent.OFFERS:
                    if "cold_drinks" in offer.get("categories", []) or "all" in offer.get("categories", []):
                        recommended_offers.append(offer)
        
        # Add loyalty offers
        for offer in OffersAgent.OFFERS:
            if "LOYALTY" in offer["id"] and offer not in recommended_offers:
                recommended_offers.append(offer)
        
        # If no context, return popular offers
        if not recommended_offers:
            recommended_offers = OffersAgent.OFFERS[:3]
        
        return recommended_offers
    
    @staticmethod
    def validate_coupon(code: str) -> Dict[str, Any]:
        """Validate if a coupon code is valid."""
        for offer in OffersAgent.OFFERS:
            if offer["code"] == code:
                return {
                    "valid": True,
                    "code": code,
                    "description": offer["description"],
                    "discount": offer["discount"],
                    "type": offer["type"]
                }
        
        return {
            "valid": False,
            "code": code,
            "message": "Invalid or expired coupon code"
        }
    
    @staticmethod
    def apply_offer(
        order_items: List[Dict[str, float]],
        offer_code: str
    ) -> Dict[str, Any]:
        """Apply an offer to an order."""
        offer = None
        for o in OffersAgent.OFFERS:
            if o["code"] == offer_code:
                offer = o
                break
        
        if not offer:
            return {"success": False, "message": "Invalid offer code"}
        
        # Calculate total
        total = sum([item.get("price", 0) * item.get("quantity", 1) for item in order_items])
        
        # Apply discount
        if offer["type"] == "percentage":
            discount_amount = total * (offer["discount"] / 100)
        else:
            discount_amount = offer["discount"]
        
        return {
            "success": True,
            "offer_code": offer_code,
            "original_total": total,
            "discount_amount": discount_amount,
            "final_total": max(0, total - discount_amount),
            "description": offer["description"]
        }
