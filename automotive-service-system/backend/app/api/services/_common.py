from __future__ import annotations

from typing import Any, TypeVar

from fastapi import HTTPException
from sqlalchemy.orm import Session


TModel = TypeVar("TModel")


def get_or_404(db: Session, model: type[TModel], obj_id: int, *, detail: str) -> TModel:
    obj = db.get(model, obj_id)
    if not obj:
        raise HTTPException(status_code=404, detail=detail)
    return obj


def apply_partial_update(obj: Any, data: dict[str, Any]) -> None:
    for key, value in data.items():
        setattr(obj, key, value)
