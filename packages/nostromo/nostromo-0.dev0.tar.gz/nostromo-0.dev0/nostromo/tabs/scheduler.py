from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label


class SchedulerContent(Widget):
    @classmethod
    def get_id(cls):
        return 'Scheduler'

    def compose(self) -> ComposeResult:
        yield Label('Scheduler')
