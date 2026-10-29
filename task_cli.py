
import sys
import json
from pathlib import Path
from datetime import datetime

TASKS_FILE = Path(__file__).parent / "tasks.json"


def load_tasks():
    if not TASKS_FILE.exists():
        TASKS_FILE.write_text("[]", encoding="utf-8")

    try:
        return json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("Error: tasks.json contains invalid JSON.")
        sys.exit(1)


def save_tasks(tasks):
    TASKS_FILE.write_text(
        json.dumps(tasks, indent=4),
        encoding="utf-8"
    )


def current_time():
    return datetime.now().isoformat(timespec="seconds")


def add_task(description):
    tasks = load_tasks()
    task_id = max((t["id"] for t in tasks), default=0) + 1
    now = current_time()

    task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }

    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")


def list_tasks(status=None):
    tasks = load_tasks()

    if status:
        tasks = [t for t in tasks if t["status"] == status]

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print(
            f'ID: {task["id"]} | {task["description"]} | '
            f'{task["status"]}'
        )


def update_task(task_id, description):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = current_time()
            save_tasks(tasks)
            print(f"Task updated successfully (ID: {task_id})")
            return

    print(f"Task with ID {task_id} not found.")


def delete_task(task_id):
    tasks = load_tasks()
    updated_tasks = [t for t in tasks if t["id"] != task_id]

    if len(tasks) == len(updated_tasks):
        print(f"Task with ID {task_id} not found.")
        return

    save_tasks(updated_tasks)
    print(f"Task deleted successfully (ID: {task_id})")


def mark_task(task_id, status):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = current_time()
            save_tasks(tasks)
            print(f"Task marked as {status} (ID: {task_id})")
            return

    print(f"Task with ID {task_id} not found.")


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: python task_cli.py <command> [arguments]")
        return

    command = args[0]
    if command in ("--help", "-h", "help"):
        print('Commands: add, list, update, delete, mark-in-progress, mark-done')
        return

    if command in ("--help", "-h", "help"):
        print("""
            Task Tracker CLI

            Commands:
            add "description"
            list [todo|in-progress|done]
            update <id> "new description"
            delete <id>
            mark-in-progress <id>
            mark-done <id>
            """)
        return

    if command == "add":
        if len(args) < 2 or not " ".join(args[1:]).strip():
            print('Usage: python task_cli.py add "Task description"')
            return
        add_task(" ".join(args[1:]).strip())

    elif command == "list":
        if len(args) == 1:
            list_tasks()
        elif len(args) == 2 and args[1] in (
            "done", "todo", "in-progress"
        ):
            list_tasks(args[1])
        else:
            print("Usage: python task_cli.py list [done|todo|in-progress]")

    elif command == "update":
        if len(args) < 3 or not " ".join(args[2:]).strip():
            print('Usage: python task_cli.py update <id> "New description"')
            return
        try:
            update_task(int(args[1]), " ".join(args[2:]).strip())
        except ValueError:
            print("Error: Task ID must be a number.")

    elif command == "delete":
        if len(args) != 2:
            print("Usage: python task_cli.py delete <id>")
            return
        try:
            delete_task(int(args[1]))
        except ValueError:
            print("Error: Task ID must be a number.")

    elif command in ("mark-in-progress", "mark-done"):
        if len(args) != 2:
            print(f"Usage: python task_cli.py {command} <id>")
            return
        try:
            status = "in-progress" if command == "mark-in-progress" else "done"
            mark_task(int(args[1]), status)
        except ValueError:
            print("Error: Task ID must be a number.")

    else:
        print("Unknown command.")


if __name__ == "__main__":
    main()
