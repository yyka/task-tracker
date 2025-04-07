# task-tracker
Simple Task Tracker CLI app, built in Python.

For more info: https://roadmap.sh/projects/task-tracker

Usage: `task-tracker.py [-h] {add,delete,update,mark-in-progress,mark-done,list} ...`

>```py
> # show a list of commands
> task-tracker.py --help
>
> # add a new task
> task-tracker.py add [description]
>
> # list all tasks
> task-tracker.py list (todo|in-progress|done)
>
> # delete a task
> task-tracker.py delete [id]
>
> # update the description of a task
> task-tracker.py update [id] [new_description]
>
> # update the status of a task
> task-tracker.py mark-[in-progress|done] [id]


The code is currently very messy, I'll update it in the next few days.