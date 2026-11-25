"""Prépare les tests : le programme s'importe même sur une machine sans Tkinter."""
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    import tkinter  # noqa: F401
except ImportError:  # pragma: no cover - seulement sur une machine sans Tkinter
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
    """Chaque test démarre en français (langue du code source)."""
    pocket_book.choisir_langue("fr")
    yield
    pocket_book.choisir_langue("fr")
