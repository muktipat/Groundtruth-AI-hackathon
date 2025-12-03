# AuraCX Backend - Setup & Development Guide

## Quick Start

### 1. Prerequisites
- Python 3.11+
- OpenAI API Key
- pip or conda

### 2. Installation

```bash
# Clone the repository
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Run the Server

```bash
python run.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

### 4. Test the API

**Using the test client:**
```bash
python client.py
```

**Using curl:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Is your store open?",
    "customer_id": "cust_001",
    "location": {
      "latitude": 40.7128,
      "longitude": -74.0060
    }
  }'
```

**Using Python requests:**
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

## Project Structure

```
backend/
├── app/
│   ├── agents/              # Specialized agents
│   │   ├── intent_agent.py         # Intent detection
│   │   ├── store_agent.py          # Store info
│   │   ├── inventory_agent.py      # Stock info
│   │   ├── order_agent.py          # Order tracking
│   │   └── offers_agent.py         # Coupons & offers
│   ├── services/            # High-level services
│   │   └── synthesizer.py          # Agent orchestration
│   ├── utils/               # Utilities
│   │   ├── pii_masker.py           # Privacy protection
│   │   ├── llm_client.py           # OpenAI integration
│   │   └── logger.py               # Logging
│   ├── models/
│   │   └── schemas.py              # Pydantic schemas
│   ├── main.py              # FastAPI app
│   └── config.py            # Configuration
├── run.py                   # Server entrypoint
├── client.py                # Test client
├── test_agents.py           # Unit tests
├── Dockerfile               # Docker config
├── docker-compose.yml       # Docker Compose config
└── requirements.txt         # Python dependencies
```

## Architecture

### Two-Mode Design

1. **Tooling Mode** (Current Implementation)
   - Fast, deterministic agents
   - Handles: store hours, stock, orders, offers
   - No hallucination risk

2. **RAG Mode** (Future)
   - Complex/vague queries
   - Uses vector search + reranking
   - Deployed by your friend

### Agent Workflow

```
User Message
    ↓
PII Masking
    ↓
Intent Detection → Emotion Analysis
    ↓
Route to Agents
    ├── Store Agent (if store_hours)
    ├── Inventory Agent (if stock_check)
    ├── Order Agent (if order_status)
    ├── Offers Agent (if recommendations)
    └── ...
    ↓
Synthesizer Combines Results
    ↓
LLM Generates Response
    ↓
Return ChatResponse
```

## Configuration

### Environment Variables (.env)

```env
# Required
OPENAI_API_KEY=sk-...your-key...

# Optional
ENVIRONMENT=development          # development or production
LOG_LEVEL=INFO                  # DEBUG, INFO, WARNING, ERROR
```

### Model Configuration (app/config.py)

```python
GPT_MODEL = "gpt-4-turbo-preview"  # Model to use
TEMPERATURE = 0.7                 # Creativity level
MAX_TOKENS = 2048                # Response length
CONFIDENCE_THRESHOLD = 0.7        # Escalation threshold
```

## API Reference

### Endpoints

#### 1. Health Check
```
GET /health

Response:
{
  "status": "healthy",
  "timestamp": "2025-12-03T10:00:00",
  "environment": "development"
}
```

#### 2. Chat
```
POST /chat

Request:
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

Response:
{
  "message": "The Starbucks Downtown is open until 9 PM.",
  "intent": "store_hours",
  "emotion": "neutral",
  "confidence": 0.95,
  "mode": "tooling",
  "data": {
    "store_hours": {...},
    "nearby_stores": [...]
  },
  "requires_escalation": false,
  "timestamp": "2025-12-03T10:00:00"
}
```

## Supported Intents

1. **store_hours** - Query store operating hours
2. **stock_check** - Check product availability
3. **order_status** - Track order status
4. **location_recommendation** - Find nearby stores
5. **product_recommendation** - Get personalized suggestions
6. **other** - Escalate or use RAG mode

## Testing

### Run Unit Tests
```bash
pytest test_agents.py -v
```

### Run with Coverage
```bash
pytest test_agents.py --cov=app --cov-report=html
```

## Docker

### Build Image
```bash
docker build -t auracrx-backend:latest .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-... \
  auracrx-backend:latest
```

### Using Docker Compose
```bash
OPENAI_API_KEY=sk-... docker-compose up
```

## Development

### Adding a New Agent

1. Create `app/agents/new_agent.py`
2. Implement agent class with methods
3. Add to `app/agents/__init__.py`
4. Update Synthesizer routing logic
5. Add tests in `test_agents.py`

### Example Agent
```python
from app.utils.logger import get_logger

logger = get_logger(__name__)

class NewAgent:
    @staticmethod
    def do_something(data):
        logger.info("Processing...")
        return {"result": "data"}
```

## Troubleshooting

### OpenAI API Key Error
```
ValueError: OPENAI_API_KEY not set in environment
```
→ Make sure to set OPENAI_API_KEY in .env file

### Port Already in Use
```
OSError: [Errno 48] Address already in use
```
→ Change port in `run.py` or kill existing process

### Slow Responses
→ Check OpenAI API status
→ Reduce MAX_TOKENS in config.py
→ Use faster model (gpt-3.5-turbo)

## Production Deployment

### Prerequisites
- Docker and Docker Compose
- GPU (optional, for faster inference)
- Monitoring setup (Prometheus, ELK, etc.)

### Steps
1. Set ENVIRONMENT=production in .env
2. Disable LOG_LEVEL=WARNING
3. Use `docker-compose up -d`
4. Set up reverse proxy (Nginx)
5. Enable HTTPS/TLS
6. Add rate limiting
7. Set up monitoring

## Next Steps

- [ ] Integrate with real database
- [ ] Add authentication (JWT)
- [ ] Implement rate limiting
- [ ] Add request/response logging
- [ ] Set up monitoring & alerts
- [ ] Integrate RAG mode
- [ ] Add frontend
- [ ] Performance optimization

## Support

For issues or questions, please check:
1. The main README.md
2. API documentation at /docs
3. Test examples in client.py
4. Issue tracker on GitHub

---

**Happy coding! 🚀**
