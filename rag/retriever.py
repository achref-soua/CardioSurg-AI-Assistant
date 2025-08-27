import os
import chromadb
from typing import List, Dict, Any
from .embedding import embedding_model
from dotenv import load_dotenv

load_dotenv()


class ChromaRetriever:
    def __init__(self):
        db_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "database", "chroma_db")
        )
        self.client = chromadb.PersistentClient(path=db_path)

    def query_collection(
        self, collection_name: str, query: str, n_results: int = 5, filters: Dict = None
    ) -> List[Dict[str, Any]]:
        """Query a specific collection with optional filters"""
        try:
            collection = self.client.get_collection(name=collection_name)
            query_embedding = embedding_model.embed_text(query)

            # Prepare where clause if filters are provided
            where_clause = None
            if filters:
                where_clause = {"$and": []}
                for key, value in filters.items():
                    where_clause["$and"].append({key: {"$eq": value}})

            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_clause,
            )

            # Format results
            formatted_results = []
            if results["documents"]:
                for i in range(len(results["documents"][0])):
                    formatted_results.append(
                        {
                            "document": results["documents"][0][i],
                            "metadata": results["metadatas"][0][i],
                            "distance": results["distances"][0][i],
                        }
                    )

            return formatted_results
        except Exception as e:
            print(f"Error querying collection {collection_name}: {e}")
            return []

    def get_patient_info(self, patient_id: str) -> Dict[str, Any]:
        """Get specific patient information by ID"""
        try:
            collection = self.client.get_collection(name="patients")

            # Query specifically for this patient
            results = collection.get(where={"patient_id": {"$eq": patient_id}})

            if results["ids"]:
                # Return the first match (should be only one)
                return {
                    "document": results["documents"][0],
                    "metadata": results["metadatas"][0],
                }
            else:
                return None
        except Exception as e:
            print(f"Error retrieving patient {patient_id}: {e}")
            return None

    def get_collection_names(self) -> List[str]:
        """Get list of all available collections"""
        return [col.name for col in self.client.list_collections()]


# Singleton instance
chroma_retriever = ChromaRetriever()
