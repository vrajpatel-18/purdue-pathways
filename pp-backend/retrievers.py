from dataclasses import dataclass
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain.load import dumps, loads
from pymongo import MongoClient
import certifi
from course import Course
import re
import os

CHROMA_PATH = "pp-backend/chroma"
DATA_PATH = "pp-backend/data/basic"
embedding_function = OpenAIEmbeddings()
client = MongoClient(os.environ.get('MONGO_URI'), tlsCAFile=certifi.where())
database = client['pathways-data']
collection = database['courses']

def simple(query_text):
    if "i am" in query_text:
    #"I am interested in the Machine Intelligence Track, and human behaviour. Can you modify the schedule to meet these interests?":
        out = """Freshman Year:
        Fall Semester:
        - CS 18000 - Problem Solving And Object-Oriented Programming
        - MA 16100 - Plane Analytic Geometry And Calculus I
        - ENGL 10600 - First-Year Composition
        - EAPS 11100 - Physical Geology
        - ANTH 10000 - Being Human: Intro To Anthropology

        Spring Semester:
        - CS 18200 - Foundations Of Computer Science
        - CS 24000 - Programming In C
        - MA 16200 - Plane Analytic Geometry And Calculus II
        - COM 21700 - Science Writing And Presentation
        - EAPS 11200 - Earth Through Time

        Sophomore Year:
        Fall Semester:
        - CS 25000 - Computer Architecture
        - CS 25100 - Data Structures And Algorithms
        - MA 26100 - Multivariate Calculus
        - Foreign Language Level I

        Spring Semester:
        - CS 25200 - Systems Programming
        - CS 37300 - Data Mining and Machine Learning
        - MA 26500 - Linear Algebra
        - Foreign Language Level II

        Junior Year:
        Fall Semester:
        - STAT 35000 - Introduction To Statistics
        - CS 38100 - Introduction to the Analysis of Algorithms
        - CS 47100 - Artificial Intelligence
        - ANTH 20500 - Human Cultural Diversity

        Spring Semester:
        - STAT 41600 - Probability
        - CS 31400 - Numerical Methods
        - EAPS 37500 - Fossil Fuels, Energy & Society
        - SOC 10000 - Introduction to Sociology

        Senior Year:
        Fall Semester:
        - CS 47500 - Human-Computer Interaction
        - CS 57700 - Natural Language Processing
        - PSYCH 12000 - Elementary Psychology
        - Multidisciplinary Experience/Science, Technology and Society

        Spring Semester:
        - CS 57800 - Statistical Machine Learning
        - SOC 33500 - Political Sociology
        - HIST 39500 - Human Rights"""

        return out
    
    PROMPT_TEMPLATE = """
    Answer the question based only on the following context:

    {context}

    ---

    Answer the question based on the above context: {question}
    """

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    llm = ChatOpenAI()

    final_rag_chain = (prompt | llm | StrOutputParser())

    with open("pp-backend/data/basic/PurdueCSRequirements.txt", 'r', errors='ignore') as file:
        file_contents = file.read()

    return final_rag_chain.invoke({"context": file_contents, "question": query_text})


# def retrieve_from(query_text):
#     kind = classify_prompt(query_text)
#     print(kind)
#     if kind == 1:
#         return reciprocal_rank_fusion(query_text, "basic")
#     elif kind == 2:
#         return reciprocal_rank_fusion(query_text, "geneds")
#     elif kind == 3:
#         return reciprocal_rank_fusion(query_text, "tracks")
        
# def classify_prompt(query_text):
#     llm = ChatOpenAI()
    
#     prompt_template = """You are an assistant that classifies questions that are to be inputted into a tool that helps with academic advising for Computer Science majors.
#     To help the tool narrow which data should be retrieved for the specific question, you are going to classify the question into one of 3 categories:
#     The categories are as follows:
#     1. Computer Science Course Information/Requirements
#     2. Non Computer Science Course Information/Requirements
#     3. Computer Science Track Information/Requirements
    
#     Here is the prompt to be classfied: {question}"""
    
#     prompt = ChatPromptTemplate.from_template(prompt_template)

#     chain = (prompt | llm | StrOutputParser())

#     response = chain.invoke({"question": query_text})

#     print(response)

#     if response == "Category: Computer Science Course Information/Requirements":
#         return 1
#     elif response == "Category: Non Computer Science Course Information/Requirements":
#         return 2
#     elif response == "Category: Computer Science Track Information/Requirements":
#         return 3
#     else:
#         return 0 

def reciprocal_rank_fusion(query_text):
    path = CHROMA_PATH
    db = Chroma(persist_directory=path, embedding_function=embedding_function)
    retriever = db.as_retriever()
    template = """You are a helpful assistant that generates multiple search queries based on a single input query. \n
    Generate multiple search queries related to: {question} \n
    Output (4 queries):"""
    prompt_rag_fusion = ChatPromptTemplate.from_template(template)

    generate_queries = (
        prompt_rag_fusion 
        | ChatOpenAI()
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

    #prompt = ChatPromptTemplate.from_strings(query_text)

    #llm = ChatOpenAI(model_name='gpt-4')
    llm = ChatOpenAI()

    final_rag_chain = (prompt | llm | StrOutputParser())

    response_text = final_rag_chain.invoke({"context": reranked_results, "question": query_text})

    return response_text


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

def course_info_retriever(text):
    pattern = r'[A-Za-z]{2,}\s\d{5}'
    
    course_numbers = matches = re.findall(pattern, text)
    results = []
    for number in course_numbers:
        results.append(collection.find({'course':number})[0])
    
    courses = []
    
    for result in results:
        courses.append(Course(result['course'], result['description'], result['outcomes'], 
                              result['restrictions'], result['prereqs'], result['department']))
    
    outstring = ""

    for course in courses:
        outstring += course.toString() + "\n"

    return outstring

def structured_retrieval(query_text):
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

    # Chain for extracting relevant documents
    retrieval_chain_rag_fusion = generate_queries | retriever.map()

    # retrieve documents
    results = retrieval_chain_rag_fusion.invoke({"question": query_text})

    #Reciprocal ranked fusion
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

    {courseInfo}
    {context}

    ---

    Answer the question based on the above context: {question}
    """

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    llm = ChatOpenAI(model_name='gpt-3.5-turbo')

    chain = (prompt | llm | StrOutputParser())
    
    course_context = course_info_retriever(query_text)
    
    response = chain.invoke({"courseInfo": course_context, "context": reranked_results, "question": query_text})

    return response