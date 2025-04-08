import argparse
import sys
from datetime import datetime
from task_class import Task


def parse_args():
    parser = argparse.ArgumentParser(
        description="task-tracker: a CLI app to manage your to-do-list."
    )
    subparsers = parser.add_subparsers(
        title="subcommands", dest="subparser_name", required=True
    )
    
    # add
    parser_add = subparsers.add_parser("add", help="add a new task")
    parser_add.add_argument("description", type=str)
    
    # delete
    parser_delete = subparsers.add_parser("delete", help="delete an existing task")
    parser_delete.add_argument("id", type=int)
    
    # update
    parser_update = subparsers.add_parser("update", help="update an existing task")
    parser_update.add_argument("id", type=int)
    parser_update.add_argument("description", type=str)
    
    # mark in-progress
    parser_mark_progress = subparsers.add_parser(
        "mark-in-progress", help="mark a task as \"in progress\""
    )
    parser_mark_progress.add_argument("id", type=int)
    
    # mark done
    parser_mark_done = subparsers.add_parser("mark-done", help="mark a task as \"done\"")
    parser_mark_done.add_argument("id", type=int)
    
    # list
    parser_list = subparsers.add_parser("list", help="list all tasks")
    parser_list.add_argument("status", nargs="?", choices=["todo", "in-progress", "done"])

    return parser.parse_args()


def main():
    args = parse_args()
    match args.subparser_name:
        case "add":
            add_task(args.description)
        case "delete":
            delete_task(args.id)
        case "update":
            update_task(args.id, "description", args.description)
        case "mark-in-progress":
            update_task(args.id, "status", "in-progress")
        case "mark-done":
            update_task(args.id, "status", "done")
        case "list":
            list_tasks(args.status)


def add_task(desc):
    '''
    Add task to database
    '''
    task = Task(description=desc)
    data = Task.fetch_db()
    data["tasks"].append(task.to_json())
    Task.write_db(data)
    print(f"Task added:\n{task}")


def delete_task(id):
    '''
    Delete task from database
    '''
    data = Task.fetch_db()
    
    for index, task in enumerate(data["tasks"]):
        if task["id"] == id:
            task_json = task
            task_json["updatedAt"] = (
                datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S")
                )   # Set updatedAt to current time
            del data["tasks"][index]
            Task.write_db(data)
            print(f"Task deleted:\n{Task.format_json(task_json)}")
            break
    else:
        print("Task not found")
        
    
def update_task(id, property, new_value):
    """
    Update task in database
    """
    data = Task.fetch_db()
    
    for index, task in enumerate(data["tasks"]):
        if task["id"] == id:
            data["tasks"][index][property] = new_value
            data["tasks"][index]["updatedAt"] = (
                datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S")
                )   # Set updatedAt to current time
            task_json = task
            Task.write_db(data)
            print(f"Task updated:\n{Task.format_json(task_json)}")
            break
    else:
        print("Task not found")


def list_tasks(status=None):
    tasks = Task.fetch_db()["tasks"]
    i = 0
    
    if status is None:
        for task in tasks:
            print(Task.format_json(task))
            i += 1
    else:
        for task in tasks:
            if task["status"] == status:
                print(Task.format_json(task))
                i += 1
    
    if i == 0:
        print("No tasks found")
        

if __name__ == "__main__":
    main()
