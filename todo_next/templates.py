from langchain import PromptTemplate


def sort_template():
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
    return template

def done_template():
    template="""
    あなたはユーザーのことをよく知る友人です。
    今ユーザーは{task_title}をしました。
    まずあなたは1,2のどちらかを選んでください。
    以下に示す選んだ数字の指示に従うような、友好的な発話内容を出力をしてください
    例: 
    なんで{task_title}したの？　大変だった？
    おめでとう, また頑張ろう!

    1. なぜ{task_title}をおこなったのか背景などを聞いて友好関係を深める
    2. {task_title}をおこなったことをとにかく称賛してやる気を上げる
    出力:
    """
    return template

def qa_template():
    template="""
    あなたは私の秘書です。今私のタスクは次のようになっています。
    各タスクは
    タスク番号. タスク内容/いつまでにやりたいか/登録日時
    のように与えられています。
    
    現在の日時は{now}です。
    {tasks}

    それを踏まえて以下の質問に回答してください
    質問:{question}
    出力:
    """
    return template

def db_template():
    template = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Answer should be 
    Use the following format:

    Question: "Question here"
    SQLQuery: "SQL Query to run"
    SQLResult: "Result of the SQLQuery"
    Answer: "Final answer here"

    Only use the following tables:

    {table_info}

    Question: {input}"""
    return template

def gen_template():
    template = """あなたはコンサルタントです。
    以下のタスクを参考にして次のタスクを提案してください:
    タスク: {task}

    回答:
    """
    return template