# AuraCX Backend

Complete backend for AuraCX - Hyper-Personalized Customer Experience Automation.

## Architecture

### Agents
- **Intent Agent**: Detects user intent and emotion from messages
- **Store Agent**: Manages store hours and location information
- **Inventory Agent**: Tracks product availability and stock
- **Order Agent**: Handles order tracking and status
- **Offers Agent**: Manages coupons and personalized offers

### Services
- **Synthesizer**: Orchestrates all agents and synthesizes responses

### Utilities
- **PII Masker**: Masks sensitive personal information
- **LLM Client**: Wrapper for OpenAI API calls
- **Logger**: Centralized logging

## Setup

### 1. Create .env file
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the server
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```bash
GET /health
```

### Chat Endpoint
```bash
POST /chat
Content-Type: application/json

{
  "message": "Is your store open?",
  "customer_id": "cust_001",
  "location": {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "address": "New York, NY"
  },
  "customer_profile": {
    "customer_id": "cust_001",
    "location": {
      "latitude": 40.7128,
      "longitude": -74.0060
    },
    "past_visits": [],
    "preferences": {},
    "weather_context": "cold"
  }
}
```

## Docker

### Build
```bash
docker build -t auracrx-backend .
```

### Run
```bash
docker run -p 8000:8000 -e OPENAI_API_KEY=<your_key> auracrx-backend
```

### Docker Compose
```bash
OPENAI_API_KEY=<your_key> docker-compose up
```

## Features

✅ Intent Detection with emotion analysis
✅ Store hours and location intelligence
✅ Inventory and stock checking
✅ Order tracking
✅ Personalized offers and coupons
✅ PII masking for privacy
✅ Multi-agent orchestration
✅ Confidence scoring and escalation
✅ FastAPI with async support
✅ CORS enabled for frontend integration

## Data

Mock data is included for:
- 3 Starbucks locations (Downtown NYC, Phoenix, LA)
- Inventory items (coffee, latte, hot cocoa, pastries, etc.)
- Sample orders
- Coupons and offers

Replace with real data sources as needed.

## Testing

### Example Request
```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "Is your store open?",
        "customer_id": "cust_001",
        "location": {
            "latitude": 40.7128,
            "longitude": -74.0060
        }
    }
)

print(response.json())
```

## Next Steps

- ✅ Core tooling mode agents
- ⏳ RAG mode implementation (friend's task)
- ⏳ Frontend integration
- ⏳ Real database integration
- ⏳ Authentication & authorization
- ⏳ Rate limiting
- ⏳ Advanced analytics
