import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

memory = []

def run_agent(prompt: str):
    global memory

    try:
        memory.append({"role": "user", "content": prompt})

        # 🧠 планирование
        plan = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Разбей задачу на шаги"},
                {"role": "user", "content": prompt}
            ]
        )

        steps = plan.choices[0].message.content

        # ⚡ выполнение
        execution = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Выполни план и дай результат"},
                {"role": "user", "content": f"{prompt}\n\nПлан:\n{steps}"}
            ]
        )

        result = execution.choices[0].message.content

        memory.append({"role": "assistant", "content": result})

        return {
            "type": "agent",
            "plan": steps,
            "result": result
        }

    except Exception as e:
        return {
            "type": "error",
            "error": str(e)
        }
