# src/llm.py
import os
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = ""
class LLM:
    def __init__(self):
        self.client = OpenAI()

    def summarize_issues_prs(self, issues, pull_requests):
        prompt = (
            "Summarize the following GitHub issues and pull requests in a formal report format:\n\n"
            "## Issues\n"
        )
        for issue in issues:
            prompt += f"- {issue['title']} #{issue['number']}: {issue['body']}\n"
        prompt += "\n## Pull Requests\n"
        for pr in pull_requests:
            prompt += f"- {pr['title']} #{pr['number']}: {pr['body']}\n"

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content":prompt}
            ]
        )
        print(response)
        return response.choices[0].text.strip()
