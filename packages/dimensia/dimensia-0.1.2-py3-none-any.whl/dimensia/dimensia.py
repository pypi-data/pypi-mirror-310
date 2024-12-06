import os
import pickle
import hashlib
from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from dimensia.utils import ensure_directory_exists
from dimensia.exceptions import (
    CollectionAlreadyExistsError, CollectionNotFoundError, DocumentAlreadyExistsError,
    DatabaseLoadError, DatabaseSaveError, EmbeddingModelNotSetError,
    DocumentNotFoundError
)
import ssl
import requests

class Dimensia:
    """
    Dimensia is a vector-based database for handling documents with embeddings.
    It supports creating collections, adding documents with optional metadata, searching for documents,
    and retrieving document information.
    """
    def __init__(self, db_path=None):
        """
        Initializes the Dimensia class for handling the vector database.
        """
        self.db_path = db_path or "dimensia_data"
        self.collections = {}
        self.embedding_model = None
        self.set_embedding_model()
        self._load_db()

    def set_embedding_model(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """
        Sets the embedding model for generating document embeddings.
        """
        try:
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
            ssl._create_default_https_context = ssl._create_unverified_context

            self.embedding_model = SentenceTransformer(model_name)
        except Exception as e:
            raise EmbeddingModelNotSetError(f"Error setting embedding model: {str(e)}")

    def _load_db(self):
        """
        Loads the database or creates a new one if it doesn't exist.
        """
        ensure_directory_exists(self.db_path)
        db_file = os.path.join(self.db_path, "data.dim")


        if os.path.exists(db_file):
            try:
                with open(db_file, "rb") as f:
                    self.collections = pickle.load(f)
            except Exception as e:
                raise DatabaseLoadError(f"Error loading database: {str(e)}")
        else:
            self._save_db()

    def _save_db(self):
        """
        Saves the current database to file.
        """
        db_file = os.path.join(self.db_path, "data.dim")
        try:
            with open(db_file, "wb") as f:
                pickle.dump(self.collections, f)
        except Exception as e:
            raise DatabaseSaveError(f"Error saving database: {str(e)}")

    def create_collection(self, collection_name):
        """
        Creates a new collection in the database.
        """
        if collection_name in self.collections:
            raise CollectionAlreadyExistsError(f"Collection '{collection_name}' already exists.")
        self.collections[collection_name] = {
            "documents": [],
            "next_id": 1,
            "texts": set(),
            "metadata": {}
        }
        self._save_db()

    def add_documents(self, collection_name, documents, metadata=None):
        """
        Adds multiple documents to a collection, with optional metadata.
        """
        if collection_name not in self.collections:
            raise CollectionNotFoundError(f"Collection '{collection_name}' not found.")

        collection = self.collections[collection_name]
        metadata = metadata or {}

        existing_hashes = set(self._get_text_hash(doc['content']) for doc in collection['documents'])

        with ThreadPoolExecutor() as executor:
            futures = []
            for doc in documents:
                doc_content_hash = self._get_text_hash(doc['content'])

                if doc_content_hash in existing_hashes:
                    print(f"Duplicate document found with content: {doc['content']}.")
                    continue

                if 'id' not in doc:
                    doc['id'] = collection['next_id']
                    collection['next_id'] += 1

                futures.append(executor.submit(self._process_document, doc, collection, metadata))

            # Wait for all documents to be processed
            for future in tqdm(futures, desc="Ingesting documents", unit="document"):
                future.result()

        self._save_db()

    def _process_document(self, doc, collection, metadata):
        """
        Processes a single document, generates its embedding, and adds it to the collection.
        """
        if self.embedding_model is None:
            raise EmbeddingModelNotSetError("Embedding model is not set.")

        if 'id' not in doc:
            doc['id'] = collection['next_id']
            collection['next_id'] += 1

        if any(existing_doc['id'] == doc['id'] for existing_doc in collection['documents']):
            raise DocumentAlreadyExistsError(f"Document with ID '{doc['id']}' already exists.")

        vector = self._generate_embedding(doc['content'])
        doc['vector'] = vector
        doc['metadata'] = metadata.get(doc['id'], {})
        collection['documents'].append(doc)
        collection['texts'].add(self._get_text_hash(doc['content']))

    def _get_text_hash(self, text):
        """
        Generates a hash for the document text to track uniqueness.
        """
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def _generate_embedding(self, text):
        """
        Generates an embedding for the given text.
        """
        if self.embedding_model is None:
            raise EmbeddingModelNotSetError("Embedding model is not set.")
        vector = self.embedding_model.encode(text).tolist()
        return vector

    def get_structure(self, collection_name):
        """
        Returns the structure of a collection, including the number of documents and metadata.
        """
        if collection_name not in self.collections:
            raise CollectionNotFoundError(f"Collection '{collection_name}' not found.")
        collection = self.collections[collection_name]
        return {
            "document_count": len(collection["documents"]),
            "vector_size": len(collection["documents"][0]['vector']) if collection["documents"] else 0,
            "metadata": collection["metadata"]
        }

    def get_vector_size(self, collection_name):
        """
        Returns the size of the vectors used in the collection.
        """
        if collection_name not in self.collections:
            raise CollectionNotFoundError(f"Collection '{collection_name}' not found.")
        collection = self.collections[collection_name]
        if not collection["documents"]:
            return 0
        return len(collection["documents"][0]['vector'])

    def get_collection_info(self, collection_name):
        """
        Provides high-level info about the collection, including document count, vector size, and metadata.
        """
        if collection_name not in self.collections:
            raise CollectionNotFoundError(f"Collection '{collection_name}' not found.")
        collection = self.collections[collection_name]
        return {
            "document_count": len(collection["documents"]),
            "vector_size": self.get_vector_size(collection_name),
            "metadata": collection["metadata"],
        }

    def search(self, query, collection_name, top_k=10, metric="cosine"):
        """
        Searches a collection for the top-k most relevant documents based on the query.
        """
        if collection_name not in self.collections:
            raise CollectionNotFoundError(f"Collection '{collection_name}' not found.")
        collection = self.collections[collection_name]
        query_vector = self._generate_embedding(query)
        distances = []

        for doc in collection["documents"]:
            doc_vector = doc['vector']
            score = self._calculate_similarity(query_vector, doc_vector, metric)
            distances.append((score, doc))

        distances.sort(key=lambda x: x[0], reverse=True if metric == "cosine" else False)
        return [{"score": round(dist[0], 4), "document": dist[1]} for dist in distances[:top_k]]

    def _calculate_similarity(self, query_vector, doc_vector, metric):
        """
        Calculates similarity between the query vector and document vector.
        """
        if metric == "cosine":
            return self._cosine_similarity(query_vector, doc_vector)
        elif metric == "euclidean":
            return self._euclidean_distance(query_vector, doc_vector)
        elif metric == "manhattan":
            return self._manhattan_distance(query_vector, doc_vector)
        else:
            raise ValueError(f"Unsupported metric: {metric}")

    def _euclidean_distance(self, vector1, vector2):
        """
        Calculates Euclidean distance between two vectors.
        """
        return np.linalg.norm(np.array(vector1) - np.array(vector2))

    def _cosine_similarity(self, vector1, vector2):
        """
        Calculates Cosine similarity between two vectors.
        """
        dot_product = np.dot(vector1, vector2)
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        return dot_product / (norm1 * norm2)

    def _manhattan_distance(self, vector1, vector2):
        """
        Calculates Manhattan distance between two vectors.
        """
        return np.sum(np.abs(np.array(vector1) - np.array(vector2)))

    def get_document(self, collection_name, document_id):
        """
        Fetches a document by ID from a specified collection.
        """
        if collection_name not in self.collections:
            raise CollectionNotFoundError(f"Collection '{collection_name}' not found.")
        doc = next((d for d in self.collections[collection_name]['documents'] if d['id'] == document_id), None)
        if not doc:
            raise DocumentNotFoundError(f"Document with ID '{document_id}' not found.")
        return doc

    def get_collections(self):
        """
        Returns the list of collection names.
        """
        return list(self.collections.keys())

    def get_all_docs(self, collection_name):
        """
        Returns all documents in a collection with their vectors and metadata, sorted by their ID.
        """
        if collection_name not in self.collections:
            raise CollectionNotFoundError(f"Collection '{collection_name}' not found.")

        collection = self.collections[collection_name]
        documents = collection['documents']

        if not documents:
            return {"error": f"No documents found in collection '{collection_name}'."}

        docs_data = {
            "collection_name": collection_name,
            "document_count": len(documents),
            "vector_size": self.get_vector_size(collection_name),
            "documents": []
        }

        sorted_documents = sorted(documents, key=lambda doc: doc['id'])

        for doc in sorted_documents:
            doc_info = {
                "id": doc['id'],
                "content": doc['content'],
                "vector": doc['vector'],
                "metadata": doc.get('metadata', 'No metadata available'),
            }
            docs_data["documents"].append(doc_info)

        return docs_data
