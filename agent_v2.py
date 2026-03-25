import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

memory = []

def run_agent(prompt: str):
    global memory

    memory.append({"role": "user", "content": prompt})

    # 🧠 планирование
    plan = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
Ты автономный AI-агент.

Разбей задачу на шаги.
Ответь списком действий.

Пример:
1. Найти информацию
2. Проанализировать
3. Дать ответ
"""
            },
            {"role": "user", "content": prompt}
        ]
    )

    steps = plan.choices[0].message.content

    # ⚡ выполнение
    execution = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Ты выполняешь план шаг за шагом и даешь итог"
            },
            {"role": "user", "content": f"Задача: {prompt}\nПлан:\n{steps}"}
        ]
    )

    result = execution.choices[0].message.content

    memory.append({"role": "assistant", "content": result})

    return {
        "type": "agent",
        "plan": steps,
        "result": result
    }

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
