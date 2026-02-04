#!/usr/bin/env python3
"""
Interactive CLI Todo Application
Phase I - Hackathon Project

A professional console-based todo manager with rich interactive menus,
arrow-key navigation, and JSON persistence.
"""

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import copy

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box


# ============================================================================
# User Story 4: Error Recovery - Validation (T025, T026)
# ============================================================================

def validate_title(title: str) -> tuple[bool, str]:
    """Validate todo title (T025)."""
    if not title or not title.strip():
        return False, "Title cannot be empty"
    if len(title) > 200:
        return False, "Title must be 200 characters or less"
    return True, ""


def validate_description(description: str) -> tuple[bool, str]:
    """Validate todo description (T025)."""
    if len(description) > 1000:
        return False, "Description must be 1000 characters or less"
    return True, ""


def validate_category(category: str) -> tuple[bool, str]:
    """Validate todo category (T025)."""
    if len(category) > 50:
        return False, "Category must be 50 characters or less"
    return True, ""


def show_error(message: str):
    """Display error message in a panel (T026)."""
    console.print(Panel(
        f"[bold red]Error:[/bold red] {message}",
        border_style="red",
        padding=(0, 1)
    ))


# ============================================================================
# Data Models (T005)
# ============================================================================

@dataclass
class Todo:
    """Todo item with all required fields."""
    id: str
    title: str
    description: str = ""
    category: str = ""
    completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Todo':
        """Create Todo from dictionary."""
        return cls(**data)


# ============================================================================
# Application State (T007)
# ============================================================================

class AppState:
    """Manages application state including todos and undo history."""

    def __init__(self):
        self.todos: List[Todo] = []
        self.undo_stack: List[List[Todo]] = []
        self.max_undo_levels = 10

    def save_state_for_undo(self):
        """Save current state to undo stack before mutation."""
        # Deep copy current todos
        state_snapshot = copy.deepcopy(self.todos)
        self.undo_stack.append(state_snapshot)

        # Limit undo stack size
        if len(self.undo_stack) > self.max_undo_levels:
            self.undo_stack.pop(0)

    def undo(self) -> bool:
        """Restore previous state from undo stack."""
        if not self.undo_stack:
            return False

        self.todos = self.undo_stack.pop()
        return True


# ============================================================================
# JSON Persistence (T006)
# ============================================================================

STORAGE_FILE = Path("todos.json")


def load_todos() -> List[Todo]:
    """Load todos from JSON file with error handling."""
    if not STORAGE_FILE.exists():
        return []

    try:
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            todos_data = data.get('todos', [])
            return [Todo.from_dict(todo) for todo in todos_data]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        # Backup corrupted file
        if STORAGE_FILE.exists():
            backup_file = STORAGE_FILE.with_suffix('.json.backup')
            STORAGE_FILE.rename(backup_file)
            console.print(f"[yellow]Warning: Corrupted file backed up to {backup_file}[/yellow]")
        return []
    except Exception as e:
        console.print(f"[red]Error loading todos: {e}[/red]")
        return []


