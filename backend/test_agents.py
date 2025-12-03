"""Unit tests for AuraCX backend."""
import pytest
from app.utils.pii_masker import pii_masker
from app.agents.intent_agent import IntentAgent
from app.agents.store_agent import StoreAgent
from app.agents.inventory_agent import InventoryAgent
from app.agents.order_agent import OrderAgent
from app.agents.offers_agent import OffersAgent
from app.models.schemas import LocationData


class TestPIIMasker:
    """Test PII masking functionality."""
    
    def test_mask_email(self):
        """Test email masking."""
        text = "Contact me at john.doe@example.com"
        masked, pii = pii_masker.mask_text(text)
        assert "john.doe@example.com" not in masked
        assert "emails" in pii
    
    def test_mask_phone(self):
        """Test phone masking."""
        text = "Call me at 555-123-4567"
        masked, pii = pii_masker.mask_text(text)
        assert "555-123-4567" not in masked
        assert "phones" in pii
    
    def test_no_pii(self):
        """Test text without PII."""
        text = "I want a hot coffee"
        masked, pii = pii_masker.mask_text(text)
        assert masked == text
        assert len(pii) == 0


class TestStoreAgent:
    """Test store agent functionality."""
    
    def test_find_nearby_stores(self):
        """Test finding nearby stores."""
        location = LocationData(latitude=40.7128, longitude=-74.0060)
        stores = StoreAgent.find_nearby_stores(location)
        assert len(stores) > 0
        assert "starbucks_downtown" in [s["store_id"] for s in stores]
    
    def test_get_store_hours(self):
        """Test getting store hours."""
        hours = StoreAgent.get_store_hours("starbucks_downtown")
        assert hours is not None
        assert "hours" in hours
        assert "monday" in hours["hours"]
    
    def test_check_if_open(self):
        """Test checking if store is open."""
        status = StoreAgent.check_if_open("starbucks_downtown")
        assert "is_open" in status
        assert "hours" in status


class TestInventoryAgent:
    """Test inventory agent functionality."""
    
    def test_check_availability(self):
        """Test checking product availability."""
        result = InventoryAgent.check_availability("starbucks_downtown", "hot cocoa")
        assert "available" in result
        assert "quantity" in result
    
    def test_search_product_location(self):
        """Test searching for product across stores."""
        results = InventoryAgent.search_product_location("coffee")
        assert isinstance(results, list)
    
    def test_get_store_menu(self):
        """Test getting store menu."""
        menu = InventoryAgent.get_store_menu("starbucks_downtown")
        assert "products" in menu
        assert len(menu["products"]) > 0


class TestOrderAgent:
    """Test order agent functionality."""
    
    def test_get_order_status(self):
        """Test getting order status."""
        status = OrderAgent.get_order_status("1234")
        assert status["found"] == True
        assert "status" in status
    
    def test_get_customer_orders(self):
        """Test getting customer orders."""
        orders = OrderAgent.get_customer_orders("cust_001")
        assert isinstance(orders, list)
    
    def test_create_order(self):
        """Test creating new order."""
        result = OrderAgent.create_order(
            "cust_test",
            ["Hot Cocoa"],
            "starbucks_downtown"
        )
        assert "order_id" in result
        assert result["status"] == "created"


class TestOffersAgent:
    """Test offers agent functionality."""
    
    def test_get_personalized_offers(self):
        """Test getting personalized offers."""
        offers = OffersAgent.get_personalized_offers(
            "cust_001",
            weather_context="cold"
        )
        assert isinstance(offers, list)
    
    def test_validate_coupon(self):
        """Test coupon validation."""
        result = OffersAgent.validate_coupon("HOT10")
        assert result["valid"] == True
    
    def test_invalid_coupon(self):
        """Test invalid coupon."""
        result = OffersAgent.validate_coupon("INVALID")
        assert result["valid"] == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
