"""Test setup: the program can be imported even on a machine without Tkinter."""
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    import tkinter  # noqa: F401
except ImportError:  # pragma: no cover - only on a machine without Tkinter
    tk = types.ModuleType("tkinter")
    for subfolder in ("filedialog", "messagebox", "ttk", "font"):
        module = types.ModuleType(f"tkinter.{subfolder}")
        setattr(tk, subfolder, module)
        sys.modules[f"tkinter.{subfolder}"] = module
    sys.modules["tkinter"] = tk

import pytest  # noqa: E402

import pocket_book  # noqa: E402


@pytest.fixture(autouse=True)
def english_language():
    """Every test starts in English (the source code's language)."""
    pocket_book.set_language("en")
    yield
    pocket_book.set_language("en")
