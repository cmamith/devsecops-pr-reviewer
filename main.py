import os
import sys
from dotenv import load_dotenv
from crewai import Crew, Process

from tasks import create_code_review_task, create_formatting_task
from agents import get_security_reviewer_agent

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

def run_pr_review(diff_file_path: str):
    """
    Reads a PR diff from a file and runs the CrewAI DevOps Review agent on it.
    """
    if not os.path.exists(diff_file_path):
        print(f"Error: Diff file '{diff_file_path}' not found.")
        sys.exit(1)

    with open(diff_file_path, 'r') as f:
        pr_diff_content = f.read()

    print("Initializing DevSecOps Crew...")
    
    # 1. Initialize Agents
    reviewer_agent = get_security_reviewer_agent()
    
    # 2. Initialize Tasks
    review_task = create_code_review_task(pr_diff_content)
    format_task = create_formatting_task()

    # 3. Assemble Crew
    devsecops_crew = Crew(
        agents=[reviewer_agent],
        tasks=[review_task, format_task],
        process=Process.sequential,
        verbose=True
    )

    print("Starting PR Review Process...\n")
    
    # 4. Kickoff the process
    result = devsecops_crew.kickoff()
    
    print("\n" + "="*50)
    print("FINAL PR COMMENT GENERATED:")
    print("="*50 + "\n")
    print(result)
    
    # Optional: Save result to file for CI/CD ingestion
    with open("pr_comment.md", "w") as out_file:
        out_file.write(str(result))
    print("\nResult saved to pr_comment.md")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_diff_file>")
        sys.exit(1)
        
    diff_path = sys.argv[1]
    run_pr_review(diff_path)
