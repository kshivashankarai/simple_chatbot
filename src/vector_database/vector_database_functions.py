import chromadb

class VectorDatabaseFunctions:
    def __init__(self):
        self.chroma_client = chromadb.Client()

    def update_vectors(self, collection_name, documents, ids):
        collection = self.chroma_client.create_collection(name=collection_name)
        existing_ids = collection.get(ids=ids)["ids"]
        new_ids = [id for id in ids if id not in existing_ids]
        existing_data_ids = [id for id in ids if id in existing_ids]
        if existing_data_ids:
            existing_docs = [documents[ids.index(id)] for id in existing_data_ids if id in ids]
            collection.update(documents=existing_docs, ids=existing_data_ids)
        if new_ids:
            new_docs = [documents[ids.index(id)] for id in new_ids if id in ids]
            collection.add(documents=new_docs, ids=new_ids)
        return existing_data_ids, new_ids
    
    def fetch_similar_tables(self, collection_name, query, count, max_distance):
        collection = self.chroma_client.get_collection(name=collection_name)
        results = collection.query(
            query_texts=[query],
            n_results=count
        )
        combined = list(zip(results['distances'][0], results['documents'][0]))
        sorted_combined = sorted(combined, key=lambda x: x[0])

        filtered_documents = []
        for distance, document in sorted_combined:
            if distance < max_distance:
                filtered_documents.append(document)
        filtered_documents_string = ' | '.join(filtered_documents)
        return filtered_documents_string