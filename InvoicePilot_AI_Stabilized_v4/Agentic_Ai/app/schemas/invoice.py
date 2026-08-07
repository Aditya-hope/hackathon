from typing import List, Optional

from pydantic import BaseModel, Field


class LineItem(BaseModel):
    """
    Represents a single line item in an invoice.
    """

    description: Optional[str] = None

    quantity: Optional[float] = Field(
        default=0,
        ge=0,
    )

    unit_price: Optional[float] = Field(
        default=0,
        ge=0,
    )

    amount: Optional[float] = Field(
        default=0,
        ge=0,
    )


class Invoice(BaseModel):
    """
    Structured invoice extracted by the AI.
    """

    vendor_name: Optional[str] = Field(
        default=None,
        description="Supplier or vendor name",
    )

    invoice_number: Optional[str] = Field(
        default=None,
        description="Unique invoice number",
    )

    invoice_date: Optional[str] = Field(
        default=None,
        description="Invoice issue date",
    )

    due_date: Optional[str] = None

    currency: str = Field(
        default="INR",
        description="Invoice currency",
    )

    subtotal: float = Field(
        default=0,
        ge=0,
    )

    tax: float = Field(
        default=0,
        ge=0,
    )

    total_amount: Optional[float] = Field(
        default=0,
        ge=0,
    )

    gst_number: Optional[str] = None

    purchase_order: Optional[str] = None

    payment_terms: Optional[str] = None

    line_items: List[LineItem] = Field(
        default_factory=list,
    )

    confidence: float = Field(
        default=95,
        ge=0,
        le=100,
    )