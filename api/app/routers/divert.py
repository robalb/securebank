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
  #attempt the transaction with autocommit disabled,
  #so that exceptions during the transaction will cause a rollback
  try:
      with Cursor(False) as cur:
          #get informations associated to uuid
          cur.execute("SELECT * FROM transfers WHERE id=?", (str(d.uid),))
          res = cur.fetchone()
          logger.error(res)
  except HTTPException as e:
      raise e
  except Exception as e:
      logger.error(e)
      raise HTTPException(status_code=500, detail="transaction_failed")
  # calculate new balance - for presentation purpose only, may be subject to race conditions
