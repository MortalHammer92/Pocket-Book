"""Test setup: the program can be imported even on a machine without Tkinter."""
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    import tkinter  # noqa: F401
except ImportError:  # pragma: no cover - only on a machine without Tkinter
    tk = types.ModuleType("tkinter")
    for sous in ("filedialog", "messagebox", "ttk", "font"):
        module = types.ModuleType(f"tkinter.{sous}")
        setattr(tk, sous, module)
        sys.modules[f"tkinter.{sous}"] = module
    sys.modules["tkinter"] = tk

import pytest  # noqa: E402

import pocket_book  # noqa: E402


@pytest.fixture(autouse=True)
def langue_francaise():
    """Every test starts in French (the source code's language)."""
    pocket_book.choisir_langue("fr")
    yield
    pocket_book.choisir_langue("fr")
