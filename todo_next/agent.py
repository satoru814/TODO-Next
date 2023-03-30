import ast
import datetime
import json
from langchain import LLMChain, OpenAI, PromptTemplate


def get_now():
    time = datetime.datetime.now()
    return time.strftime('%Y年%m月%d日 %H時%M分')

def task_list():
    with open("task.json", "r") as f:
        tasks = json.load(f)["task"]
        tasks = "\n".join(tasks)
    print(tasks)


def task_sort():
    with open("task.json", "r") as f:
        tasks = json.load(f)["task"]
        sorted_tasks = sort_task(tasks)
    with open("task.json", "w") as f:
        f.write(json.dumps({"task":sorted_tasks}, ensure_ascii=False))



def task_push():
    new_task = input("Hi! What's your task:\n")
    comment = input("""I got it! You can write comment(exp. tomorrow night is deadline, This is difficult and so on)\n""")
    now = get_now()
    task_describe = f"タスク内容:{new_task}/いつまでにやりたいか:{comment}/登録日時{now}"

    with open("task.json", "r") as f:
        current_tasks = json.load(f)["task"]
    current_tasks.append(task_describe)
    sorted_tasks = sort_task(current_tasks)
    with open("task.json", "w") as f:
        f.write(json.dumps({"task":sorted_tasks}, ensure_ascii=False))


    
def sort_task(tasks):
    llm = OpenAI(temperature=0, model="text-davinci-003")
    template="""
    現在の日時は{now}です。
    あなたは私の秘書です。今私のタスクは次のようになっています。
    各タスクは
    タスク番号. タスク内容/いつまでにやりたいか/登録日時
    のように与えられています。
    
    {tasks}

    各タスクの重要度、登録日時、現在の日時、コメントなどを総合的に評価して優先度の高い順番に並び替えて出力してください。
    出力する際には以下に示す例のようにタスク番号を出力してください。
    例: [1,3,5,4,2]

    出力する際には以下の制約を守ってください
    1. 1~{tasks_num}までの番号を１回づつ出力する

    では始めてください
    出力:
    """
    prompt = PromptTemplate(template=template, 
                            input_variables=["tasks", "tasks_num", "now"])
    bot = LLMChain(llm=llm, prompt=prompt, verbose=True)
    gpt_tasks = ""
    for i, task in enumerate(tasks):
        gpt_tasks += f"{i+1}. {task}\n"
    sorted_number = bot.predict(tasks=str(gpt_tasks), now=get_now(), tasks_num=len(tasks))
    sorted_number = ast.literal_eval(sorted_number)
    sorted_tasks = []
    for i in sorted_number:
        sorted_tasks.append(tasks[int(i)-1])
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