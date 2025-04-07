import argparse
import sys
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
            task = Task(args.description)
            print(f"Task added:\n{task}")
        case "delete":
            is_in_db(args.id)
            task = Task.db_get_task(args.id)
            Task.db_task_delete(args.id)
            print(f"Task deleted:")
            Task.db_print(task)
        case "update":
            is_in_db(args.id)
            Task.db_task_update(args.id, "description", args.description)
            print(f"Task updated:")
            Task.db_print(Task.db_get_task(args.id))
        case "mark-in-progress":
            is_in_db(args.id)
            Task.db_task_update(args.id, "status", "in-progress")
            print(f"Task updated:")
            Task.db_print(Task.db_get_task(args.id))
        case "mark-done":
            is_in_db(args.id)
            Task.db_task_update(args.id, "status", "done")
            print(f"Task updated:")
            Task.db_print(Task.db_get_task(args.id))
        case "list":
            Task.db_list(args.status)

# FIx spaghetti : each function returns the old/new task so you can get directly pass the return value db_print


def is_in_db(id):
    if not Task.db_get_task(id):
        sys.exit("Task does not exist")
        

if __name__ == "__main__":
    main()
