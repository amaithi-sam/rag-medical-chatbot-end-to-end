from langchain_huggingface import HuggingFaceEmbeddings 

from app.common.logger import get_logger 
from app.common.custom_exception import CustomException 

logger = get_logger(__name__)

def get_embedding_model():
    try:
        logger.info("Initializing Huggingface Embedding Model")

        model = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")

        logger.info("HF Model loaded successfully")

        return model 
    except Exception as e:
        error_message = CustomException("Error Occured while loading embedding Model", e)
        logger.error(str(error_message))
        raise error_message
