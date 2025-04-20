

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Bankily API",
    description="A simple banking system API allowing users to send and receive money using a Mauritanian phone number (+222)",
    version="1.0"
)

# -----------------------------
# STEP 1: Define data models
# -----------------------------

class User(BaseModel):
    phone: str  # E.g., '+222XXXXXXXXX'
    name: str
    balance: float

class UserCreate(BaseModel):
    phone: str
    name: str

class Transaction(BaseModel):
    sender_phone: str
    receiver_phone: str
    amount: float

class Deposit(BaseModel):
    phone: str
    amount: float

# -----------------------------
# STEP 2: In-memory storage
# -----------------------------

users: List[User] = []

# -----------------------------
# STEP 3: GET Endpoints
# -----------------------------

@app.get("/", summary="Welcome Message")
def read_root():
    # DO MAGIC
    return {"message": "Welcome to Bankily API!"}

@app.get("/users", response_model=List[User], summary="Get all users")
def get_all_users():
    return users

@app.get("/users/{phone}", response_model=User, summary="Get a user by phone number")
def get_user_by_phone(phone: str):
    for user in users:
        if user.phone == phone:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# -----------------------------
# STEP 4: POST Endpoints
# -----------------------------

@app.post("/users", response_model=User, summary="Create a new user")
def create_user(new_user: UserCreate):
    if any(user.phone == new_user.phone for user in users):
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(phone=new_user.phone, name=new_user.name, balance=0.0)
    users.append(user)
    return user

@app.post("/deposit", summary="Deposit money to a user account")
def deposit_money(deposit: Deposit):
    for user in users:
        if user.phone == deposit.phone:
            user.balance += deposit.amount
            return {"message": "Deposit successful", "balance": user.balance}
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/transfer", summary="Transfer money from one user to another")
def transfer_money(transaction: Transaction):
    sender = next((u for u in users if u.phone == transaction.sender_phone), None)
    receiver = next((u for u in users if u.phone == transaction.receiver_phone), None)

    if not sender:
        raise HTTPException(status_code=404, detail="Sender not found")
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")
    if sender.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    sender.balance -= transaction.amount
    receiver.balance += transaction.amount

    return {"message": "Transfer successful", "sender_balance": sender.balance, "receiver_balance": receiver.balance}

# -----------------------------
# STEP 5: PATCH Endpoint
# -----------------------------

@app.patch("/users/{phone}", response_model=User, summary="Update user information")
def update_user(phone: str, update: UserCreate):
    for user in users:
        if user.phone == phone:
            user.name = update.name
            return user
    raise HTTPException(status_code=404, detail="User not found")

# -----------------------------
# STEP 6: DELETE Endpoint
# -----------------------------

@app.delete("/users/{phone}", summary="Delete a user")
def delete_user(phone: str):
    global users
    for user in users:
        if user.phone == phone:
            users = [u for u in users if u.phone != phone]
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

