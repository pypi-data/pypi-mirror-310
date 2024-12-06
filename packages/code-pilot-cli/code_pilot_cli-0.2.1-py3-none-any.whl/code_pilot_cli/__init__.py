"""
CodePilot CLI: Your customizable coding assistant for the command line interface (CLI).
"""

from typing import Optional
from rich.markdown import Markdown
from rich.panel import Panel


# Constants
CHAT_LLM = "HuggingFaceH4/starchat2-15b-v0.1"
COMPLETION_LLM = "bigcode/starcoder2-15b"
SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are CodePilot, an advanced coding assistant powered by "
    "state-of-the-art Large Language Models, and specifically optimized for enhanced "
    "performance in coding tasks. You have the experience and knowledge of senior software"
    "engineer, site reliability engineer and cybersecurity engineer.",
}


def create_panel(title: str, content: str, subtitle: Optional[str] = None) -> Panel:
    """
    Highlight and print the provided code.

    Args:
        title (str): Panel title.
        content (str): Panel content.
        subtitle (str, optional): An optional subtitle for the panel.

    Returns:
        Panel
    """

    md = Markdown(content, code_theme="lightbulb")

    return Panel(
        md,
        title=f"[bold red]{title}[/bold red]",
        title_align="left",
        subtitle=subtitle,
        subtitle_align="right",
    )
