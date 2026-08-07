"""
Vendor Lookup Result.
"""

from dataclasses import dataclass

from app.vendors.vendor_record import Vendor


@dataclass
class VendorLookupResult:
    """
    Result returned after looking up (and recording activity for)
    a vendor in the Vendor Database.
    """

    vendor: Vendor

    is_new_vendor: bool = False

    is_blocked: bool = False

    reason: str = ""
