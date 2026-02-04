# Quickstart Guide: Interactive CLI Todo Application

**Version**: 1.0.0
**Date**: 2026-02-02
**Feature**: Interactive CLI Todo Application

## Overview

This guide provides step-by-step instructions for setting up, running, and using the Interactive CLI Todo Application. The application is a professional Python console-based todo manager with rich interactive menus and JSON persistence.

## Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: Version 3.13 or higher
- **Terminal**: Any modern terminal with UTF-8 support
- **Disk Space**: Minimum 50MB for application and dependencies

### Required Tools
- **UV Package Manager**: For Python dependency management
- **Git**: For version control (optional but recommended)

## Installation

### Step 1: Install UV Package Manager

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)**:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify installation:
```bash
uv --version
```

### Step 2: Clone or Download the Project

**Option A: Clone with Git**:
```bash
git clone <repository-url>
cd <project-directory>
git checkout 1-cli-todo-app
```

**Option B: Download ZIP**:
1. Download the project ZIP file
2. Extract to your desired location
3. Navigate to the project directory

### Step 3: Install Dependencies

From the project root directory:

```bash
# Create virtual environment and install dependencies
uv sync

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

This will install:
- `rich>=13.7.0` - Terminal UI library
- `pytest>=7.4.0` - Testing framework (dev)
- `pytest-cov>=4.1.0` - Coverage reporting (dev)

### Step 4: Verify Installation

Run the application to verify setup:

```bash
python src/main.py
```

You should see the main menu with interactive options.

## Running the Application

### Basic Usage

**Start the application**:
```bash
python src/main.py
```

**Navigate the menu**:
- Use **Arrow Keys** (↑/↓) to navigate menu options
- Press **Enter** to select an option
- Follow on-screen prompts for each action

**Exit the application**:
- Select "Exit" from the main menu
- Or press **Ctrl+C** (data will be saved automatically)

### First-Time Setup

On first run, the application will:
1. Create a `todos.json` file in the application directory
2. Initialize with an empty todo list
3. Display the main menu

## Features and Usage

### 1. Add Todo

**Steps**:
1. Select "Add todo" from main menu
2. Enter todo title (required, 1-200 characters)
3. Enter description (optional, up to 1000 characters)
4. Enter category (optional, up to 50 characters)
5. Confirm to save

**Example**:
```
Title: Buy groceries
Description: Milk, eggs, bread, and vegetables
Category: shopping
```

### 2. List All Todos

**Steps**:
1. Select "List all todos" from main menu
2. View todos in a formatted table with:
   - ID (first 8 characters)
   - Title
   - Category
   - Status (✓ Complete / ○ Incomplete)
   - Created date

**Display Format**:
```
┌──────────┬─────────────────┬──────────┬────────┬─────────────┐
│ ID       │ Title           │ Category │ Status │ Created     │
├──────────┼─────────────────┼──────────┼────────┼─────────────┤
│ 550e8400 │ Buy groceries   │ shopping │ ○      │ 2026-02-02  │
│ 661f9511 │ Call dentist    │ health   │ ✓      │ 2026-02-01  │
└──────────┴─────────────────┴──────────┴────────┴─────────────┘
```

### 3. Search Todos

**Steps**:
1. Select "Search todos" from main menu
2. Enter search keyword
3. View matching todos (case-insensitive search in title and description)

**Example**:
```
Search query: grocery
Results: 1 todo found matching "grocery"
```

### 4. Filter by Category

**Steps**:
1. Select "Filter todos by category" from main menu
2. View list of available categories
3. Select a category
4. View filtered todos

**Example**:
```
Available categories:
- shopping (3 todos)
- health (1 todo)
- work (5 todos)
```

### 5. Complete Todo

**Steps**:
1. Select "Complete todo" from main menu
2. View list of incomplete todos
3. Select todo by ID or number
4. Confirm completion

**Result**: Todo marked as complete (✓)

### 6. Mark Todo as Incomplete

**Steps**:
1. Select "Mark todo as incomplete" from main menu
2. View list of completed todos
3. Select todo by ID or number
4. Confirm status change

**Result**: Todo marked as incomplete (○)

### 7. Update Todo

**Steps**:
1. Select "Update todo" from main menu
2. Select todo to update
3. Choose what to update:
   - Title
   - Description
   - Category
4. Enter new value
5. Confirm changes

**Note**: Leave field empty to keep current value

### 8. Delete Todo

**Steps**:
1. Select "Delete todo" from main menu
2. Select todo to delete
3. Confirm deletion (this action cannot be undone except via Undo)

**Warning**: Deleted todos are permanently removed unless you use Undo immediately

### 9. Undo Last Action

**Steps**:
1. Select "Undo last action" from main menu
2. Previous state is restored
3. View confirmation message

**Limitations**:
- Maximum 10 undo levels
- Undo history cleared on application restart
- Cannot undo after exiting application

### 10. Help

**Steps**:
1. Select "Help" from main menu
2. View comprehensive usage instructions
3. See keyboard shortcuts and tips

### 11. Exit

**Steps**:
1. Select "Exit" from main menu
2. Application saves current state to `todos.json`
3. Application terminates gracefully

## Data Storage

### Location
- **File**: `todos.json` in the application directory
- **Format**: Human-readable JSON
- **Backup**: Automatic backup created on corrupted file detection

### Manual Backup

**Create backup**:
```bash
cp todos.json todos.backup.json
```

**Restore from backup**:
```bash
cp todos.backup.json todos.json
```

### Data Structure

```json
{
  "version": "1.0",
  "todos": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "category": "shopping",
      "completed": false,
      "created_at": "2026-02-02T10:30:00Z",
      "updated_at": "2026-02-02T10:30:00Z"
    }
  ]
}
```

## Troubleshooting

### Application Won't Start

**Problem**: `ModuleNotFoundError: No module named 'rich'`
**Solution**:
```bash
uv sync
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

