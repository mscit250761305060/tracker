# Task Tracker CLI

A simple command-line application built with Python to manage daily tasks. Tasks are stored locally in a JSON file.

## Requirements
- Python 3
- No external libraries required

## How to Run

Open the terminal in the project directory.

### Add a Task
```bash
python task_cli.py add "Study Python"
```

### List Tasks
```bash
python task_cli.py list
python task_cli.py list todo
python task_cli.py list in-progress
python task_cli.py list done
```

### Update a Task
```bash
python task_cli.py update 1 "Practice Python"
```

### Delete a Task
```bash
python task_cli.py delete 1
```

### Change Task Status
```bash
python task_cli.py mark-in-progress 1
python task_cli.py mark-done 1
```

### Show Help
```bash
python task_cli.py --help
```

## Storage

Tasks are stored in `tasks.json`. Each task contains an ID, description, status, creation timestamp, and last-updated timestamp.

## Available Statuses
- `todo`
- `in-progress`
- `done`

## Project URL

https://roadmap.sh/projects/task-tracker
