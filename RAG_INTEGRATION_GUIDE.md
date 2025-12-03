# AuraCX Backend - RAG Mode Integration Guide

This document explains how the RAG Mode (your friend's task) will integrate with the existing Tooling Mode backend.

## Architecture Overview

```
User Message
    ↓
PII Masking (Shared Layer)
    ↓
Intent Detection
    ↓
    ├─→ [HIGH CONFIDENCE] → Tooling Mode Agents ✅ (Your implementation)
    │       ├── Store Agent
    │       ├── Inventory Agent
    │       ├── Order Agent
    │       └── Offers Agent
    │       ↓
    │       Synthesizer
    │       ↓
    │       Response
    │
    └─→ [LOW CONFIDENCE / COMPLEX] → RAG Mode 🔄 (Friend's implementation)
            ├── Query Rewriting
            ├── Vector Search
            ├── Reranking
            ├── Context Compression
            └── Hallucination Check
            ↓
            Response
```

## Current Implementation

### Synthesizer Routing Logic
Located in `app/services/synthesizer.py`:

```python
# Step 2: Intent Detection
intent_result = IntentAgent.detect_intent(masked_message)

# Check confidence threshold
if intent_result.confidence < settings.CONFIDENCE_THRESHOLD:
    return Synthesizer._create_escalation_response(request)

# Step 3: Route to appropriate agents based on intent
agent_data = Synthesizer._route_to_agents(...)
```

**Current behavior:** Low confidence → Escalation to human

**After RAG Integration:** Low confidence → Route to RAG Mode

## Integration Points

### 1. Confidence Threshold Routing

**File:** `app/services/synthesizer.py`

**Current code (lines ~80-85):**
```python
# Check confidence threshold
if intent_result.confidence < settings.CONFIDENCE_THRESHOLD:
    return Synthesizer._create_escalation_response(request)
```

**Will become:**
```python
# Check confidence threshold
if intent_result.confidence < settings.CONFIDENCE_THRESHOLD:
    # Route to RAG Mode
    rag_response = RAGService.process_request(request, masked_message)
    return rag_response
```

### 2. Create RAG Service Class

**New file:** `app/services/rag_service.py`

```python
from typing import Optional
from app.models.schemas import ChatRequest, ChatResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)

class RAGService:
    """Handles RAG Mode processing."""
    
    @staticmethod
    def process_request(request: ChatRequest, message: str) -> ChatResponse:
        """
        Process request using RAG Mode.
        
        Args:
            request: Chat request
            message: Masked message
            
        Returns:
            ChatResponse from RAG processing
        """
        try:
            # Step 1: Query Rewriting
            rewritten_query = RAGService._rewrite_query(message)
            
            # Step 2: Vector Search / Semantic Retrieval
            retrieved_docs = RAGService._retrieve_documents(rewritten_query)
            
            # Step 3: Reranking
            ranked_docs = RAGService._rerank_documents(retrieved_docs, rewritten_query)
            
            # Step 4: Context Compression
            compressed_context = RAGService._compress_context(ranked_docs)
            
            # Step 5: Generate Answer
            answer = RAGService._generate_answer(message, compressed_context)
            
            # Step 6: Hallucination Check
            is_hallucinating = RAGService._check_hallucination(answer, ranked_docs)
            
            if is_hallucinating:
                answer = "I'm not certain about that. Let me connect you with a specialist."
                requires_escalation = True
            else:
                requires_escalation = False
            
            return ChatResponse(
                message=answer,
                confidence=0.75,  # RAG confidence
                mode="rag",
                requires_escalation=requires_escalation
            )
            
        except Exception as e:
            logger.error(f"RAG processing error: {str(e)}")
            return ChatResponse(
                message="I couldn't find information to answer that.",
                confidence=0.0,
                mode="rag",
                requires_escalation=True
            )
    
    @staticmethod
    def _rewrite_query(query: str) -> str:
        """Rewrite query for better retrieval."""
        # TODO: Implement query rewriting with LLM
        pass
    
    @staticmethod
    def _retrieve_documents(query: str) -> list:
        """Retrieve relevant documents from vector store."""
        # TODO: Implement vector search (FAISS/ChromaDB)
        pass
    
    @staticmethod
    def _rerank_documents(docs: list, query: str) -> list:
        """Rerank documents by relevance."""
        # TODO: Implement reranking
        pass
    
    @staticmethod
    def _compress_context(docs: list) -> str:
        """Compress context to essential information."""
        # TODO: Implement context compression
        pass
    
    @staticmethod
    def _generate_answer(query: str, context: str) -> str:
        """Generate answer from context."""
        # TODO: Implement answer generation
        pass
    
    @staticmethod
    def _check_hallucination(answer: str, docs: list) -> bool:
        """Check if answer hallucinates (contradicts docs)."""
        # TODO: Implement hallucination detection
        return False
```

### 3. Update Synthesizer

**File:** `app/services/synthesizer.py`

**Add import:**
```python
from app.services.rag_service import RAGService
```

**Modify routing (around line 80):**
```python
# Step 2: Intent Detection
intent_result = IntentAgent.detect_intent(masked_message)
logger.info(f"Intent detected: {intent_result.intent} (confidence: {intent_result.confidence})")

# Check confidence threshold
if intent_result.confidence < settings.CONFIDENCE_THRESHOLD:
    logger.info("Low confidence - routing to RAG Mode")
    return RAGService.process_request(request, masked_message)

# Rest of tooling mode logic...
```

### 4. Update Services __init__.py

**File:** `app/services/__init__.py`

```python
from app.services.synthesizer import Synthesizer
from app.services.rag_service import RAGService

__all__ = ['Synthesizer', 'RAGService']
```

## Data Flow Examples

### Example 1: High Confidence (Tooling Mode)

```
User: "Is your store open?"
    ↓
Intent: store_hours (confidence: 0.95)
    ↓
Confidence > 0.7 → TOOLING MODE
    ↓
Store Agent → Returns hours
    ↓
Response: "Yes, open until 9 PM"
```

### Example 2: Low Confidence (RAG Mode)

```
User: "What makes you unique compared to competitors?"
    ↓
Intent: other (confidence: 0.45)
    ↓
Confidence < 0.7 → RAG MODE
    ↓
Query Rewriting → Vector Search → Reranking
    ↓
Context: [Document 1, Document 2, ...]
    ↓
Answer Generation: "We stand out because..."
    ↓
Hallucination Check → Pass
    ↓
Response: "We stand out because..."
```

### Example 3: Escalation from RAG

```
User: "Provide investment advice"
    ↓
Intent: other (confidence: 0.40)
    ↓
RAG Mode → No relevant documents found
    ↓
Hallucination detected OR confidence too low
    ↓
requires_escalation = True
    ↓
Response: "I can't help with that. Connect with agent."
```

## Configuration for RAG

Add to `app/config.py`:

```python
# RAG Configuration
RAG_ENABLED: bool = os.getenv("RAG_ENABLED", "false").lower() == "true"
VECTOR_STORE_TYPE: str = os.getenv("VECTOR_STORE_TYPE", "chromadb")  # or "faiss"
RETRIEVAL_TOP_K: int = 5
RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
HALLUCINATION_THRESHOLD: float = 0.5
```

Add to `.env.example`:

```env
# RAG Mode Configuration
RAG_ENABLED=false
VECTOR_STORE_TYPE=chromadb
VECTOR_STORE_PATH=./data/vectors
CHROMA_HOST=localhost
CHROMA_PORT=8001
```

## Vector Store Setup

### Option 1: ChromaDB (Recommended for simplicity)

```python
# app/services/vector_store.py
import chromadb

class VectorStore:
    def __init__(self):
        self.client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT
        )
        self.collection = self.client.get_or_create_collection(
            name="auracrx_docs"
        )
    
    def search(self, query: str, top_k: int = 5) -> list:
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        return results
```

### Option 2: FAISS (For larger scale)

```python
# app/services/vector_store.py
import faiss
import numpy as np

class FAISSVectorStore:
    def __init__(self):
        self.index = faiss.read_index("./data/vectors/index.faiss")
        self.documents = self._load_documents()
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> list:
        distances, indices = self.index.search(
            query_embedding.reshape(1, -1),
            top_k
        )
        return [self.documents[i] for i in indices[0]]
```

## Testing RAG Integration

### Mock Test

```python
# test_rag_service.py
def test_rag_mode_low_confidence():
    request = ChatRequest(
        message="Complex philosophical question?",
        customer_id="test",
        location=LocationData(latitude=0, longitude=0)
    )
    
    response = RAGService.process_request(request, request.message)
    
    assert response.mode == "rag"
    assert isinstance(response.message, str)
```

### Integration Test

```python
def test_synthesizer_routes_to_rag():
    request = ChatRequest(
        message="Some vague question",
        customer_id="test",
        location=LocationData(latitude=0, longitude=0)
    )
    
    response = Synthesizer.process_request(request)
    
    # Should use RAG mode for low confidence intent
    assert response.confidence < 0.7 or response.mode == "rag"
```

## Deployment Considerations

### Docker Compose with RAG

Update `docker-compose.yml`:

```yaml
version: '3.8'

services:
  auracrx-backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - RAG_ENABLED=true
      - CHROMA_HOST=chromadb
    depends_on:
      - chromadb
    
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    environment:
      - ANONYMIZED_TELEMETRY=false
    volumes:
      - chroma_data:/chroma/data

volumes:
  chroma_data:
```

## Handoff Checklist

Before your friend starts RAG implementation:

- [ ] Review this integration guide
- [ ] Understand the ChatRequest/ChatResponse schemas
- [ ] Review confidence threshold logic in Synthesizer
- [ ] Plan vector store choice (ChromaDB vs FAISS)
- [ ] Design document preparation pipeline
- [ ] Set up mock documents for testing
- [ ] Plan query rewriting strategy
- [ ] Design reranking approach
- [ ] Plan hallucination detection method

## Summary

**Tooling Mode (You)** - Fast, deterministic, zero hallucination
- ✅ Ready to use
- Store hours, inventory, orders, offers
- High confidence (>0.7)

**RAG Mode (Friend)** - Semantic, flexible, requires safety checks
- 🔄 To be implemented
- Complex questions, recommendations
- Low confidence (<0.7)

**Integration** - Clean routing through Synthesizer
- Add RAGService.process_request() call
- Update confidence threshold check
- Share PII masking layer
- Common response schema

Good luck! 🚀
