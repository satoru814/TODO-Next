import ast
import os

import sys

from langchain import LLMChain, OpenAI, PromptTemplate, SQLDatabaseChain
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from todo_next.templates import sort_template, done_template, qa_template, db_template, gen_template
from todo_next.task_base import Task, TaskItems
from todo_next.utils import datetime_to_describe, getnow
from todo_next.db import DB



class TaskAgent:
    def __init__(self, task_path="task.json", db_path="sqlite:///old_task.db"):
        if os.path.isfile(task_path):
            self.taskitems = TaskItems.load_local()
        else:
            self.taskitems = TaskItems()
        if os.path.isfile(db_path):
            self.db = DB.load_local(filepath=db_path)
        else:
            self.db = DB()

    def task_list(self):
        print(self.taskitems.to_list_fmt(), sys.stdout)
        
    def task_sort(self):
        self.sort_task()
        self.taskitems.save_local()

    def task_push(self):
        new_task = input("Hi! What's your task:\n")
        comment = input(
        """I got it! You can write comment(exp. tomorrow night is deadline, 
        This is difficult and so on)\n"""
        )
        task = Task(task_title=new_task, comment=comment)
        self.taskitems.add(task)
        self.sort_task()
        self.taskitems.save_local()

    def sort_task(self):
        llm = OpenAI(temperature=0, model="text-davinci-003")
        prompt = PromptTemplate(template=sort_template(), 
                                input_variables=["tasks", "tasks_num", "now"])
        bot = LLMChain(llm=llm, prompt=prompt, verbose=True)
        gpt_tasks = ""
        gpt_tasks = self.taskitems.to_sort_fmt()
        now = getnow()
        now = datetime_to_describe(now)
        sorted_number = bot.predict(tasks=str(gpt_tasks), 
                                    now=now, 
                                    tasks_num=len(self.taskitems))
        sorted_number = ast.literal_eval(sorted_number)
        sorted_tasks = []
        for i in sorted_number:
            sorted_tasks.append(self.taskitems.tasks[int(i)-1])
        self.taskitems = TaskItems(sorted_tasks)

    def search_tasks(self, task):
        embeddings = OpenAIEmbeddings()
        db = FAISS.load_local("old_tasks", embeddings)
        docs = db.similarity_search(task.describe())
        return docs.page_content

    def store_tasks(self, task):
        embeddings = OpenAIEmbeddings()
        db = FAISS.load_local("old_tasks", embeddings)
        db.add_texts([task.describe()])
        db.save_local("old_tasks")

    def task_done(self):
        self.task_list()
        done_num = input("which task did you done\n")
        task = self.taskitems.tasks[int(done_num)-1]
        self.db.add(task.is_done())
        self.taskitems.remove(int(done_num)-1)

        llm = OpenAI(temperature=1, model="text-davinci-003")
        prompt = PromptTemplate(template=done_template(), 
                                input_variables=["task_title"])
        bot = LLMChain(llm=llm, prompt=prompt, verbose=True)
        ans = bot.predict(task_title=task.title)
        self.taskitems.save_local()
        return ans
        # store_tasks(task)

    def task_qa(self):
        self.task_list()
        question = input("input your question about your tasks\n")
        llm = OpenAI(temperature=0, model="text-davinci-003")
        prompt = PromptTemplate(template=qa_template(), 
                                input_variables=["tasks", "question", "now"])
        bot = LLMChain(llm=llm, prompt=prompt, verbose=True)
        now = getnow()
        now = datetime_to_describe(now)
        ans = bot.predict(question=question, 
                          tasks=self.taskitems.to_sort_fmt(), 
                          now=now)
        print(ans)

    def db_sarch(self):
        query = input("過去のタスクについて調べたいことを雑に聞いてください\n")
        prompt = PromptTemplate(
            input_variables=["input", "table_info", "dialect"], template=db_template()
        )
        sql_chain = SQLDatabaseChain(
            llm=OpenAI(temperature=0),
            database = self.db.to_langchain_db(),
            prompt = prompt,
            verbose=True,
            return_intermediate_steps=True
        )
        ans = sql_chain(query)["result"]
        return ans
    
    def gen(self):
        self.task_list()
        gen_num = input("新たな何番のタスクを参考にしてタスクを設定しますか？")
        llm = OpenAI(temperature=1, model="text-davinci-003")
        prompt = PromptTemplate(template=gen_template(), 
                                input_variables=["task"])
        bot = LLMChain(llm=llm, prompt=prompt, verbose=True)
        task = self.taskitems.tasks[int(gen_num)-1]
        suggest_task = bot.predict(task=task.title)
        yes_no = input(f"{suggest_task}とかどうでしょう？  [y/n]")
        if yes_no == "y":
            task = Task(task_title=suggest_task)
            self.taskitems.add(task)
            self.sort_task()
            self.taskitems.save_local()
            return "満足してもらえてよかったです😃　　タスクリストに追加しました"
        else:
            suggest_task = bot.predict(task=task.title)
            yes_no = input(f"これは！？{suggest_task}  [y/n]")
            if yes_no == "y":
                task = Task(task_title=suggest_task)
                self.taskitems.add(task)
                self.sort_task()
                self.taskitems.save_local()
                return "満足してもらえてよかったです😃　タスクリストに追加しました"
            
        return "次こそは満足させます。"

def push():
    TaskAgent().task_push()
    print("追加しましたー")

def list():
    TaskAgent().task_list()
    print("こちらリストですー")

def sort():
    TaskAgent().sort_task()
    print("優先順位変えましたー")

def done():
    ans = TaskAgent().task_done()
    print(ans)

def qa():
    ans = TaskAgent().task_qa()
    print(ans)

def old_qa():
    ans = TaskAgent().db_sarch()
    print(ans)

def gen():
    ans = TaskAgent().gen()
    print(ans)