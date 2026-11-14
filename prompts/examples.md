# WealthWise System Prompt Comparison

## Objective

Compare two system prompts for the WealthWise banking knowledge assistant using the same user question, approved context, and language model.

## 1. Understanding the Message Roles

- **System message:** Defines the assistant's role, scope, tone, constraints, and fallback behaviour.
- **User message:** Contains the question and approved context that the assistant must use to answer.

Separating these roles makes the assistant's behaviour instructions distinct from the information supplied for a particular question.

## 2. Common Test Input

**User question:**

What is the minimum investment amount for the bank's mutual fund investment product?

**Approved context:**

The approved product brochure states that the minimum initial investment is Rs. 5,000.

Additional investments can be made from Rs. 1,000.

## 3. Prompt Variation 1 — Vague System Prompt

The first prompt describes the assistant as helpful and asks it to answer banking and investment questions. It does not define strict source-grounding or fallback rules.

**Actual model output:**

The minimum investment amount for the bank's mutual fund investment product is Rs. 5,000.

## 4. Prompt Variation 2 — Clear and Constrained System Prompt

The second prompt defines the assistant as an internal banking knowledge assistant. It includes:

- A specific role and scope.
- A rule to answer only from approved context.
- Restrictions against inventing policies or figures.
- Professional and simple language.
- A 150-word answer limit.
- A fallback response when information is unavailable.

**Actual model output:**

According to the approved context, the minimum initial investment for the bank's mutual fund investment product is Rs. 5,000.

## 5. Comparison and Observations

Both prompts produced the correct investment amount.

However, Variation 2 explicitly refers to the approved context, making its grounding clearer. Variation 1 also gives the correct answer in this test, but its instructions do not establish the same source restrictions or fallback behaviour.

The difference is subtle in this straightforward example. More challenging questions, especially those involving missing information, are needed to evaluate the prompts further.

## 6. Selected Prompt

**Selected: Variation 2 — Clear and Constrained Prompt**

I selected Variation 2 because it defines the assistant's responsibilities, limits its answers to approved information, discourages unsupported claims, and specifies what to do when information is unavailable.

These controls are important for an internal banking assistant, where accuracy and consistency matter.

## 7. Test Environment

- Language model: llama3.2
- Runtime: Ollama
- API interface: OpenAI-compatible client
- Temperature: 0
- Comparison script: `prompts/run_comparison.py`
- Actual outputs: `prompts/actual_outputs.md`