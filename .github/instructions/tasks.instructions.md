---
description: "Use when creating, editing, or reviewing Invoke tasks in this project. Covers Collection wiring, task structure, and alias conventions."
applyTo: "tasks/**"
---
# Tasks Instructions

## File Location
- All invoke task modules live under `tasks/`
- `tasks/__init__.py` builds the root `Collection` — every new task module must be imported and wired there explicitly (no auto-glob loading)
- Group related tasks by concern: `tasks/repo.py`, `tasks/tests.py`, `tasks/ruff.py`

## Collection Conventions
- Sub-collections mirror file names: `tasks/repo.py` → `invoke repo.<task>`
- Top-level alias tasks (no namespace) live in `tasks/combos.py` — short names (`test`, `fix`)
- Set `namespace.configure({"auto_dash_names": False})` so task names keep underscores

## Task Structure Pattern
```python
from invoke import task


@task
def task_name(context):
    """Short description shown in `invoke -l`"""
    print("\n------------")
    print("Task Display Name")
    print("------------\n")
    context.run("shell-command --flag")
```

## Wiring a New Task Module
```python
# tasks/__init__.py
from invoke import Collection

from . import combos, my_new_module, repo, ruff, tests

namespace = Collection()
namespace.configure({"auto_dash_names": False})
namespace.add_collection(my_new_module, name="my_new_module")
```

## Alias Tasks
- Define combo/alias tasks in `tasks/combos.py`, calling sub-tasks directly:
  ```python
  @task
  def test(context):
      """Run All Tests"""
      tests.actionlint(context)
      tests.pylint(context)
      tests.rufflint(context)
      tests.yamllint(context)
  ```

## Calling Into `modules/`
- Tasks that wrap git workflow logic (`repo.pull`, `repo.push`, etc.) should be thin wrappers that
  import the module and call its `main()` — keep git/business logic in `modules/repo/*.py`, not in `tasks/repo.py`
- Unused `context` parameters (required by Invoke's `@task` signature) should be prefixed `_context`
