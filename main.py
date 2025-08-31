import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt


def main():
    load_dotenv()

    # getting user prompt from the command line arguments
    verbose = "--verbose" in sys.argv
    args = list(filter(lambda arg: arg != "--verbose", sys.argv[1:]))

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    # client initialization
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # message formatting
    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}")

    # To keep track of the entire conversation with LLM store in a list with role
    messages = [
        types.Content(
            role="user",
            parts=[
                types.Part(text=user_prompt)
            ]
        ),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
