from fastapi import APIRouter, HTTPException
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
          ret = cur.fetchone()
          #handle uuid not found
          if ret is None:
              raise HTTPException(status_code=400, detail="invalid_id")
          # handle not a transaction
          if ret['receiver_id'] is None:
              raise HTTPException(status_code=400, detail="not_a_transaction")
          # get information associated to involved parts
          cur.execute("SELECT balance FROM accounts WHERE id=?", (ret['sender_id'],))
          ret_from = cur.fetchone()
          cur.execute("SELECT balance FROM accounts WHERE id=?", (ret['receiver_id'],))
          ret_to = cur.fetchone()
          #handle uid not found (deleted account)
          if ret_from is None or ret_to is None:
              raise HTTPException(status_code=400, detail="cannot_revert")
          #handle insufficient credit
          if ret_to['balance'] < ret['amount']:
              raise HTTPException(status_code=400, detail="insufficient_credit")
          # update the new balance in both accounts, and log the transaction
          description = f"revert_{ret['id']}"
          procedure_change_balance(cur, ret['sender_id'], ret['amount'])
          procedure_change_balance(cur, ret['receiver_id'], -ret['amount'])
          uid = procedure_log_transfer(cur, ret['receiver_id'], ret['sender_id'], ret['amount'], description)
  except HTTPException as e:
      raise e
  except Exception as e:
      logger.error(e)
      raise HTTPException(status_code=500, detail="transaction_failed")
  # calculate new balance - for presentation purpose only, may be subject to race conditions
  balance_from = ret_from['balance'] + ret['amount']
  balance_to   = ret_to['balance'] - ret['amount']
  # caluclate new balance edge case - where from and to are the same
  if ret['sender_id'] == ret['receiver_id']:
    balance_from = balance_to = ret_from['balance']
  return {"transaction": uid, "balance_from": balance_from, "balance_to": balance_to}
