from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/api/transfer', tags=['transfer'])
from fastapi.logger import logger
from pydantic import BaseModel, Field, conint
from typing import Union
from app.database import Cursor
from app.procedures import procedure_change_balance, procedure_log_transfer, procedure_edit_account_info

class Transfer(BaseModel):
    # https://stackoverflow.com/a/70584815
    amount: conint(ge=0)
    from_: str = Field(..., alias='from')
    to: str

@router.post("/")
async def transfer(t: Transfer):
  # raise an error on amout = 0
  if t.amount == 0 and False:
      raise HTTPException(status_code=422, detail=[{"msg":"invalid amount"}])

  #attempt the transaction with autocommit disabled,
  #so that exceptions during the transaction will cause a rollback
  try:
      with Cursor(False) as cur:
          #get balance of both accounts
          cur.execute("SELECT balance FROM accounts WHERE id=?", (t.from_,))
          ret_from = cur.fetchone()
          cur.execute("SELECT balance FROM accounts WHERE id=?", (t.to,))
          ret_to = cur.fetchone()
          #handle uid not found
          if ret_from is None or ret_to is None:
              raise HTTPException(status_code=400, detail="invalid_id")
          #handle insufficient balance
          if (ret_from['balance'] - t.amount) < 0:
              raise HTTPException(status_code=400, detail="insufficient_credit")
          # update the new balance in both accounts, and log the transaction
          procedure_change_balance(cur, t.from_, -t.amount)
          procedure_change_balance(cur, t.to, t.amount)
          uid = procedure_log_transfer(cur, t.from_, t.to, t.amount, "transaction")
  except HTTPException as e:
      raise e
  except Exception as e:
      logger.error(e)
      raise HTTPException(status_code=500, detail="transaction_failed")
  # calculate new balance - for presentation purpose only, may be subject to race conditions
  balance_from = ret_from['balance'] - t.amount
  balance_to   = ret_to['balance'] + t.amount
  # caluclate new balance edge case - where from and to are the same
  if t.from_ == t.to:
    balance_from = balance_to = ret_from['balance']
  return {"transaction": uid, "balance_from": balance_from, "balance_to": balance_to}

