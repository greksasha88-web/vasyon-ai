import requests

def run_agent(prompt: str):
    prompt_lower = prompt.lower()

    # 🧠 определение типа запроса
    if "нарисуй" in prompt_lower or "image" in prompt_lower:
        return generate_image(prompt)

    if "видео" in prompt_lower or "video" in prompt_lower:
        return find_video(prompt)

    if "реши" in prompt_lower or "задач" in prompt_lower:
        return solve_problem(prompt)

    return smart_answer(prompt)


# 💬 умный текст
import openai

openai.api_key = "ТВОЙ_API_KEY"


def smart_answer(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты супер умный AI, отвечаешь четко, круто и понятно"},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "type": "text",
        "result": response.choices[0].message.content
    }


# 🎨 картинка
def generate_image(prompt):
    return {
        "type": "image",
        "url": f"https://dummyimage.com/600x400/000/fff&text={prompt}"
    }


# 🎬 видео
def find_video(prompt):
    return {
        "type": "video",
        "url": f"https://www.youtube.com/results?search_query={prompt}"
    }


# 📚 решение задач
def solve_problem(prompt):
    return {
        "type": "solution",
        "steps": [
            "1. Анализ условия",
            "2. Формула",
            "3. Решение",
            "4. Ответ"
        ]
    }
