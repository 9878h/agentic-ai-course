"""
Run all variants on the same problem set, produce a comparison table.
"""

from tabulate import tabulate
import llm as llm

import v1_baseline
import v2_zero_shot_cot
import v3_few_shot_cot
import v4_self_consistency
import v5_self_critique


VARIANTS = [
    ("v1 Baseline", v1_baseline),
    ("v2 Zero-Shot CoT", v2_zero_shot_cot),
    ("v3 Few-Shot CoT", v3_few_shot_cot),
    ("v4 Self-Consistency", v4_self_consistency),
    ("v5 Self-Critique", v5_self_critique),
]


def main():
    summary_rows = []

    for name, module in VARIANTS:
        print(f"\n{'='*60}")
        print(f"Running {name}...")
        print(f"{'='*60}")

        llm.reset_usage()

        results = module.run_all()

        usage = llm.get_usage()

        correct = sum(1 for r in results if r["correct"])

        total = len(results)

        easy_correct = sum(
            1 for r in results
            if r["correct"] and r["difficulty"] == "easy"
        )

        med_correct = sum(
            1 for r in results
            if r["correct"] and r["difficulty"] == "medium"
        )

        hard_correct = sum(
            1 for r in results
            if r["correct"] and r["difficulty"] == "hard"
        )

        cost = (
            usage["input_tokens"] * 3.00
            + usage["output_tokens"] * 15.00
        ) / 1_000_000

        summary_rows.append([
            name,
            f"{correct}/{total}",
            f"{correct/total*100:.0f}%",
            f"{easy_correct}/3",
            f"{med_correct}/4",
            f"{hard_correct}/3",
            usage["input_tokens"],
            usage["output_tokens"],
            f"${cost:.4f}",
        ])

    print("\n\n" + "="*60)

    print("FINAL RESULTS")

    print("="*60)

    print(tabulate(
        summary_rows,
        headers=[
            "Variant",
            "Score",
            "Accuracy",
            "Easy",
            "Med",
            "Hard",
            "In Tok",
            "Out Tok",
            "Cost",
        ],
        tablefmt="grid"
    ))


if __name__ == "__main__":
    main()
