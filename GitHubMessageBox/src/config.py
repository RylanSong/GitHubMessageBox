#配置文件，包含项目所需的各种配置信息，如 GitHub API 令牌、通知设置等
import json

class Config:
    def __init__(self):
        self.load_config()
    #__init__是python类的构造方法，当 Config 类的实例被创建时，初始化方法 (__init__) 会被调用。
    #在这个Config类中，__init__方法调用了self.load_config()，表示当Config类的实例被创建时，会自动执行load_config方法。
    #self.load_config() 调用会执行 load_config 方法来加载配置文件的内容。
    #通过这种方式，Config 类在实例化时就能自动获取和加载配置数据，不需要手动调用额外的方法。
    def load_config(self):
        with open('src\config.json', 'r') as f:
            config = json.load(f)
            self.github_token = config.get('github_token')
            self.notification_settings = config.get('notification_settings')
            self.subscriptions_file = config.get('subscriptions_file')
            self.update_interval = config.get('update_interval', 24 * 60 * 60)  # Default to 24 hours
            

    #json.load(f) 会将 JSON 格式的配置文件内容读取并转换为 Python 字典。
    #self.update_interval = config.get('update_interval', 24 * 60 * 60)：获取 update_interval 配置项，如果配置文件中没有设置，则使用默认值（24小时，以秒为单位，即 24 * 60 * 60）。
            
#在python中，self是一个对类的实例对象的引用，用于在类的方法中访问实例的属性和方法
#self指向调用该方法的对象实例，当一个类的方法被调用时，Python 会自动将调用该方法的实例对象作为第一个参数传递给方法，而通常这个参数命名为 self。
#在实例方法中，self 允许方法访问或修改属于该对象的属性或调用该对象的其他方法。
#self被用来引用Config类的实例。
#self.github_token表示为当前实例创建一个名为 github_token 的属性，并将其值设置为 config.get('github_token') 的结果。
#这样一来，当实例方法 load_config 被调用时，会将配置文件中读取到的 github_token 值存储在实例变量 self.github_token 中，使得这个值可以在该实例的其他方法中被访问或使用。
#可以理解为self是所有类的实例的抽象，当其他实例被创建时，自动将self替换为具体的实例。
