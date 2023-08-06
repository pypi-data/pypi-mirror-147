"""This module contains the `Button` class."""


from __future__ import annotations

from typing import Any, Callable, Optional

from ...ansi_interface import MouseAction, MouseEvent
from ...parser import markup, StyledText
from ...regex import real_length
from .. import styles as w_styles
from ...input import keys
from ..base import Widget


class Button(Widget):
    """A simple Widget representing a mouse-clickable button"""

    styles = w_styles.StyleManager(
        label=w_styles.CLICKABLE,
        highlight=w_styles.CLICKED,
    )

    chars: dict[str, w_styles.CharType] = {"delimiter": ["[ ", " ]"]}

    def __init__(
        self,
        label: str = "Button",
        onclick: Optional[Callable[[Button], Any]] = None,
        padding: int = 0,
        **attrs: Any,
    ) -> None:
        """Initialize object"""

        super().__init__(**attrs)

        self.label = label
        self.onclick = onclick
        self.padding = padding
        self._selectables_length = 1

    def handle_mouse(self, event: MouseEvent) -> bool:
        """Handle a mouse event"""

        if event.action == MouseAction.LEFT_CLICK:
            self.selected_index = 0
            if self.onclick is not None:
                self.onclick(self)

            return True

        if event.action == MouseAction.RELEASE:
            self.selected_index = None
            return True

        return super().handle_mouse(event)

    def handle_key(self, key: str) -> bool:
        """Handles a keypress"""

        if key == keys.RETURN and self.onclick is not None:
            self.onclick(self)
            return True

        return False

    def get_lines(self) -> list[str]:
        """Get object lines"""

        delimiters = self._get_char("delimiter")
        assert isinstance(delimiters, list) and len(delimiters) == 2
        left, right = delimiters

        word: str = markup.parse(left + self.label + right)
        if self.selected_index is None:
            word = self.styles.label(word)
        else:
            word = self.styles.highlight(word)

        line = StyledText(word + self.padding * " ")
        self.width = real_length(line)

        return [line]
