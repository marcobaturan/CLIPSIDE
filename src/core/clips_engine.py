"""CLIPS Engine — wraps CLIPSpy Environment with output capture and IDE controls."""

import clips
import threading
from typing import Callable, Optional


class OutputRouter(clips.Router):
    """Custom CLIPSpy router that captures engine output to a Python callback."""

    NAME = "clipside-router"
    PRIORITY = 40

    def __init__(self, callback: Callable[[str], None]) -> None:
        super().__init__(self.NAME, self.PRIORITY)
        self._callback = callback

    def query(self, name: str) -> bool:
        """Route stdout and stderr through this router."""
        return name in ("stdout", "stderr", "wdisplay")

    def write(self, name: str, message: str) -> None:
        """Forward CLIPS output to the registered callback."""
        self._callback(message)

    def read(self, name: str) -> str:
        return ""

    def readline(self, name: str) -> str:
        return ""


class ClipsEngine:
    """Thread-safe wrapper around a CLIPSpy Environment for IDE use."""

    def __init__(self, output_callback: Optional[Callable[[str], None]] = None) -> None:
        self._env = clips.Environment()
        self._lock = threading.Lock()
        self._callback = output_callback or (lambda msg: None)
        self._router = OutputRouter(self._callback)
        self._env.add_router(self._router)

    # ------------------------------------------------------------------
    # Engine control
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Reset the CLIPS environment (clears facts, keeps constructs)."""
        with self._lock:
            self._env.reset()

    def clear(self) -> None:
        """Clear all constructs and facts from the environment."""
        with self._lock:
            self._env.clear()

    def run(self, limit: int = 0) -> int:
        """Run the inference engine. Returns number of rules fired."""
        with self._lock:
            return self._env.run(limit if limit > 0 else None)

    def step(self) -> int:
        """Execute a single rule activation (step mode)."""
        with self._lock:
            return self._env.run(1)

    # ------------------------------------------------------------------
    # Fact management
    # ------------------------------------------------------------------

    def assert_string(self, fact_string: str) -> None:
        """Assert a fact from a CLIPS-syntax string."""
        with self._lock:
            self._env.assert_string(fact_string)

    def get_facts(self) -> list[str]:
        """Return all current facts as a list of strings."""
        with self._lock:
            return [str(f) for f in self._env.facts()]

    # ------------------------------------------------------------------
    # Construct loading
    # ------------------------------------------------------------------

    def load_file(self, path: str) -> None:
        """Load CLIPS constructs from a .clp file."""
        with self._lock:
            self._env.load(path)

    def build(self, construct: str) -> None:
        """Build a CLIPS construct from a string."""
        with self._lock:
            self._env.build(construct)

    def eval(self, expression: str) -> object:
        """Evaluate a CLIPS expression and return the result."""
        with self._lock:
            return self._env.eval(expression)

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------

    def get_agenda(self) -> list[str]:
        """Return all pending rule activations as strings."""
        with self._lock:
            return [str(a) for a in self._env.activations()]

    def get_instances(self) -> list[str]:
        """Return all COOL instances as strings."""
        with self._lock:
            return [str(i) for i in self._env.instances()]

    def get_rules(self) -> list[str]:
        """Return all defined rules by name."""
        with self._lock:
            return [r.name for r in self._env.rules()]
