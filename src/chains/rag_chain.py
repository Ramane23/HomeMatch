from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from loguru import logger

# from src.llms import groqllm
from src.prompt_templates.rag_prompt import rag_prompt
from src.config import settings
from src.tools.chromadb.chroma_store import ChromaStore
from src.chains.query_cleaning import QueryCleaner


class Rag:
    """
    This class is responsible of building and running the Rag chain
    """

    # class attributes
    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5",
        model_kwargs={"device": "cpu"},  # or "cuda" if GPU is available
    )

    rag_prompt = rag_prompt

    def __init__(self, model):

        self.llm = model
        self.chroma_store = ChromaStore()

    def get_rag_chain(self):
        """
        This method is responsible of building and returning the rag_chain
        """

        # 1️⃣  combine the retrieved docs + prompt + model
        combine_docs_chain = create_stuff_documents_chain(
            llm=self.llm, prompt=rag_prompt
        )

        # 2️⃣  wire the retriever and the doc-combining chain together
        rag_chain = create_retrieval_chain(
            retriever=self.chroma_store.build_retriever(),
            combine_docs_chain=combine_docs_chain,
        )

        return rag_chain

    def invoke_rag_chain(self, raw_query):
        """
        This method will be used to invoke the rag_chain
        """
        # instantiate a QueryCleaner object
        query_cleaner = QueryCleaner()
        query_cleaner_chain = query_cleaner.query_cleaning_chain()

        chain = query_cleaner_chain | self.get_rag_chain()

        try:
            logger.info(
                f" cleaning user raw query, retrieving similar listings and generating suggestions : {raw_query}"
            )
            rag_answer = chain.invoke({"raw_query": raw_query})
            logger.info(
                f"✅ listing documents sucessfully retrieved and an answer has been generated: {rag_answer}"
            )

        except Exception as e:
            # Check if it's a 403 access denied error
            if "403" in str(e) and "Access denied" in str(e):
                logger.error(
                    "🚫 API Access Denied - Please check your API key and network settings"
                )
                logger.error("This might be due to:")
                logger.error("  - Invalid or expired API key")
                logger.error("  - Network/firewall restrictions")
                logger.error("  - API quota exceeded")
                logger.error("  - VPN/proxy blocking the connection")
            else:
                logger.error(f"❌ Unexpected error: {str(e)}")

                # Exit gracefully or return empty data
                exit(1)

        return rag_answer


if __name__ == "__main__":

    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name="gemma2-9b-it",  # or another Groq model
        temperature=0.8,
        max_tokens=512,  # plenty for one JSON listing
    )
    # instantiate a ChromaStore object
    rag = Rag(llm)

    # get the retriever
    rag.invoke_rag_chain(
        raw_query="I'd like a modern 3-bedroom around 2000 sqft, solar panels, "
        "backyard, quiet neighborhood, near public transit. Budget about $600k."
    )
