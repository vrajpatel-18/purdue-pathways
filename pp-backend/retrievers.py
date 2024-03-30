from dataclasses import dataclass
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain.load import dumps, loads

CHROMA_PATH = "chroma"
DATA_PATH = "data"
embedding_function = OpenAIEmbeddings()

def reciprocal_rank_fusion(query_text):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    retriever = db.as_retriever()
    template = """You are a helpful assistant that generates multiple search queries based on a single input query. \n
    Generate multiple search queries related to: {question} \n
    Output (4 queries):"""
    prompt_rag_fusion = ChatPromptTemplate.from_template(template)

    generate_queries = (
        prompt_rag_fusion 
        | ChatOpenAI(temperature=0)
        | StrOutputParser() 
        | (lambda x: x.split("\n"))
    )

    ## Chain for extracting relevant documents
    retrieval_chain_rag_fusion = generate_queries | retriever.map()

    # retrieve documents
    results = retrieval_chain_rag_fusion.invoke({"question": query_text})

    #Reciprical ranked fusion
    fused_scores = {}
    k=60
    for docs in results:
        for rank, doc in enumerate(docs):
            doc_str = dumps(doc)
            # If the document is not yet in the fused_scores dictionary, add it with an initial score of 0
            # print('\n')
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            # Retrieve the current score of the document, if any
            previous_score = fused_scores[doc_str]
            # Update the score of the document using the RRF formula: 1 / (rank + k)
            fused_scores[doc_str] += 1 / (rank + k)

    # final reranked result
    reranked_results = [(loads(doc), score) for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)]

    PROMPT_TEMPLATE = """
    Answer the question based only on the following context:

    {context}

    ---

    Answer the question based on the above context: {question}
    """

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    llm = ChatOpenAI(temperature=0)

    final_rag_chain = (prompt | llm | StrOutputParser())

    return final_rag_chain.invoke({"context": reranked_results, "question": query_text})


def similarity_search(query_text):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    PROMPT_TEMPLATE = """
    Answer the question based only on the following context:

    {context}

    ---

    Answer the question based on the above context: {question}
    """
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    #print(prompt)

    model = ChatOpenAI()
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    #print(formatted_response)
    
    return formatted_response
