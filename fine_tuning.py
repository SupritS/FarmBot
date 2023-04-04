import openai
import os

model_name = "Enter your trained model name"


def custom_data(prompt):
    openai.api_key = "Enter your OpenAI API-Key."

    completion = openai.Completion.create(
        model=model_name, prompt=prompt, max_tokens=50
    )
    return completion.choices[0]["text"]
