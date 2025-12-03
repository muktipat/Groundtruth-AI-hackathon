"""Order management agent."""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OrderAgent:
    """Manages order tracking and information."""
    
    # Mock orders database
    ORDERS = {
        "1001": {
            "customer_id": "cust_001",
            "items": ["Hot Cocoa", "Pastry"],
            "total": 10.94,
            "status": "ready_for_pickup",
            "store": "starbucks_downtown",
            "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
            "pickup_time": "2:00 PM today",
            "notes": "Extra hot"
        },
        "1002": {
            "customer_id": "cust_002",
            "items": ["Latte", "Croissant"],
            "total": 12.45,
            "status": "in_progress",
            "store": "starbucks_phoenix",
            "created_at": (datetime.now() - timedelta(minutes=15)).isoformat(),
            "estimated_ready": "5 minutes",
            "notes": "Oat milk"
        },
        "1234": {
            "customer_id": "cust_001",
            "items": ["Cappuccino", "Pastry"],
            "total": 11.44,
            "status": "ready_for_pickup",
            "store": "starbucks_phoenix",
            "created_at": (datetime.now() - timedelta(hours=1)).isoformat(),
            "pickup_time": "Now",
            "notes": "No foam"
        },
        "1003": {
            "customer_id": "cust_003",
            "items": ["Iced Coffee"],
            "total": 3.45,
            "status": "completed",
            "store": "starbucks_la",
            "created_at": (datetime.now() - timedelta(days=1)).isoformat(),
            "pickup_time": "Yesterday",
            "notes": "Extra ice"
        }
    }
    
    @staticmethod
    def get_order_status(order_id: str) -> Dict[str, Any]:
        """Get status of a specific order."""
        order = OrderAgent.ORDERS.get(order_id)
        
        if not order:
            return {
                "order_id": order_id,
                "found": False,
                "error": "Order not found"
            }
        
        return {
            "order_id": order_id,
            "found": True,
            "status": order["status"],
            "items": order["items"],
            "total": order["total"],
            "store": order["store"],
            "created_at": order["created_at"],
            "pickup_time": order.get("pickup_time", order.get("estimated_ready")),
            "notes": order.get("notes")
        }
    
    @staticmethod
    def get_customer_orders(customer_id: str) -> List[Dict[str, Any]]:
        """Get all orders for a customer."""
        customer_orders = []
        
        for order_id, order in OrderAgent.ORDERS.items():
            if order.get("customer_id") == customer_id:
                customer_orders.append({
                    "order_id": order_id,
                    "status": order["status"],
                    "items": order["items"],
                    "total": order["total"],
                    "store": order["store"],
                    "created_at": order["created_at"]
                })
        
        return sorted(
            customer_orders,
            key=lambda x: x["created_at"],
            reverse=True
        )
    
    @staticmethod
    def create_order(
        customer_id: str,
        items: List[str],
        store_id: str,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new order."""
        # Generate order ID (mock)
        order_id = str(max([int(oid) for oid in OrderAgent.ORDERS.keys()]) + 1)
        
        total = sum([5.0 for _ in items])  # Mock pricing
        
        order = {
            "customer_id": customer_id,
            "items": items,
            "total": total,
            "status": "pending",
            "store": store_id,
            "created_at": datetime.now().isoformat(),
            "estimated_ready": "10-15 minutes",
            "notes": notes
        }
        
        OrderAgent.ORDERS[order_id] = order
        
        return {
            "order_id": order_id,
            "status": "created",
            "items": items,
            "total": total,
            "estimated_ready": "10-15 minutes",
            "message": f"Order {order_id} created successfully"
        }
