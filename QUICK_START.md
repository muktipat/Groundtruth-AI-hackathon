# 🚀 AuraCX - Quick Start Guide

Welcome to AuraCX! This guide will get you up and running in minutes.

## What's Been Built

✅ **Complete Backend with 5 Intelligent Agents**
- Intent Detection (what does user want?)
- Store Intelligence (hours, locations, availability)
- Inventory Management (stock checking)
- Order Tracking (where's my order?)
- Personalized Offers (smart coupons)

✅ **Multi-Agent Orchestration System**
- PII Masking for privacy
- Confidence scoring with escalation
- Emotion & intent analysis
- GPT-powered response generation

✅ **Production-Ready Infrastructure**
- FastAPI server
- Docker containerization
- Comprehensive logging
- Unit tests
- API documentation

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Add Your OpenAI Key
```bash
cp .env.example .env
# Edit .env and paste your OPENAI_API_KEY
```

### Step 3: Start the Server
```bash
python run.py
```

You'll see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 4: Test It!
In a new terminal:
```bash
python client.py
```

You'll see 5 test conversations running! 🎉

## What Just Happened?

Your backend is now running with:
- **REST API** at `http://localhost:8000`
- **API Docs** at `http://localhost:8000/docs` (try interactive testing!)
- **5 Expert Agents** ready to handle customer requests
- **Real-time Response Generation** using GPT

## Try the API

### Using Swagger UI (Easiest)
1. Open http://localhost:8000/docs
2. Click on `/chat` endpoint
3. Click "Try it out"
4. Paste this and click "Execute":

```json
{
  "message": "Is your store open?",
  "customer_id": "cust_001",
  "location": {
    "latitude": 40.7128,
    "longitude": -74.0060
  }
}
```

### Using curl
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Do you have hot cocoa?",
    "customer_id": "cust_001",
    "location": {"latitude": 40.7128, "longitude": -74.0060}
  }' | jq
```

### Using Python
```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "Where is my order?",
        "customer_id": "cust_001",
        "location": {"latitude": 40.7128, "longitude": -74.0060}
    }
)

print(response.json()["message"])
```

## Test Different Intents

Try these messages to see different agents in action:

| Message | Agent Triggered | Description |
|---------|-----------------|-------------|
| "Is your store open?" | Store Agent | Check hours |
| "Do you have hot cocoa?" | Inventory Agent | Check stock |
| "Where is order 1234?" | Order Agent | Track order |
| "Find me nearby" | Store Agent | Nearby locations |
| "I'm cold" | Offers Agent | Smart recommendations |

## Project Structure

```
backend/
├── app/agents/          ← 5 Intelligent Agents
├── app/services/        ← Orchestration (Synthesizer)
├── app/utils/           ← PII masking, logging, LLM
├── app/models/          ← Data schemas
├── app/main.py          ← FastAPI app
├── app/config.py        ← Configuration
├── run.py              ← Server startup
├── client.py           ← Test client
└── test_agents.py      ← Unit tests
```

## Key Concepts

### Agents
Each agent is an expert at one task:
- **IntentAgent** - "What does the user want?"
- **StoreAgent** - "Where are we and when are we open?"
- **InventoryAgent** - "Do we have this product?"
- **OrderAgent** - "What's the status of this order?"
- **OffersAgent** - "What deal fits this customer?"

### Synthesizer
The orchestrator that:
1. Detects intent
2. Routes to right agents
3. Gathers all data
4. Generates final response

### PII Masking
Protects customer privacy:
- Hides emails, phone numbers, SSNs
- Done BEFORE sending to GPT
- Ensures compliance with regulations

### Confidence Scoring
- Agents return confidence scores (0-1)
- Low confidence → Escalate to human
- High confidence → Send response

## Customization

### Change the Model
Edit `app/config.py`:
```python
GPT_MODEL = "gpt-3.5-turbo"  # Faster, cheaper
GPT_MODEL = "gpt-4"          # Smarter
```

### Change the Stores
Edit mock data in:
- `app/agents/store_agent.py` - Store locations & hours
- `app/agents/inventory_agent.py` - Products & prices
- `app/agents/order_agent.py` - Sample orders

### Change Confidence Threshold
Edit `app/config.py`:
```python
CONFIDENCE_THRESHOLD = 0.8  # Higher = more escalations
```

## Docker Deployment

```bash
# Build image
docker build -t auracrx .

# Run with your key
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... auracrx

# Or use Docker Compose
OPENAI_API_KEY=sk-... docker-compose up
```

## Next Steps

### 1. Frontend Integration
Your friend or you can build a React/Vue frontend:
```javascript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  body: JSON.stringify({
    message: userInput,
    customer_id: customerId,
    location: {latitude, longitude}
  })
});
```

### 2. Database Integration
Replace mock data with real database:
- User profiles
- Order history
- Product catalog
- Store locations

### 3. RAG Mode
Your friend will add sophisticated NLP:
- Vector search for complex questions
- Semantic understanding
- Hallucination prevention
- Smart reranking

### 4. Advanced Features
- User authentication
- Chat history
- Analytics dashboard
- Multi-language support
- Voice input/output

## Common Issues

### "OPENAI_API_KEY not set"
→ Make sure `.env` file exists with your key

### "Port 8000 already in use"
→ Kill the process or change port in `run.py`

### "ModuleNotFoundError"
→ Run `pip install -r requirements.txt`

### Slow responses
→ Try faster model: `gpt-3.5-turbo`

## File Reference

| File | Purpose |
|------|---------|
| `SETUP.md` | Detailed setup instructions |
| `README.md` | Technical overview |
| `API_EXAMPLES.json` | Request/response examples |
| `RAG_INTEGRATION_GUIDE.md` | How RAG mode will work |
| `BACKEND_IMPLEMENTATION.md` | What was built |

## Architecture at a Glance

```
User Query
    ↓
[FastAPI] Validates request
    ↓
[PII Masker] Hides sensitive data
    ↓
[Intent Agent] "What does user want?"
    ↓
[Synthesizer] Picks right agents
    ↓
[Agents] Gather data in parallel
    ├── Store Agent
    ├── Inventory Agent
    ├── Order Agent
    ├── Offers Agent
    └── ...
    ↓
[LLM] Generates response
    ↓
[Response] Returned to user
```

## Success Criteria

Your backend is working when:
- ✅ Server starts without errors
- ✅ `/docs` shows interactive API
- ✅ `python client.py` runs 5 tests
- ✅ You can get responses from `/chat`
- ✅ Different intents trigger different agents

## Performance Notes

- Response time: ~1-2 seconds (API call to GPT included)
- Throughput: Limited by OpenAI API rate limits
- Concurrency: FastAPI handles many requests
- Scalability: Docker/K8s ready

## Security Features

- ✅ PII masking before LLM
- ✅ Confidence thresholds prevent hallucinations
- ✅ CORS configured for frontend
- ✅ Environment variables for secrets
- ✅ Structured logging for audit trail

## Getting Help

1. **Check API Docs** - `http://localhost:8000/docs`
2. **Read SETUP.md** - Detailed instructions
3. **Check API_EXAMPLES.json** - Sample requests/responses
4. **Review test_agents.py** - Unit test examples
5. **Check client.py** - Working example code

## Ready? Let's Go! 🎉

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your key
python run.py
```

Then in another terminal:
```bash
python client.py
```

Watch it work! 🚀

---

**Questions?** Check the documentation or run the examples!

**Next?** Start planning your frontend integration!

**Your friend?** Have them read RAG_INTEGRATION_GUIDE.md!

Happy building! 💪
