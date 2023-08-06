from dataclasses import dataclass
from datetime import datetime

from .base_model import BaseModel


@dataclass
class RenewAccountModel(BaseModel):
    """
    Attributes:
        expiration_ts (int): new expiration date for this account, as a timestamp
            in milliseconds since epoch
        expiration_date (datetime): new expiration date for this account,
            as a datetime object
    """

    expiration_ts: int

    @property
    def expiration_date(self) -> datetime:
        return datetime.fromtimestamp(self.expiration_ts / 1000)
