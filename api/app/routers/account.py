from fastapi import APIRouter, HTTPException
from fastapi.logger import logger
from pydantic import BaseModel
import secrets
from app.database import Cursor
from argon2 import PasswordHasher

router = APIRouter(prefix='/api/account')


@router.get("/")
async def get_all_accounts():
    with Cursor() as cur:
        try:
            cur.execute(""" SELECT id, name, surname FROM accounts LIMIT 200 """ )
        except:
            raise HTTPException(status_code=500, detail="query_failed")
        return cur.fetchall()


class NewAccount(BaseModel):
    name: str
    surname: str
    password: str

@router.post("/")
async def create_account(account: NewAccount):
    name = account.name
    surname = account.surname
    password = account.password
    #generate id
    accountid = secrets.token_hex(10)
    #generate password hash - argon2ID
    ph = PasswordHasher()
    password_hash = ph.hash(password)

    with Cursor() as cur:
        try:
            cur.execute("""
                    INSERT INTO accounts
                    (id, name, surname, password) VALUES
                    (?,  ?,    ?,       ?)
                    """, (accountid, name, surname, password_hash) )
        except:
            raise HTTPException(status_code=500, detail="query_failed")
    return {"accountid": accountid}



@router.delete("/")
async def delete_account(accountid: str):
    with Cursor() as cur:
        try:
            cur.execute("""
                    DELETE from accounts
                    WHERE id = ? """, (accountid,) )
        except:
            raise HTTPException(status_code=500, detail="query_failed")
        if cur.rowcount == 0:
            raise HTTPException(status_code=400, detail="userid_not_found")
    return {"success": True}



@router.get("/{accountid}")
async def read_user(accountid: str):
    return {"accountid": accountid}
