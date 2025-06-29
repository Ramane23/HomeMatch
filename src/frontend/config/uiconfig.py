import configparser

class Config:
    def __init__(self, path="src/frontend/config/uiconfig.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(path)

    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE", "LangGraph")

    def get_llm_options(self):
        return self.config["DEFAULT"].get("LLM_OPTIONS", "").split(",")

    def get_groq_model_options(self):
        return self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS", "").split(",")

    def get_amenities(self):
        return self.config["DEFAULT"].get("AMENITIES", "").split(", ")

    def get_transportation_options(self):
        return self.config["DEFAULT"].get("TRANSPORTATION", "").split(", ")

    def get_neighborhood_traits(self):
        return self.config["DEFAULT"].get("NEIGHBORHOOD_TRAITS", "").split(", ")

ui_config = Config()