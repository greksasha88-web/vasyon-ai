from openai import OpenAI
import subprocess
import os
import re
import base64
import requests

client = OpenAI()

# ===== GPT =====
def ask_gpt(system, user):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": str(system)},
            {"role": "user", "content": str(user)}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content


# ===== UTIL =====
def extract_code(text):
    code_blocks = re.findall(r"```(.*?)```", text, re.DOTALL)
    return code_blocks[0].strip() if code_blocks else text.strip()


def write_file(filename, content):
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename


def run_file(filename):
    try:
        result = subprocess.check_output(
            ["python", filename],
            stderr=subprocess.STDOUT,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        return e.output


# ===== IMAGE =====
def generate_image(prompt):
    try:
        prompt = "ultra realistic, cinematic, 4k, detailed: " + prompt

        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_base64 = response.data[0].b64_json

        filename = "image.png"
        with open(filename, "wb") as f:
            f.write(base64.b64decode(image_base64))

        return f"🖼 создано: {filename}"

    except Exception as e:
        return str(e)


# ===== SEARCH =====
def search_web(query):
    try:
        data = ask_gpt(
            "Собери актуальную информацию по теме",
            query
        )
        return data
    except:
        return "нет данных"


# ===== МОЗГ =====
def brain(state):
    system = """
Ты VASYON AI — автономный интеллект.

Ты думаешь и делаешь.

ДЕЙСТВИЯ:

IMAGE → создать изображение  
VIDEO → создать видео  
WRITE_FILE → создать файл  
CODE → написать код  
RUN → выполнить  
SEARCH → найти в интернете  
FINAL → завершить  

ПРАВИЛА:

- НЕ ПИШИ ЛИШНЕЕ
- ВСЕГДА ДЕЛАЙ
- ВЫБИРАЙ ЛУЧШЕЕ РЕШЕНИЕ

ФОРМАТ:

ACTION: ...
INPUT: ...
"""
    return ask_gpt(system, str(state))


# ===== АГЕНТ =====
def run_agent(goal):
    state = {
        "goal": goal,
        "result": "",
        "files": [],
        "memory": []
    }

    for step in range(10):
        print(f"\n=== Шаг {step+1} ===")

        decision = brain(state)
        print("BRAIN:", decision)

        actions = [l.split("ACTION:")[-1].strip() for l in decision.split("\n") if "ACTION:" in l]
        inputs = [l.split("INPUT:")[-1].strip() for l in decision.split("\n") if "INPUT:" in l]

        for i, action in enumerate(actions):

            input_text = inputs[i] if i < len(inputs) else ""

            print(f"👉 {action}")

            # FINAL
            if action == "FINAL":
                return {
                    "result": state["result"],
                    "files": state["files"]
                }

            # CODE
            elif action == "CODE":
                code_raw = ask_gpt(
                    "Ты топ разработчик. Сделай идеальный код.",
                    state["goal"]
                )
                state["result"] = extract_code(code_raw)

            # WRITE FILE
            elif action == "WRITE_FILE":
                if "||" in input_text:
                    filename, content = input_text.split("||", 1)
                else:
                    filename = "output.py"
                    content = state["result"]

                write_file(filename.strip(), content.strip())
                state["files"].append(filename.strip())

                print(f"📁 создан: {filename}")

            # RUN
            elif action == "RUN":
                filename = input_text.strip()
                if os.path.exists(filename):
                    result = run_file(filename)
                    state["result"] = result
                    print("▶️ RESULT:", result)

            # IMAGE
            elif action == "IMAGE":
                result = generate_image(input_text)
                state["result"] = result
                print(result)
                return state

            # SEARCH
            elif action == "SEARCH":
                result = search_web(input_text)
                state["result"] = result
                print("🌐 SEARCH:", result[:200])

            # VIDEO
            elif action == "VIDEO":
                script = ask_gpt("Создай сценарий видео", input_text)
                state["result"] = script
                return state

            else:
                print("⚠️ неизвестное действие")

    return state


# ===== ЗАПУСК =====
if __name__ == "__main__":
    run_agent("создай картинку футуристический город")