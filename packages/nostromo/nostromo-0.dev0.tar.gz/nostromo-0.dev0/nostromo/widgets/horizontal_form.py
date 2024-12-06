from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Label, OptionList


class HorizontalForm(Horizontal):
    DEFAULT_CSS = """
    HorizontalForm Label {
        padding: 1;
        text-align: right;
    }
    
    DefaultOptionList {
        min-height: 3;
    }
    """

    def __init__(self, *form_items: Widget, name: str | None = None, id: str | None = None, classes: str | None = None,
                 disabled: bool = False) -> None:
        super().__init__(*[], name=name, id=id, classes=classes, disabled=disabled)
        self._form_items = form_items

    def compose(self) -> ComposeResult:
        labels = Vertical(*[Label(w.name) for w in self._form_items])
        labels.styles.max_width = max(*[len(w.name) for w in self._form_items])
        yield labels

        items = []
        for item in self._form_items:
            if isinstance(item, OptionList):
                items.append(Label(item.name))
            items.append(item)

        yield Vertical(*items)
