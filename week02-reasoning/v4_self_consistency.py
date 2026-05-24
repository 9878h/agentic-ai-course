"""
v4: Self-consistency. Sample multiple reasoning paths, vote on answer.
Builds on v3 (few-shot CoT) — same prompt, different temperature, multiple samples.
"""

import re
from collections import Counter
from llm  import call


SYSTEM = """You are a careful math problem solver. Reason step by step inside
<reasoning>...</reasoning>, then give the final integer in <answer>...</answer>."""


FEW_SHOT_EXAMPLES = """Here are examples of the format I want:

Question: Lisa bought 4 packs of pens. Each pack has 6 pens. She gave 1/3 of the
pens to her sister. How many pens does she have left?

<reasoning>
Total pens = 4 packs * 6 pens = 24 pens.
She gave away 1/3, which is 24 / 3 = 8 pens.
She has 24 - 8 = 16 pens left.
</reasoning>

<answer>16</answer>


Question: A water tank holds 200 liters. It is 3/4 full. A pipe drains 25 liters
per hour. After how many hours will the tank be empty?

<reasoning>
Current water = 200 * 3/4 = 150 liters.
Drain rate = 25 liters/hour.
Time to empty = 150 / 25 = 6 hours.
</reasoning>

<answer>6</answer>


Now solve the next question in the same format.
"""


N_SAMPLES = 5
TEMPERATURE = 0.7


def parse_answer(text: str) -> int | None:
    match = re.search(
        r"<answer>\s*(-?\d[\d,]*)\s*</answer>",
        text,
        re.IGNORECASE
    )

    if match:
        try:
            return int(match.group(1).replace(",", ""))
        except ValueError:
            return None

    nums = re.findall(r"-?\d+", text.replace(",", ""))

    return int(nums[-1]) if nums else None


def solve(question: str) -> dict:
    """Sample N reasoning paths, vote on the answer."""

    prompt = f"{FEW_SHOT_EXAMPLES}\n\nQuestion: {question}"

    answers = []

    for i in range(N_SAMPLES):
        response = call(
            prompt=prompt,
            system=SYSTEM,
            temperature=TEMPERATURE,
            max_tokens=1024,
        )

        ans = parse_answer(response)

        if ans is not None:
            answers.append(ans)

    if not answers:
        return {
            "answer": None,
            "votes": [],
            "winner_count": 0,
        }

    counter = Counter(answers)

    winner, count = counter.most_common(1)[0]

    return {
        "answer": winner,
        "votes": answers,
        "winner_count": count,
    }


def run_all() -> list[dict]:
    from problems import get_problems

    results = []

    for p in get_problems():
        r = solve(p["question"])

        correct = (r["answer"] == p["answer"])

        results.append({
            "id": p["id"],
            "difficulty": p["difficulty"],
            "expected": p["answer"],
            "got": r["answer"],
            "correct": correct,
            "votes": r["votes"],
            "winner_count": r["winner_count"],
        })

        confidence = f"{r['winner_count']}/{N_SAMPLES}"

        print(
            f"  {p['id']} ({p['difficulty']}): "
            f"got {r['answer']} "
            f"(votes={r['votes']}, conf={confidence}) "
            f"expected {p['answer']} "
            f"{'OK' if correct else 'FAIL'}"
        )

    return results


if __name__ == "__main__":
    print(
        f"=== v4: Self-Consistency "
        f"(N={N_SAMPLES}, T={TEMPERATURE}) ==="
    )

    results = run_all()

    correct = sum(1 for r in results if r["correct"])

    print(
        f"\nAccuracy: {correct}/{len(results)} = "
        f"{correct/len(results)*100:.0f}%"
    )