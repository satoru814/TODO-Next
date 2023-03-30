import datetime
import json
from todo_next.utils import datetime_to_describe

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