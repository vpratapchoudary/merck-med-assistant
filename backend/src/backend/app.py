from backend.config import PINECONE_CFG
from backend.vectors.embedding import embed_query, load_embedding_model
from backend.vectors.retriever import query_pinecone_index


class MedicalAssistant:
	"""Application service with the embedding model loaded during startup."""

	def __init__(self, index_host: str):
		self.index_host = index_host
		self.embedding_model = load_embedding_model()

	def query(self, user_query: str, top_k: int = 3) -> dict:
		"""Embed a user query and retrieve matching manual chunks."""
		query_vector = embed_query(user_query, self.embedding_model)
		return query_pinecone_index(
			index_host=self.index_host,
			query_vector=query_vector,
			top_k=top_k,
			namespace=PINECONE_CFG["namespace"],
		)

if __name__ == "__main__":
	# Example usage
	assistant = MedicalAssistant(index_host=PINECONE_CFG["index_host"])
	user_query = "What are the symptoms of diabetes?"
	results = assistant.query(user_query)
	print(results)
