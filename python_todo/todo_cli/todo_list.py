import click
import json
import os

todo_file = "todo.json"

def load_todos():
    """Load todos from file."""
    if os.path.exists(todo_file):
        with open(todo_file, "r") as f:
            return json.load(f)
    return []  

def save_tasks(tasks):
    """Save tasks to file."""
    with open(todo_file, "w") as f:
        json.dump(tasks, f, indent=4)

@click.group()
def cli():
    """Simple Todo List CLI"""
    pass

@cli.command()
@click.argument("task")
def add(task):
    """Add a new task to the todo list."""
    tasks = load_todos()
    tasks.append({"task": task, "done": False})
    save_tasks(tasks)
    click.echo(f"Task added successfully: {task}")

@cli.command()
def list():
    """List all tasks"""
    tasks = load_todos()
    if not tasks:
        click.echo("No tasks found.")
        return
    
    for idx, task in enumerate(tasks, start=1):
        status = "✅" if task["done"] else "❌"
        click.echo(f"{idx}. {task['task']} [{status}]")

@cli.command()
@click.argument("task_number", type=int)
def complete(task_number):
    """Mark a task as completed."""
    tasks = load_todos()
    if 0 < task_number <= len(tasks):
        tasks[task_number - 1]["done"] = True
        save_tasks(tasks)
        click.echo(f"Task {task_number} marked as completed ✅")
    else:
        click.echo(f"Invalid task number: {task_number}")

@cli.command()
@click.argument("task_number", type=int)
def remove(task_number):
    """Remove a task from the list"""
    tasks = load_todos()
    if 0 < task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        click.echo(f"Task '{removed_task['task']}' removed successfully")
    else:
        click.echo(f"Invalid task number: {task_number}")

if __name__ == "__main__":
    cli()
