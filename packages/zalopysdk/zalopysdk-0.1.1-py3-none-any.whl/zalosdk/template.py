"""This module contains clasess and function for ZNS Template"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ZNSTplStatus(Enum):
    UNKNOWN = 0  # ZNS not defined this
    ENABLE = 1
    PENDING_REVIEW = 2
    REJECT = 3
    DISABLE = 4

    @classmethod
    def from_code(cls, code: int) -> "ZNSTplStatus":
        """
        Get ZNSTemplateStatus enum from status code

        Parameters
        ----------
        code : int
            Status code from Zalo API

        Returns
        -------
        ZNSTemplateStatus
            Corresponding enum value
        """
        for status in cls:
            if status.value == code:
                return status
        return cls.UNKNOWN

    @classmethod
    def from_name(cls, name: str) -> "ZNSTplStatus":
        """
        Get ZNSTemplateStatus enum from status name

        Parameters
        ----------
        name : str
            Status name from Zalo API

        Returns
        -------
        ZNSTemplateStatus
            Corresponding enum value
        """
        try:
            return cls[name.upper()]
        except KeyError:
            return cls.UNKNOWN

    @classmethod
    def c2n(cls, code: int) -> str:
        """
        Convert status code to status name

        Parameters
        ----------
        code : int
            Status code from Zalo API

        Returns
        -------
        str
            Status name in uppercase
        """
        status = cls.from_code(code)
        return status.name

    @classmethod
    def n2c(cls, name: str) -> int:
        """
        Convert status name to status code
        """
        status = cls.from_name(name)
        return status.value

@dataclass
class ZNSTplListRequest:
    offset: int = 0
    limit: int = 10
    status: Optional[ZNSTplStatus] = None
