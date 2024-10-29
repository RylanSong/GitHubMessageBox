#将报告生成逻辑放在 report_generator.py 中，读取每日进展模块生成的 Markdown 文件，并使用 GPT-4 生成每日报告。
import os
from llm import LLM

class ReportGenerator:
    def __init__(self, llm):
        self.llm = llm
        
    def generate_daily_report(self, markdown_file):
        with open(markdown_file, 'r') as f:
            content = f.read()
        
        issues = self.parse_section(content, '## Issues')#self.parse_section(content, "## Issues") 会查找 content 中的 “## Issues” 部分，将其内容提取并赋值给 issues 变量。
        pull_requests = self.parse_section(content, '## Pull Requests')#self.parse_section(content, "## Pull Requests") 会查找 “## Pull Requests” 部分，并将其内容赋值给 pull_requests。
        
        summary = self.llm.summarize_issue_prs(issues, pull_requests)#self.llm.summarize_issues_prs(issues, pull_requests) 会调用一个语言模型（llm）的方法，将 issues 和 pull_requests 的内容生成总结并存储在 summary 变量中。
        report_filename = markdown_file.replace('.md', '_report.md')#通过将原始 Markdown 文件名（markdown_file）中的 “.md” 替换为 “_report.md”，生成一个新的文件名 report_filename，用于保存报告文件。
        
        with open(report_filename, 'w') as f:
            f.write('#Daily Report\n\n')
            f.write(summary)
            
        print(f'Generated daily report: {report_filename}')
        
    def parse_section(self, content, section):
        lines = content.split('\n')#content.split("\n") 将 content 按行分割成列表 lines，这样可以逐行处理文本内容。
        section_lines =[]#定义一个空列表 section_lines，用于存储指定章节的内容（如 “## Issues” 下的所有文本行）。
        capture = False#定义一个布尔变量 capture，用于表示当前是否在指定章节内。
            
        for line in lines:#这个代码块会遍历 lines 列表中的每一行，并根据条件判断将特定内容存入 section_lines，最后返回提取的章节内容。
            if line.strip() == section:#判断当前行是否等于指定的章节标题（例如 "## Issues"）。
                capture = True#如果是，将 capture 设置为 True，表示从这一行之后开始捕获内容，并 continue 跳过当前行，以避免把章节标题本身加入 section_lines。
                continue
            if capture and line.startwith("##"):#如果 capture 已经为 True（说明已经在捕获章节内容），并且当前行以 “##” 开头，则说明遇到了下一个章节标题，结束捕获过程并跳出循环。
                break
            if capture:#如果 capture 为 True，表示当前行属于指定章节内容，将其加入 section_lines 列表。
                section_lines.append(line.strip())#line.strip() 去掉行首和行尾的空白，确保内容整洁。
                    
        return section_lines#循环结束后，返回 section_lines，即指定章节的所有内容行。