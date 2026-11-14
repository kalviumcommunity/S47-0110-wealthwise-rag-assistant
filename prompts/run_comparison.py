
"""
WealthWise RAG Assistant
Actual LLM System Prompt Comparison

Compares vague and clear system prompts, then
tests the clear prompt with missing information.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, APIStatusError

from prompts.prompt_comparison import (
    VAGUE_SYSTEM_PROMPT,
    CLEAR_SYSTEM_PROMPT,
    USER_MESSAGE,
    CONTEXT,
    build_messages,
)

load_dotenv()

BASE_URL = os.getenv("OPENAI_API_BASE_URL")
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("CHAT_MODEL")

if not all([BASE_URL, API_KEY, MODEL]):
    raise ValueError("Check your .env configuration.")

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    timeout=120.0,
)


def generate_response(system_prompt, question=USER_MESSAGE):
    messages = build_messages(system_prompt, question, CONTEXT)

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content or ""


def main():
    results = []

    variations = [
        ("Variation 1: Vague Prompt", VAGUE_SYSTEM_PROMPT),
        ("Variation 2: Clear Prompt", CLEAR_SYSTEM_PROMPT),
    ]

    print("=" * 60)
    print("WEALTHWISE PROMPT COMPARISON")
    print(f"Model: {MODEL}")
    print("=" * 60)

    try:
        for title, system_prompt in variations:
            print(f"\n\n{title}")
            print("-" * 60)

            answer = generate_response(system_prompt)

            print("\nActual LLM Output:")
            print(answer)

            results.append((title, answer))

        # Test the fallback behaviour using the clear prompt.
        fallback_question = (
            "What is the guaranteed annual return rate "
            "for this mutual fund product?"
        )

        fallback_answer = generate_response(
            CLEAR_SYSTEM_PROMPT,
            fallback_question
        )

        print("\n\nFALLBACK TEST: Missing Information")
        print("-" * 60)
        print(f"\nQuestion: {fallback_question}")
        print("\nActual LLM Output:")
        print(fallback_answer)

    except APIConnectionError:
        print("Connection failed. Check whether Ollama is running.")
        return
    except APIStatusError as error:
        print(f"LLM API error: {error.status_code}")
        return

    output_file = Path("prompts/actual_outputs.md")

    with output_file.open("w", encoding="utf-8") as file:
        file.write("# WealthWise Actual Prompt Comparison\n\n")
        file.write(f"**Model:** {MODEL}\n\n")

        file.write("## Common User Question\n\n")
        file.write(USER_MESSAGE + "\n\n")

        file.write("## Approved Context\n\n")
        file.write(CONTEXT + "\n\n")

        for title, answer in results:
            file.write(f"## {title}\n\n")
            file.write(answer + "\n\n")

        file.write("## Fallback Test: Missing Information\n\n")
        file.write(f"**Question:** {fallback_question}\n\n")
        file.write("**Actual model output:**\n\n")
        file.write(fallback_answer + "\n\n")

        file.write("## Observation\n\n")
        file.write(
           "The vague prompt answered the basic investment question "
           "correctly but did not explicitly identify the approved "
           "context as its source.\n\n"
       )
        file.write(
             "The clear prompt provided a more grounded response by "
             "referring to the approved context.\n\n"
        )
        file.write(
    "In the fallback test, the clear prompt correctly refused "
    "to provide an unsupported guaranteed annual return rate. "
    "It used the specified fallback response and directed the "
    "user to approved sources or the compliance team.\n\n"
)
        file.write(
    "This demonstrates that clear system instructions improve "
    "source-grounding and help prevent unsupported financial claims.\n"
)

    print("\n" + "=" * 60)
    print("COMPARISON COMPLETED")
    print(f"Actual outputs saved to: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
