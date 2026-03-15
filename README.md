# AI PR Reviewer Agent 

A DevSecOps Pull Request Reviewer built with CrewAI. This agent automatically analyzes PR diffs to identify security vulnerabilities, reliability issues, and configuration flaws (like exposed secrets, overly permissive IAM policies, and missing Kubernetes resource limits) and posts a human-like review comment.



## Setup for Cross-Repository Usage

To use this AI Reviewer across multiple repositories in your organization, the best approach is to publish it as a centralized **Custom GitHub Action**.

### 1. Centralize the Action Repository
Create a dedicated repository (e.g., `org-name/devsecops-pr-reviewer`) and push this codebase to it. Ensure this repository is accessible to the other repositories where you want to run the action.

### 2. Configure Organization Secrets
1. Go to your GitHub Organization Settings -> Secrets and variables -> Actions.
2. Add a new Organization Secret named `OPENAI_API_KEY` containing your valid OpenAI key. Make it available to the repositories that will use the action.

### 3. Implement the Workflow in Target Repositories
In any repository where you want PRs to be reviewed automatically, create a workflow file: `.github/workflows/ai-pr-review.yml`.

Use the following configuration to call your centralized action:

```yaml
name: DevSecOps AI PR Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  pull-requests: write # Required to post comments
  contents: read

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Required to generate a complete diff

      - name: Generate PR Diff
        id: generate_diff
        run: |
          git diff origin/${{ github.base_ref }}...HEAD > pr.diff
          echo "diff_path=pr.diff" >> $GITHUB_OUTPUT

      - name: Run AI PR Reviewer
        uses: your-org-name/devsecops-pr-reviewer@main # ⚠️ Change 'your-org-name' to your actual central repo
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          diff_file: ${{ steps.generate_diff.outputs.diff_path }}

      - name: Post Comment on PR
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            // The action saves the output to pr_comment.md
            const commentBody = fs.readFileSync('pr_comment.md', 'utf8');
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: commentBody
            });
```

---

## 🛠️ Local Development and Testing

If you want to test the CrewAI logic locally without GitHub Actions:

### 1. Setup Virtual Environment
```bash
python 3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Run the Reviewer
Provide a diff file to the script. A sample diff (`sample_diff.txt`) is provided in the repository.

```bash
python main.py sample_diff.txt
```

The output will be printed to the terminal and saved to `pr_comment.md`.
