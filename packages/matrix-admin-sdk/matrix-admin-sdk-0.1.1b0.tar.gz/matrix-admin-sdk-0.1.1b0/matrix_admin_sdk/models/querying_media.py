from dataclasses import dataclass
from typing import List

from .base_model import BaseModel


@dataclass
class QueryingMediaModel(BaseModel):
    """
    Querying media model.
    Attributes:
        local (list[str]):
        remote (list[str]):
    """

    local: List[str]
    remote: List[str]
