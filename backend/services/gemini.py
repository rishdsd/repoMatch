import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def call_gemini(prompt: str) -> str:  # keeping same function name so nothing else breaks
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def parse_json_response(text: str) -> any:
    clean = text.replace("```json", "").replace("```", "").strip()
    start = clean.find("[") if "[" in clean else clean.find("{")
    end = clean.rfind("]") if "[" in clean else clean.rfind("}")
    if start == -1:
        raise ValueError("No JSON found in response")
    return json.loads(clean[start:end+1])