"""
Traceability API routes.
Exposes the requirement → signals → APIs → UI components mapping.
"""

from fastapi import APIRouter
from typing import Any, Dict, List

from backend.traceability.mapper import get_mapper

router = APIRouter(prefix="/traceability", tags=["Traceability"])


@router.get("/map", summary="Get development traceability map")
async def get_traceability_map() -> List[Dict[str, Any]]:
    """
    Return the full traceability mapping from requirements
    to extracted signals, generated APIs, and UI components.
    """
    mapper = get_mapper()
    return mapper.get_map()
