"""RAG Service - Semantic search and retrieval."""
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from app.utils.logger import get_logger
from app.utils.llm_client import llm_client

logger = get_logger(__name__)


class VectorStore:
    """Simple vector store using TF-IDF."""
    
    def __init__(self, documents: List[Dict[str, Any]]):
        """Initialize vector store with documents."""
        self.documents = documents
        self.vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
        
        # Extract document texts
        self.texts = [doc.get('content', '') for doc in documents]
        
        # Fit vectorizer
        self.vectors = self.vectorizer.fit_transform(self.texts)
        logger.info(f"Vector store initialized with {len(documents)} documents")
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search for similar documents.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of (document, similarity_score) tuples
        """
        try:
            # Vectorize query
            query_vector = self.vectorizer.transform([query])
            
            # Calculate similarities
            similarities = query_vector.dot(self.vectors.T).toarray()[0]
            
            # Get top k indices
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            # Return documents with scores
            results = []
            for idx in top_indices:
                results.append((self.documents[idx], float(similarities[idx])))
            
            return results
        except Exception as e:
            logger.error(f"Vector search error: {str(e)}")
            return []


class RAGService:
    """RAG Mode Service for complex queries."""
    
    def __init__(self):
        """Initialize RAG service."""
        self.documents = self._load_rag_documents()
        self.vector_store = VectorStore(self.documents) if self.documents else None
        logger.info("RAG Service initialized")
    
    @staticmethod
    def _load_rag_documents() -> List[Dict[str, Any]]:
        """Load RAG documents from JSON."""
        try:
            doc_path = Path('backend/data/rag_docs/customers.json')
            if doc_path.exists():
                with open(doc_path, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.warning(f"Could not load RAG documents: {str(e)}")
            return []
    
    def _rewrite_query(self, query: str) -> str:
        """
        Rewrite vague query using LLM.
        
        Args:
            query: Original user query
            
        Returns:
            Rewritten, structured query
        """
        try:
            prompt = f"""Rewrite this vague customer query into a structured form that captures intent, emotion, and context:

Original query: "{query}"

Provide a structured interpretation that includes:
1. Primary intent (what they need)
2. Emotional state
3. Context (time, weather, location relevance)
4. Recommended store type

