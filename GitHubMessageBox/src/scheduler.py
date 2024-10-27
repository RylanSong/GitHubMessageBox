import time
import threading # pylint: disable=unused-import
#time模块用于控制程序的休眠和计时。
#threading 模块可用于创建和管理多线程（尽管在这段代码中没有使用多线程功能）。

class Scheduler:
    def __init__(self, github_client, notifier, report_generator, subscription_manager, interval):
        self.github_client = github_client
        self.notifier = notifier
        self.report_generator = report_generator
        self.subscription_manager = subscription_manager
        self.interval = interval
#github_client：用于获取 GitHub 仓库更新的客户端。
#notifier：负责发送通知的对象。
#report_generator：生成更新报告的对象。
#subscription_manager：管理订阅列表的对象。
#interval：调度的时间间隔，以秒为单位。    
    def start(self):
        while True:
            self.run()
            time.sleep(self.interval)
#start 方法启动调度器的执行。
#while True 创建一个无限循环，持续运行任务。
#每次运行任务后，程序会调用 time.sleep(self.interval)，让调度器休眠一段时间（interval 秒），然后再次执行任务。  
    def run(self):
        subscriptions = self.subscription_manager.get_subscriptions()
        updates = self.github_client.fetch_updates(subscriptions)
        report = self.report_generator.generate(updates)
        self.notifier.notify(report)
#run 方法执行调度的具体任务。
#获取订阅列表：调用 self.subscription_manager.get_subscriptions() 来获取用户订阅的 GitHub 仓库列表。
#获取更新：调用 self.github_client.fetch_updates(subscriptions) 获取这些仓库的更新信息。
#生成报告：使用 self.report_generator.generate(updates) 将获取到的更新信息生成一个格式化的报告。
#发送通知：调用 self.notifier.notify(report) 发送生成的报告。

#使用 subscriptions = self.subscription_manager.get_subscriptions() 而不是 self.subscriptions = self.subscription_manager.get_subscriptions() 是因为 subscriptions 是一个局部变量，只在 run 方法内部使用，而不需要存储在对象的实例属性中。
#由于它只在 run 方法内使用，不需要在对象的其他方法中访问，所以使用局部变量 subscriptions 就足够了。
#实例属性（如 self.subscriptions）通常用于需要在类的不同方法之间共享的数据。
#如果某个数据只在一个方法的上下文中使用，就没有必要将其存储为实例属性，因为这样会增加对象的状态管理复杂性






#Scheduler 类通过初始化接受多个功能组件的实例（如 GitHubClient、Notifier、ReportGenerator 和 SubscriptionManager），并设置一个时间间隔。
#start 方法启动一个无限循环，按照设定的时间间隔不断执行 run 方法。
#run 方法获取最新的仓库更新信息，生成报告并发送通知。