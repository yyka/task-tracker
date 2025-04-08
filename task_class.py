from datetime import datetime
import json
import os


class Task:
    json_db_file = "tasks.json"

    def __init__(self, id=None, description="unnamed", status="todo", createdAt=None, updatedAt=None):
        # id
        if id is None:
            self._id = Task._generate_id()
        else:
            self._id = id
        # description
        self._description = str(description)
        # status
        if status not in ("todo", "in-progress", "done"):
            raise ValueError("Invalid status. Try: todo|in-progress|done")
        self._status = status
        # createdAt
        if createdAt is None:
            self._createdAt = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S")
        else:
            self._createdAt = createdAt
        # updatedAt
        if updatedAt is None:
            self._updatedAt = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S")
        else:
            self._updatedAt = updatedAt

    def __repr__(self):
        return f"{json.dumps(self.json, indent=4)}"

    def __str__(self):
        string = (f"#{self.id} | created: {self.createdAt} | updated: {self.updatedAt}"
                  f" | \"{self.description}\" ({self.status.upper()})")
        return string

    @property
    def id(self):
        return self._id

    @property
    def description(self):
        return self._description

    @property
    def status(self):
        return self._status

    @property
    def createdAt(self):
        return self._createdAt

    @property
    def updatedAt(self):
        return self._updatedAt

    @classmethod
    def _generate_id(cls):
        '''
        Fetch and increment global_id from database
        '''
        data = Task.fetch_db()
        data["global_id"] = data["global_id"] + 1
        Task.write_db(data)
        
        return data["global_id"]
    
    def to_json(self):
        '''
        Convert Task object data to a json string
        '''
        data = {"id": self.id,
                "description": self.description,
                "status": self.status,
                "createdAt": self.createdAt,
                "updatedAt": self.updatedAt,
                }
        return data    

    @classmethod
    def fetch_db(cls):
        '''
        Returns the json database as a python object
        '''
        # Check if file exists; set data value to None if not
        if not os.path.exists(Task.json_db_file):
            data = None
            with open(Task.json_db_file, "w", encoding="utf-8") as f:
                json.dump(data, f)
        # Load file data to a variable
        with open(Task.json_db_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        # If no existing data, set a default value
        if data is None:
            data = json.loads('{"global_id": 0, "tasks": []}')
        return data

    @classmethod
    def fetch_task(cls, id):
        '''
        Retrieve and return Task object from the database
        '''
        data = Task.fetch_db()
        for task in data["tasks"]:
            if task["id"] == id:
                args = [task["id"], task["description"], task["status"],
                        task["createdAt"], task["updatedAt"]]
                return Task(*args)
        else:
            return print("Task not found")  

    @classmethod
    def format_json(cls, data):
        '''
        Format task json data
        '''
        string = (f"#{data["id"]} | created: {data["createdAt"]} | updated: {data["updatedAt"]}"
                  f" | \"{data["description"]}\" ({data["status"].upper()})")
        return string
    
    @classmethod
    def to_task(cls, json):
        '''
        Convert json string to Task object
        '''
        args = [json["id"], json["description"], json["status"],
                json["createdAt"], json["updatedAt"]]
        return Task(*args)
    
    @classmethod
    def write_db(cls, data):
        '''
        Write json data string to database
        '''
        with open(Task.json_db_file, "w", encoding="utf-8") as f:
            json.dump(data, f)