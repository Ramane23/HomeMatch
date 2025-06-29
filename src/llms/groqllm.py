"""
This module defines the GroqLLM class, which retrieves a Groq LLM model instance
based on user inputs from a Streamlit UI.
"""

import os  # For accessing environment variables
import streamlit as st  # Streamlit for UI feedback
from langchain_groq import ChatGroq  # Groq LLM interface from LangChain-Groq integration

class GroqLLM:
    """
    A class to configure and return a Groq LLM (Language Model) based on user input.
    """

    def __init__(self, user_controls_input):
        """
        Initializes the GroqLLM object with user inputs.

        Args:
            user_controls_input (dict): Dictionary containing keys like
                                        'GROQ_API_KEY' and 'selected_groq_model'.
        """
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        """
        Retrieves and initializes the Groq language model.

        Returns:
            ChatGroq: An instance of the selected Groq language model.

        Raises:
            ValueError: If any error occurs while creating the LLM instance.
        """
        try:
            # Extract API key and model name from user controls
            groq_api_key = self.user_controls_input["GROQ_API_KEY"]
            selected_groq_model = self.user_controls_input["selected_groq_model"]

            # Check if both input and environment API keys are empty
            if groq_api_key == '' and os.environ.get("GROQ_API_KEY", '') == '':
                st.error("Please Enter the Groq API KEY")  # Show error in Streamlit
                return None  # Prevent execution if no API key is present

            # Instantiate the ChatGroq model with API key and selected model
            llm = ChatGroq(api_key=groq_api_key, model=selected_groq_model)

        except Exception as e:
            # Raise a user-friendly error if anything goes wrong
            raise ValueError(f"Error Occurred With Exception: {e}")

        return llm  # Return the instantiated model

groqllm =GroqLLM()