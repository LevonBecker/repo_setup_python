import sys
from pathlib import Path

from invoke import Collection

# Ensure the repo root (parent of tasks/) is importable so `modules.*` resolves
# regardless of how invoke was invoked.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from . import claude, combos, repo, ruff, skeleton, tests  # noqa: E402  # pylint: disable=wrong-import-position

namespace = Collection()
namespace.configure({"auto_dash_names": False})

namespace.add_collection(claude, name="claude")
namespace.add_collection(repo, name="repo")
namespace.add_collection(ruff, name="ruff")
namespace.add_collection(skeleton, name="skeleton")
namespace.add_collection(tests, name="tests")

namespace.add_task(combos.fix, name="fix")
namespace.add_task(combos.test, name="test")
