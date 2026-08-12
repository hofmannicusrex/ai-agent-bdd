import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

def main():

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("No API key was found in the environment file (.env).")

    parser = argparse.ArgumentParser(description="Chatbot")
    # Add one argument of type String.
    parser.add_argument("user_prompt", type=str, help="The prompt which the user would like to receive a response regarding.")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    # Client object. Add more details later.
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # Response object. Add more details later.
    response = client.chat.completions.create(
        model="openrouter/free",
        messages = [
            {
                "role": "user",
                "content": args.user_prompt,
            }
        ]
    )

    # Verify that the "usage" property is not None before trying to access its properties.
    if response.usage is None:
        raise RuntimeError("Error! The \"usage\" property was \"None\"... something most likely went wrong with the API request!")

    print(response.choices[0].message.content)
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")


if __name__ == "__main__":
    main()
