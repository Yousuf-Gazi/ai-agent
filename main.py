import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from call_function import available_functions, call_function
from config import MAX_ITERATIONS
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

    # run the agent for multiple turns (up to 20) to allow tool use + feedback loop
    for _ in range(MAX_ITERATIONS):
        try:
            content_response = generate_content(client, messages, verbose)
            if content_response and content_response.text:
                print("final response:")
                print(content_response.text)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")
            break

    # manually check and print if limit reached
    # iteration = 0
    # while True:
    #     iteration += 1
    #     if iteration > MAX_ITERATIONS:
    #         print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
    #         sys.exit(1)
    #
    #     try:
    #         final_response = generate_content(client, messages, verbose)
    #         if final_response and final_response.text:
    #             print("Final response:")
    #             print(final_response.text)
    #             break
    #     except Exception as e:
    #         print(f"Error in generate_content: {e}")

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # after the model response, capture its message(s) so the conversation persists
    # each candidate is a possible response; we append its conntent to `messages`

    # saves AI's response to conversation's history (`messages`)
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if not response.function_calls:
        return response

    # excute any tool calls the model requested and collect their results
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)

        # sanity-check: ensure the tool actually return a function response
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    # if the model asked for tools, we expect at least one tool response
    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    # convert each tool result into user-role content
    # store it to messages to preserve context for next turn
    messages.append(
        types.Content(
            role="user",
            parts=function_responses
        )
    )


if __name__ == "__main__":
    main()
