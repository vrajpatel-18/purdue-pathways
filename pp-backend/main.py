from vector_db import generate_data_store
from retrievers import simple

def invoke(question):
    generate_data_store()
    return simple(question)

# start = "y"
# while start == "y":
#     question = input("Ask your pdf some question: ")
#     #print(structured_retrieval(question))
#     print(reciprocal_rank_fusion(question))
#     start = input("Would you like to keep chatting: ")