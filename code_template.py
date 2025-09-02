from typing import Tuple, Dict
import dotenv
import os
from dotenv import load_dotenv
import requests
import json
import streamlit as st
from openai import OpenAI

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

load_dotenv()
EXCHANGERATE_API_KEY = os.getenv('EXCHANGERATE_API_KEY')




def get_exchange_rate(base: str, target: str, amount: str) -> Tuple:
    """Return a tuple of (base, target, amount, conversion_result (2 decimal places))"""
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{target}/{base}/{amount}"
    response = json.loads(requests.get(url).text)
    return(base, target, amount, f'{response["conversion_result"]:.2f}')

print(get_exchange_rate("USD", "EUR", "200"))

def call_llm(textbox_input) -> Dict:
    """Make a call to the LLM with the textbox_input as the prompt.
       The output from the LLM should be a JSON (dict) with the base, amount and target"""
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": textbox_input,
                }
            ],
            model=model_name
        )
       
    except Exception as e:
        print(f"Exception {e} for {Exception}")
    else:
        return  response.choices[0].message.content

st.title("Multilingual Money Changer")

# Create a text box for user input
user_input = st.text_input("Enter the amount and currency (e.g., 100 USD):")

# Create a submit button
if st.button("Submit"):
    if user_input:
        st.write(call_llm(user_input))
    else:
        st.error("Please enter a valid amount and currency.")