def save_todos(todos: List[Todo]) -> bool:
    """Save todos to JSON file with atomic writes."""
    try:
        # Prepare data
        data = {
            "version": "1.0",
            "todos": [todo.to_dict() for todo in todos]
        }

        # Write to temporary file first (atomic write pattern)
        temp_file = STORAGE_FILE.with_suffix('.json.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Atomic rename
        temp_file.replace(STORAGE_FILE)
        return True
    except Exception as e:
        console.print(f"[red]Error saving todos: {e}[/red]")
        return False


# ============================================================================
# Rich Console Setup (T008)
# ============================================================================

console = Console()


def display_header():
    """Display application header."""
    console.print()
    console.print(Panel.fit(
        "[bold cyan]Interactive CLI Todo Application[/bold cyan]\n"
        "[dim]Phase I - Hackathon Project[/dim]",
        border_style="cyan"
    ))
    console.print()


# ============================================================================
# Main Menu Display (T009)
# ============================================================================

MENU_OPTIONS = [
    "Add todo",
    "List all todos",
    "Search todos",
    "Filter todos by category",
    "Complete todo",
    "Mark todo as incomplete",
    "Update todo",
    "Delete todo",
    "Undo last action",
    "Help",
    "Exit"
]


def display_menu() -> str:
    """Display main menu and get user selection."""
    console.print("\n[bold]Main Menu:[/bold]")

    # Display menu options
    for i, option in enumerate(MENU_OPTIONS, 1):
        console.print(f"  {i}. {option}")

    console.print()

    # Get user choice
    while True:
        choice = Prompt.ask(
            "Select an option",
            choices=[str(i) for i in range(1, len(MENU_OPTIONS) + 1)]
        )
        return MENU_OPTIONS[int(choice) - 1]


# ============================================================================
# User Story 1: New User Experience (T010, T011)
# ============================================================================

def add_todo(state: AppState):
    """Add a new todo item (T010) with validation (T028)."""
    console.print("\n[bold cyan]Add New Todo[/bold cyan]\n")

    # Collect and validate title (required)
    while True:
        title = Prompt.ask("Title (required)")
        is_valid, error_msg = validate_title(title)
        if is_valid:
            break
        show_error(error_msg)

    # Collect and validate description (optional)
    while True:
        description = Prompt.ask("Description (optional)", default="")
        is_valid, error_msg = validate_description(description)
        if is_valid:
            break
        show_error(error_msg)

    # Collect and validate category (optional)
    while True:
        category = Prompt.ask("Category (optional)", default="")
        is_valid, error_msg = validate_category(category)
        if is_valid:
            break
        show_error(error_msg)

    # Save state for undo
    state.save_state_for_undo()

    # Create new todo
    new_todo = Todo(
        id=str(uuid.uuid4()),
        title=title.strip(),
        description=description.strip(),
        category=category.strip()
    )

    # Add to list
    state.todos.append(new_todo)

    console.print(f"\n[green]✓ Todo added successfully[/green]")
    console.print(f"[dim]ID: {new_todo.id[:8]}...[/dim]")


def list_todos(state: AppState):
    """Display all todos in a formatted table (T011)."""
    if not state.todos:
        console.print("\n[yellow]No todos found. Add your first todo to get started![/yellow]")
        return

    console.print(f"\n[bold cyan]All Todos ({len(state.todos)})[/bold cyan]\n")

    # Create table
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim", width=10)
    table.add_column("Title", style="white", width=30)
    table.add_column("Category", style="magenta", width=15)
    table.add_column("Status", justify="center", width=8)
    table.add_column("Created", style="dim", width=12)

    # Add rows
    for todo in state.todos:
        status = "[green]✓[/green]" if todo.completed else "[yellow]○[/yellow]"
        created_date = todo.created_at[:10]  # YYYY-MM-DD

        table.add_row(
            todo.id[:8],
            todo.title[:30],
            todo.category[:15] if todo.category else "-",
            status,
            created_date
        )

    console.print(table)
    console.print()


# ============================================================================
# User Story 2: Daily Usage (T015, T016, T017, T018)
# ============================================================================

def mark_complete(state: AppState):
    """Mark a todo as complete (T015)."""
    if not state.todos:
        console.print("\n[yellow]No todos available[/yellow]")
        return

    # Show incomplete todos
    incomplete = [t for t in state.todos if not t.completed]
    if not incomplete:
        console.print("\n[yellow]All todos are already complete![/yellow]")
        return

    console.print("\n[bold cyan]Mark Todo as Complete[/bold cyan]\n")
    for i, todo in enumerate(incomplete, 1):
        console.print(f"  {i}. {todo.title} [dim]({todo.id[:8]})[/dim]")

    console.print()
    choice = Prompt.ask("Select todo number", choices=[str(i) for i in range(1, len(incomplete) + 1)])
    selected_todo = incomplete[int(choice) - 1]

    # Save state for undo
    state.save_state_for_undo()

    # Mark as complete
    selected_todo.completed = True
    selected_todo.updated_at = datetime.now().isoformat()

    console.print(f"\n[green]✓ '{selected_todo.title}' marked as complete[/green]")


def mark_incomplete(state: AppState):
    """Mark a todo as incomplete (T016)."""
    if not state.todos:
        console.print("\n[yellow]No todos available[/yellow]")
        return

    # Show completed todos
    completed = [t for t in state.todos if t.completed]
    if not completed:
        console.print("\n[yellow]No completed todos found[/yellow]")
        return

    console.print("\n[bold cyan]Mark Todo as Incomplete[/bold cyan]\n")
    for i, todo in enumerate(completed, 1):
        console.print(f"  {i}. {todo.title} [dim]({todo.id[:8]})[/dim]")

    console.print()
    choice = Prompt.ask("Select todo number", choices=[str(i) for i in range(1, len(completed) + 1)])
    selected_todo = completed[int(choice) - 1]

    # Save state for undo
    state.save_state_for_undo()

    # Mark as incomplete
    selected_todo.completed = False
    selected_todo.updated_at = datetime.now().isoformat()

    console.print(f"\n[green]✓ '{selected_todo.title}' marked as incomplete[/green]")


def search_todos(state: AppState):
    """Search todos by keyword (T017)."""
    if not state.todos:
        console.print("\n[yellow]No todos available[/yellow]")
        return

    console.print("\n[bold cyan]Search Todos[/bold cyan]\n")
    keyword = Prompt.ask("Enter search keyword")

    if not keyword.strip():
        console.print("[red]✗ Search keyword cannot be empty[/red]")
        return

    # Case-insensitive search in title and description
    keyword_lower = keyword.lower()
    results = [
        todo for todo in state.todos
        if keyword_lower in todo.title.lower() or keyword_lower in todo.description.lower()
    ]

    if not results:
        console.print(f"\n[yellow]No todos found matching '{keyword}'[/yellow]")
        return

    console.print(f"\n[bold cyan]Search Results ({len(results)} found)[/bold cyan]\n")

    # Create table
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim", width=10)
    table.add_column("Title", style="white", width=30)
    table.add_column("Category", style="magenta", width=15)
    table.add_column("Status", justify="center", width=8)

    for todo in results:
        status = "[green]✓[/green]" if todo.completed else "[yellow]○[/yellow]"
        table.add_row(
            todo.id[:8],
            todo.title[:30],
            todo.category[:15] if todo.category else "-",
            status
        )

    console.print(table)
    console.print()


def filter_by_category(state: AppState):
    """Filter todos by category (T018)."""
    if not state.todos:
        console.print("\n[yellow]No todos available[/yellow]")
        return

    # Get unique categories
    categories = list(set(todo.category for todo in state.todos if todo.category))

    if not categories:
        console.print("\n[yellow]No categories found. Add categories to your todos first.[/yellow]")
        return

    console.print("\n[bold cyan]Filter by Category[/bold cyan]\n")
    console.print("[bold]Available categories:[/bold]")
    for i, cat in enumerate(sorted(categories), 1):
        count = sum(1 for t in state.todos if t.category == cat)
        console.print(f"  {i}. {cat} [dim]({count} todo(s))[/dim]")

    console.print()
    choice = Prompt.ask("Select category number", choices=[str(i) for i in range(1, len(categories) + 1)])
    selected_category = sorted(categories)[int(choice) - 1]

    # Filter todos
    filtered = [t for t in state.todos if t.category == selected_category]

    console.print(f"\n[bold cyan]Category: {selected_category} ({len(filtered)} todo(s))[/bold cyan]\n")

    # Create table
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim", width=10)
    table.add_column("Title", style="white", width=30)
    table.add_column("Status", justify="center", width=8)
    table.add_column("Created", style="dim", width=12)

    for todo in filtered:
        status = "[green]✓[/green]" if todo.completed else "[yellow]○[/yellow]"
        created_date = todo.created_at[:10]
        table.add_row(
            todo.id[:8],
            todo.title[:30],
            status,
            created_date
        )

    console.print(table)
    console.print()


# ============================================================================
# User Story 3: Bulk Operations (T021, T022, T023, T024)
# ============================================================================

def update_todo(state: AppState):
    """Update a todo's details (T021)."""
    if not state.todos:
        console.print("\n[yellow]No todos available[/yellow]")
        return

    console.print("\n[bold cyan]Update Todo[/bold cyan]\n")
    for i, todo in enumerate(state.todos, 1):
        status = "✓" if todo.completed else "○"
        console.print(f"  {i}. [{status}] {todo.title} [dim]({todo.id[:8]})[/dim]")

    console.print()
    choice = Prompt.ask("Select todo number", choices=[str(i) for i in range(1, len(state.todos) + 1)])
    selected_todo = state.todos[int(choice) - 1]

    console.print(f"\n[bold]Current values:[/bold]")
    console.print(f"  Title: {selected_todo.title}")
    console.print(f"  Description: {selected_todo.description or '(empty)'}")
    console.print(f"  Category: {selected_todo.category or '(empty)'}")
    console.print()

    # Save state for undo (T024)
    state.save_state_for_undo()

    # Update fields
    new_title = Prompt.ask("New title (press Enter to keep current)", default=selected_todo.title)
    new_description = Prompt.ask("New description (press Enter to keep current)", default=selected_todo.description)
    new_category = Prompt.ask("New category (press Enter to keep current)", default=selected_todo.category)

    # Apply updates
    selected_todo.title = new_title.strip() if new_title.strip() else selected_todo.title
    selected_todo.description = new_description.strip()
    selected_todo.category = new_category.strip()
    selected_todo.updated_at = datetime.now().isoformat()

    console.print(f"\n[green]✓ Todo updated successfully[/green]")


def delete_todo(state: AppState):
    """Delete a todo with confirmation (T022)."""
    if not state.todos:
        console.print("\n[yellow]No todos available[/yellow]")
        return

    console.print("\n[bold cyan]Delete Todo[/bold cyan]\n")
    for i, todo in enumerate(state.todos, 1):
        status = "✓" if todo.completed else "○"
        console.print(f"  {i}. [{status}] {todo.title} [dim]({todo.id[:8]})[/dim]")

    console.print()
    choice = Prompt.ask("Select todo number", choices=[str(i) for i in range(1, len(state.todos) + 1)])
    selected_todo = state.todos[int(choice) - 1]

    # Confirm deletion
    confirm = Confirm.ask(f"\n[bold red]Delete '{selected_todo.title}'?[/bold red]")

    if not confirm:
        console.print("[yellow]Deletion cancelled[/yellow]")
        return

    # Save state for undo (T024)
    state.save_state_for_undo()

    # Remove from list
    state.todos.remove(selected_todo)

    console.print(f"\n[green]✓ Todo deleted successfully[/green]")


def undo_last_action(state: AppState):
    """Undo the last action (T023)."""
    if state.undo():
        console.print("\n[green]✓ Last action undone successfully[/green]")
    else:
        console.print("\n[yellow]No actions to undo[/yellow]")


# ============================================================================
# Help & Polish (T029)
# ============================================================================

def show_help():
    """Display help information (T029)."""
    help_text = """
[bold cyan]Interactive CLI Todo Application - Help[/bold cyan]

[bold]Available Commands:[/bold]

1. [cyan]Add todo[/cyan] - Create a new todo with title, description, and category
2. [cyan]List all todos[/cyan] - View all todos in a formatted table
3. [cyan]Search todos[/cyan] - Search by keyword in title or description
4. [cyan]Filter by category[/cyan] - View todos in a specific category
5. [cyan]Complete todo[/cyan] - Mark a todo as complete
6. [cyan]Mark as incomplete[/cyan] - Mark a completed todo as incomplete
7. [cyan]Update todo[/cyan] - Modify todo title, description, or category
8. [cyan]Delete todo[/cyan] - Remove a todo (with confirmation)
9. [cyan]Undo last action[/cyan] - Revert the last change (up to 10 levels)
10. [cyan]Help[/cyan] - Display this help message
11. [cyan]Exit[/cyan] - Save todos and exit application

[bold]Navigation:[/bold]
- Enter the number of your choice and press Enter
- Follow on-screen prompts for each action

[bold]Data Storage:[/bold]
- Todos are automatically saved to 'todos.json' when you exit
- Data persists between application sessions

[bold]Tips:[/bold]
- Use categories to organize your todos
- Search is case-insensitive
- Undo works for add, update, delete, and completion changes
"""
    console.print(Panel(help_text, border_style="cyan", padding=(1, 2)))


# ============================================================================
# Main Application Entry Point (T012, T013, T014)
# ============================================================================

def main():
    """Main application entry point."""
    # Initialize state (T014)
    state = AppState()

    # Load existing todos (T014)
    state.todos = load_todos()

    # Display welcome (T014)
    display_header()
    console.print(f"[green]Loaded {len(state.todos)} todo(s)[/green]\n")

    # Main menu navigation loop (T012)
    while True:
        selected_option = display_menu()

        # Route to appropriate function
        if selected_option == "Add todo":
            add_todo(state)

        elif selected_option == "List all todos":
            list_todos(state)

        elif selected_option == "Search todos":
            search_todos(state)

        elif selected_option == "Filter todos by category":
            filter_by_category(state)

        elif selected_option == "Complete todo":
            mark_complete(state)

        elif selected_option == "Mark todo as incomplete":
            mark_incomplete(state)

        elif selected_option == "Update todo":
            update_todo(state)

        elif selected_option == "Delete todo":
            delete_todo(state)

        elif selected_option == "Undo last action":
            undo_last_action(state)

        elif selected_option == "Help":
            show_help()

        elif selected_option == "Exit":
            # Exit and save (T013)
            if save_todos(state.todos):
                console.print("\n[green]✓ Todos saved successfully[/green]")
            console.print("[cyan]Goodbye! 👋[/cyan]\n")
            break


if __name__ == "__main__":
    main()

