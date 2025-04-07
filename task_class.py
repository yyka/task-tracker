from datetime import datetime
import json
import os


class Task:
    json_db_file = "tasks.json"

    def __init__(self, description="unnamed", status="todo"):
        self.id = Task.global_id(incr=True)
        self.description = description
        self.status = status
        self.createdAt = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S")
        self.updatedAt = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S")
        self.json = {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }

        Task.db_task_add(self)

    def __repr__(self):
        return f"{json.dumps(self.json, indent=4)}"

    def __str__(self):
        string = (f"#{self.id} | created: {self.createdAt} | updated: {self.updatedAt}"
                  f" | \"{self.description}\" ({self.status.upper()})")
        return string

    @classmethod
    def db_init(cls):
        if not os.path.exists(Task.json_db_file):
            data = json.loads('{"global_id": 0, "tasks": []}')
            with open(Task.json_db_file, "w", encoding="utf-8") as f:
                json.dump(data, f)

        with open(Task.json_db_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if data == None:
            data = json.loads('{"global_id": 0, "tasks": []}')

        return data

    @classmethod
    def global_id(cls, incr=False):
        data = Task.db_init()

        if incr == True:
            data["global_id"] = data["global_id"] + 1
            with open(Task.json_db_file, "w", encoding="utf-8") as f:
                json.dump(data, f)

        return data["global_id"]

    @classmethod
    def db_task_add(cls, self):
        data = Task.db_init()

        data["tasks"].append(self.json)

        with open(Task.json_db_file, "w", encoding="utf-8") as f:
            json.dump(data, f)

    @classmethod
    def db_task_delete(cls, task_id):
        data = Task.db_init()

        for index, task in enumerate(data["tasks"]):
            if task["id"] == task_id:
                del data["tasks"][index]
                break

        with open(Task.json_db_file, "w", encoding="utf-8") as f:
            json.dump(data, f)

    @classmethod
    def db_task_update(cls, task_id, task_property, new_value):
        """
        For task_id, updates task_property to new_value
        """
        data = Task.db_init()

        for index, task in enumerate(data["tasks"]):
            if task["id"] == task_id:
                data["tasks"][index][task_property] = new_value
                data["tasks"][index]["updatedAt"] = (
                    datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S")
                    )
                break

        with open(Task.json_db_file, "w", encoding="utf-8") as f:
            json.dump(data, f)
            
    @classmethod
    def db_list(cls, status=None):
        data = Task.db_init()
        tasks = data["tasks"]
        
        if status == None:
            list = tasks
        else:
            list = [task for task in tasks if task["status"] == status]

        Task.db_print(list)
                    
    @classmethod
    def db_print(cls, task_obj):
        '''Prints task(s) passed as argument'''
        if isinstance(task_obj, list):
            for task in task_obj:
                print(f"#{task["id"]} | created: {task["createdAt"]} | updated: {task["updatedAt"]}"
                    f" | \"{task["description"]}\" ({task["status"].upper()})")
        elif isinstance(task_obj, dict):
            print(f"#{task_obj["id"]} | created: {task_obj["createdAt"]} | updated: {task_obj["updatedAt"]}"
                  f" | \"{task_obj["description"]}\" ({task_obj["status"].upper()})")
        else:
            pass

    @classmethod
    def db_get_task(cls, task_id):
        data = Task.db_init()
        value = None
        
        for index, task in enumerate(data["tasks"]):
            if task["id"] == task_id:
                value = data["tasks"][index]
                break
            
        return value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        if not isinstance(new_id, int):
            raise ValueError("Invalid id: not an integer")
        self._id = new_id

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_desc):
        self._description = str(new_desc)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        if new_status not in ("todo", "in-progress", "done"):
            raise ValueError("Invalid status. Try: todo|in-progress|done")
        self._status = new_status

    @property
    def createdAt(self):
        return self._createdAt

    @createdAt.setter
    def createdAt(self, new_datetime):
        self._createdAt = new_datetime

    @property
    def updatedAt(self):
        return self._updatedAt

    @updatedAt.setter
    def updatedAt(self, new_datetime):
        self._updatedAt = new_datetime

    @property
    def json(self):
        return self._json

    @json.setter
    def json(self, new_json):
        self._json = new_json
