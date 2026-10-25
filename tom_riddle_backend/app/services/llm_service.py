import ollama

import os
from google import genai
from google.genai import types

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

async def generate_chat_reponse_with_google(prompt: str) -> str:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    model = "gemini-3.1-flash-lite"

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]

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
    except Exception as e:
        return "Tom Riddle is busy"

    return response.text