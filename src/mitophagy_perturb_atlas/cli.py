"""Typer-based CLI for mitophagy_perturb_atlas.

This is the `[project.scripts]` entrypoint. Every operation that a notebook
would invoke must also be reachable from this CLI, so the repo is usable
without opening Jupyter.
"""

from __future__ import annotations

import logging

import typer
from rich.console import Console
from rich.logging import RichHandler

from mitophagy_perturb_atlas import __version__
from mitophagy_perturb_atlas.config import AppConfig

app = typer.Typer(
    name="mitophagy-perturb-atlas",
    help="mitophagy-perturb-atlas — see README.md for the biological question this answers.",
    no_args_is_help=True,
)
console = Console()


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )


@app.command()
def version() -> None:
    """Print the installed version and exit."""
    console.print(f"mitophagy-perturb-atlas v{__version__}")


@app.command()
def demo(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose logging."),
) -> None:
    """End-to-end demo. See `notebooks/01_demo.ipynb` for the full walkthrough."""
    _configure_logging(verbose)
    log = logging.getLogger(__name__)
    cfg = AppConfig()
    log.info("Loaded config: cache_dir=%s, seed=%d", cfg.paths.cache_dir, cfg.random_seed)
    log.info("Demo entrypoint reached. Implement me in subsequent commits.")
    raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
