import ast
import datetime
import json
from langchain import LLMChain, OpenAI, PromptTemplate


def get_now():
    return str(datetime.datetime.now())
    
def task_push():
    new_task = input("Hi! What's your task:\n")
    comment = input("""I got it! You can write comment(exp. tomorrow night is deadline, This is difficult and so on)\n""")
    now = get_now()
    task_describe = f"Task title:{new_task}/User comment:{comment}/Push time:{now}"

    with open("task.json", "r") as f:
        current_tasks = json.load(f)["task"]
    current_tasks.append(task_describe)
    sorted_tasks = sort_task(current_tasks)
    with open("task.json", "w") as f:
        f.write(json.dumps({"task":sorted_tasks}, ensure_ascii=False))

    
def sort_task(tasks):
    llm = OpenAI(temperature=0, model="text-davinci-003")
    template="""
    あなたは私の秘書です。今私のタスクは次のようになっています。
    現在の日付と時刻は{now}です。
    各タスクの重要度や作業時間などを考慮して優先度の高い順番に並び替えてください。
    Task titleはタスクの内容を示しています。
    User commentはユーザーがそのタスクについて考えていることです。
    Push timeはユーザーがそのタスクを登録した時刻です。

    例
    現在のタスクのPython list: ["テスト勉強をする", "ドレッシングを買いに行く", "中期の目標を立てる。"]
    並び替えた後のタスク:
    中期の目標を立てる。
    テスト勉強をする
    ドレッシングを買いに行く

    現在の実行
    現在のタスクのPython list: {tasks}
    並び替えた後のタスク:
    """
    prompt = PromptTemplate(template=template, 
                            input_variables=["tasks", "now"])
    bot = LLMChain(llm=llm, prompt=prompt, verbose=True)
    sorted_tasks = bot.predict(tasks=str(tasks), now=get_now())
    sorted_tasks = sorted_tasks.split("\n")[1:]
    print(sorted_tasks)
    return sorted_tasks

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