"""Synthesizer service - orchestrates all agents and synthesizes responses."""
from typing import Optional, Dict, Any
from app.models.schemas import ChatRequest, ChatResponse, IntentResult
from app.agents import IntentAgent, StoreAgent, InventoryAgent, OrderAgent, OffersAgent
from app.rag.rag_service import RAGService
from app.utils.pii_masker import pii_masker
from app.utils.llm_client import llm_client
from app.utils.logger import get_logger
from app.config import settings

logger = get_logger(__name__)

# Initialize RAG Service
rag_service = RAGService()


class Synthesizer:
    """Orchestrates agent execution and synthesizes final response."""
    
    RESPONSE_SYSTEM_PROMPT = """You are AuraCX - a hyper-personalized customer service AI.
    
Generate a helpful, accurate, and personalized response based on the intent, data, and context provided.
Keep responses concise and actionable. Include relevant offers when applicable.
Format: Natural conversation, avoid technical jargon."""
    
    @staticmethod
    def process_request(request: ChatRequest) -> ChatResponse:
        """
        Process customer request through all agents.
        
        Args:
            request: Chat request with message and context
            
        Returns:
            ChatResponse with synthesized answer
        """
        try:
            # Step 1: PII Masking
            masked_message, pii_found = pii_masker.mask_text(request.message)
            logger.info(f"PII masked. Found: {list(pii_found.keys())}")
            
            # Step 2: Intent Detection
            intent_result = IntentAgent.detect_intent(masked_message)
            logger.info(f"Intent detected: {intent_result.intent} (confidence: {intent_result.confidence})")
            
            # Check confidence threshold
            if intent_result.confidence < settings.CONFIDENCE_THRESHOLD:
                logger.info(f"Low confidence ({intent_result.confidence}) - routing to RAG Mode")
                return Synthesizer._process_rag_mode(request, masked_message)
            
            # Step 3: Route to appropriate agents based on intent
            agent_data = Synthesizer._route_to_agents(
                intent_result,
                request,
                masked_message
            )
            
            # Step 4: Generate response
            response = Synthesizer._generate_response(
                intent_result,
                agent_data,
                request
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return Synthesizer._create_error_response(request)
    
    @staticmethod
    def _route_to_agents(
        intent_result: IntentResult,
        request: ChatRequest,
        message: str
    ) -> Dict[str, Any]:
        """Route request to appropriate agents based on intent."""
        agent_data = {
            "intent": intent_result.intent,
            "emotion": intent_result.emotion,
            "entities": intent_result.entities
        }
        
        if intent_result.intent == "store_hours":
            nearby_stores = StoreAgent.find_nearby_stores(request.location)
            if nearby_stores:
                store = nearby_stores[0]
                hours = StoreAgent.get_store_hours(store["store_id"])
                agent_data["store_hours"] = hours
                agent_data["nearby_stores"] = nearby_stores
        
        elif intent_result.intent == "stock_check":
            product = intent_result.entities.get("product", "item")
            nearby_stores = StoreAgent.find_nearby_stores(request.location)
            agent_data["inventory"] = []
            for store in nearby_stores:
                availability = InventoryAgent.check_availability(store["store_id"], product)
                agent_data["inventory"].append(availability)
        
        elif intent_result.intent == "order_status":
            order_id = intent_result.entities.get("order_id")
            if order_id:
                order_status = OrderAgent.get_order_status(order_id)
                agent_data["order"] = order_status
        
        elif intent_result.intent == "location_recommendation":
            nearby_stores = StoreAgent.find_nearby_stores(request.location)
            agent_data["nearby_stores"] = nearby_stores
        
        elif intent_result.intent == "product_recommendation":
            # Get personalized offers based on emotion/weather
            weather = request.customer_profile.weather_context if request.customer_profile else None
            offers = OffersAgent.get_personalized_offers(
                request.customer_id,
                weather_context=weather
            )
            agent_data["offers"] = offers
            
            # Find nearby stores
            nearby_stores = StoreAgent.find_nearby_stores(request.location, max_distance_km=3.0)
            agent_data["nearby_stores"] = nearby_stores
        
        return agent_data
    
    @staticmethod
    def _generate_response(
        intent_result: IntentResult,
        agent_data: Dict[str, Any],
        request: ChatRequest
    ) -> ChatResponse:
        """Generate final response using LLM."""
        try:
            # Build context for LLM
            context = f"""
Intent: {intent_result.intent}
Emotion: {intent_result.emotion}
Confidence: {intent_result.confidence:.2f}
Location: {request.location.latitude}, {request.location.longitude}

Data:
{str(agent_data)[:1000]}  # Limit context size
"""
            
            prompt = f"""
Based on the customer's message and intent analysis, generate a personalized response.

Customer message: {request.message}
{context}

Generate a concise, helpful response that addresses their need.
"""
            
            response_text = llm_client.query(
                prompt=prompt,
                system_prompt=Synthesizer.RESPONSE_SYSTEM_PROMPT,
                temperature=0.7,
                max_tokens=500
            )
            
            return ChatResponse(
                message=response_text,
                intent=intent_result.intent,
                emotion=intent_result.emotion,
                confidence=intent_result.confidence,
                mode="tooling",
                data=agent_data,
                requires_escalation=False
            )
        except Exception as e:
            logger.error(f"Response generation error: {str(e)}")
            return ChatResponse(
                message="I'm having trouble processing your request. Please try again.",
                intent=intent_result.intent,
                emotion=intent_result.emotion,
                confidence=0.0,
                mode="tooling",
                requires_escalation=True
            )
    
    @staticmethod
    def _process_rag_mode(request: ChatRequest, message: str) -> ChatResponse:
        """
        Process request through RAG mode.
        
        Args:
            request: Chat request
            message: Masked message
            
        Returns:
            ChatResponse from RAG processing
        """
        try:
            # Extract location if available
            user_location = None
            if request.location:
                user_location = {
                    "latitude": request.location.latitude,
                    "longitude": request.location.longitude
                }
            
            # Process through RAG
            rag_result = rag_service.process_query(message, user_location)
            
            return ChatResponse(
                message=rag_result.get("answer", "Unable to process your query."),
                confidence=rag_result.get("confidence", 0.5),
                mode="rag",
                data={
                    "rewritten_query": rag_result.get("rewritten_query"),
                    "sources": rag_result.get("sources", []),
                    "source_count": rag_result.get("source_count", 0)
                },
                requires_escalation=rag_result.get("requires_escalation", False)
            )
        except Exception as e:
            logger.error(f"RAG mode processing failed: {str(e)}")
            return ChatResponse(
                message="I encountered an issue processing your request. Let me connect you with a specialist.",
                confidence=0.0,
                mode="rag",
                requires_escalation=True
            )
    
    @staticmethod
    def _create_escalation_response(request: ChatRequest) -> ChatResponse:
        """Create response for low confidence requests."""
        return ChatResponse(
            message="I'm not sure I fully understand your request. Could you provide more details or let me connect you with a support agent?",
            confidence=0.0,
            mode="tooling",
            requires_escalation=True
        )
    
    @staticmethod
    def _create_error_response(request: ChatRequest) -> ChatResponse:
        """Create response for errors."""
        return ChatResponse(
            message="I encountered an error processing your request. Please try again or contact support.",
            confidence=0.0,
            mode="tooling",
            requires_escalation=True
        )
