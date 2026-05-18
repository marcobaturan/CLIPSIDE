"""Tests for ClipsEngine — written TDD-first before implementation."""

import pytest
from unittest.mock import MagicMock, patch


# Skip all tests if clipspy is not installed on this system
clipspy_available = pytest.importorskip("clips", reason="clipspy not installed")


from src.core.clips_engine import ClipsEngine


@pytest.fixture()
def engine() -> ClipsEngine:
    """Provide a fresh ClipsEngine for each test."""
    return ClipsEngine()


@pytest.fixture()
def engine_with_callback() -> tuple[ClipsEngine, list[str]]:
    """Provide engine with captured output list."""
    captured: list[str] = []
    eng = ClipsEngine(output_callback=lambda msg: captured.append(msg))
    return eng, captured


class TestEngineControl:
    """Tests for reset, clear, run, step operations."""

    def test_reset_clears_facts(self, engine: ClipsEngine) -> None:
        engine.assert_string("(test-fact)")
        engine.reset()
        assert engine.get_facts() == []

    def test_clear_removes_rules_and_facts(self, engine: ClipsEngine) -> None:
        engine.build("(defrule test-rule (trigger) => (printout t \"fired\" crlf))")
        engine.clear()
        assert engine.get_rules() == []

    def test_run_returns_fire_count(self, engine: ClipsEngine) -> None:
        engine.build("(defrule fire-once (trigger) => )")
        engine.reset()
        engine.assert_string("(trigger)")
        fired = engine.run()
        assert fired == 1

    def test_step_fires_one_rule(self, engine: ClipsEngine) -> None:
        engine.build("(defrule r1 (go) => )")
        engine.build("(defrule r2 (go) => )")
        engine.reset()
        engine.assert_string("(go)")
        fired = engine.step()
        assert fired == 1


class TestFactManagement:
    """Tests for assert, retract, get_facts."""

    def test_assert_string_adds_fact(self, engine: ClipsEngine) -> None:
        engine.reset()
        engine.assert_string("(color red)")
        facts = engine.get_facts()
        assert any("color red" in f for f in facts)

    def test_get_facts_returns_list(self, engine: ClipsEngine) -> None:
        engine.reset()
        result = engine.get_facts()
        assert isinstance(result, list)

    def test_multiple_facts(self, engine: ClipsEngine) -> None:
        engine.reset()
        engine.assert_string("(fruit apple)")
        engine.assert_string("(fruit banana)")
        facts = engine.get_facts()
        assert len(facts) >= 2


class TestConstructLoading:
    """Tests for build and eval."""

    def test_build_defrule(self, engine: ClipsEngine) -> None:
        engine.build("(defrule my-rule (active) => )")
        assert "my-rule" in engine.get_rules()

    def test_build_deffacts(self, engine: ClipsEngine) -> None:
        engine.build("(deffacts initial-facts (started))")
        engine.reset()
        facts = engine.get_facts()
        assert any("started" in f for f in facts)

    def test_eval_arithmetic(self, engine: ClipsEngine) -> None:
        result = engine.eval("(+ 1 2)")
        assert result == 3


class TestAgendaInspection:
    """Tests for agenda retrieval via env.activations()."""

    def test_get_agenda_returns_list(self, engine: ClipsEngine) -> None:
        engine.reset()
        result = engine.get_agenda()
        assert isinstance(result, list)

    def test_agenda_contains_activated_rule(self, engine: ClipsEngine) -> None:
        engine.build("(defrule agenda-test (ready) => )")
        engine.reset()
        engine.assert_string("(ready)")
        agenda = engine.get_agenda()
        assert any("agenda-test" in item for item in agenda)


class TestOutputCapture:
    """Tests for the custom output router."""

    def test_output_callback_receives_printout(
        self, engine_with_callback: tuple[ClipsEngine, list[str]]
    ) -> None:
        engine, captured = engine_with_callback
        engine.build(
            '(defrule print-test (hello) => (printout t "HELLO_WORLD" crlf))'
        )
        engine.reset()
        engine.assert_string("(hello)")
        engine.run()
        full_output = "".join(captured)
        assert "HELLO_WORLD" in full_output
