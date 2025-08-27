import torch
from transformers import AutoModel, AutoTokenizer
from dotenv import load_dotenv

load_dotenv()


class EmbeddingModel:
    def __init__(self):
        self.model_name = "BAAI/bge-large-en-v1.5"
        self.model = AutoModel.from_pretrained(self.model_name, trust_remote_code=True)
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, trust_remote_code=True
        )

    def embed_text(self, text):
        """Generates an embedding for the given text"""
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, max_length=512
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
            embedding = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
        return embedding


# Singleton instance
embedding_model = EmbeddingModel()
