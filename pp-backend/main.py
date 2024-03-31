from vector_db import generate_data_store
from retrievers import similarity_search, reciprocal_rank_fusion, structured_retrieval

# generate_data_store("pp-backend/chroma/basic", "pp-backend/data/basic")
# generate_data_store("pp-backend/chroma/geneds", "pp-backend/data/geneds")
# generate_data_store("pp-backend/chroma/track", "pp-backend/data/track")

generate_data_store()

start = "y"
while start == "y":
    question = input("Ask your pdf some question: ")
    #print(structured_retrieval(question))
    print(reciprocal_rank_fusion(question))
    start = input("Would you like to keep chatting: ")
    