"""Inventory and stock availability agent."""
from typing import Dict, List, Any, Optional
from app.utils.logger import get_logger

logger = get_logger(__name__)


class InventoryAgent:
    """Manages inventory and stock information."""
    
    # Mock inventory database
    INVENTORY = {
        "starbucks_downtown": {
            "hot_cocoa": {"quantity": 50, "price": 4.95},
            "coffee": {"quantity": 100, "price": 2.95},
            "latte": {"quantity": 75, "price": 5.45},
            "cappuccino": {"quantity": 60, "price": 5.45},
            "iced_coffee": {"quantity": 40, "price": 3.45},
            "pastry": {"quantity": 120, "price": 5.99}
        },
        "starbucks_phoenix": {
            "hot_cocoa": {"quantity": 80, "price": 4.95},
            "coffee": {"quantity": 150, "price": 2.95},
            "latte": {"quantity": 120, "price": 5.45},
            "cappuccino": {"quantity": 100, "price": 5.45},
            "iced_coffee": {"quantity": 50, "price": 3.45},
            "pastry": {"quantity": 200, "price": 5.99}
        },
        "starbucks_la": {
            "hot_cocoa": {"quantity": 60, "price": 4.95},
            "coffee": {"quantity": 120, "price": 2.95},
            "latte": {"quantity": 90, "price": 5.45},
            "cappuccino": {"quantity": 80, "price": 5.45},
            "iced_coffee": {"quantity": 30, "price": 3.45},
            "pastry": {"quantity": 150, "price": 5.99}
        }
    }
    
    @staticmethod
    def check_availability(store_id: str, product: str) -> Dict[str, Any]:
        """Check if product is available at store."""
        store_inventory = InventoryAgent.INVENTORY.get(store_id)
        
        if not store_inventory:
            return {"available": False, "error": "Store not found"}
        
        product_lower = product.lower().replace(" ", "_")
        item = store_inventory.get(product_lower)
        
        if not item:
            return {
                "product": product,
                "available": False,
                "reason": "Product not found in this store"
            }
        
        available = item["quantity"] > 0
        
        return {
            "product": product,
            "available": available,
            "quantity": item["quantity"] if available else 0,
            "price": item["price"],
            "message": f"In stock at {store_id}" if available else "Out of stock"
        }
    
    @staticmethod
    def search_product_location(product: str) -> List[Dict[str, Any]]:
        """Search all stores for a product."""
        results = []
        product_lower = product.lower().replace(" ", "_")
        
        for store_id, inventory in InventoryAgent.INVENTORY.items():
            if product_lower in inventory:
                item = inventory[product_lower]
                if item["quantity"] > 0:
                    results.append({
                        "store_id": store_id,
                        "quantity": item["quantity"],
                        "price": item["price"],
                        "available": True
                    })
        
        return results
    
    @staticmethod
    def get_store_menu(store_id: str) -> Dict[str, Any]:
        """Get all available products at a store."""
        inventory = InventoryAgent.INVENTORY.get(store_id)
        
        if not inventory:
            return {"error": "Store not found"}
        
        products = []
        for product_key, details in inventory.items():
            products.append({
                "name": product_key.replace("_", " ").title(),
                "price": details["price"],
                "in_stock": details["quantity"] > 0,
                "quantity": details["quantity"]
            })
        
        return {"store_id": store_id, "products": products}
