from langchain_community.retrievers import BM25Retriever
import numpy as np


class HybridRet:

    def __init__(self, docs, em_model):

        self.bm_model = BM25Retriever.from_documents(docs)
        self.em_model = em_model
        self.docs   = docs

    
    def keyword_search(self, key, k = 5):

        scores = self.bm_model.invoke(key)
        top_k  = scores[:k]
        return top_k

    def semantic_search(self, key, docs, k = 3):

        key_embed = self.em_model.embed_query(key)
        docs_content = [d.page_content for d in docs]
        docs_embed   = self.em_model.embed_documents(docs_content)

        scores = np.dot(docs_embed, key_embed)

        top_k  = sorted(range(len(scores)), key=lambda i:scores[i], reverse=True)[:k]
        return [docs[i] for i in top_k]

    def similarity_search(self, key, key_a = 2, key_b = 4):

        best_k = self.keyword_search(key, key_b)
        final_k = self.semantic_search(key, best_k, key_a)

        return final_k

    