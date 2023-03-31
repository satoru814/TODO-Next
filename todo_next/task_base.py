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

    def remove(self, index):
        del self.tasks[index]
    def to_sort_fmt(self):
        return "\n".join(f"{i+1}. {task.describe()}" for i, task in enumerate(self.tasks))

    def to_list_fmt(self):
        return "\n".join(f"{i+1}. {task.describe_ui()}" for i, task in enumerate(self.tasks))
        
class Task:
    def __init__(self, task_title, comment="", start_time=None, done_time=None):
        self.title = task_title
        self.comment = comment
        if not start_time:
            self.push_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
        else:
            self.push_time = start_time
        self.done_time = done_time

    def describe(self):
        time = datetime_to_describe(self.push_time)

        if not self.comment:
            return f"タスク内容:{self.title}/登録日時{time}"    
        return f"タスク内容:{self.title}/いつまでにやりたいか:{self.comment}/登録日時{time}"

    def describe_ui(self):
        time = datetime_to_describe(self.push_time)
        return f"{time}: {self.comment}-{self.title}"
    
    def to_json(self):
        return {"task_title":self.title, 
                "start_time":self.push_time,
                "comment":self.comment}
    
    def is_done(self):
        self.done_time = datetime.datetime.now()
        self.push_time = datetime.datetime(*[int(t) for t in self.push_time.split("-")])
        return {"task_title":self.title, 
                "start_time":self.push_time,
                "done_time":self.done_time,
                "comment":self.comment}
    