"""Smoke test: import + version + CLI invocation."""
from __future__ import annotations

from typer.testing import CliRunner


def test_import_and_version() -> None:
    import mitophagy_perturb_atlas

    assert mitophagy_perturb_atlas.__version__ == "0.1.0"


def test_cli_version() -> None:
    from mitophagy_perturb_atlas.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "mitophagy-perturb-atlas" in result.stdout.lower() or "0.1.0" in result.stdout
