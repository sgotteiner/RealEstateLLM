import os
import openai
from dotenv import load_dotenv

# Load environment variables from the .env file
# This line looks for a .env file in the current directory and loads its content into the environment
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Make sure you have created a .env file with your OPENAI_API_KEY.")
openai.api_key = api_key

# --- Test Call to the OpenAI Model ---
try:
    print("Making a test call to the OpenAI API...")

    # Create a chat completion request to test the API
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # A fast and capable model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Can you hear me?"}
        ]
    )

    # Extract and print the assistant's reply
    assistant_message = response.choices[0].message.content
    print(f"\nSuccess! Assistant's response: '{assistant_message}'")

except Exception as e:
    print(f"\nAn error occurred: {e}")