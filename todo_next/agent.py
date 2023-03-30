import ast
import datetime
import json
from dataclasses import dataclass, field
from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from todo_next.templates import sort_template
from todo_next.task_base import Task, TaskItems
from todo_next.utils import datetime_to_describe


def task_list():
    tasks = TaskItems.load_local()
    tasks = tasks.to_list_fmt()
    print(tasks)

def task_sort():
    tasks = TaskItems.load_local()
    sorted_tasks = sort_task(tasks)
    sorted_tasks.save_local()

def task_push():
    new_task = input("Hi! What's your task:\n")
    comment = input("""I got it! You can write comment(exp. tomorrow night is deadline, This is difficult and so on)\n""")
    task = Task(title=new_task, comment=comment)
    taskitems = TaskItems.load_local()
    taskitems.add(task)
    sorted_tasks = sort_task(taskitems)
    sorted_tasks.save_local()

def sort_task(taskitems):
    llm = OpenAI(temperature=0, model="text-davinci-003")
    prompt = PromptTemplate(template=sort_template(), 
                            input_variables=["tasks", "tasks_num", "now"])
    bot = LLMChain(llm=llm, prompt=prompt, verbose=True)
    gpt_tasks = ""
    gpt_tasks = taskitems.to_sort_fmt()
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
    now = datetime_to_describe(now)
    sorted_number = bot.predict(tasks=str(gpt_tasks), now=now, tasks_num=len(taskitems))
    sorted_number = ast.literal_eval(sorted_number)
    sorted_tasks = []
    for i in sorted_number:
        sorted_tasks.append(taskitems.tasks[int(i)-1])
    sorted_tasks = TaskItems(sorted_tasks)
    return sorted_tasks

def search_tasks(task):
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local("old_tasks", embeddings)
    docs = db.similarity_search(task.describe())
    return docs.page_content

def store_tasks(task):
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local("old_tasks", embeddings)
    db.add_texts([task.describe()])
    db.save_local("old_tasks")

def task_done():
    task_list()
    done_num = input("which task did you done")



class TaskItems:
    def __init__(self, tasks):
        self.tasks = tasks

    @classmethod
    def load_local(cls, filepath="task.json"):
        tasks = []
        with open(filepath) as f:
            tasks_local = json.load(f)["task"]
            for task_json in tasks_local:
                task = Task(**task_json)
                tasks.append(task)
        return cls(tasks=tasks)
    
    def __len__(self):
        return len(self.tasks)

    def save_local(self, filepath="task.json"):
        out = []
        with open(filepath, "w") as f:
            for task in self.tasks:
                task_json = task.to_json()
                out.append(task_json)
            f.write(json.dumps({"task":out}, ensure_ascii=False))

    def add(self, task):
        self.tasks.append(task)

    def to_sort_fmt(self):
        return "\n".join(f"{i+1}. {task.describe()}" for i, task in enumerate(self.tasks))

    def to_list_fmt(self):
        return "\n".join(f"{i+1}. {task.describe_ui()}" for i, task in enumerate(self.tasks))
        
class Task:
    def __init__(self, title, comment, push_time=None, done_time=None):
        self.title = title
        self.comment = comment
        if not push_time:
            self.push_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
        else:
            self.push_time = push_time
        self.done_time = done_time

    def describe(self):
        time = datetime_to_describe(self.push_time)
        return f"タスク内容:{self.title}/いつまでにやりたいか:{self.comment}/登録日時{time}"

    def describe_ui(self):
        time = datetime_to_describe(self.push_time)
        return f"{time}: {self.comment}-{self.title}"
    
    def to_json(self):
        return {"title":self.title, 
                "push_time":self.push_time,
                "comment":self.comment}
# def main():
#     llm = OpenAI(temperature=0, model="text-davinci-003")
#     template="""
#     あなたは私の秘書です。今私のタスクは次のようになっています。私のタスクに優先度の高い順番に並び替えてください。

#     例
#     現在のタスクのPython list: ["テスト勉強をする", "ドレッシングを買いに行く", "中期の目標を立てる。"]
#     並び替えた後のタスク:
#     中期の目標を立てる。
#     テスト勉強をする
#     ドレッシングを買いに行く

#     現在の実行
#     現在のタスクのPython list: {tasks}
#     並び替えた後のタスク:
#     """
#     prompt = PromptTemplate(template=template, 
#                             input_variables=["tasks"])
#     with open("task.json") as f:
#         task = json.load(f)["task"]
#     bot = LLMChain(llm=llm, prompt=prompt, verbose=True)
#     sorted_tasks = bot.predict(tasks=str(task))
#     sorted_tasks = sorted_tasks.split("\n")[1:]

#     # with open("sorted_task.json", "w") as f:
#     #     f.write(json.dumps({"task":sorted_tasks}, ensure_ascii=False))

# main()