"""Data converter - CSV to JSON format."""
import csv
import json
from pathlib import Path
from typing import List, Dict, Any


class DataConverter:
    """Convert CSV dataset to JSON format for RAG and Tooling modes."""
    
    @staticmethod
    def csv_to_json(csv_path: str, output_path: str) -> None:
        """
        Convert CSV to JSON format.
        
        Args:
            csv_path: Path to CSV file
            output_path: Path to output JSON file
        """
        customers = []
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                customer = {
                    "user_id": int(row['user_id']),
                    "gps_coordinates": row['gps_coordinates'],
                    "nearest_store": row['nearest_store'],
                    "distance_m": int(row['distance_m']),
                    "weather": row['weather'],
                    "temperature": int(row['temperature']),
                    "user_emotion": row['user_emotion'],
                    "emotion_intensity": float(row['emotion_intensity']),
                    "query_text": row['query_text'],
                    "interpreted_need": row['interpreted_need'],
                    "expanded_query_by_rewriter": row['expanded_query_by_rewriter'],
                    "personalized_offer_generated": row['personalized_offer_generated'],
                    "coupon_click": int(row['coupon_click']),
                    "in_store_visit": int(row['in_store_visit']),
                    "time_of_day": row['time_of_day'],
                    "competitor_distance_m": int(row['competitor_distance_m']),
                    "loyalty_tier": row['loyalty_tier'],
                    "predicted_visit_probability": float(row['predicted_visit_probability']),
                    "agent_routed_mode": row['agent_routed_mode'],
                    "query_complexity_score": float(row['query_complexity_score']),
                    "phone_number_raw": row['phone_number_raw']
                }
                customers.append(customer)
        
        # Write to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(customers, f, indent=2)
        
        print(f"✅ Converted {len(customers)} records to {output_path}")
    
    @staticmethod
    def create_rag_documents(customers: List[Dict[str, Any]]) -> None:
        """
        Create RAG documents from customer data.
        
        Args:
            customers: List of customer records
        """
        rag_docs = []
        
        for customer in customers:
            doc = {
                "doc_id": f"customer_{customer['user_id']}",
                "content": customer['expanded_query_by_rewriter'],
                "metadata": {
                    "user_id": customer['user_id'],
                    "emotion": customer['user_emotion'],
                    "emotion_intensity": customer['emotion_intensity'],
                    "weather": customer['weather'],
                    "temperature": customer['temperature'],
                    "store": customer['nearest_store'],
                    "distance": customer['distance_m'],
                    "loyalty": customer['loyalty_tier'],
                    "time": customer['time_of_day'],
                    "interpreted_need": customer['interpreted_need'],
                    "offer": customer['personalized_offer_generated'],
                    "complexity_score": customer['query_complexity_score']
                },
                "original_query": customer['query_text'],
                "inferred_intent": customer['interpreted_need'],
                "ground_truth_visit": customer['in_store_visit']
            }
            rag_docs.append(doc)
        
        # Save RAG documents
        output_path = Path('backend/data/rag_docs/customers.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(rag_docs, f, indent=2)
        
        print(f"✅ Created {len(rag_docs)} RAG documents")


if __name__ == "__main__":
    # Convert CSV to JSON
    csv_file = "Backend/groundtruth_300_rows_with_phone.csv"
    json_file = "backend/data/customers.json"
    
    converter = DataConverter()
    converter.csv_to_json(csv_file, json_file)
    
    # Load and create RAG documents
    with open(json_file, 'r') as f:
        customers = json.load(f)
    
    converter.create_rag_documents(customers)
    print("✅ Data conversion complete!")
