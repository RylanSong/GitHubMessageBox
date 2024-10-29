# src/github_client.py

import requests
import datetime

class GitHubClient:
    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': f'token {self.token}'}

    def fetch_updates(self, repos):
        updates = {}
        for repo in repos:
            updates[repo] = {
                'commits': self.fetch_commits(repo),
                'issues': self.fetch_issues(repo),
                'pull_requests': self.fetch_pull_requests(repo)
            }
        return updates

    def fetch_commits(self, repo):
        url = f'https://api.github.com/repos/{repo}/commits'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_issues(self, repo):
        url = f'https://api.github.com/repos/{repo}/issues'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_pull_requests(self, repo):
        url = f'https://api.github.com/repos/{repo}/pulls'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def export_daily_progress(self, repo):
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        issues = self.fetch_issues(repo)
        pull_requests = self.fetch_pull_requests(repo)
        filename = f"{repo.replace('/', '_')}_{date_str}.md"

        with open(filename, 'w') as f:
            f.write(f"# {repo} Daily Progress - {date_str}\n\n")
            f.write("## Issues\n")
            for issue in issues:
                f.write(f"- {issue['title']} #{issue['number']}\n")
            f.write("\n## Pull Requests\n")
            for pr in pull_requests:
                f.write(f"- {pr['title']} #{pr['number']}\n")

        print(f"Exported daily progress to {filename}")

        return filename





#在 Python 中，__init__ 方法会在类的实例被创建时自动调用，不需要手动调用它。
#它通常用于为新创建的对象分配初始值或进行设置。
#__init__ 方法接受两个参数：self 和 token
#self 是指向实例对象本身的引用，用于访问对象的属性和方法。每个类的方法的第一个参数都必须是 self。
#token 是传递给 GitHubClient 类的参数，用于初始化实例的属性。
#使用场景：每当创建 GitHubClient 类的一个实例时，例如：client=GitHubClient('my_github_token)
#__init__ 方法会被自动调用，'my_github_token' 会被传递给 token 参数，然后赋值给 self.token。
#这样，client 对象就有了一个名为 token 的属性，其值为 'my_github_token'。
