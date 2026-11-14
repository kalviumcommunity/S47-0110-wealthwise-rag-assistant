
"""
WealthWise RAG Assistant
System Prompt Comparison

Task:
Compare a vague system prompt with a clear,
constrained system prompt using the same user question.
"""

# ==========================================
# VARIATION 1: VAGUE SYSTEM PROMPT
# ==========================================

VAGUE_SYSTEM_PROMPT = """
You are a helpful banking assistant.
Answer questions about banking and investments.
Be clear and helpful.
"""


# ==========================================
# VARIATION 2: CLEAR AND CONSTRAINED PROMPT
# ==========================================

CLEAR_SYSTEM_PROMPT = """
You are WealthWise, an internal banking knowledge
assistant for relationship managers.

ROLE:
Help relationship managers understand approved
banking, investment, and tax-related information.

SCOPE:
- Answer using only the supplied approved context.
- Do not invent policies, rates, figures, or eligibility rules.
- Do not provide unsupported investment recommendations.
- Do not expose confidential customer information.

CONSTRAINTS:
- Use professional and simple language.
- Keep answers under 150 words.
- Use short paragraphs or bullet points.
- Clearly distinguish verified information from uncertainty.

FALLBACK:
If the supplied context does not contain the answer,
respond:

"I cannot verify this information from the approved
knowledge sources. Please consult the relevant policy
document or compliance team."

Never guess or invent information.
"""


# ==========================================
# COMMON USER QUESTION AND CONTEXT
# ==========================================

USER_MESSAGE = """
What is the minimum investment amount for the bank's
mutual fund investment product?
"""

CONTEXT = """
The approved product brochure states that the minimum
initial investment is Rs. 5,000.

Additional investments can be made from Rs. 1,000.
"""


# ==========================================
# MESSAGE BUILDER
# ==========================================

def build_messages(system_prompt, user_question, context):

    return [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"""
Approved Context:
{context}

Question:
{user_question}
"""
        }
    ]


# ==========================================
# DISPLAY PROMPT COMPARISON
# ==========================================

def display_comparison():

    variations = {
        "VARIATION 1 - VAGUE PROMPT": VAGUE_SYSTEM_PROMPT,
        "VARIATION 2 - CLEAR PROMPT": CLEAR_SYSTEM_PROMPT
    }

    for title, system_prompt in variations.items():

        print("\n" + "=" * 60)
        print(title)
        print("=" * 60)

        messages = build_messages(
            system_prompt,
            USER_MESSAGE,
            CONTEXT
        )

        for message in messages:
            print(f"\nROLE: {message['role']}")
            print(message["content"])


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    display_comparison()