**Problem**: `Python version too old`
**Solution**: Install Python 3.13+ from python.org

### Display Issues

**Problem**: Colors or formatting not displaying correctly
**Solution**:
- Ensure terminal supports UTF-8 encoding
- Try a different terminal (Windows Terminal, iTerm2, etc.)
- Update terminal to latest version

**Problem**: Arrow keys not working
**Solution**:
- Use number keys as alternative (if implemented)
- Check terminal key bindings
- Try different terminal emulator

### Data Issues

**Problem**: `todos.json` corrupted
**Solution**:
- Application automatically creates backup
- Restore from `todos.json.backup`
- Or start fresh (file will be recreated)

**Problem**: Cannot save data
**Solution**:
- Check file permissions in application directory
- Ensure sufficient disk space
- Run application with appropriate permissions

### Performance Issues

**Problem**: Slow with many todos
**Solution**:
- Application supports 1000+ todos
- If experiencing slowness, consider archiving old todos
- Check system resources (CPU, memory)

## Testing

### Run Unit Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_todo_operations.py
```

### Test Coverage

View coverage report:
```bash
# Generate HTML report
pytest --cov=src --cov-report=html

# Open in browser
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

## Best Practices

### Regular Backups
- Backup `todos.json` regularly
- Use version control for important todos
- Export to external storage periodically

### Organization Tips
- Use consistent category names
- Keep titles concise and descriptive
- Use descriptions for detailed information
- Review and clean up completed todos regularly

### Performance Tips
- Archive old completed todos
- Use categories for better organization
- Use search instead of scrolling through long lists

## Advanced Usage

### Command-Line Arguments (Future)

Currently not implemented, but planned for future versions:
```bash
# Quick add
python src/main.py add "Buy milk"

# List todos
python src/main.py list

# Search
python src/main.py search "grocery"
```

### Integration with Other Tools

**Export todos**:
```bash
# Copy todos.json to another location
cp todos.json ~/Documents/todos-backup.json
```

**Import todos**:
```bash
# Replace current todos with backup
cp ~/Documents/todos-backup.json todos.json
```

## Getting Help

### Documentation
- **Specification**: `specs/1-cli-todo-app/spec.md`
- **Data Model**: `specs/1-cli-todo-app/data-model.md`
- **Research**: `specs/1-cli-todo-app/research.md`

### Support
- Check the Help menu within the application
- Review error messages for specific guidance
- Consult the troubleshooting section above

## Next Steps

After mastering Phase I, you'll be ready for:
- **Phase II**: Web application with multi-user support
- **Phase III**: AI-powered chatbot interface
- **Phase IV**: Kubernetes deployment
- **Phase V**: Advanced features and cloud deployment

## Version History

- **1.0.0** (2026-02-02): Initial release
  - Interactive CLI with arrow-key navigation
  - Full CRUD operations
  - Search and filter functionality
  - Undo capability
  - JSON persistence
