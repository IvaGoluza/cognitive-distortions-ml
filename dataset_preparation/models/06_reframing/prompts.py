"""
Prompt templates for the cognitive reframing experiments.

Four experiments are defined as:
    E1 — zero-shot
    E2 — few-shot, randomly sampled examples
    E3 — few-shot, category-matched examples
    E4 — few-shot, category-matched examples + situation field

The system message is fixed across all four experiments. Only the user
message varies. The output contract (one reframed thought)
is identical across all four.
"""

from dataclasses import dataclass
from typing import List, Optional


# ---------------------------------------------------------------------------
# Shared system message (identical for E1–E4)
# ---------------------------------------------------------------------------

SYSTEM_MESSAGE = """You are a cognitive behavioral therapy (CBT) assistant that helps people reframe \
unhelpful automatic thoughts. Given an unhelpful thought, you produce a single \
reframed thought that:
- preserves the speaker's situation and the original referent of the thought,
- reduces the dysfunctional element (catastrophizing, overgeneralization, mind \
reading, and so on) without denying the speaker's experience,
- is realistic and balanced rather than dismissive, falsely positive, or preachy,
- is written in the first person, in one or two sentences.

Respond with the reframed thought only. Do not add explanations, labels, \
preambles, or quotation marks."""


# ---------------------------------------------------------------------------
# Example container
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Example:
    """One in-context example drawn from the development pool."""
    situation: str
    thought: str
    reframe: str
    category: str


# ---------------------------------------------------------------------------
# E1 — Zero-shot
# ---------------------------------------------------------------------------

def build_prompt_e1(thought: str) -> str:
    return (
        "Reframe the following unhelpful thought.\n\n"
        f"Thought: {thought}\n\n"
        "Reframed thought:"
    )


# ---------------------------------------------------------------------------
# E2 — Few-shot, randomly sampled examples (no category conditioning)
# ---------------------------------------------------------------------------

def build_prompt_e2(thought: str, examples: List[Example]) -> str:
    if len(examples) != 3:
        raise ValueError(f"E2 expects exactly 3 examples, got {len(examples)}.")

    header = (
        "Reframe the following unhelpful thought. Below are three examples of "
        "how to perform this task.\n\n"
    )
    example_blocks = "\n\n".join(
        f"Example {i + 1}\n"
        f"Thought: {ex.thought}\n"
        f"Reframed thought: {ex.reframe}"
        for i, ex in enumerate(examples)
    )
    footer = (
        "\n\nNow reframe the following thought.\n\n"
        f"Thought: {thought}\n\n"
        "Reframed thought:"
    )
    return header + example_blocks + footer


# ---------------------------------------------------------------------------
# E3 — Few-shot, category-matched examples
# ---------------------------------------------------------------------------

def build_prompt_e3(thought: str, category: str, examples: List[Example]) -> str:
    if len(examples) != 3:
        raise ValueError(f"E3 expects exactly 3 examples, got {len(examples)}.")

    header = (
        "Reframe the following unhelpful thought. The thought reflects a "
        f'cognitive distortion of the type "{category}". Below are three '
        "examples of reframing thoughts that exhibit this same distortion.\n\n"
    )
    example_blocks = "\n\n".join(
        f"Example {i + 1}\n"
        f"Thought: {ex.thought}\n"
        f"Reframed thought: {ex.reframe}"
        for i, ex in enumerate(examples)
    )
    footer = (
        "\n\nNow reframe the following thought, addressing the "
        f'"{category}" distortion.\n\n'
        f"Thought: {thought}\n\n"
        "Reframed thought:"
    )
    return header + example_blocks + footer


# ---------------------------------------------------------------------------
# E4 — Few-shot, category-matched examples + situation field
# ---------------------------------------------------------------------------

def build_prompt_e4(
    thought: str,
    situation: str,
    category: str,
    examples: List[Example],
) -> str:
    if len(examples) != 3:
        raise ValueError(f"E4 expects exactly 3 examples, got {len(examples)}.")

    header = (
        "Reframe the following unhelpful thought. The thought arises in a "
        "specific situation described below, and reflects a cognitive "
        f'distortion of the type "{category}". Below are three examples of '
        "reframing thoughts that exhibit this same distortion.\n\n"
    )
    example_blocks = "\n\n".join(
        f"Example {i + 1}\n"
        f"Situation: {ex.situation}\n"
        f"Thought: {ex.thought}\n"
        f"Reframed thought: {ex.reframe}"
        for i, ex in enumerate(examples)
    )
    footer = (
        "\n\nNow reframe the following thought, taking the situation into "
        f'account and addressing the "{category}" distortion.\n\n'
        f"Situation: {situation}\n"
        f"Thought: {thought}\n\n"
        "Reframed thought:"
    )
    return header + example_blocks + footer


# ---------------------------------------------------------------------------
# Unified dispatcher
# ---------------------------------------------------------------------------

def build_prompt(
    experiment_id: str,
    thought: str,
    situation: Optional[str] = None,
    category: Optional[str] = None,
    examples: Optional[List[Example]] = None,
) -> str:
    """
    Dispatch to the correct prompt builder for the given experiment.

    Parameters
    ----------
    experiment_id : one of "E1", "E2", "E3", "E4".
    thought       : the test thought to reframe.
    situation     : required for E4; ignored otherwise.
    category      : required for E3 and E4; ignored otherwise.
    examples      : required for E2/E3/E4 (length 3); ignored for E1.
    """
    eid = experiment_id.upper()

    if eid == "E1":
        return build_prompt_e1(thought)

    if eid == "E2":
        if examples is None:
            raise ValueError("E2 requires `examples`.")
        return build_prompt_e2(thought, examples)

    if eid == "E3":
        if examples is None or category is None:
            raise ValueError("E3 requires `examples` and `category`.")
        return build_prompt_e3(thought, category, examples)

    if eid == "E4":
        if examples is None or category is None or situation is None:
            raise ValueError("E4 requires `examples`, `category`, and `situation`.")
        return build_prompt_e4(thought, situation, category, examples)

    raise ValueError(f"Unknown experiment_id: {experiment_id!r}")


# ---------------------------------------------------------------------------
# Decoding parameters (frozen across all experiments)
# ---------------------------------------------------------------------------

DECODING_PARAMS = {
    "model": "claude-sonnet-4-6",
    "max_tokens": 200,
    "temperature": 0.3,
    "top_p": 1.0,
}