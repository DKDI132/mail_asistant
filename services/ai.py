import os
import json
from google import genai
from pydantic import BaseModel
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

class EmailAnalysis(BaseModel):
    importance: bool
    summary: str

async def skrot(mess: str):
    try:
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=mess,
            config=types.GenerateContentConfig(
                system_instruction="Jesteś inteligentnym asystentem pocztowym. Twoim zadaniem jest ocena ważności wiadomości e-mail oraz generowanie zwięzłych, 1-2 zdaniowych podsumowań w języku polskim.",
                response_mime_type="application/json",
                response_schema=EmailAnalysis,
            ),
        )
        dictona = json.loads(response.text)
        return dictona
    except Exception as ex:
        print(f"Błąd komunikacji z Gemini API: {ex}")
        return {
            "importance": False,
            "summary": "Błąd analizy AI."
        }