Be concise and specific."""
            
            rewritten = llm_client.query(
                prompt=prompt,
                temperature=0.3,
                max_tokens=200
            )
            return rewritten
        except Exception as e:
            logger.warning(f"Query rewriting failed: {str(e)}")
            return query
    
    def _retrieve_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents using vector search.
        
        Args:
            query: Search query
            top_k: Number of results
            
        Returns:
            List of retrieved documents
        """
        if not self.vector_store:
            logger.warning("Vector store not available")
            return []
        
        try:
            results = self.vector_store.search(query, top_k=top_k)
            return [doc for doc, _ in results]
        except Exception as e:
            logger.error(f"Document retrieval failed: {str(e)}")
            return []
    
    def _rerank_documents(self, documents: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """
        Rerank documents by relevance using LLM scoring.
        
        Args:
            documents: Retrieved documents
            query: Original query
            
        Returns:
            Reranked documents
        """
        if not documents:
            return []
        
        try:
            # Score each document
            scored_docs = []
            for doc in documents:
                score_prompt = f"""Rate how relevant this customer interaction is to the query.

Query: {query}
Customer context: {doc.get('content', '')}
Interpreted need: {doc.get('metadata', {}).get('interpreted_need', '')}

Provide a relevance score (0-1) with brief explanation."""
                
                response = llm_client.query(
                    prompt=score_prompt,
                    temperature=0.1,
                    max_tokens=100
                )
                
                # Extract score (simple parsing)
                try:
                    score = float([w for w in response.split() if w.replace('.', '').isdigit()][0])
                    score = min(1.0, max(0.0, score))
                except:
                    score = 0.5
                
                scored_docs.append((doc, score))
            
            # Sort by score
            scored_docs.sort(key=lambda x: x[1], reverse=True)
            return [doc for doc, _ in scored_docs]
        except Exception as e:
            logger.warning(f"Reranking failed: {str(e)}")
            return documents
    
    def _compress_context(self, documents: List[Dict[str, Any]]) -> str:
        """
        Compress context to essential information.
        
        Args:
            documents: Retrieved documents
            
        Returns:
            Compressed context string
        """
        if not documents:
            return "No relevant information found."
        
        try:
            # Build context summary
            context_parts = []
            for doc in documents[:3]:  # Top 3 docs
                metadata = doc.get('metadata', {})
                context_parts.append(f"""
- Context: {doc.get('content', '')}
  Emotion: {metadata.get('emotion', 'unknown')}
  Weather: {metadata.get('weather', 'unknown')}
  Store: {metadata.get('store', 'unknown')}
  Need: {metadata.get('interpreted_need', 'unknown')}
  Offer: {metadata.get('offer', 'none')}
""")
            
            return "Based on similar customer interactions:\n" + "\n".join(context_parts)
        except Exception as e:
            logger.error(f"Context compression failed: {str(e)}")
            return "No context available."
    
    def _generate_answer(self, query: str, context: str) -> str:
        """
        Generate answer using context.
        
        Args:
            query: User query
            context: Retrieved context
            
        Returns:
            Generated answer
        """
        try:
            prompt = f"""You are a helpful customer service AI. Answer the customer's query using the provided context from similar customer interactions.

Customer Query: {query}

Context from similar interactions:
{context}

Provide a helpful, personalized response that:
1. Addresses their likely need
2. Recommends specific store/offer if relevant
3. Considers weather/location/emotion
4. Is concise and actionable"""
            
            answer = llm_client.query(
                prompt=prompt,
                temperature=0.7,
                max_tokens=300
            )
            return answer
        except Exception as e:
            logger.error(f"Answer generation failed: {str(e)}")
            return "I'm unable to answer that right now. Please try again."
    
    def _check_hallucination(self, answer: str, documents: List[Dict[str, Any]]) -> bool:
        """
        Check if answer hallucinates (contradicts documents).
        
        Args:
            answer: Generated answer
            documents: Source documents
            
        Returns:
            True if hallucinating, False otherwise
        """
        if not documents:
            return True  # No source = hallucination
        
        try:
            # Extract facts from documents
            facts = []
            for doc in documents:
                metadata = doc.get('metadata', {})
                facts.extend([
                    f"store: {metadata.get('store')}",
                    f"emotion: {metadata.get('emotion')}",
                    f"weather: {metadata.get('weather')}",
                    f"need: {metadata.get('interpreted_need')}"
                ])
            
            # Check if answer contradicts facts
            check_prompt = f"""Analyze if this answer contradicts the source information.

Answer: {answer}

Source facts:
{', '.join(facts[:5])}

Is the answer consistent with the sources? Answer yes or no."""
            
            response = llm_client.query(
                prompt=check_prompt,
                temperature=0.1,
                max_tokens=20
            )
            
            return "no" in response.lower()
        except Exception as e:
            logger.warning(f"Hallucination check failed: {str(e)}")
            return False
    
    def process_query(self, query: str, user_location: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Process query through RAG pipeline.
        
        Args:
            query: User query
            user_location: User GPS coordinates
            
        Returns:
            RAG response
        """
        try:
            logger.info(f"Processing RAG query: {query[:50]}...")
            
            # Step 1: Rewrite query
            rewritten = self._rewrite_query(query)
            logger.info(f"Rewritten query: {rewritten[:50]}...")
            
            # Step 2: Retrieve documents
            documents = self._retrieve_documents(rewritten, top_k=5)
            logger.info(f"Retrieved {len(documents)} documents")
            
            if not documents:
                return {
                    "answer": "I couldn't find relevant information to answer that query.",
                    "confidence": 0.3,
                    "source_count": 0,
                    "requires_escalation": True
                }
            
            # Step 3: Rerank documents
            documents = self._rerank_documents(documents, query)
            logger.info(f"Reranked to {len(documents)} documents")
            
            # Step 4: Compress context
            context = self._compress_context(documents)
            
            # Step 5: Generate answer
            answer = self._generate_answer(query, context)
            
            # Step 6: Check hallucination
            is_hallucinating = self._check_hallucination(answer, documents)
            
            if is_hallucinating:
                answer = "I'm not confident about that answer. Let me connect you with a specialist who can help better."
                requires_escalation = True
                confidence = 0.4
            else:
                requires_escalation = False
                confidence = min(0.95, 0.6 + len(documents) * 0.1)
            
            return {
                "answer": answer,
                "confidence": confidence,
                "source_count": len(documents),
                "rewritten_query": rewritten,
                "requires_escalation": requires_escalation,
                "sources": [doc.get('doc_id') for doc in documents[:3]]
            }
        except Exception as e:
            logger.error(f"RAG query processing failed: {str(e)}")
            return {
                "answer": "An error occurred processing your query.",
                "confidence": 0.0,
                "source_count": 0,
                "requires_escalation": True
            }
