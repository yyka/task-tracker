# task-tracker
Simple Task Tracker CLI app, built in Python.

For more info: https://roadmap.sh/projects/task-tracker

Usage: `task-tracker.py [-h] {add,delete,update,mark-in-progress,mark-done,list} ...`

```md
# show a list of commands
task-tracker.py --help

# add a new task
task-tracker.py add [description]

# delete a task
task-tracker.py delete [id]

# update the description of a task
task-tracker.py update [id] [new_description]

# update the status of a task
task-tracker.py mark-[in-progress|done] [id]

# list all tasks
task-tracker.py list (todo|in-progress|done)
```

<details>
<summary>Personal notes</summary>
<ul>
    <li> This was my first project done outside of CS50 and CS50P
    <li> Total time taken: 15h
</ul>
</details>