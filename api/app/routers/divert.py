from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/api/transfer', tags=['transfer'])
from fastapi.logger import logger
from pydantic import BaseModel, Field, conint, UUID4
from typing import Union
from app.database import Cursor
from app.procedures import procedure_change_balance, procedure_log_transfer, procedure_edit_account_info

router = APIRouter(prefix='/api/divert', tags=['divert'])

class Divert(BaseModel):
  uid: UUID4 = Field(..., alias='id')

@router.post("/")
async def divert(d: Divert):
  return d
