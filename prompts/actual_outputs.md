# WealthWise Actual Prompt Comparison

**Model:** llama3.2

## Common User Question


What is the minimum investment amount for the bank's
mutual fund investment product?


## Approved Context


The approved product brochure states that the minimum
initial investment is Rs. 5,000.

Additional investments can be made from Rs. 1,000.


## Variation 1: Vague Prompt

The minimum investment amount for the bank's mutual fund investment product is Rs. 5,000.

## Variation 2: Clear Prompt

According to the approved context, the minimum initial investment for the bank's mutual fund investment product is Rs. 5,000.

## Fallback Test: Missing Information

**Question:** What is the guaranteed annual return rate for this mutual fund product?

**Actual model output:**

I cannot verify the guaranteed annual return rate for this mutual fund product from the approved knowledge sources. Please consult the relevant policy document or compliance team.

## Observation

The vague prompt answered the basic investment question correctly but did not explicitly identify the approved context as its source.

The clear prompt provided a more grounded response by referring to the approved context.

In the fallback test, the clear prompt correctly refused to provide an unsupported guaranteed annual return rate. It used the specified fallback response and directed the user to approved sources or the compliance team.

This demonstrates that clear system instructions improve source-grounding and help prevent unsupported financial claims.
