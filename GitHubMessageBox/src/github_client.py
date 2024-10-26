#GitHub API 客户端，负责与 GitHub API 进行交互，获取仓库更新信息
import requests

class GitHubClient:
    def __init__(self, token):
        self.token = token
#当创建GithubClient类的实例时，初始化方法会被调用。
#参数token时用于认证的Github访问令牌。
#self.token=token将令牌保存为实例变量，以便后续的API请求使用。
    def fetch_updates(self, subscriptions):
        headers = {
            'Authorization': f'token {self.token}'
        }
        updates = {}
        for repo in subscriptions:
            response = requests.get(f'https://api.github.com/repos/{repo}/events', headers=headers)
            if response.status_code == 200:
                updates[repo] = response.json()
        return updates
#fetch_updates负责从Github获取指定仓库的更新信息。
#参数subscriptions是一个包含仓库名称的列表，这些仓库是用户订阅的，需要检查更新。
#headers 字典中包含了认证信息，用于 GitHub API 请求。'Authorization': f'token {self.token}' 表示将令牌作为认证的方式，以 token 作为前缀。
#创建一个空的字典 updates，用于存储每个仓库的更新信息。
#遍历 subscriptions 列表中的每个仓库名称，执行以下操作：
#1.使用 requests.get 发送一个 GET 请求到 GitHub API，访问指定仓库的事件接口 https://api.github.com/repos/{repo}/events。
#2.请求中包含构建好的 headers，以便进行认证。
#3.如果响应的状态码为 200（即请求成功），则将返回的 JSON 数据添加到 updates 字典中，键为仓库名称，值为对应的更新数据（JSON 格式）。

#最终返回一个包含所有订阅仓库更新信息的字典 updates。字典的键是仓库名称，值是该仓库的事件数据。

#在 Python 中，__init__ 方法会在类的实例被创建时自动调用，不需要手动调用它。
#它通常用于为新创建的对象分配初始值或进行设置。
#__init__ 方法接受两个参数：self 和 token
#self 是指向实例对象本身的引用，用于访问对象的属性和方法。每个类的方法的第一个参数都必须是 self。
#token 是传递给 GitHubClient 类的参数，用于初始化实例的属性。
#使用场景：每当创建 GitHubClient 类的一个实例时，例如：client=GitHubClient('my_github_token)
#__init__ 方法会被自动调用，'my_github_token' 会被传递给 token 参数，然后赋值给 self.token。
#这样，client 对象就有了一个名为 token 的属性，其值为 'my_github_token'。
