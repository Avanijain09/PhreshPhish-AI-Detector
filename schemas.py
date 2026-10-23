from enum import Enum
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator


class Verdict(str, Enum):
    phish = "phish"
    benign = "benign"


class IndicatorType(str, Enum):
    credential_form = "credential_form"
    brand_domain_mismatch = "brand_domain_mismatch"
    suspicious_url = "suspicious_url"
    external_form_action = "external_form_action"
    obfuscation = "obfuscation"
    urgency_language = "urgency_language"
    hidden_iframe = "hidden_iframe"
    free_hosting_abuse = "free_hosting_abuse"
    other = "other"


class Indicator(BaseModel):
    type: IndicatorType
    evidence: str = Field(
        ...,
        max_length=300,
        description="Quote or value taken directly from the input",
    )
    severity: Literal["low", "medium", "high"]


class PhishingAnalysis(BaseModel):
    verdict: Verdict
    confidence: float = Field(..., ge=0.0, le=1.0)
    impersonated_brand: Optional[str] = Field(
        default=None,
        description="Brand being imitated, null if benign/unknown",
    )
    brand_domain_match: Optional[bool] = Field(
        default=None,
        description="True if URL domain belongs to the brand",
    )
    indicators: list[Indicator] = Field(default_factory=list, max_length=8)
    rationale: str = Field(..., max_length=500)

    @field_validator("impersonated_brand")
    @classmethod
    def normalize_brand(cls, v):
        return v.strip().lower() if v else None