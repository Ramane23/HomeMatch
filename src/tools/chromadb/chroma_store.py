import json, os
from typing import List
import json
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import json
import os
from langchain.schema import Document
from typing import List
from loguru import logger

# from src.llms import groqllm
from src.prompt_templates.rag_prompt import rag_prompt
from src.config import settings
from src.llm_parsers.listing_parser import Listing
import os, json


class ChromaStore:
    """
    This class is responsible of building and running the Rag chain
    """

    # class attributes
    # llm_groq = groqllm().get_llm_model()
    llm_groq = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name="gemma2-9b-it",  # or another Groq model
        temperature=0.8,
        max_tokens=512,  # plenty for one JSON listing
    )

    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5",
        model_kwargs={"device": "cpu"},  # or "cuda" if GPU is available
    )

    rag_prompt = rag_prompt

    def __init__(self):

        pass

    @classmethod
    def load_listings(cls, path: str = "./src/listings/docs") -> List[Document]:
        """
        This method is responsible of loading the generted listings in langchain documents format
        """

        raw_listings = []

        for filename in os.listdir(path):
            with open(os.path.join(path, filename), "r") as f:
                data = json.load(f)

            for item in data:
                listing_object = Listing(**item)
                raw_listings.append(listing_object)
            # breakpoint()s
        # convert to langchain documents
        documents = cls.listings_to_documents(raw_listings)

        return documents

    @staticmethod
    def listings_to_documents(raw_listings: List[Listing]) -> List[Document]:
        """
        this method will convert generated listings from json to langchain Document
        """
        docs: list[Document] = []

        for item in raw_listings:
            # Combine the prose fields into the text that will be embedded
            text_block = "\n\n".join(
                [
                    item.description.strip(),
                    item.neighborhood_description.strip(),
                ]
            ).strip()

            # Everything else becomes structured metadata for filtering/ranking later
            item_dict = item.model_dump()  # For Pydantic v2
            # item_dict = item.dict()      # For Pydantic v1

            metadata = {
                k: v
                for k, v in item_dict.items()
                if k not in ("description", "neighborhood_description")
            }

            docs.append(Document(page_content=text_block, metadata=metadata))

        logger.info(f"✅ Converted {len(docs)} listings to LangChain Documents")

        return docs

    def build_retriever(self):
        """
        This method will create a chromadb vector
        """

        # build the vectorestore
        PERSIST_DIR = "./src/tools/chromadb"
        os.makedirs(PERSIST_DIR, exist_ok=True)

        vector_store = Chroma.from_documents(
            documents=self.load_listings("./src/listings/docs"),
            embedding=self.embedding_model,
            collection_name="listings",
            persist_directory=PERSIST_DIR,
        )

        vector_store.persist()  # writes the DB files to disk
        logger.info(f"💾 Stored & persisted to {PERSIST_DIR}")

        # cast the vectorestore as a retriever
        retriever = vector_store.as_retriever(
            search_kwargs={
                "k": 5  # number of listings to return on each query (tweak as you like)
                # you can also add a metadata filter later, e.g.:
                # "filter": {"bedrooms": 3}
            }
        )

        logger.info(f"✅ listings retriever has been successfully created")

        return retriever


if __name__ == "__main__":

    # instantiate a ChromaStore object
    chroma_store = ChromaStore()

    # get the retriever
    retriever = chroma_store.build_retriever()
