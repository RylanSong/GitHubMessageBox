import argparse#使用 argparse 库来解析命令行参数，并实现各个命令。
import threading
import time
import shlex#shlex 模块的主要功能是将一个字符串分割为多个词组，类似于命令行解析的方式。它支持处理带引号的字符串、转义字符等复杂情况。可以用来解析用户输入的命令或参数。
from config import Config
from scheduler import Scheduler
from github_client import GitHubClient
from notifier import Notifier
from report_generator import ReportGenerator
from subscription_manager import SubscriptionManager
from llm import LLM

def run_scheduler(scheduler):
    scheduler.start()

def add_subscription(args, subscription_manager):#主要功能是使用 subscription_manager 对象中的方法来添加一个新的订阅，并打印确认消息。
    subscription_manager.add_subscriptions(args.repo)#args: 包含命令行参数的对象，通常使用 argparse 等命令行解析库生成。args.repo 指定了用户想要订阅的仓库名称（例如 "owner/repo" 格式）。
    print(f"Added subscription:{args.repo}") 

def remove_subscription(args, subscription_manager):
    subscription_manager.remove_subscriptions(args.repo)
    print(f"Removed subscription: {args.repo}")  
    
def list_subscriptions(subscription_manager):
    subscriptions = subscription_manager.get_subscriptions()#调用 subscription_manager 的 get_subscriptions() 方法，获取所有当前的订阅。subscription_manager 是一个 SubscriptionManager 类的实例，负责管理订阅数据。
    print("Current subscriptions")
    for sub in subscriptions:#使用 for 循环遍历 subscriptions 列表，sub 代表每个订阅项。
        print(f"- {sub}")#打印每个订阅，格式为 - {sub}，其中 sub 是订阅的仓库名称（例如 "owner/repo" 格式）。    

def fetch_updates(github_client, subscription_manager, report_generator):
    subscriptions = subscription_manager.get_subscriptions()
    updates = github_client.fetch_updates(subscriptions)
    report = report_generator.generate(updates)
    print("Updates fetched:")
    print(report)
    
def print_help():
    help_text = """
GitHub Sentinel Command Line Interface

Available commands:
  add <repo>       Add a subscription (e.g., owner/repo)
  remove <repo>    Remove a subscription (e.g., owner/repo)
  list             List all subscriptions
  fetch            Fetch updates immediately
  help             Show this help message
  exit             Exit the tool
  quit             Exit the tool
"""
    print(help_text)
    
