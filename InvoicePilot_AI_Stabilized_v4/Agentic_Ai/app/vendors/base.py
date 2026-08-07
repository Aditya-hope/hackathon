"""
Base Vendor Repository.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.vendors.vendor_record import Vendor
from app.vendors.vendor_result import VendorLookupResult

if TYPE_CHECKING:
    from app.schemas.invoice import Invoice


class BaseVendorRepository(ABC):
    """
    Storage contract for the Vendor Database.
    """

    @abstractmethod
    def get(
        self,
        name: str,
    ) -> Vendor | None:

        raise NotImplementedError

    @abstractmethod
    def list_all(
        self,
    ) -> list[Vendor]:

        raise NotImplementedError

    @abstractmethod
    def record_invoice(
        self,
        invoice: "Invoice",
    ) -> VendorLookupResult:

        raise NotImplementedError
