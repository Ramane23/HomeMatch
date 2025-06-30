from loguru import logger
from IPython.display import display, Markdown
from langchain_groq import ChatGroq

from src.chains.query_cleaning import QueryCleaner
from src.chains.rag_chain import Rag
from src.config import settings


class HomeMatch():
    
    """
    This is a class is responsible of builing and running the full home match chain
    """
    
    def __init__(self, model):
        
        self.query_cleaner = QueryCleaner(model)
        self.rag = Rag(model)
    
    def get_full_chain(self):
        """
        This method will build the full chain
        """
        query_cleaning_chain = self.query_cleaner.query_cleaning_chain()
        rag_chain = self.rag.get_rag_chain()

        #defining the full chain
        full_chain = query_cleaning_chain | rag_chain
        
        return full_chain

    def invoke_full_chain(
        self,
        raw_query : str
    ):
        """
        This method will run the full chain
        """
        
        try:
            logger.info(f" cleaning user raw query, retrieving similar listings and generating suggestions : {raw_query}")
            home_match = self.get_full_chain().invoke({"raw_query":raw_query})
            logger.info(f"✅ listing documents sucessfully retrieved and an answer has been generated: {home_match}")
        
        except Exception as e:
            # Check if it's a 403 access denied error
            if "403" in str(e) and "Access denied" in str(e):
                logger.error("🚫 API Access Denied - Please check your API key and network settings")
                logger.error("This might be due to:")
                logger.error("  - Invalid or expired API key")
                logger.error("  - Network/firewall restrictions")
                logger.error("  - API quota exceeded")
                logger.error("  - VPN/proxy blocking the connection")
            else:
                logger.error(f"❌ Unexpected error: {str(e)}")
                    
                # Exit gracefully or return empty data
                exit(1)  
            
        return home_match


if __name__=="__main__":
    
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name="gemma2-9b-it",  # or another Groq model
        temperature=0.8,
        max_tokens=512   # plenty for one JSON listing
    )
    
    #instantiate a HomeMatch object
    home_match = HomeMatch(llm)
    
    #get the home suggestions
    home_match.invoke_full_chain(raw_query = "I'd like a modern 3-bedroom around 2000 sqft, solar panels, "
                  "backyard, quiet neighborhood, near public transit. Budget about $600k.")
    