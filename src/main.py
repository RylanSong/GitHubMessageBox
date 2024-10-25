from config import Config
from scheduler import Scheduler
from github_client import GitHubClient
from notifier import Notifier
from report_generator import ReportGenerator
from subscription_manager import SubscriptionManager
    
def main():
    config = Config()
    #配置文件，包含项目所需的各种配置信息，如 GitHub API 令牌、通知设置等。
    github_client = GitHubClient(config.github_token)
    #GitHub API 客户端，负责与 GitHub API 进行交互，获取仓库更新信息。
    #调用了 GitHubClient 类的构造方法（__init__），用于创建一个新的 GitHubClient 实例。
    #config.github_token 是传递给 GitHubClient 构造方法的参数，它表示从配置文件中读取到的 GitHub 访问令牌（github_token）。
    notifier = Notifier(config.notification_settings)
    #通知模块，负责将更新信息通过指定的渠道（如邮件、Slack 等）发送给用户。
    report_generator = ReportGenerator()
    #报告生成器，负责将更新信息生成详细的报告。
    subscription_manager = SubscriptionManager(config.subscriptions_file)
    #订阅管理模块，负责管理用户订阅的 GitHub 仓库列表。
    scheduler = Scheduler(
        github_client=github_client,
        notifier=notifier,
        report_generator=report_generator,
        subscription_manager=subscription_manager,
        interval=config.update_interval
    )
    #Scheduler 对象通常是用于管理和调度任务的一个自定义类，负责在特定的时间间隔内执行各种操作（如获取数据、发送通知、生成报告）。
    
    scheduler.start()
    #依赖注入，通过初始化时传入的参数（如 github_client、notifier 等）来整合各个模块，使调度器能直接调用这些模块的方法。
if __name__ == "__main__":
    main()