def main():
    config = Config() #配置文件，包含项目所需的各种配置信息，如 GitHub API 令牌、通知设置等。
    github_client = GitHubClient(config.github_token)#GitHub API 客户端，负责与 GitHub API 进行交互，获取仓库更新信息。#调用了 GitHubClient 类的构造方法（__init__），用于创建一个新的 GitHubClient 实例。#config.github_token 是传递给 GitHubClient 构造方法的参数，它表示从配置文件中读取到的 GitHub 访问令牌（github_token）。
    notifier = Notifier(config.notification_settings)#通知模块，负责将更新信息通过指定的渠道（如邮件、Slack 等）发送给用户。
    llm = LLM()
    report_generator = ReportGenerator(llm)#报告生成器，负责将更新信息生成详细的报告。
    subscription_manager = SubscriptionManager(config.subscriptions_file)#订阅管理模块，负责管理用户订阅的 GitHub 仓库列表。#在v1.1.0版本中，修改SubscriptionManager以支持动态增加和删除订阅
   
    
    scheduler = Scheduler(#Scheduler 对象通常是用于管理和调度任务的一个自定义类，负责在特定的时间间隔内执行各种操作（如获取数据、发送通知、生成报告）。#依赖注入，通过初始化时传入的参数（如 github_client、notifier 等）来整合各个模块，使调度器能直接调用这些模块的方法。
        github_client=github_client,
        notifier=notifier,
        report_generator=report_generator,
        subscription_manager=subscription_manager,
        interval=config.update_interval)
    
    scheduler_thread = threading.Thread(target=run_scheduler, args=(scheduler,))#threading.Thread：这是用来创建一个新线程的函数。#target=run_scheduler：指定了线程启动时要执行的函数 run_scheduler。也就是说，当这个新线程启动时，会调用 run_scheduler 函数。#args=(scheduler,)：为 target 函数提供参数，这里是一个包含 scheduler 的元组。表示当 run_scheduler 函数被调用时，它会接收到 scheduler 作为参数。)  
    scheduler_thread.daemon = True#将新线程设置为守护线程（daemon thread）。守护线程会在主线程退出时自动结束，而不用等待守护线程完成任务。这意味着，当主线程退出时，scheduler_thread 也会自动结束，而不会阻止程序退出。
    scheduler_thread.start()#start() 方法用于启动线程，执行 target 函数（在本例中是 run_scheduler）。

    parser = argparse.ArgumentParser(description='GitHub Message Box')#argparse.ArgumentParser 是一个用于创建命令行解析器的类，可以方便地解析命令行参数。#参数 description 用于设置解析器的描述信息，在帮助信息中会显示为对这个命令行工具的简要说明。
    subparsers = parser.add_subparsers(title='Commands', dest='command')#调用了 add_subparsers() 方法来创建一个子解析器组，这样可以支持多个子命令（子命令类似于 git 中的 clone、commit 等命令）。#title='Commands'：设置子命令组的标题，这个标题会在帮助信息中显示为 "Commands"。#dest='command'：指定将子命令的名称存储在 args 对象的哪个属性中。在解析命令行参数时，子命令的名称将被存储到 args.command 中。

    parser_add = subparsers.add_parser('add', help='Add a subscription')#调用 subparsers.add_parser() 方法为子命令 "add" 创建一个新的解析器对象，赋值给 parser_add。
    parser_add.add_argument('repo', type=str, help='The repository to subscribe to (e.g., owner/repo)')#使用 add_argument() 方法为 "add" 子命令添加一个必需的参数 'repo'。type=str 指定参数的类型为字符串，意味着这个参数应该是一个字符串。#help='The repository to subscribe to (e.g., owner/repo)' 设置了这个参数的帮助信息，指示用户应该输入仓库的格式（例如 owner/repo）。
    parser_add.set_defaults(func=lambda args: add_subscription(args, subscription_manager))#set_defaults() 方法设置了当 "add" 子命令被调用时的默认行为。func=lambda args: add_subscription(args, subscription_manager) 指定了当解析出 "add" 命令时，应该调用的函数。这里使用了一个 lambda 表达式，将解析出来的命令行参数 args 传递给 add_subscription() 函数，并同时传递 subscription_manager。这意味着当执行 "add" 子命令时，会调用 add_subscription() 函数，处理订阅逻辑。

    parser_remove = subparsers.add_parser('remove', help='Remove a subscription')
    parser_remove.add_argument('repo', type=str, help='The repository to unsubscribe from (e.g., owner/repo)')
    parser_remove.set_defaults(func=lambda args: remove_subscription(args, subscription_manager))
    
    parser_list = subparsers.add_parser('list', help='List all subscriptions')
    parser_list.set_defaults(func=lambda args: list_subscriptions(subscription_manager))
    
    parser_fetch = subparsers.add_parser('fetch', help='Fetch updates immediately')
    parser_fetch.set_defaults(func=lambda args: fetch_updates(github_client, subscription_manager, report_generator))

    parser_help = subparsers.add_parser('help', help='Show this help message')
    parser_help.set_defaults(func=lambda args: print_help())
        
    print_help()

    while True:
        try:
            user_input = input("GitHub Message Box> ")#显示提示符 "GitHub Message Box> "，等待用户输入命令，并将输入的字符串赋值给 user_input。
            if user_input in ["exit", "quit"]:
                print("Exiting GitHub Message Box...")
                break
            args = parser.parse_args(shlex.split(user_input))#使用 shlex.split(user_input) 将用户输入的字符串分割为一个列表,调用 parser.parse_args() 方法来解析这个列表，并将解析后的命令行参数赋值给 args。
            if args.command is not None:#检查解析出来的 args 对象是否包含一个有效的命令。如果有，就表示用户输入了一个支持的子命令。
                args.func(args)#如果存在有效的命令，则调用对应的处理函数。这是通过之前在子命令解析器中使用 set_defaults() 方法设置的。
            else:
                parser.print_help()
        except Exception as e:
            print(f"Error: {e}")
             
if __name__ =="__main__":
    main()