from typing import Any
from typing_extensions import TypedDict


class Label(TypedDict, total=False):
    """
    A "label" on a file in TDP.

    For further info, see
    https://developers.tetrascience.com/docs/basic-concepts-metadata-tags-and-labels
    """
    name: str
    value: Any
