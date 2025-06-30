# 🏡 HomeMatch: Your AI‑Powered Real Estate Assistant

**HomeMatch** is a conversational AI app built with **LangChain**, **Groq LLMs**, **ChromaDB**, and **Streamlit**. It allows users to discover ideal home listings through a combination of structured filters and intelligent, natural-language queries. Designed with an intuitive interface and smart recommendations, HomeMatch streamlines the real estate discovery experience.

---

## 🚀 Features

* ✨ AI-powered home search with natural-language summaries
* 🔍 Sidebar filters: bedrooms, bathrooms, size, budget, lifestyle, etc.
* 🧠 Smart query generation with LangChain RAG pipeline
* ⚙️ Groq + OpenAI LLM integration (model-selectable)
* 📂 ChromaDB vector store retrieval
* 🏨 Beautiful results display using Streamlit expanders
* 🔐 API key secured via `.env`
* 📊 Listing-based context and AI-generated summary
* 🩵 Logging with Loguru

---
## 🖼 Preview

![HomeMatch UI]([./assets/demo-screenshot.png](https://githubimagesbucket.s3.us-east-1.amazonaws.com/HomeMatch.PNG))
---

## 🛠️ Environment Variables

Create a `.env` file in the root of your project:

```env
GROQ_API_KEY=your_groq_key
```

Make sure these match the keys you select from the UI dropdown.

---

## ▶️ How to Run

### Using the main entry point
```bash
# Clone the repository
git clone https://github.com/your-username/HomeMatch.git
cd HomeMatch

# activate the uv workspace
uv .venv/bin/activate

#run the streamlit app
streamlit run src/main.py
```

### Using the app entry point
```bash
streamlit run app.py
```

Then visit [http://localhost:8501](http://localhost:8501) in your browser.

### Using Make (if available)
```bash
make run
```

---

## 📁 Project Structure

```
HomeMatch/
│
├── Makefile                      # Build and run commands
├── README.md                     # Project documentation
├── app.py                        # Alternative app entry point
├── pyproject.toml               # Project configuration and dependencies
├── uv.lock                      # Dependency lock file
│
└── src/                         # Main source code
    ├── main.py                  # Primary application entry point
    ├── config.py                # Application configuration
    │
    ├── chains/                  # LangChain RAG pipeline components
    │   ├── full_chain.py        # Complete processing chain
    │   ├── query_cleaning.py    # Query preprocessing and cleaning
    │   └── rag_chain.py         # Retrieval-Augmented Generation chain
    │
    ├── frontend/                # User interface components
    │   ├── config/              # UI configuration
    │   │   ├── uiconfig.ini     # UI settings file
    │   │   └── uiconfig.py      # UI configuration parser
    │   └── streamlit/           # Streamlit UI components
    │       ├── display_streamlit.py      # Result display logic
    │       └── load_streamlit_ui.py      # UI loading and setup
    │
    ├── listings/                # Property listing management
    │   ├── docs/
    │   │   └── listings.json    # Sample listing data
    │   └── generate_listings.py # Listing data generation utilities
    │
    ├── llm_parsers/            # LLM response parsing
    │   ├── buyer_preferences.py # Parse user preferences
    │   └── listing_parser.py    # Parse listing information
    │
    ├── llms/                   # Language model integrations
    │   └── groqllm.py          # Groq LLM configuration and wrapper
    │
    ├── notebooks/              # Jupyter notebooks for development
    │   ├── db/                 # Database files for notebooks
    │   │   └── listings_chroma/ # ChromaDB data for notebooks
    │   ├── home_match.ipynb    # Main development notebook
    │   ├── listings.ipynb      # Listing analysis notebook
    │   └── listings.json       # Notebook-specific listing data
    │
    ├── prompt_templates/       # LLM prompt templates
    │   ├── listing_prompt.py   # Listing generation prompts
    │   ├── query_cleaning_prompt.py # Query cleaning prompts
    │   └── rag_prompt.py       # RAG-specific prompts
    │
    ├── tests/                  # Test suite
    │   ├── test_full_chain.py  # Full chain integration tests
    │   ├── test_query_cleaning.py # Query cleaning tests
    │   └── test_rag_chain.py   # RAG chain tests
    │
    └── tools/                  # Utility tools and scripts
        └── chromadb/          # ChromaDB management tools
            ├── chroma_store.py # ChromaDB store operations
            ├── chroma.sqlite3  # ChromaDB SQLite database
            └── [vector_data]/  # Vector embeddings storage
```

---

## 📊 Example Inputs

| Feature             | Example                           |
| ------------------- | --------------------------------- |
| Bedrooms            | 3                                 |
| Bathrooms           | 2                                 |
| House Size          | 2000 sqft                         |
| Budget              | $600k                            |
| Amenities           | Solar panels, Backyard, Garden    |
| Transportation      | Public transit                    |
| Lifestyle           | Remote work                       |
| Neighborhood Traits | Quiet, Tree-lined, Close to parks |

### Sample Natural Language Queries
```
"Find me a 3-bedroom house with a large backyard for under $500k"
"I need a modern apartment near public transportation"
"Show me eco-friendly homes with solar panels"
"Looking for a quiet neighborhood perfect for families"
```

---

## 🧱 Built With

* 🧠 [LangChain](https://www.langchain.com/) – Framework for building RAG pipelines
* 💬 [Groq](https://groq.com/) – Fast inference LLM backend
* 🌐 [Streamlit](https://streamlit.io/) – Frontend for interactive UI
* 🧯 [ChromaDB](https://www.trychroma.com/) – Open-source vector store
* 🧠 HuggingFace – for embeddings
* 🩵 [Loguru](https://github.com/Delgan/loguru) – Logging framework
* ⚡ uv – Fast Python package installer and resolver

---

```

---

## 🚀 Development Workflow

### Using Jupyter Notebooks
The project includes development notebooks in `src/notebooks/`:

```bash
# Start Jupyter
jupyter notebook src/notebooks/

# Open development notebooks
# - home_match.ipynb: Main development and testing
# - listings.ipynb: Listing data generation
```

### Database Management
```bash
# Initialize ChromaDB
python src/tools/chromadb/chroma_store.py

# Generate sample listings
python src/listings/generate_listings.py
```

---

## 📌 Future Plans

* ✅ **CSV Export**: Let users download listing data
* 🔍 **Location Filters**: Radius/distance based filtering
* 🌍 **Multilingual**: Internationalized text and inputs
* 📱 **Mobile Support**: Responsive sidebar and layout
* 📂 **Persistent Vector Store**: Maintain stateful sessions
* ✨ **LLM Feedback Loop**: Upvote/reject summary suggestions
* 📤 **Integrate Zapier or CRM**: Auto-send leads to sales
* 🔄 **Real-time Data**: Integration with MLS and real estate APIs
* 🎯 **Advanced Matching**: Machine learning-based preference learning
* 📍 **Map Integration**: Interactive map view of listings
* 💬 **Chat Interface**: Conversational search experience

---

## 🧪 Advanced Features

### Query Processing Pipeline
1. **Raw Query Input** → `src/chains/query_cleaning.py`
2. **Cleaned Query** → `src/chains/rag_chain.py`
3. **Context Retrieval** → `src/tools/chromadb/chroma_store.py`
4. **Response Generation** → `src/chains/full_chain.py`
5. **Result Parsing** → `src/llm_parsers/`

### Customization Points
- **Prompt Templates**: Modify prompts in `src/prompt_templates/`
- **LLM Models**: Configure models in `src/llms/groqllm.py`
- **UI Components**: Customize interface in `src/frontend/streamlit/`
- **Data Processing**: Extend listing processing in `src/listings/`

---

## 🔧 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure you're in the project directory
cd HomeMatch

# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

#### ChromaDB Issues
```bash
# Clear ChromaDB cache
rm -rf src/tools/chromadb/*.sqlite3
rm -rf src/tools/chromadb/[uuid-directories]

# Reinitialize database
python src/tools/chromadb/chroma_store.py
```

#### API Key Errors
```bash
# Verify .env file exists and contains keys
cat .env

# Check environment variables are loaded
python -c "import os; print(os.getenv('GROQ_API_KEY'))"
```

---

## 🤝 Contributing

We welcome contributions! You can:

* Submit feature requests
* Report bugs or UI issues
* Open pull requests with enhancements

### Development Setup
```bash
# Clone the repository
git clone https://github.com/your-username/HomeMatch.git
cd HomeMatch

# activate the uv workspace
uv .venv/bin/activate

# Install development dependencies
uv sync --dev

# Make your changes and test
# Submit a pull request
```

Please ensure your changes follow the existing project structure and naming conventions.

---

## 🙌 Acknowledgments

* **Groq** – For blazing-fast inference on large language models
* **LangChain** – For making composable agent and RAG workflows possible
* **ChromaDB** – For free and easy local document retrieval
* **Streamlit** – For building delightful interactive UIs
* **uv** – For fast and reliable Python dependency management
