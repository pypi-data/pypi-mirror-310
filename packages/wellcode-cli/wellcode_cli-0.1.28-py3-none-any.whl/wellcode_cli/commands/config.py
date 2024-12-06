from pathlib import Path
import json
import rich_click as click
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()
CONFIG_FILE = Path.home() / '.wellcode' / 'config.json'

@click.command()
def config():
    """Configure Wellcode CLI settings"""
    console.print(Panel.fit(
        "🔧 Wellcode CLI Configuration",
        subtitle="Setup your integrations"
    ))

    # Create config directory if it doesn't exist
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Load existing config if available
    config_data = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            config_data = json.load(f)

    # GitHub configuration
    console.print("\n[bold blue]GitHub Configuration[/]")
    config_data['GITHUB_TOKEN'] = Prompt.ask(
        "Enter your GitHub token",
        default=config_data.get('GITHUB_TOKEN', ''),
        password=True
    )
    config_data['GITHUB_ORG'] = Prompt.ask(
        "Enter your GitHub organization",
        default=config_data.get('GITHUB_ORG', '')
    )

    # Linear configuration
    console.print("\n[bold green]Linear Configuration[/] (optional)")
    config_data['LINEAR_API_KEY'] = Prompt.ask(
        "Enter your Linear API key",
        default=config_data.get('LINEAR_API_KEY', ''),
        password=True
    )

    # Split.io configuration
    console.print("\n[bold magenta]Split.io Configuration[/] (optional)")
    config_data['SPLIT_API_KEY'] = Prompt.ask(
        "Enter your Split.io API key",
        default=config_data.get('SPLIT_API_KEY', ''),
        password=True
    )

    # Anthropic configuration
    console.print("\n[bold yellow]Anthropic Configuration[/] (optional)")
    config_data['ANTHROPIC_API_KEY'] = Prompt.ask(
        "Enter your Anthropic API key",
        default=config_data.get('ANTHROPIC_API_KEY', ''),
        password=True
    )

    # Save configuration
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=2)

    console.print("\n✅ [green]Configuration saved successfully![/]")
