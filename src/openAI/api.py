import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.organization = os.getenv("ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_new_query(lib, input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[
                {"role": "system", "content": lib.PROMPT1},
                {"role": "user", "content": input}
            ],
        temperature=0,
        max_tokens=1024
    )

    return response['choices'][0]['message']['content']

def analysis_main_product(lib, input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[
                {"role": "system", "content": lib.PROMPT2},
                {"role": "user", "content": input}
            ],
        temperature=0,
        max_tokens=1024
    )

    return response['choices'][0]['message']['content']

def analysis_brand(lib, input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[
                {"role": "system", "content": lib.PROMPT3},
                {"role": "user", "content": input}
            ],
        temperature=0,
        max_tokens=1024
    )

    return response['choices'][0]['message']['content']
