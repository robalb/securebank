from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.logger import logger
from pydantic import BaseModel, constr
from typing import Union
import secrets
from app.database import Cursor
from argon2 import PasswordHasher
import uuid

router = APIRouter(prefix='/api/account', tags=['account'])


@router.get("/")
async def get_all_accounts():
    with Cursor() as cur:
        try:
            cur.execute("SELECT id, name, surname FROM accounts LIMIT 200" )
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
            cur.execute("DELETE from accounts WHERE id = ? ", (id,) )
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
    amount: int

@router.post("/{accountid}")
async def transfer_to_account(accountid: constr(min_length=20, max_length=20), amount: PaymentAmount):
    # raise an error on amout = 0
    if amount.amount == 0:
        raise HTTPException(status_code=422, detail=[{"msg":"invalid amount"}])

    #set the transaction description in a machine readable format
    description = "direct_payment"
    if amount.amount < 0:
        description = "direct_withdrawal"
    #attempt the transaction with autocommit disabled,
    #so that exceptions during the transaction will cause a rollback
    try:
        with Cursor(False) as cur:
            #get current balance
            cur.execute("SELECT balance FROM accounts WHERE id=?", (accountid,))
            ret = cur.fetchone()
            #handle uid not found
            if ret is None:
                raise HTTPException(status_code=400, detail="invalid_id")
            #handle not enough balance for this withdrawal
            elif amount.amount < 0 and (ret['balance'] + amount.amount) < 0:
                raise HTTPException(status_code=400, detail="insufficient_credit")
            # calculate new balance
            balance = ret['balance'] + amount.amount
            # update the new balance and log the transaction
            procedure_change_balance(cur, accountid, amount.amount)
            uid = procedure_log_transfer(cur, None, accountid, amount.amount, description)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="transaction_failed")
    return {"transaction": uid, "balance":balance}



@router.get("/{accountid}")
async def get_account_info(accountid: constr(min_length=20, max_length=20)):
    try:
        with Cursor() as cur:
            #get account info
            cur.execute("SELECT name, surname, balance FROM accounts WHERE id=?", (accountid,))
            account = cur.fetchone()
            #get transactions info
            cur.execute("""
                    SELECT id, sender_id, receiver_id, UNIX_TIMESTAMP(time) AS time, amount, description FROM transfers
                    WHERE sender_id = ? or receiver_id = ?
                    ORDER BY time ASC LIMIT 500
                    """, (accountid, accountid))
            transactions = cur.fetchall()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="transaction_failed")
    # prepare response data
    responseJSON = account | {"transactions": transactions}
    responseHeaders = {"X-Sistema-Bancario": f"{account['name']};{account['surname']}"}
    return JSONResponse(content=responseJSON, headers=responseHeaders)


class EditAccountInfo(BaseModel):
    name: Union[str, None] = None
    surname: Union[str, None] = None

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

@router.put("/{accountid}")
async def edit_account_info(accountid: constr(min_length=20, max_length=20), newdata: EditAccountInfo):
    if newdata.name is None or newdata.surname is None:
        raise HTTPException(status_code=422, detail=[{"msg":"name and surname required"}])
    with Cursor() as cur:
        procedure_edit_account_info(cur, accountid, newdata.name, newdata.surname)
    return {"success": True}


@router.patch("/{accountid}")
async def edit_account_info(accountid: constr(min_length=20, max_length=20), newdata: EditAccountInfo):
    if newdata.name is None and newdata.surname is None:
        raise HTTPException(status_code=422, detail=[{"msg":"name or surname required"}])
    with Cursor() as cur:
        procedure_edit_account_info(cur, accountid, newdata.name, newdata.surname)
    return {"success": True}


@router.head("/{accountid}")
async def weird_head(accountid: constr(min_length=20, max_length=20)):
    try:
        with Cursor() as cur:
            #get account info
            cur.execute("SELECT name, surname, balance FROM accounts WHERE id=?", (accountid,))
            account = cur.fetchone()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="transaction_failed")
    responseHeaders = {"X-Sistema-Bancario": f"{account['name']};{account['surname']}"}
    return JSONResponse(headers=responseHeaders)



