"""Intent detection and emotion analysis agent."""
from app.utils.llm_client import llm_client
from app.utils.logger import get_logger
from app.models.schemas import IntentResult

logger = get_logger(__name__)


class IntentAgent:
    """Detects user intent and emotion from message."""
    
    INTENT_SYSTEM_PROMPT = """You are an intent detection expert. Analyze the user message and respond with JSON.
    
Detect:
1. Intent: "store_hours", "stock_check", "order_status", "location_recommendation", "product_recommendation", or "other"
2. Confidence: 0.0 to 1.0
3. Emotion: "positive", "negative", "neutral", "frustrated", "cold", "warm"
4. Entities: Extract relevant entities (store name, product, order ID, etc.)

Respond with valid JSON only."""
    
    @staticmethod
    def detect_intent(message: str) -> IntentResult:
        """
        Detect intent from user message.
        
        Args:
            message: User input message
            
        Returns:
            IntentResult with detected intent, confidence, emotion, and entities
        """
        try:
            prompt = f"Analyze this message: '{message}'"
            
            response = llm_client.query(
                prompt=prompt,
                system_prompt=IntentAgent.INTENT_SYSTEM_PROMPT,
                temperature=0.3,
                max_tokens=500,
                json_mode=True
            )
            
            data = llm_client.extract_json(response)
            
            return IntentResult(
                intent=data.get("intent", "other"),
                confidence=float(data.get("confidence", 0.5)),
                emotion=data.get("emotion"),
                entities=data.get("entities", {})
            )
        except Exception as e:
            logger.error(f"Intent detection error: {str(e)}")
            return IntentResult(
                intent="other",
                confidence=0.0,
                emotion="neutral",
                entities={}
            )
