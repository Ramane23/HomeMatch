# Import the loguru logger for structured and colorful logging
from loguru import logger
# Import Pydantic's Field for metadata and field customization, and field_validator for validation
from pydantic import Field, field_validator
# Import BaseSettings for environment-based configuration, and SettingsConfigDict for model config
from pydantic_settings import BaseSettings, SettingsConfigDict


# Define a settings class that reads from environment and validates config
class Settings(BaseSettings):
    """
    A Pydantic-based settings class for managing application configurations.
    """

    # --- Pydantic Settings ---
    # Configuration for how Pydantic should behave (e.g., load from .env file)
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",                      # Path to the environment file
        env_file_encoding="utf-8"            # Encoding used in the .env file
    )


    # --- GROQ API Configuration ---
    # Required API key for GROQ (no default, must be provided)
    GROQ_API_KEY: str = Field(
        description="API key for GROQ service authentication.",
    )

    # Custom validator to ensure OPENAI_API_KEY is not empty or just whitespace
    @field_validator("GROQ_API_KEY")
    @classmethod
    def check_not_empty(cls, value: str, info) -> str:
        if not value or value.strip() == "":
            logger.error(f"{info.field_name} cannot be empty.")  # Log an errors
            raise ValueError(f"{info.field_name} cannot be empty.")  # Raise validation error
        return value  # Return the valid (non-empty) value


# Try to instantiate the settings from environment and defaults
try:
    settings = Settings()  # This loads values from env/.env and validates them
except Exception as e:
    logger.error(f"Failed to load configuration: {e}")  # Log error on failure
    raise SystemExit(e)  # Exit the program if config fails to load

