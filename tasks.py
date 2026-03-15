from crewai import Task
from agents import get_security_reviewer_agent

def create_code_review_task(pr_diff_content: str) -> Task:
    """
    Creates the task for analyzing the PR diff.
    """
    return Task(
        description=(
            f"Review the following Pull Request diff for an infrastructure change.\n\n"
            f"Diff Content:\n"
            f"```\n{pr_diff_content}\n```\n\n"
            f"Your specific objectives are:\n"
            f"1. Identify any open security groups (e.g., 0.0.0.0/0 on port 22 or 3389).\n"
            f"2. Identify any missing resource limits (CPU/Memory) in Kubernetes specifications.\n"
            f"3. Identify any missing liveness or readiness probes in Kubernetes objects.\n"
            f"4. Identify wildcard permissions in IAM policies (e.g., Action: '*').\n"
            f"5. Identify any potential hardcoded secrets or credentials.\n"
        ),
        expected_output=(
            "A structured list of findings detailing specific misconfigurations, "
            "their potential impact, and file/line references if possible."
        ),
        agent=get_security_reviewer_agent()
    )

def create_formatting_task() -> Task:
    """
    Creates the task to format the review findings into a human-readable PR comment.
    """
    return Task(
        description=(
            "Take the security and reliability findings provided by the previous task and "
            "format them into a professional, human-readable markdown comment suitable "
            "for pasting directly into a GitHub or GitLab Pull Request.\n\n"
            "Guidelines:\n"
            "- Be polite but clear about the severity of the findings.\n"
            "- Group findings logically (e.g., 'Security Vulnerabilities', 'Reliability Risks').\n"
            "- Provide actionable recommendations on how to fix each issue.\n"
            "- Use markdown features like bolding, lists, and code blocks for readability.\n"
            "- If no issues are found, return a simple 'LGTM! No critical security or reliability issues found.' message."
        ),
        expected_output="A polished markdown string ready to be used as a PR comment.",
        agent=get_security_reviewer_agent()
    )
