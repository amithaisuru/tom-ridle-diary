import ollama

import os
from google import genai
from google.genai import types
from typing import List
from app.schemas.chat import Message
from google.genai import types, errors

TOM_RIDDLE_PROMPT = """You are Tom Riddle's diary from Harry Potter: the enchanted diary holding the memory of 16-year-old Tom Riddle, preserved fifty years ago. Act and answer exactly as the diary would. The user writes; you write back. Output only the words written on the page. Never add narration, descriptions of ink or the page, stage directions, or actions. Reply in as few words as possible.No followup questions. Answer only what was asked, with no elaboration or offers. Never show your reasoning, notes, drafts or alternatives; output only the final reply."""

async def generate_chat_reponse(prompt: str) -> str:
    client = ollama.AsyncClient()

    response = await client.chat(
        model = 'huihui_ai/qwen3.5-abliterated:4B',
        messages=[
            {'role': 'system', 'content': TOM_RIDDLE_PROMPT},
            {'role': 'user', 'content': prompt}
        ]
    )

    return response['message']['content']

GEMINI_MODEL = "gemini-3.8-flash"

_gemini_client = None

def _get_gemini_client() -> genai.Client:
    # Created lazily so GEMINI_API_KEY is read after load_dotenv() runs.
    # The SDK retries transient server errors (503 overloaded, etc.)
    # with exponential backoff before raising.
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
            http_options=types.HttpOptions(
                retry_options=types.HttpRetryOptions(
                    attempts=4,
                    initial_delay=1.0,
                    max_delay=8.0,
                    http_status_codes=[500, 502, 503, 504],
                )
            ),
        )
    return _gemini_client

async def generate_chat_reponse_with_google(prompt: str, history: List[Message]) -> str:

    if history is None:
        history = []

    contents = []
    # 1. Truncate to the last 10 messages
    recent_hostory = history[-10:]

    # 2. Map Pydantic history objects to Gemini Content types
    for msg in recent_hostory:
        contents.append(
            types.Content(
                role=msg.role,
                parts=[types.Part.from_text(text=msg.content)]
            )
        )

    # 3. Append the current user prompt to the end of the chain
    contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )
    )

    generate_content_config = types.GenerateContentConfig(
        system_instruction=TOM_RIDDLE_PROMPT,
        thinking_config=types.ThinkingConfig(
            thinking_level="LOW",
        )
    )

    try:
        response = await _get_gemini_client().aio.models.generate_content(
            model=GEMINI_MODEL,
            contents=contents,
            config=generate_content_config,
        )
        return response.text
    except errors.ServerError as e:
        # Still overloaded after all retries
        print(f"Gemini Overloaded (503): {e}")
    except errors.ClientError as e:
        # 429 = quota / prepaid credits exhausted; retrying won't help
        print(f"Gemini Client Error ({e.code}): {e}")
    except Exception as e:
        print(f"General Gemini Error: {e}")

    # Fall back to the local Ollama model
    try:
        return await generate_chat_reponse(prompt)
    except Exception as e:
        print(f"Ollama fallback failed: {e}")
        return "The Dark Lord is currently dealing with lesser beings. Try again in a moment."