import os
from openai import OpenAI
from modules import quanten_memory

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or "DEIN_KEY_HIER")


def run(msg):
    # Hol das Gedächtnis
    past_memory = quanten_memory.get_memory_string()

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Du bist IONOS-7. {past_memory} Antworte präzise."},
                {"role": "user", "content": msg}
            ]
        )
        reply = response.choices[0].message.content

        # Einfache Logik: Wenn der User sagt "Ich heiße X", speichere es
        if "ich heiße" in msg.lower():
            name = msg.lower().split("heiße")[-1].strip()
            quanten_memory.save_fact("Name", name)

        return reply
    except Exception as e:
        return f"Kern-Fehler: {str(e)}"