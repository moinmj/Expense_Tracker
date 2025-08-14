from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
import pymongo

# -------------------------
# DB setup (your existing names)
# -------------------------
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Learning"]

collection1 = db["expense"]      # expenses
collection2 = db["categories"]   # categories
collection3 = db["userr_data"]   # users
collection4 = db["role"]         # roles (email -> role)

ADMIN_EMAIL = "moinmj7@gmail.com"

app = FastAPI(title="Expense Tracker - Role Based (Simple)")

# -------------------------
# Helper utilities
# -------------------------
def objid_to_str(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert _id ObjectId to string for a single document."""
    if not doc:
        return doc
    doc = dict(doc)
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

def list_objid_to_str(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert _id ObjectId to string for list of documents."""
    result = []
    for d in docs:
        d2 = dict(d)
        if "_id" in d2:
            d2["_id"] = str(d2["_id"])
        result.append(d2)
    return result

def parse_date_str(d: str) -> datetime:
    try:
        return datetime.strptime(d, "%Y-%m-%d")
    except Exception:
        raise HTTPException(status_code=422, detail="Date must be in YYYY-MM-DD format")

def is_admin_email(email: str) -> bool:
    return email and email.lower() == ADMIN_EMAIL.lower()

def ensure_user_exists(email: str):
    if not collection3.find_one({"email": email}):
        raise HTTPException(status_code=404, detail="User not found")

def ensure_admin(email: str):
    """Simple admin guard by email (only ADMIN_EMAIL)."""
    if not is_admin_email(email):
        raise HTTPException(status_code=403, detail="Admin access required")

# -------------------------
# Pydantic models
# -------------------------
class RegisterModel(BaseModel):
    username: str
    email: str
    password: str
    First_name: Optional[str] = ""
    Middle_name: Optional[str] = ""
    Last_name: Optional[str] = ""

class LoginModel(BaseModel):
    email: str
    password: str

class ExpenseIn(BaseModel):
    amount: float
    category: str
    date: str = Field(..., description="YYYY-MM-DD")
    description: Optional[str] = ""
    user_email: str

class UpdateExpenseModel(BaseModel):
    expense_id: str
    amount: Optional[float] = None
    category: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None

class CategoryIn(BaseModel):
    category: str

class UpdateCategoryModel(BaseModel):
    category_id: str
    category: str

class UpdateUserModel(BaseModel):
    username: Optional[str] = None
    First_name: Optional[str] = None
    Middle_name: Optional[str] = None
    Last_name: Optional[str] = None
    password: Optional[str] = None

# -------------------------
# AUTH: Register & Login
# -------------------------
@app.post("/register")
def register(user: RegisterModel):
    # Prevent duplicate email
    if collection3.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    # store plain password (kept intentionally as in your code)
    user_doc = {
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "First_name": user.First_name,
        "Middle_name": user.Middle_name,
        "Last_name": user.Last_name
    }
    collection3.insert_one(user_doc)

    # assign role in collection4
    role_value = "admin" if is_admin_email(user.email) else "user"
    collection4.insert_one({"email": user.email, "role": role_value})

    return {"message": "User registered successfully", "role": role_value}

@app.post("/login")
def login(data: LoginModel):
    user = collection3.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # fix: compare provided password with stored password
    if data.password != user.get("password"):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # fetch role
    role_doc = collection4.find_one({"email": data.email})
    role_value = role_doc["role"] if role_doc else "user"
    return {"message": "Login successful", "email": data.email, "role": role_value}

# -------------------------
# Add Expense (user)
# -------------------------
@app.post("/add-expense")
def add_expense(expense: ExpenseIn):
    # user must exist
    ensure_user_exists(expense.user_email)

    # category normalization/check
    cat = (expense.category or "").strip().lower()
    existing_cat = collection2.find_one({"category": cat}) or collection2.find_one({"name": cat})
    # allow expense even if category not present (as before)

    # parse date and store month
    _ = parse_date_str(expense.date)
    month = _.month

    doc = {
        "amount": float(expense.amount),
        "category": cat,
        "date": expense.date,
        "month": month,
        "description": expense.description or "",
        "user_email": expense.user_email
    }
    res = collection1.insert_one(doc)
    return {"message": "Expense added successfully", "expense_id": str(res.inserted_id)}

# -------------------------
# Get My Expenses
# -------------------------
@app.get("/get-my-expenses")
def get_my_expenses(email: str = Query(..., description="Your login email")):
    ensure_user_exists(email)
    docs = list(collection1.find({"user_email": email}))
    return {"email": email, "expenses": list_objid_to_str(docs)}

# -------------------------
# Get My Categories (distinct categories used by this user)
# -------------------------
@app.get("/get-my-categories")
def get_my_categories(email: str = Query(...)):
    ensure_user_exists(email)
    cats = collection1.distinct("category", {"user_email": email})
    return {"email": email, "categories": cats}

# -------------------------
# Get Expenses By Month
# -------------------------
@app.get("/expensebymonth/")
def get_expenses_by_month(email: str = Query(...), month: int = Query(..., ge=1, le=12)):
    ensure_user_exists(email)
    docs = list(collection1.find({"user_email": email, "month": month}))
    return list_objid_to_str(docs)

# -------------------------
# Top 3 categories for a user
# -------------------------
@app.get("/get-top-categories")
def get_top_categories(email: str = Query(...)):
    ensure_user_exists(email)
    pipeline = [
        {"$match": {"user_email": email}},
        {"$group": {"_id": "$category", "total_amount": {"$sum": "$amount"}}},
        {"$sort": {"total_amount": -1}},
        {"$limit": 3}
    ]
    data = list(collection1.aggregate(pipeline))
    return [{"category": d["_id"], "total_amount": d["total_amount"]} for d in data]

# -------------------------
# Update My Expense (user can update only their expense)
# -------------------------
@app.put("/update-my-expense")
def update_my_expense(email: str = Query(...), payload: UpdateExpenseModel = None):
    if payload is None:
        raise HTTPException(status_code=400, detail="No update payload provided")
    # ensure expense exists and belongs to user
    try:
        oid = ObjectId(payload.expense_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expense id")

    exp = collection1.find_one({"_id": oid})
    if not exp:
        raise HTTPException(status_code=404, detail="Expense not found")
    if exp.get("user_email") != email:
        raise HTTPException(status_code=403, detail="Not authorized to update this expense")

    update_fields = {}
    if payload.amount is not None:
        update_fields["amount"] = float(payload.amount)
    if payload.category:
        update_fields["category"] = payload.category.strip().lower()
    if payload.date:
        _ = parse_date_str(payload.date)
        update_fields["date"] = payload.date
        update_fields["month"] = _.month
    if payload.description is not None:
        update_fields["description"] = payload.description

    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    collection1.update_one({"_id": oid}, {"$set": update_fields})
    return {"message": "Expense updated successfully"}

# -------------------------
# Admin: View all users (hide passwords)
# -------------------------
@app.get("/view-all-users")
def view_all_users(email: str = Query(...)):
    ensure_admin(email)
    users = list(collection3.find({}, {"password": 0}))
    return {"users": list_objid_to_str(users)}

# -------------------------
# Admin: Delete user (by user_id)
# -------------------------
@app.delete("/delete-user/{user_id}")
def delete_user(user_id: str = Path(...), email: str = Query(...)):
    ensure_admin(email)
    try:
        oid = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user id")

    # fetch user doc to get email to cleanup role & expenses
    user_doc = collection3.find_one({"_id": oid})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    user_email = user_doc.get("email")

    # delete user
    res = collection3.delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    # delete role doc for that email
    collection4.delete_many({"email": user_email})
    # delete their expenses
    collection1.delete_many({"user_email": user_email})

    return {"message": "User and related data deleted successfully"}

# -------------------------
# Admin: Update user (by user_id)
# -------------------------
@app.put("/update-user/{user_id}")
def update_user(user_id: str = Path(...), email: str = Query(...), updates: UpdateUserModel = None):
    ensure_admin(email)
    if updates is None:
        raise HTTPException(status_code=400, detail="No update data provided")

    try:
        oid = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user id")

    update_fields = {}
    if updates.username is not None:
        update_fields["username"] = updates.username
    if updates.First_name is not None:
        update_fields["First_name"] = updates.First_name
    if updates.Middle_name is not None:
        update_fields["Middle_name"] = updates.Middle_name
    if updates.Last_name is not None:
        update_fields["Last_name"] = updates.Last_name
    if updates.password is not None:
        update_fields["password"] = updates.password

    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    res = collection3.update_one({"_id": oid}, {"$set": update_fields})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}

# -------------------------
# Admin: Add Category
# -------------------------
@app.post("/add-category")
def add_category(email: str = Query(...), payload: CategoryIn = None):
    ensure_admin(email)
    if not payload or not payload.category:
        raise HTTPException(status_code=400, detail="Category is required")
    cat = payload.category.strip().lower()
    if collection2.find_one({"category": cat}) or collection2.find_one({"name": cat}):
        raise HTTPException(status_code=400, detail="Category already exists")
    collection2.insert_one({"category": cat})
    return {"message": "Category added successfully"}

# -------------------------
# Admin: Update Category
# -------------------------
@app.put("/update-category")
def update_category(email: str = Query(...), payload: UpdateCategoryModel = None):
    ensure_admin(email)
    if not payload:
        raise HTTPException(status_code=400, detail="Payload required")
    try:
        oid = ObjectId(payload.category_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid category id")
    new_name = (payload.category or "").strip().lower()
    if not new_name:
        raise HTTPException(status_code=400, detail="New category name required")
    res = collection2.update_one({"_id": oid}, {"$set": {"category": new_name}})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category updated successfully"}

# -------------------------
# Admin: Delete Category
# -------------------------
@app.delete("/delete-category/{category_id}")
def delete_category(category_id: str = Path(...), email: str = Query(...)):
    ensure_admin(email)
    try:
        oid = ObjectId(category_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid category id")
    res = collection2.delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}

# -------------------------
# Admin: View All Expenses
# -------------------------
@app.get("/view-all-expenses")
def view_all_expenses(email: str = Query(...)):
    ensure_admin(email)
    docs = list(collection1.find())
    return {"expenses": list_objid_to_str(docs)}

# -------------------------
# Utility endpoints
# -------------------------
@app.get("/categories")
def fetch_categories_only():
    # Try to return distinct names in categories collection
    cats = collection2.distinct("category")
    if not cats:
        # maybe categories stored with "name" field
        cats = collection2.distinct("name")
    return cats

@app.get("/categories-full")
def fetch_categories_full():
    """Return full category documents (with _id) for admin management in frontend."""
    docs = list(collection2.find())
    return {"categories": list_objid_to_str(docs)}
