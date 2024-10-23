# config.py
import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()
def get_variable(name):
    if hasattr(st, 'secrets') and name in st.secrets:
        return st.secrets[name]
    return os.getenv(name)

GEMINI_API_KEY = get_variable('GEMINI_API_KEY')
GROQ_API_KEY = get_variable('GROQ_API_KEY')
REPLICATE_API_TOKEN = get_variable('REPLICATE_API_TOKEN')
HG_API_KEY = get_variable('HG_API_KEY')