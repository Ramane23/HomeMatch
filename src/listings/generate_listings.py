from pathlib import Path
import json, time
from typing import List
import json, time
from langchain_groq import ChatGroq
from langchain.docstore.document import Document
from loguru import logger
from tqdm import tqdm

from src.config import settings
from src.llm_parsers.listing_parser import Listing
from src.prompt_templates.listing_prompt import listing_prompt


class GenerateListings:
    """
    This class will be responsible of generating n home listings
    """

    # class attribute

    llm_groq = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name="gemma2-9b-it",  # or another Groq model
        temperature=0.8,
        max_tokens=512,  # plenty for one JSON listing
    )

    def __init__(self, saving_path):

        self.saving_path: str = saving_path

    @classmethod
    def listing_chain(cls):
        """
        This method will build the langchain chain using LCEL for listings generation
        """
        listing_llm = cls.llm_groq.with_structured_output(Listing)
        listing_chain = listing_prompt | listing_llm

        return listing_chain

    # ---------------------------------------------------------------------
    # Generate N listings with retry / pacing
    # ---------------------------------------------------------------------
    def generate_listings(
        self,
        n: int,
        chain,
        pause: float = 0.3,  # polite delay between calls in seconds
        max_retries: int = 2,  # how many times to retry on an error
    ) -> List[Listing]:
        """Generate *n* real-estate listings via the Groq chain."""

        listings: List[Listing] = []

        for i in tqdm(range(n), desc="Generating listings"):
            attempts = 0
            while attempts <= max_retries:
                try:
                    listing = chain.invoke({})
                    listings.append(listing)
                    break  # success → exit retry loop
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
                    # exit(1)  # or return [] if you want to continue with empty data
                    attempts += 1
                    if attempts > max_retries:
                        print(f"[{i}] failed after {max_retries} retries → {e}")
                    else:
                        print(f"[{i}] error, retrying ({attempts}) → {e}")
                        time.sleep(pause)
            time.sleep(pause)  # pacing to avoid rate limits
        return listings

    def listings_to_documents(self, raw_listings: List[Listing]) -> List[Document]:
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

    # ---------------------------------------------------------------------
    # Optional helper: save to JSON
    # ---------------------------------------------------------------------
    def save_listings(
        self,
        listings: List[Listing] | List[Document],
    ):
        """Serialize listing objects to pretty-printed JSON."""
        Path(self.saving_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.saving_path, "w") as fp:
            if listings and isinstance(listings[0], Document):
                # Handle Document objects
                json.dump(
                    [
                        {"page_content": doc.page_content, "metadata": doc.metadata}
                        for doc in listings
                    ],
                    fp,
                    indent=2,
                )
            else:
                # Handle Listing objects
                json.dump([l.dict() for l in listings], fp, indent=2)
        logger.info(f"✅ Saved {len(listings)} listings → {self.saving_path}")


if __name__ == "__main__":

    # instantiate the listing class
    listing = GenerateListings(
        saving_path="./src/listings/docs/listings.json",
    )

    # generate 50 listings in json format

    # This is where your API call is happening
    data_json = listing.generate_listings(50, listing.listing_chain())

    # save the generated listings to the
    listing.save_listings(data_json)
