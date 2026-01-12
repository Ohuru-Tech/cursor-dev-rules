"""CLI module for cursor-dev-rules."""

import shutil
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def get_rules_path():
    """Get the path to the bundled rules directory.

    Returns either a Traversable (from importlib.resources) or a Path.
    """
    import importlib.resources

    try:
        # Try to get the rules from the installed package
        package_ref = importlib.resources.files("cursor_dev_rules")
        rules_ref = package_ref / "rules"
        # Check if it's a directory (Traversable) or exists as a path
        if hasattr(rules_ref, "is_dir") and rules_ref.is_dir():
            return rules_ref
        elif isinstance(rules_ref, Path) and rules_ref.exists() and rules_ref.is_dir():
            return rules_ref
    except (ModuleNotFoundError, AttributeError, TypeError):
        # Log the exception for debugging, but continue to fallback
        pass
    except Exception:
        # Catch any other exceptions and continue to fallback
        pass

    # Fallback: look for rules in the package directory (for development/editable installs)
    package_dir = Path(__file__).parent
    rules_path = package_dir / "rules"
    if rules_path.exists() and rules_path.is_dir():
        return rules_path

    # Additional fallback: look for rules in the project root (for development)
    project_root = Path(__file__).parent.parent
    rules_path = project_root / "rules"
    if rules_path.exists() and rules_path.is_dir():
        return rules_path

    raise FileNotFoundError("Could not find rules directory")


def copy_rule_file(source, dest: Path, console: Console) -> bool:
    """Copy a rule file from source to destination.

    Source can be either a Traversable (from importlib.resources) or a Path.
    """
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)

        # Use importlib.resources if source is a Traversable
        if hasattr(source, "read_bytes"):
            # It's a Traversable from importlib.resources
            content = source.read_bytes()
            dest.write_bytes(content)
        elif isinstance(source, Path):
            # It's a regular Path
            shutil.copy2(source, dest)
        else:
            # Try to read as bytes
            content = source.read_bytes()
            dest.write_bytes(content)

        return True
    except Exception as e:
        console.print(f"[red]Error copying file to {dest}: {e}[/red]")
        return False


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Cursor Dev Rules - Fetch and install Cursor dev rules into your project."""
    pass


@main.command()
@click.argument("rule_path", type=str)
def fetch(rule_path: str):
    """Fetch rules for a specific framework.

    RULE_PATH should be in the format: category/framework
    Examples: backend/django, backend/fastapi, frontend/nextjs
    """
    try:
        # Parse the rule path
        parts = rule_path.split("/")
        if len(parts) != 2:
            console.print(
                Panel(
                    "[red]Invalid rule path format.[/red]\n\n"
                    "Expected format: [bold]category/framework[/bold]\n"
                    "Examples:\n"
                    "  • backend/django\n"
                    "  • backend/fastapi\n"
                    "  • frontend/nextjs",
                    title="[red]Error[/red]",
                    border_style="red",
                )
            )
            raise click.Abort()

        category, framework = parts

        # Get the current working directory
        cwd = Path.cwd()
        cursor_rules_dir = cwd / ".cursor" / "rules"

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Task 1: Validate and locate rules
            task1 = progress.add_task("Locating rules...", total=None)

            rules_path = get_rules_path()
            general_rule_source = rules_path / category / "general" / "RULE.md"
            specific_rule_source = rules_path / category / framework / "RULE.md"

            # Check if rules exist
            # Handle both Traversable (from importlib.resources) and Path objects
            general_exists = False
            specific_exists = False

            if hasattr(general_rule_source, "is_file"):
                # Traversable from importlib.resources
                general_exists = general_rule_source.is_file()
            elif isinstance(general_rule_source, Path):
                # Regular Path object
                general_exists = (
                    general_rule_source.exists() and general_rule_source.is_file()
                )

            if hasattr(specific_rule_source, "is_file"):
                # Traversable from importlib.resources
                specific_exists = specific_rule_source.is_file()
            elif isinstance(specific_rule_source, Path):
                # Regular Path object
                specific_exists = (
                    specific_rule_source.exists() and specific_rule_source.is_file()
                )

            if not general_exists:
                console.print(
                    Panel(
                        f"[red]General rule not found:[/red] {general_rule_source}\n\n"
                        f"Available categories: backend, frontend",
                        title="[red]Error[/red]",
                        border_style="red",
                    )
                )
                raise click.Abort()

            if not specific_exists:
                console.print(
                    Panel(
                        f"[red]Framework rule not found:[/red] {specific_rule_source}\n\n"
                        f"Available frameworks for [bold]{category}[/bold]:\n"
                        f"  • Check the cursor_dev_rules/rules/{category}/ directory",
                        title="[red]Error[/red]",
                        border_style="red",
                    )
                )
                raise click.Abort()

            progress.update(task1, completed=True)

            # Task 2: Copy general rule
            task2 = progress.add_task("Copying general rule...", total=None)
            general_dest = cursor_rules_dir / "general" / "RULE.md"
            if copy_rule_file(general_rule_source, general_dest, console):
                progress.update(task2, completed=True)
                console.print(
                    f"[green]✓[/green] Copied general rule to [bold]{general_dest.relative_to(cwd)}[/bold]"
                )
            else:
                raise click.Abort()

            # Task 3: Copy specific rule
            task3 = progress.add_task(f"Copying {framework} rule...", total=None)
            specific_dest = cursor_rules_dir / "code-patterns" / "RULE.md"
            if copy_rule_file(specific_rule_source, specific_dest, console):
                progress.update(task3, completed=True)
                console.print(
                    f"[green]✓[/green] Copied {framework} rule to [bold]{specific_dest.relative_to(cwd)}[/bold]"
                )
            else:
                raise click.Abort()

        # Success message
        console.print()
        console.print(
            Panel(
                f"[green]Successfully installed rules for [bold]{rule_path}[/bold]![/green]\n\n"
                f"Rules are now available at:\n"
                f"  • {cursor_rules_dir.relative_to(cwd) / 'general' / 'RULE.md'}\n"
                f"  • {cursor_rules_dir.relative_to(cwd) / 'code-patterns' / 'RULE.md'}",
                title="[green]Success[/green]",
                border_style="green",
            )
        )

    except FileNotFoundError as e:
        console.print(
            Panel(
                f"[red]Could not find rules directory:[/red] {e}\n\n"
                "Make sure the package is properly installed.",
                title="[red]Error[/red]",
                border_style="red",
            )
        )
        raise click.Abort()
    except Exception as e:
        console.print(
            Panel(
                f"[red]Unexpected error:[/red] {e}",
                title="[red]Error[/red]",
                border_style="red",
            )
        )
        raise click.Abort()


if __name__ == "__main__":
    main()
