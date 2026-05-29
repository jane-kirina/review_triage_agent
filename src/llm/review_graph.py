from typing import TypedDict, Optional


class ReviewGraphState(TypedDict):
    review_text: str
    review_score: Optional[int]

    category: Optional[str]
    sentiment: Optional[str]
    severity: Optional[str]
    topic: Optional[str]
    summary: Optional[str]
    suggested_action: Optional[str]
    confidence: Optional[float]

    error: Optional[str]