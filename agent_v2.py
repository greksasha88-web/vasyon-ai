import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_agent(prompt: str):
    prompt_lower = prompt.lower()

    if "нарисуй" in prompt_lower:
        return generate_image(prompt)

    if "видео" in prompt_lower:
        return find_video(prompt)

    if "реши" in prompt_lower:
        return solve_problem(prompt)

    return smart_answer(prompt)


def smart_answer(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты мощный AI как ChatGPT"},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "type": "text",
        "result": response.choices[0].message.content
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
