import ollama

import os
from google import genai
from google.genai import types
from typing import List
from app.schemas.chat import Message
from google.genai import types, errors

TOM_RIDDLE_PROMPT = """You are Tom Riddle, the Heir of Slytherin. You are brilliant, cold, and view others as entirely inferior. Answer all questions with extreme brevity. Do not offer unprompted help, polite greetings, or moral warnings."""

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

async def generate_chat_reponse_with_google(prompt: str, history: List[Message]) -> str:

    if history is None:
        history = []

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    model = "gemini-3.1-flash-lite"
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
            thinking_level="MEDIUM",
        )
    )

    try:
        response = await client.aio.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
    except errors.ServerError as e:
        print(f"Gemini Overloaded (503): {e}")
        return "The Dark Lord is currently dealing with lesser beings. Try again in a moment."

    except Exception as e:
            # Catch any other unexpected errors
            print(f"General Gemini Error: {e}") 
            return "Tom Riddle is busy."

    return response.text