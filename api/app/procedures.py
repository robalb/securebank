import uuid
from fastapi import APIRouter, HTTPException
from fastapi.logger import logger

def procedure_change_balance(cur, account: str, amount: int):
    cur.execute("""
            UPDATE accounts
            SET balance = balance + ?
            WHERE id = ?
            """, (amount, account) )


def procedure_log_transfer(cur, sender: str, receiver: str, amount: int, description: str = ""):
    transactionid = str(uuid.uuid4())
    cur.execute("""
            INSERT INTO transfers
            (id, sender_id, receiver_id, amount, description) VALUES
            (?,  ?,      ?,        ?,      ?)
            """, (transactionid, sender, receiver, amount, description) )
    return transactionid

def procedure_edit_account_info(cur, accountid, name, surname):
    try:
        rowcount = 0
        if name is not None:
            cur.execute("UPDATE accounts SET name=? where id= ?", (name, accountid))
            rowcount += cur.rowcount
        if surname is not None:
            cur.execute("UPDATE accounts SET surname=? where id= ?", (surname, accountid))
            rowcount += cur.rowcount
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="transaction_failed")
    if rowcount == 0:
        raise HTTPException(status_code=400, detail="invalid_id_or_repeated_operation")
