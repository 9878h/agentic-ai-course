""" 
v1: Baseline solver. No CoT, no reasoning scaffolding. 
Just: question -> answer. 
""" 
import re 
from llm import call 
  
  
SYSTEM = """You are a math problem solver. Read the problem and provide ONLY 
the final numerical answer. Do not show your work. Do not explain. 
Reply with just an integer.""" 
  
  
def solve(question: str) -> dict: 
    """Solve a single problem. Return {answer: int|None, raw: str}.""" 
    response = call( 
        prompt=question, 
        system=SYSTEM, 
        temperature=0.0, 
        max_tokens=50, 
    ) 
    answer = parse_answer(response) 
    return {"answer": answer, "raw": response} 
  
  
def parse_answer(text: str) -> int | None: 
    """Extract an integer from the response. Return None if can't find one.""" 
    # Look for the first integer in the text 
    match = re.search(r"-?\d+", text.replace(",", "")) 
    if match: 
        try: 
            return int(match.group()) 
        except ValueError: 
            return None 
    return None 
  
  
def run_all() -> list[dict]:
    """Run baseline on all problems. Return list of results."""
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
        })

        print(
            f"{p['id']} ({p['difficulty']}): "
            f"got {r['answer']}, expected {p['answer']} "
            f"{'OK' if correct else 'FAIL'}"
        )

    return results


if __name__ == "__main__":
    print("=== v1: Baseline ===")

    results = run_all()

    correct = sum(1 for r in results if r["correct"])

    print(
        f"\nAccuracy: {correct}/{len(results)} = "
        f"{correct/len(results)*100:.0f}%"
    )
    