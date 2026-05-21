import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

def call_gemini(prompt: str) -> str:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text.strip()

def parse_json_response(text: str) -> any:
    clean = text.replace("```json", "").replace("```", "").strip()
    start = clean.find("[") if "[" in clean else clean.find("{")
    end = clean.rfind("]") if "[" in clean else clean.rfind("}")
    if start == -1:
        raise ValueError("No JSON found in response")
    return json.loads(clean[start:end+1])