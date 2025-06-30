from langchain.prompts import PromptTemplate

listing_prompt = PromptTemplate(
    template=(
        "You are an expert real-estate copywriter.\n\n"
        "Generate a **fictional but realistic** property listing that follows this brief:\n"
        "• Each call must describe a different neighborhood.\n"
        "• Keep data plausible and coherent.\n\n"
    ),
)
