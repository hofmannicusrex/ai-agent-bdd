import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessage

from call_function import available_functions, call_function
from prompts import system_prompt


def main():

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("No API key was found in the environment file (.env).")

    parser = argparse.ArgumentParser(description="Chatbot")
    # Add one argument of type String.
    parser.add_argument("user_prompt", type=str, help="The prompt which the user would like to receive a response regarding.")
    parser.add_argument("--verbose", action="store_true", help="Enables verbose output from the LLM.")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    # Client object. Add more details later.
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # List of messages to store the user's prompts.
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt}
    ]

    # Response object. Add more details later.
    response: ChatCompletion = client.chat.completions.create(
        model="openrouter/free",
        # Pass the list of messages.
        messages = messages,
        tools=available_functions,
        temperature=0  # Set the "temperature" to "0" for more deterministic output.
    )

    # Verify that the "usage" property is not None before trying to access its properties.
    if response.usage is None:
        raise RuntimeError("Error! The \"usage\" property was \"None\"... something most likely went wrong with the API request!")

    # Grab the message from the agent's response.
    message: ChatCompletionMessage = response.choices[0].message

    # If the message (ChatCompletionMessage) used any tool calls, inform the user.
    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue

        # Store the result of the "tool call".
        result_message = call_function(tool_call)

        # If the function that was called does not return correctly(?) raise an exception.
        if result_message["content"] is None:
            raise RuntimeError(f"Empty function response for {tool_call.function.name}")

        if args.verbose:
            print(f"-> {result_message['content']}")

    if args.verbose:
        print("\n----------------")
        print("Verbose output enabled!")
        print("----------------")
        print(f"User prompt: \"{args.user_prompt}\"")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
        print("----------------")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
