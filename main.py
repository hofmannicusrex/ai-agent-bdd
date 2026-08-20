import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessage

from call_function import available_functions, call_function
from config import MAX_ITERATIONS
from prompts import system_prompt


def main() -> None:

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("No API key was found in the environment file (.env).")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument(
        "user_prompt",
        type=str,
        help="The prompt which the user would like to receive a response regarding.",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enables verbose output from the LLM."
    )
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
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(MAX_ITERATIONS):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error: Error encountered in the agent loop: {e}")

    # If maximum loop iterations reached, exit. Should save some tokens!
    print(f"Maximum iterations ({MAX_ITERATIONS}) reached")
    sys.exit(1)


def generate_content(client: OpenAI, messages: list, verbose: bool) -> str | None:
    # Response object. Add more details later.
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,  # Pass the list of messages.
        tools=available_functions,
        temperature=0,  # Set the "temperature" to "0" for more deterministic output.
    )

    # Verify that the "usage" property is set before trying to access its properties.
    if not response.usage:
        raise RuntimeError(
            "Error: The API response appears to be malformed. Something most likely went wrong with the API request"
        )

    if verbose:
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)

    # Grab the message from the agent's response.
    message = response.choices[0].message
    # Grab the model's message/response and append it to the messages list.
    messages.append(message)

    if not message.tool_calls:
        return message.content

    # Loop through any tool calls that the model executes and keep track of those calls.
    for tool_call in message.tool_calls:
        # Skip any non-function calls.
        if tool_call.type != "function":
            continue

        # Store the result of any "tool calls".
        result_message = call_function(tool_call, verbose)

        # If the function that was called does not return correctly(?) raise an exception.
        if not result_message.get("content"):
            raise RuntimeError(f"Empty function response for {tool_call.function.name}")

        if verbose:
            print(f"-> {result_message['content']}")

        # After each tool call, grab the model's message and append it to the messages list.
        messages.append(result_message)

    return None


if __name__ == "__main__":
    main()
