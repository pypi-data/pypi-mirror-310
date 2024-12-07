from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Sequence

from gradio.components.base import Component, FormComponent
from gradio.events import Events

if TYPE_CHECKING:
    from gradio.components import Timer


class MagicSketch(FormComponent):
    def __init__(
        self,
        value: str | Callable | None = None,
        *,
        theme: str | None = None,
        visible: bool = True,
        render: bool = True,
    ):
        self.theme = theme
        super().__init__(
            value=value,
            render=render,
        )

    def preprocess(self, payload: str | None) -> str | None:
        """
        Parameters:
            payload: the text entered in the textarea.
        Returns:
            Passes text value as a {str} into the function.
        """
        # print("preprocess", payload)
        return None if payload is None else payload

    def postprocess(self, value: str | None) -> str | None:
        """
        Parameters:
            value: Expects a {str} returned from function and sets textarea value to it.
        Returns:
            The value to display in the textarea.
        """
        # print("postprocess", value)
        return None if value is None else value

    def api_info(self) -> dict[str, Any]:
        return {"type": "string"}

    def example_payload(self) -> Any:
        return "Hello!!"

    def example_value(self) -> Any:
        return "Hello!!"
    from typing import Callable, Literal
    from gradio.blocks import Block

class MagicQuill(FormComponent):
    def __init__(
        self,
        value: str | Callable | None = None,
        *,
        theme: str | None = None,
        url: str | None = None,
        visible: bool = True,
        render: bool = True,
    ):
        self.theme = theme
        self.url = url
        super().__init__(
            value=value,
            render=render,
        )

    def preprocess(self, payload: str | None) -> str | None:
        """
        Parameters:
            payload: the text entered in the textarea.
        Returns:
            Passes text value as a {str} into the function.
        """
        # print("preprocess", payload)
        return None if payload is None else payload

    def postprocess(self, value: str | None) -> str | None:
        """
        Parameters:
            value: Expects a {str} returned from function and sets textarea value to it.
        Returns:
            The value to display in the textarea.
        """
        # print("postprocess", value)
        return None if value is None else value

    def api_info(self) -> dict[str, Any]:
        return {"type": "string"}

    def example_payload(self) -> Any:
        return "Hello!!"

    def example_value(self) -> Any:
        return "Hello!!"
    from typing import Callable, Literal, Sequence, Any, TYPE_CHECKING
    from gradio.blocks import Block
    if TYPE_CHECKING:
        from gradio.components import Timer

    