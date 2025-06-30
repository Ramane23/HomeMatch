from langchain_groq import ChatGroq
from langchain.schema.runnable import  RunnableLambda
from loguru import logger

from src.llm_parsers.buyer_preferences import BuyerPreferences
from src.prompt_templates.query_cleaning_prompt import query_cleaner_prompt
from src.config import settings



class QueryCleaner():
    
    """
    This class is responsible of taking in the user raw_query and extract key characteristics of the home
    to generate a a cleaner query for the llm.
    """
    
    
    cleaning_prompt = query_cleaner_prompt
    
    def __init__(self, model):
        
        self.llm = model
    
    def query_cleaning_chain(self):
        
        """
        This method will build and return the query cleaning chain
        """
        
        # Bind the parser to the LLM
        cleaning_llm = self.llm.with_structured_output(BuyerPreferences)
        
        #create a RunnableLambda to extract the query attribute from the BuyerPreference object
        extract_query = RunnableLambda(lambda prefs: {"input" : prefs.query})
        
        #defining the user query cleaning chain
        query_cleaning_chain = self.cleaning_prompt | cleaning_llm | extract_query
        
        return query_cleaning_chain
    
    def invoke_clean_query(
        self, 
        raw_query : str
        ):
        """
        This method will take in the user raw query and clean it before it goes to the llm
        """
        
        #defining the user query cleaning chain
        query_cleaning_chain = self.query_cleaning_chain()
        
        #invocation
        try:
            logger.info(f" cleaning user raw query : {raw_query}")
            cleaned_query = query_cleaning_chain.invoke({"raw_query":raw_query})
        
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
                
        logger.info(f"✅ user raw query has successfully been cleaned : {cleaned_query}")
                    
        return cleaned_query
    
    
if __name__=="__main__":
    
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name="gemma2-9b-it",  # or another Groq model
        temperature=0.8,
        max_tokens=512   # plenty for one JSON listing
    )
        
    #instantiate a QueryCleaner object
    query_cleaner = QueryCleaner(llm)
        
    #clean the user raw query
    query_cleaner.invoke_clean_query(raw_query = "I'd like a modern 3-bedroom around 2000 sqft, solar panels, "
                  "backyard, quiet neighborhood, near public transit. Budget about $600k.")
        