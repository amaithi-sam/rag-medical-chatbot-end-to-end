# # from langchain_classic.chains.retrieval import create_retrieval_chain
# # from langchain_classic.chains.combine_documents import create_stuff_documents_chain


# # from langchain_core.prompts import PromptTemplate 

# # from app.components.llm import load_llm 
# # from app.components.vector_store import load_vector_store 

# # from app.common.logger import get_logger 

# # from app.common.custom_exception import CustomException 
# # import os

# # logger = get_logger(__name__)

# # CUSTOM_PROMPT_TEMPLATE = """Answer the following medical question in 2-3 lines using only the information provided in the context

# # context: 
# # {context}

# # Question:
# # {question}

# # Answer:
# # """

# # def set_custom_prompt():
# #     return PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE, input_variables=["context", "question"])


# # def create_qa_chain():
# #     try:
# #         logger.info("Loading vector store for context")

# #         db = load_vector_store()

# #         if db is None:
# #             raise CustomException("Vector Store Not Present or empty")

# #         llm = load_llm()

# #         if llm is None:
# #             raise CustomException("LLM is not loaded")
        

# #         # 3. Create the Combine Documents Chain
# #         combine_docs_chain = create_stuff_documents_chain(llm, set_custom_prompt())

# #         # 4. Create the Retrieval Chain
# #         qa_chain = create_retrieval_chain(db.as_retriever(search_kwargs={'k': 1}), combine_docs_chain)

# #         # Invoke the chain
# #         # response = retrieval_chain.invoke({"input": "What is RAG?"})
        
# #         # qa_chain = RetrievalQA.from_chain_type(
# #         #     llm=llm,
# #         #     chain_type="stuff",
# #         #     retriever=db.as_retriever(search_kwargs={'k': 1}),
# #         #     return_source_documents=False,
# #         #     chain_type_kwargs={'prompt': set_custom_prompt()}
# #         # )

# #         logger.info("Successfully created the QA chain")
# #         return qa_chain

# #     except Exception as e:
# #         error_message = CustomException("Failed to make a QA chain", e)
# #         logger.error(str(error_message))
# #         # 🚨 Explicitly return None on failure
# #         return None




# from langchain_classic.chains.retrieval import create_retrieval_chain
# from langchain_classic.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import PromptTemplate 

# from app.components.llm import load_llm 
# from app.components.vector_store import load_vector_store 
# from app.common.logger import get_logger 
# from app.common.custom_exception import CustomException 
# import os

# logger = get_logger(__name__)

# CUSTOM_PROMPT_TEMPLATE = """Answer the following medical question in 2-3 lines using only the information provided in the context.

# Context: 
# {context}

# Question: {input}

# Answer:"""

# def set_custom_prompt():
#     return PromptTemplate(
#         template=CUSTOM_PROMPT_TEMPLATE, 
#         input_variables=["context", "input"],
#         #   partial_variables=[{'question': input}]
#     )

# def create_qa_chain():
#     try:
#         logger.info("Loading vector store for context")
#         db = load_vector_store()
#         if db is None:
#             raise CustomException("Vector Store Not Present or empty")
        
#         llm = load_llm()
#         if llm is None:
#             raise CustomException("LLM is not loaded")
       
#         # Create the document combination chain
#         combine_docs_chain = create_stuff_documents_chain(llm, set_custom_prompt())
        
#         # Create retriever with k=3 for better medical context (k=1 was too restrictive)
#         retriever = db.as_retriever(search_kwargs={'k': 3})
        
#         # Create the full retrieval chain
#         qa_chain = create_retrieval_chain(retriever, combine_docs_chain)
        
#         logger.info("Successfully created the QA chain")
#         return qa_chain

#     except Exception as e:
#         error_message = CustomException("Failed to make a QA chain", e)
#         logger.error(str(error_message))
#         return None

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from app.components.llm import load_llm 
from app.components.vector_store import load_vector_store 
from app.common.logger import get_logger 
from app.common.custom_exception import CustomException 

logger = get_logger(__name__)

CUSTOM_PROMPT_TEMPLATE = """Answer the following medical question in 2-3 lines using only the information provided in the context.

Context: 
{context}

Question: {question}

Answer:"""

def set_custom_prompt():
    return PromptTemplate(
        template=CUSTOM_PROMPT_TEMPLATE, 
        input_variables=["context", "question"]
    )

def create_qa_chain(user_input):
    try:
        logger.info("Loading vector store for context")
        db = load_vector_store()
        
        if db is None:
            raise CustomException("Vector Store Not Present or empty")
        
        llm = load_llm()
        if llm is None:
            raise CustomException("LLM is not loaded")
       
        retriever = db.as_retriever(search_kwargs={'k': 3})
        prompt = set_custom_prompt()
        
        # Modern LCEL approach
        qa_chain = (
            {"context": retriever, 
             "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
            
        )
        
        logger.info("Successfully created the QA chain")

        response = qa_chain.invoke(user_input)
        # print(response)
        logger.info(response)
        return response

    except Exception as e:
        error_message = CustomException("Failed to make a QA chain", e)
        logger.error(str(error_message))
        return None
