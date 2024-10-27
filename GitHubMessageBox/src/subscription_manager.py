import json

class SubscriptionManager:#SubscriptionManager 类管理用户的订阅列表，能够从指定的 JSON 文件中加载这些信息。
    def __init__(self, subscriptions_file):#__init__ 方法初始化 SubscriptionManager 类实例。
        self.subscriptions_file = subscriptions_file##参数 subscriptions_file 是一个字符串，表示存储订阅列表的文件路径。#self.subscriptions_file = subscriptions_file 将文件路径保存到实例变量 self.subscriptions_file，以便在类的其他方法中使用。  
        self.subscriptions = self.load_subscriptions()#self.subscriptions 调用 load_subscriptions 方法，从文件加载当前的订阅列表。self.subcriptions是一个包含订阅的GitHub仓库列表，是python对象
        
    def load_subscriptions(self):#加载订阅
        with open(self.subscriptions_file, 'r') as f:#with open(self.subscriptions_file, 'r') as f 打开文件，模式为只读（'r'），并将文件对象赋值给变量 f。
            return json.load(f)#json.load(f) 将文件中的 JSON 数据解析为 Python 对象（通常是列表或字典）。
    
    def save_subscriptions(self):#保存订阅
        with open(self.subscriptions_file, 'w') as f:
            json.dump(self.subscriptions, f, indent=4)#self.subscriptions是要保存的数据，f是要写入的文件对象（上一步中打开的文件），indent=4用于格式化输出，增加可读性，每个嵌套级别使用4个空格缩进
        
    def get_subscriptions(self):#获取订阅
        return self.subscriptions#返回当前的订阅列表
 
    def add_subscriptions(self, repo):#增加订阅
        if repo not in self.subscriptions:
            self.subscriptions.append(repo)
            self.save_subscriptions()
            
    def remove_subscriptions(self, repo):#删除订阅
        if repo in self.subscriptions:
            self.subscriptions.remove(repo)
            self.save_subscriptions()        
        
       




