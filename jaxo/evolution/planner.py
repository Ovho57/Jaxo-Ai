"""Turns an explicit user goal into a human-reviewed change plan."""


def make_plan(goal: str, findings: list[str]) -> str:
    summary = "\n".join(f"- {item}" for item in findings) or "- No Python source files found."
    return (
        "SELF-IMPROVEMENT PLAN (proposal only)\n"
        f"Goal: {goal.strip()}\n"
        "Current source inventory:\n"
        f"{summary}\n"
        "Next: ask the user to select exact files and review a unified diff. "
        "Never auto-apply this plan."
    )
