"""Tests for file_manager — mocked dialogs and real temp files."""

import pytest
from pathlib import Path
from unittest.mock import patch


from src.core import file_manager as fm


@pytest.fixture()
def tmp_clp(tmp_path: Path) -> Path:
    """Create a temporary .clp file."""
    f = tmp_path / "test.clp"
    f.write_text("(defrule hello () => )\n", encoding="utf-8")
    return f


class TestReadFile:
    def test_reads_content_correctly(self, tmp_clp: Path) -> None:
        content = fm.read_file(str(tmp_clp))
        assert "(defrule hello" in content


class TestSaveFile:
    def test_saves_content_to_disk(self, tmp_path: Path) -> None:
        path = str(tmp_path / "output.clp")
        result = fm.save_file(path, "(assert (fact))\n")
        assert result is True
        assert "(assert (fact))" in Path(path).read_text()

    def test_returns_false_on_invalid_path(self) -> None:
        with patch("tkinter.messagebox.showerror"):
            result = fm.save_file("/nonexistent/dir/file.clp", "content")
        assert result is False


class TestSaveFileAs:
    def test_saves_when_path_chosen(self, tmp_path: Path) -> None:
        chosen = str(tmp_path / "chosen.clp")
        with patch("tkinter.filedialog.asksaveasfilename", return_value=chosen):
            result = fm.save_file_as("(reset)\n")
        assert result == chosen
        assert Path(chosen).read_text() == "(reset)\n"

    def test_returns_none_when_cancelled(self) -> None:
        with patch("tkinter.filedialog.asksaveasfilename", return_value=""):
            result = fm.save_file_as("content")
        assert result is None


class TestOpenFile:
    def test_opens_file_and_returns_path_and_content(self, tmp_clp: Path) -> None:
        with patch("tkinter.filedialog.askopenfilename", return_value=str(tmp_clp)):
            result = fm.open_file()
        assert result is not None
        path, content = result
        assert path == str(tmp_clp)
        assert "(defrule" in content

    def test_returns_none_when_cancelled(self) -> None:
        with patch("tkinter.filedialog.askopenfilename", return_value=""):
            result = fm.open_file()
        assert result is None


class TestNewFileContent:
    def test_returns_string(self) -> None:
        content = fm.new_file_content()
        assert isinstance(content, str)
        assert len(content) > 0
