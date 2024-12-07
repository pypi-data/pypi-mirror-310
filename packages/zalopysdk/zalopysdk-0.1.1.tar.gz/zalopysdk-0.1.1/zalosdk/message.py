"""This module contains clasess and function for ZNS Message"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ZNSMessage:
    phone: str
    template_id: str
    template_data: dict[str]
    tracking_id: Optional[str] = None
