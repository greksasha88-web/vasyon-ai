import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

memory = []

def run_agent(prompt: str):
    global memory

    memory.append({"role": "user", "content": prompt})

    # 🧠 AI решает что делать
    decision = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
Ты AI-агент. Твоя задача — выбрать действие.

Ответь ТОЛЬКО одним словом:
text — если нужно ответить текстом
image — если нужно создать картинку
video — если нужно найти видео
solve — если это задача/решение

Никаких объяснений.
"""
            },
            {"role": "user", "content": prompt}
        ]
    )

    action = decision.choices[0].message.content.strip().lower()

    # ⚡ выбор действия
    if action == "image":
        return generate_image(prompt)

    if action == "video":
        return find_video(prompt)

    if action == "solve":
        return solve_problem(prompt)

    return smart_answer(prompt)


def smart_answer(prompt):
    global memory

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты мощный AI как ChatGPT"}
        ] + memory[-20:]
    )

    answer = response.choices[0].message.content

    memory.append({"role": "assistant", "content": answer})

    return {
        "type": "text",
        "result": answer
    }


def generate_image(prompt):
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    return {
        "type": "image",
        "url": response.data[0].url
    }


def find_video(prompt):
    return {
        "type": "video",
        "url": f"https://www.youtube.com/results?search_query={prompt}"
    }


def solve_problem(prompt):
    return smart_answer(prompt)
