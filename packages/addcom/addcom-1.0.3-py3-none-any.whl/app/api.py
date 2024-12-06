from openai import OpenAI
from rich import print
import os


def build_prompt_messages(content: str, context: str) -> list[dict]:
    """
    Constructs messages for the LLM
    """
    # Raise an error if no code was provided
    if not content.strip():
        raise ValueError(
            "It seems that the specified file is empty, please provide code to comment"
        )

    # Create system prompt
    system_prompt = (
        "You are a coding assistant. When provided with the contents of a code file, your task is to add appropriate comments "
        "to explain its functionality where necessary. Comments should follow best practices and be concise yet informative. "
        "You may also receive example code snippets as a reference for the desired comment style. Carefully review these examples "
        "paying special attention to how functions and complex logic are explained. Sample snippets will be prefixed with 'Example:'. "
        "Your response should include only the modified code with the added comments,  without any additional text, explanations,"
        " or changes to the existing code. Make sure not to wrap the code in the brackets."
        "Again, don't provide any additional text with the code!"
    )

    # Initialize message list with the system prompt
    messages = [{"role": "system", "content": system_prompt}]

    # Add context file's contents as previous interaction - few-shot learning
    if context is not None:
        messages.append({"role": "user", "content": f"Example:\n{context}"})
        messages.append(
            {
                "role": "assistant",
                "content": (
                    "Great! Please provide another example if you have one, "
                    "or share the source code you'd like me to add comments to."
                ),
            }
        )

    # Add the uncommented code, as the last user message
    messages.append({"role": "user", "content": content})

    return messages


def generate_comments(
    file_path: str,
    content: str,
    context: str,
    api_key: str,
    url: str,
    model: str,
    stream: bool,
) -> str:
    """
    Send the file content to the API endpoint to generate comments.
    Returns the code with generated comments.
    """
    # Use environment variable for API key if it was not provided
    api_key = api_key or os.getenv("ADDCOM_API_KEY")

    # Check if API key was successfully set
    if not api_key:
        raise RuntimeError("Error: API key must be provided to generate comments")

    # Use Groq API endpoint as default if base URL not provided
    base_url = url or "https://api.groq.com/openai/v1"

    # Use LLama3 model as default if model option not provided
    model = model or "llama3-8b-8192"

    # Initialize OpenAI client (default = Groq API endpoint)
    client = OpenAI(base_url=base_url, api_key=api_key)

    try:
        response = client.chat.completions.create(
            messages=build_prompt_messages(content, context), model=model, stream=stream
        )

        if not stream:
            return response.choices[0].message.content
        else:
            streamed_content = ""

            print(f"--- {file_path} with added comments ---\n\n")

            # Print each chunk to stdout as it arrives and accumulate content
            for chunk in response:
                chunk_content = chunk.choices[0].delta.content
                if chunk_content:
                    print(chunk_content, end="", flush=True)
                    streamed_content += chunk_content

            print("\n\n")

            return streamed_content

    except Exception as e:
        raise RuntimeError(
            f"Error occurred while trying to generate comments for the file '{file_path}': {e}"
        )
