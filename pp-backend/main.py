from vector_db import generate_data_store
from retrievers import similarity_search, reciprocal_rank_fusion, colbert_retriever, structured_retrieval

generate_data_store()
start = "y"
while start == "y":
    question = input("Ask your pdf some question: ")
    #print(similarity_search(question))
    #print(reciprocal_rank_fusion(question))
    #print(colbert_retriever(question))
    print(structured_retrieval(question))
    start = input("Would you like to keep chatting: ")
    