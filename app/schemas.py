"""Pydantic schemas for the Pyrenex Risk API.

TODO — Align LoanApplication with the feature_columns from your
pyrenex_risk_v2.json metadata (M1-B1 output).
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


class LoanApplication(BaseModel):
    """Input schema for /predict.

    TODO — Replace placeholder fields with the actual feature_columns
    from your pyrenex_risk_v2.json. Add Field(..., ge=…, le=…) bounds
    where your EDA showed reasonable ranges.
    """

    loan_amnt: float = Field(..., ge=500, le=40_000, description="Loan amount (USD)")
    term: Literal["36 months", "60 months"] = Field(..., description="Loan term, e.g. '36 months' or '60 months'")
    int_rate: float = Field(..., ge=0, le=50, description="Interest rate (%)")
    annual_inc: float = Field(..., ge=0, le=10_000_000, description="Annual income (USD)")
    purpose: Literal[
        "car", "credit_card", "debt_consolidation", "home_improvement",
        "major_purchase", "medical", "other", "small_business",
    ] = Field(..., description="Purpose of the loan")
    installment: float = Field(..., ge=39.99, le=1_662.33, description="Monthly installment (USD)")
    dti: float = Field(..., ge=0.82, le=50.0, description="Debt-to-income ratio")
    delinq_2yrs: int = Field(..., ge=0, le=30, description="Delinquencies in past 2 years")
    fico_range_low: int = Field(..., ge=614, le=787, description="FICO score (low end of range)")
    revol_util: Optional[float] = Field(None, ge=1.2, le=99.1, description="Revolving line utilization (%)")
    grade: Literal["A", "B", "C", "D", "E", "F", "G"] = Field(..., description="Loan grade")
    emp_length: Optional[
        Literal[
            "< 1 year", "1 year", "2 years", "3 years", "4 years", "5 years",
            "6 years", "7 years", "8 years", "9 years", "10+ years",
        ]
    ] = Field(None, description="Employment length")
    home_ownership: Literal["MORTGAGE", "OTHER", "OWN", "RENT"] = Field(..., description="Home ownership status")
    verification_status: Literal["Not Verified", "Source Verified", "Verified"] = Field(
        ..., description="Income verification status"
    )


class Prediction(BaseModel):
    """Output schema for /predict."""

    prediction: int = Field(..., description="0 = Fully Paid, 1 = Charged Off")
    probability: float = Field(..., ge=0.0, le=1.0)
    model_version: str
    request_id: str


class HealthResponse(BaseModel):
    status: str
