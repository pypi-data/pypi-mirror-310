from textual.app import ComposeResult
from textual.screen import Screen

from nostromo.widgets.pipeline_builder import PipelineBuilderWidget


class PipelineBuilderScreen(Screen):
    BINDINGS = [('ctrl+n', 'app.pop_screen', 'Close Pipeline Builder')]

    def compose(self) -> ComposeResult:
        yield PipelineBuilderWidget()
