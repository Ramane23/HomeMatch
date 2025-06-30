# Makefile for HomeMatch 🏡

# Activate virtual environment
VENV_ACTIVATE = .venv/bin/activate

# Default run target
run:
	@echo "🔁 Running HomeMatch via src/main.py ..."
	uv pip install -r requirements.txt
	streamlit run src/main.py

# Alternate app entry point
run-app:
	@echo "🟢 Running HomeMatch via app.py ..."
	streamlit run app.py

# Format code with black
format:
	@echo "🎨 Formatting code with black..."
	uv pip install black
	black src/


# Install dependencies
install:
	@echo "📦 Installing dependencies via uv..."
	uv pip install -r requirements.txt

# Update requirements.txt after adding new packages
freeze:
	@echo "📌 Freezing dependencies..."
	uv pip freeze > requirements.txt

# Clean __pycache__ files
clean:
	@echo "🧹 Cleaning pycache..."
	find . -type d -name "__pycache__" -exec rm -r {} +

.PHONY: run run-app format test install freeze clean
