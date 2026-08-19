import os
from dotenv import load_dotenv
from google import genai

# Load biến môi trường từ file .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEFAULT_MODEL = "gemini-flash-latest"

def get_genai_client() -> genai.Client:
    """Khởi tạo và trả về Gemini Client."""
    if not GEMINI_API_KEY:
        raise ValueError("Không tìm thấy GEMINI_API_KEY. Vui lòng kiểm tra file .env!")
    return genai.Client(api_key=GEMINI_API_KEY)