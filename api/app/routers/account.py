from fastapi import APIRouter, HTTPException
from fastapi.logger import logger
from pydantic import BaseModel, Field
from typing import Union
import secrets
from app.database import Cursor
from argon2 import PasswordHasher
import uuid

router = APIRouter(prefix='/api/account')


@router.get("/")
async def get_all_accounts():
    with Cursor() as cur:
        try:
            cur.execute(""" SELECT id, name, surname FROM accounts LIMIT 200 """ )
        except:
            raise HTTPException(status_code=500, detail="transaction_failed")
        return cur.fetchall()


class NewAccount(BaseModel):
    name: str
    surname: str
    password: str

@router.post("/")
async def create_account(account: NewAccount):
    #generate id
    accountid = secrets.token_hex(10)
    #generate password hash - argon2ID
    ph = PasswordHasher()
    password_hash = ph.hash(account.password)

    with Cursor() as cur:
        try:
            cur.execute("""
                    INSERT INTO accounts
                    (id, name, surname, password) VALUES
                    (?,  ?,    ?,       ?)
                    """, (accountid, account.name, account.surname, password_hash) )
        except:
            raise HTTPException(status_code=500, detail="transaction_failed")
    return {"id": accountid}



@router.delete("/")
async def delete_account(id: str):
    with Cursor() as cur:
        try:
            cur.execute("""
                    DELETE from accounts
                    WHERE id = ? """, (id,) )
        except:
            raise HTTPException(status_code=500, detail="transaction_failed")
        if cur.rowcount == 0:
            raise HTTPException(status_code=400, detail="invalid_id")
    return {"success": True}


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


class PaymentAmount(BaseModel):
    # https://pydantic-docs.helpmanual.io/usage/types/#arguments-to-conint
    amount: int

@router.post("/{accountid}")
async def transfer_to_account(accountid: str, amount: PaymentAmount):
    #TODO: this input validation should be handled by pydantic
    if amount.amount == 0:
        raise HTTPException(status_code=422, detail=[{"msg":"invalid amount"}])

    #set the transaction description in a machine readable format
    description = "direct_payment"
    if amount.amount < 0:
        description = "direct_withdrawal"
    #attempt the transaction with autocommit disabled,
    #so that exceptions during the transaction will cause a rollback
        with Cursor(False) as cur:
            procedure_change_balance(cur, accountid, amount.amount)
            procedure_log_transfer(cur, None, accountid, amount.amount, description)
            #cur.execute("SELECT balance FROM accounts WHERE id = ?", (accountid,))
            # balance = cur.fetchone()
    return {"id": accountid}


