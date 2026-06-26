import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-2.5-flash"

CHROMA_DB_PATH = "data/chroma_db"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"