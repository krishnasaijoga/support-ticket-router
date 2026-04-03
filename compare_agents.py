import requests
import pandas as pd

BASE_URL = "https://krishnajoga-support-ticket-router-v2.hf.space"

TASKS = [
    "easy",
    "medium",
    "hard",
    "extra_hard",
    "hard_missing_info",
    "vip_priority",
    "repeat_failure",
]


def run_baseline_episode(task_name: str) -> dict:
    # 1. Reset
    reset_res = requests.post(f"{BASE_URL}/reset", json={"task_name": task_name})
    reset_res.raise_for_status()

    done = False
    step_count = 0
    history = []

    # 2. Baseline -> Step loop
    while not done:
        baseline_res = requests.get(f"{BASE_URL}/baseline")
        baseline_res.raise_for_status()
        action = baseline_res.json()["baseline_action"]

        step_res = requests.post(
            f"{BASE_URL}/step",
            json={"action_type": action}
        )
        step_res.raise_for_status()
        step_data = step_res.json()

        done = step_data["done"]
        step_count += 1
        history = step_data["info"].get("history", [])

    # 3. Final grade
    grader_res = requests.get(f"{BASE_URL}/grader")
    grader_res.raise_for_status()
    grade = grader_res.json()["grade"]

    # 4. Final state
    state_res = requests.get(f"{BASE_URL}/state")
    state_res.raise_for_status()
    state = state_res.json()

    return {
        "task": task_name,
        "baseline_grade": grade,
        "steps_taken": step_count,
        "resolved": state.get("resolved"),
        "done": state.get("done"),
        "history": " -> ".join(history),
    }


def main():
    rows = []

    for task in TASKS:
        print(f"Running baseline for task: {task}")
        row = run_baseline_episode(task)
        rows.append(row)

    df = pd.DataFrame(rows)
    print("\nComparison Table:\n")
    print(df.to_string(index=False))

    df.to_csv("baseline_comparison.csv", index=False)
    print("\nSaved to baseline_comparison.csv")


if __name__ == "__main__":
    main()