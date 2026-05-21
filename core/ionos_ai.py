import os
from openai import OpenAI
from modules import quanten_memory, project_memory

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or "DEIN_KEY_HIER")


def run(msg):
    user_mem = quanten_memory.get_memory_string()
    proj_mem = project_memory.get_project_status()

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"Du bist IONOS-7. {user_mem} {proj_mem} "
                               f"Du kennst den aktuellen Stand des Codes."
                },
                {"role": "user", "content": msg}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Quanten-Sync-Fehler: {str(e)}"