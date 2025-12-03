"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class LocationData(BaseModel):
    """User location data."""
    latitude: float = Field(..., description="User latitude")
    longitude: float = Field(..., description="User longitude")
    address: Optional[str] = Field(None, description="User address")


class CustomerProfile(BaseModel):
    """Customer profile data."""
    customer_id: str = Field(..., description="Unique customer identifier")
    location: LocationData
    past_visits: List[Dict[str, Any]] = Field(default_factory=list)
    preferences: Dict[str, Any] = Field(default_factory=dict)
    weather_context: Optional[str] = None


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str = Field(..., description="User message")
    customer_id: str = Field(..., description="Customer ID")
    location: LocationData = Field(..., description="User location")
    customer_profile: Optional[CustomerProfile] = None
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)


class IntentResult(BaseModel):
    """Intent detection result."""
    intent: str = Field(..., description="Detected intent")
    confidence: float = Field(..., description="Confidence score 0-1")
    entities: Dict[str, Any] = Field(default_factory=dict)
    emotion: Optional[str] = None


class ToolingResult(BaseModel):
    """Result from tooling mode agents."""
    store_hours: Optional[Dict[str, str]] = None
    stock_availability: Optional[Dict[str, Any]] = None
    order_status: Optional[Dict[str, Any]] = None
    nearby_locations: Optional[List[Dict[str, Any]]] = None
    offers: Optional[List[Dict[str, str]]] = None


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    message: str = Field(..., description="Response message")
    intent: Optional[str] = None
    emotion: Optional[str] = None
    confidence: float = Field(..., description="Confidence score")
    mode: str = Field(default="tooling", description="Processing mode used")
    data: Optional[Dict[str, Any]] = None
    requires_escalation: bool = Field(default=False)
    timestamp: datetime = Field(default_factory=datetime.now)


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: datetime
    environment: str
