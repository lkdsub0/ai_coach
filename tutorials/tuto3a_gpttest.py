from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv(dotenv_path=".streamlit/secrets.toml")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create(
    model="gpt-3.5-turbo",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
