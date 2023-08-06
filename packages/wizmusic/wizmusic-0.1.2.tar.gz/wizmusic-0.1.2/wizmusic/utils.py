from datetime import timedelta

from rich.progress import TextColumn, BarColumn, ProgressColumn
from rich.table import Column
from rich.text import Text


class TimeColumn(ProgressColumn):
    """Renders time elapsed."""

    def render(self, task: "Task") -> Text:
        if task.completed is None:
            return Text("-:--:--", style="progress.elapsed")
        delta = timedelta(seconds=int(task.completed / 1000))
        return Text(str(delta), style="progress.elapsed")


def default_progress_columns(rgb: tuple):
    return (
        TextColumn("[progress.description]{task.description}"),
        BarColumn(
            bar_width=None,
            complete_style="rgb({},{},{})".format(*rgb),
            style="none",
            table_column=Column(ratio=2),
        ),
        TimeColumn(),
    )
