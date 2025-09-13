from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class SubErrorResponse(BaseModel):
    status: str
    http_status: int
    message: str
    step: str


class ErrorResponse(BaseModel):
    detail: dict


class ChatRequest(BaseModel):
    message: str
    user_id: str


class ChatResponse(BaseModel):
    content: str
    user_id: str
    message_id: Optional[str] = None


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


class SearchResult(BaseModel):
    node_id: str
    text: str
    score: float
    metadata: Dict[str, Any]


class SearchResponse(BaseModel):
    results: List[SearchResult]
    query: str
    total_results: int
