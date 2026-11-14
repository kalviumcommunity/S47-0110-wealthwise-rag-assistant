
from pathlib import Path
import tiktoken

# ---------------------------------
# CONFIGURATION
# ---------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# Demonstration pricing in USD per 1 million tokens.
# Replace these with the actual model/provider rates
# before treating the estimate as a real bill.
INPUT_RATE = 0.15
OUTPUT_RATE = 0.60

encoding = tiktoken.get_encoding("cl100k_base")


# ---------------------------------
# SAMPLE INPUTS
# ---------------------------------

short_question = (
    "What are the tax benefits of investing in mutual funds?"
)

paragraph = """
Mutual funds pool money from multiple investors and invest it
in securities such as stocks and bonds. Investors receive units
based on their contribution. Different mutual fund schemes have
different levels of risk, returns, liquidity and tax implications.
Investors should understand their financial goals before investing.
"""

# Try to retrieve an actual document from the project corpus.
supported_files = [".txt", ".md"]

corpus_files = [
    path
    for path in DATA_DIR.rglob("*")
    if path.is_file() and path.suffix.lower() in supported_files
]

if corpus_files:
    longest_file = max(corpus_files, key=lambda p: p.stat().st_size)
    full_document = longest_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )
    document_name = longest_file.name
else:
    document_name = "Built-in fallback sample"
    full_document = """
    WealthWise is a retrieval-augmented generation assistant
    designed for a retail bank's wealth management division.

    The system retrieves relevant information from approved
    investment policies, tax rules and product brochures.
    Retrieved information is supplied to a language model
    to generate grounded responses for relationship managers.

    The knowledge base may contain thousands of documents.
    Each document can be divided into smaller chunks for
    embedding, indexing and retrieval.

    Before generating an answer, the system retrieves relevant
    chunks and adds them to the model's input context.
    This increases input token usage. The generated response
    also consumes output tokens.

    Token measurement helps estimate context-window usage,
    retrieval efficiency and potential model API expenses.
    """


# ---------------------------------
# SAMPLE OUTPUTS
# ---------------------------------

sample_outputs = [
    "Mutual funds pool investments from multiple investors.",
    "Mutual funds offer diversification, but their risks and tax "
    "implications depend on the scheme and applicable regulations.",
    "WealthWise retrieves relevant approved documents and provides "
    "grounded answers. Relationship managers should consult the "
    "applicable policy and product documentation before advising clients."
]


# ---------------------------------
# TOKEN AND COST FUNCTIONS
# ---------------------------------

def count_tokens(text):
    return len(encoding.encode(text))


def count_words(text):
    return len(text.split())


def estimate_cost(input_tokens, output_tokens):
    input_cost = (input_tokens / 1_000_000) * INPUT_RATE
    output_cost = (output_tokens / 1_000_000) * OUTPUT_RATE

    return input_cost, output_cost, input_cost + output_cost


# ---------------------------------
# ANALYZE THREE SAMPLES
# ---------------------------------

samples = [
    ("Short Question", short_question, sample_outputs[0]),
    ("Paragraph", paragraph, sample_outputs[1]),
    ("Full Document", full_document, sample_outputs[2])
]

report = []

report.append("WEALTHWISE - TOKEN COST REPORT")
report.append("=" * 65)
report.append(f"Tokenizer: tiktoken / cl100k_base")
report.append(f"Input rate: ${INPUT_RATE} per 1M tokens")
report.append(f"Output rate: ${OUTPUT_RATE} per 1M tokens")
report.append("Pricing: Illustrative, not a live provider quote")
report.append("")

total_input_tokens = 0
total_output_tokens = 0

for name, input_text, output_text in samples:

    input_tokens = count_tokens(input_text)
    output_tokens = count_tokens(output_text)

    characters = len(input_text)
    words = count_words(input_text)

    input_cost, output_cost, total_cost = estimate_cost(
        input_tokens,
        output_tokens
    )

    total_input_tokens += input_tokens
    total_output_tokens += output_tokens

    report.append(f"SAMPLE: {name}")
    report.append("-" * 65)
    report.append(f"Characters: {characters}")
    report.append(f"Words: {words}")
    report.append(f"Input tokens: {input_tokens}")
    report.append(f"Output tokens: {output_tokens}")
    report.append(f"Input cost: ${input_cost:.8f}")
    report.append(f"Output cost: ${output_cost:.8f}")
    report.append(f"Total estimated cost: ${total_cost:.8f}")
    report.append("")

    print(f"\n{name}")
    print(f"Characters: {characters}")
    print(f"Words: {words}")
    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Input cost: ${input_cost:.8f}")
    print(f"Output cost: ${output_cost:.8f}")
    print(f"Total cost: ${total_cost:.8f}")


# ---------------------------------
# LENGTH VS TOKEN RELATIONSHIP
# ---------------------------------

report.append("LENGTH VS TOKEN RELATIONSHIP")
report.append("=" * 65)
report.append("Sample              Characters    Words    Tokens")

for name, input_text, _ in samples:
    report.append(
        f"{name:<20} {len(input_text):<14} "
        f"{count_words(input_text):<8} {count_tokens(input_text)}"
    )


# ---------------------------------
# TOTAL COST
# ---------------------------------

total_input_cost, total_output_cost, total_cost = estimate_cost(
    total_input_tokens,
    total_output_tokens
)

report.append("")
report.append("OVERALL TOTAL")
report.append("=" * 65)
report.append(f"Total input tokens: {total_input_tokens}")
report.append(f"Total output tokens: {total_output_tokens}")
report.append(f"Total input cost: ${total_input_cost:.8f}")
report.append(f"Total output cost: ${total_output_cost:.8f}")
report.append(f"Total estimated cost: ${total_cost:.8f}")

print("\n" + "=" * 65)
print("OVERALL TOTAL")
print("=" * 65)
print(f"Input tokens: {total_input_tokens}")
print(f"Output tokens: {total_output_tokens}")
print(f"Estimated cost: ${total_cost:.8f}")


# ---------------------------------
# SAVE RESULTS
# ---------------------------------

report_path = OUTPUT_DIR / "token_report.txt"

report_path.write_text(
    "\n".join(report),
    encoding="utf-8"
)

print(f"\nReport saved to: {report_path}")
