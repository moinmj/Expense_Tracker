# from fastapi import FastAPI , Path , Query ,HTTPException, status
# from pydantic import BaseModel, Field
# from typing import Optional
# import pymongo
# from datetime import date, datetime
# # import Apifunction
# # from motor.motor_asyncio import AsyncIOMotorClient
# print("Welcome to pmongo")
# client=pymongo.MongoClient("mongodb://localhost:27017/") #this here is connection to by database
# print(client)
# db=client["Learning"] #making database name,forming a database
# collection=db["expense"]
# collection1=db["categories"]
# collection2=db["userr_data"]
# collection3=db["role"]

# app=FastAPI()

# class Expense(BaseModel):
#     amount:int 
#     category:str | dict
#     date:str=Field(...,description="Provide in YYYY-MM-DD format",example="YYYY-MM-DD") #These here are fields especially given description to date field to provide format of date
#     description:str
#     email:str
# class Cat(BaseModel):
#     category:str
# class User_data(BaseModel):
#     username:str
#     first_name:str
#     middle_name:str
#     last_name:str
#     email:str
#     password:str
#     Role:str
# class Role_data(BaseModel):
#     Role:str
# class LoginRequest(BaseModel):
#     username_or_email: str
#     password: str
#     # Role:str
# # inventory = {}
# #experiments

# # I am trying pull request

# #what is happening
# def break_date(date): #defined a function for breaking time

#     date = date #format YYYY-MM-DD
#     date_obj = datetime.strptime(date, "%Y-%m-%d") #This is a function or method that is used to break date in year,Month and day imported from datetime library
#     # date_obj = datetime.strptime(date, "%Y-%m-%d") #This is a function or method that is used to break date in year,Month and day imported from datetime library
#     # month = date_obj.month #seperated month and stored in variable month
#     return date_obj




# @app.post("/expense/{item_id}")
# def add_expense(item_id: int,email:str, expense: Expense):
#     if collection.find_one({"item_id": item_id}):
#         raise HTTPException(status_code=400, detail="Item ID already exists")
    
#     month = break_date(expense.date)
#     expense_data = {
#         "item_id": item_id,
#         "amount": expense.amount,
#         "category": expense.category.lower(),
#         "date":expense.date,
#         "month": month,
#         "description": expense.description,
#         "email":expense.email
#     }
#     collection.insert_one(expense_data)
#     return {"message": "Expenses added successfully"}
# #Post Api for user data
# @app.post("/user_data/")
# def add_userdata( user: User_data):
#     if collection2.find_one({"$or": [{"username": user.username},{"email": user.email}]}):
#         raise HTTPException(status_code=400, detail="Username or email already exists")

    
    
#     user_dataa = {
#         "username": user.username,
#         "first_name": user.first_name,
#         "middle_name": user.middle_name,
#         "last_name":user.last_name,
#         "email": user.email,
#         "password": user.password,
#         # "Role":user.Role
#     }
#     collection2.insert_one(user_dataa)
#     return {"message": "User Data added successfully"}
# @app.post("/login/")
# def login_user(login_data: LoginRequest):
#     # Try to find the user by username OR email
#     user = collection2.find_one({
#         "$or": [
#             {"username": login_data.username_or_email},
#             {"email": login_data.username_or_email}
#             # {"Role": login_data.Role},

#         ]
#     })

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     if user["password"] != login_data.password:
#         raise HTTPException(status_code=401, detail="Incorrect password")
#     user["_id"] = str(user["_id"])

#     return {
#         "message": "Login successful",
#         "user": user
#     }

# @app.post("/role/")
# def add_userdata(Role: str, role: Role_data):
    
#     rolee_dataa = {
#         "Role": Role,
#     }
#     collection3.insert_one(rolee_dataa)
#     return {"message": "Role added successfully"}
# @app.get("/yourexpensebymail/")
# def get_expensebyemailpassword(*,email: str,password:str):
#     expense = collection2.find_one({"email": email,"password":password})
#     if not expense:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
#     if "_id" in expense:
#         expense["_id"] = str(expense["_id"])
#     return expense
# @app.get("/role/{Role}")
# def get_expense(Role: str = Path(description="The Role you want to retrieve")):
#     expense = collection3.find_one({"Role": Role})
#     if not expense:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
#     if "_id" in expense:
#         expense["_id"] = str(expense["_id"])
#     return expense
# @app.get("/categories")
# def fetch_categories_only():
#     categories = collection1.distinct("category")  # only unique category values
    
#     if not categories:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="No categories found"
#         )

#     return categories


# # @app.get("/get-item-by-category/")
# # def fetch_items_by_category():
# #     categories = list(collection1.find())
# #     if not categories:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No expenses found for this category")
# #     for expense in categories:
# #         if "_id" in categories:
# #             expense["_id"] = str(expense["_id"])
# #             return categories 
# #     # return fetch_items_by_category()
# # @app.get("/categories")
# # def get_all_categories_from_collection1():
# #     categories = list(collection1.find())
# #     for category in categories:
# #         if "_id" in category:
# #             category["_id"] = str(category["_id"])

# @app.post("/expense-by-category/{_id}")
# def add_expense_by_category(_id: int = Path(description="Provide id in 0,1,2...and so on"),category: str = Query(description="only give these three items as food,salary,clothes"),cat:Cat =None):
#     @app.get("/get-item-by-category/")
#     def get_item_by_category(*,category:str= Query(...,description="You can get any category")):
#         expenses=list(collection.find({"category":category}))
#         if not expenses:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No expenses found for this categpry")
#         for expense in expenses:
#             if "_id" in expense:
#                 expense["_id"] = str(expense["_id"])
#         return expenses
#     if cat is None:
#         raise HTTPException(status_code=400, detail="Request body is required")
        
#     category_data = {
#         "_id": _id,
#         "category": category.lower()
#     }
    
#     try:
#         collection1.insert_one(category_data)
#         return {"message": "Category added successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # @app.get("/bygategory/{_id}")
# # def get_expense(_id: int = Path(description="The _id of the expense to retrieve,Should be in 0,1,2.....any number")):
# #     expenseee = collection1.find_one({"_id":_id})
# #     if not expenseee:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
# #     if "_id" in expenseee:
# #         expenseee["_id"] = str(expenseee["_id"])
#     # return expenseee

# # @app.get("/allexpense/{item_id}")
# # def get_expense(item_id: int = Path(description="The ID of the expense to retrieve")):
# #     expense = collection.find_one({"item_id": item_id})
# #     if not expense:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
# #     if "_id" in expense:
# #         expense["_id"] = str(expense["_id"])
# #     return expense
# @app.get("/allexpense/{email}")
# def get_expense(email: str = Path(description="The ID of the expense to retrieve")):
#     expense = list(collection.find({"email": email}))
#     if not expense:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
#     if "_id" in expense:
#         expense["_id"] = str(expense["_id"])
#     return expense
# @app.get("/allexpensess")
# def get_all_expenses():
#     expenses = list(collection.find())
#     for expense in expenses:
#         if "_id" in expense:
#             expense["_id"] = str(expense["_id"])
#     return expenses
# @app.get("/expensebydate/", summary="Get expenses by item ID and date range")
# def get_expense(
#     *,start_date: date = Query(description="Start date in YYYY-MM-DD format", example="2025-01-01"),  # item_id: int = Path(description="The ID of the expense to retrieve"),
#     end_date: date = Query(description="End date in YYYY-MM-DD format", example="2025-01-31")
# ):
#     query={
#         "date": {
#             "$gte": start_date.isoformat(),
#             "$lte":end_date.isoformat()

#         }
#     }
#     expenses=list(collection.find({query}))
#     if not expenses:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No expenses found for this categpry")
#     for expense in expenses:
#         if "_id" in expense:
#             expense["_id"] = str(expense["_id"])
#     return expenses

# @app.get("/categories")
# def get_all_categories_from_collection1():
#     categories = list(collection1.find())
#     for category in categories:
#         if "_id" in category:
#             category["_id"] = str(category["_id"])
# #     return categories
# # @app.get("/categoriess")
# # def get_all_categories_from_collection():
# #     categoriess = list(collection.find({},{"_id":0,"category":1}))
# #     # for category in categoriess:
# #     #     if "_id" in category:
# #     #         category["_id"] = str(category["_id"])
# #     return [{"category": category["category"]} for category in categoriess]
# #     # return categoriess
# @app.get("/get-item-by-category/")
# def get_item_by_category(*,category:str= Query(...,description="You can get any category")):
#     expenses=list(collection.find({"category":category}))
#     if not expenses:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No expenses found for this categpry")
#     for expense in expenses:
#         if "_id" in expense:
#             expense["_id"] = str(expense["_id"])
#     return expenses

# @app.get("/expensebymonth/")
# def get_expenses_by_month(month: int = Query(..., description="Month as a number (1-12)")):
#     # Fetch all records
#       # Use empty filter to get all documents
#     expenses = list(collection.find({ "month":month}))
#     if not expenses:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No expenses found for this month")
#     # Filter based on the month extracted from string-formatted date
#     # filtered_expenses = []
#     for expense in expenses:
#          if "_id" in expense:
#             expense["_id"] = str(expense["_id"])
#     return expenses
# @app.get("/top-categories")
# def get_top_categories():
#     expense = [{"$group": {"_id": "$category", "total_amount": {"$sum": "$amount"}}},
#         {"$sort": {"total_amount": -1}},
#         {"$limit": 3}
#     ]
#     # expense = [
#     #     {"$group": {"_id": "$category", "total_amount": {"$sum": "$amount"}}},
#     #     {"$sort": {"total_amount": -1}},
#     #     {"$limit": 3}
#     # ]
#     expenses = list(collection.aggregate(expense))
#     return expenses
#     # result = list(collection.aggregate(expense))
#     # return [{"category": r["_id"], "total_amount": r["total_amount"]} for r in result]
from fastapi import FastAPI, HTTPException,Query
import pymongo
from collections import defaultdict
from datetime import date,datetime
from pydantic import BaseModel, Field
from typing import Optional

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Learning"]
collection1=db["expense"]
collection3=db["categories"]
collection2=db["userr_data"]

app = FastAPI()

class Expense(BaseModel):
    amount:int 
    category:str | dict
    date:str=Field(...,description="Provide in YYYY-MM-DD format",example="YYYY-MM-DD") #These here are fields especially given description to date field to provide format of date
    description:str
    user_email:str
@app.post("/register")
def register(username: str, email: str, password: str,First_name:str,Middle_name:str,Last_name:str):
    if collection2.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    collection2.insert_one({"username": username, "email": email, "password": password,"First_name":First_name,"Middle_name":Middle_name,"Last_name":Last_name})
    return {"message": "User registered successfully"}

@app.post("/login")
def login(email: str, password: str):
    user = collection2.find_one({"email": email})
    if not user or user["password"] != password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful", "email": email}

def break_date(date): #defined a function for breaking time

    date = date #format YYYY-MM-DD
    date_obj = datetime.strptime(date, "%Y-%m-%d") #This is a function or method that is used to break date in year,Month and day imported from datetime library
    date_obj = datetime.strptime(date, "%Y-%m-%d") #This is a function or method that is used to break date in year,Month and day imported from datetime library
    month = date_obj.month #seperated month and stored in variable month
    return month

@app.post("/add-expense")
def add_expense(expense:Expense):
    month=break_date(expense.date)
    expense = {
        "amount": expense.amount,
        "category": expense.category.lower(),
        "date":expense.date,
        "month": month,
        "description": expense.description,
        "user_email":expense.user_email
    }
    collection1.insert_one(expense)
    return {"message": "Expense added successfully"}
@app.get("/categories")
def fetch_categories_only():
    categories = collection3.distinct("category")  # only unique category values
    
    if not categories:
        raise HTTPException(status_code=400, detail="No categories found")
    return categories
@app.get("/get-my-expenses")
def get_my_expenses(email: str):
    expenses = list(collection1.find({"user_email": email}))
    for exp in expenses:
        exp["_id"] = str(exp["_id"])
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found for this user")
    return {"email": email, "expenses": expenses}

@app.get("/get-my-categories")
def get_my_categories(email: str):
    categories = collection1.distinct("category", {"user_email": email})
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found for this user")
    return {"email": email, "categories": categories}
@app.get("/expensebymonth/")
def get_expenses_by_month(email:str,month: int = Query(..., description="Month as a number (1-12)")):
    monthh = list(collection1.find({ "user_email":email,"month":month}))
    if not monthh:
        raise HTTPException(status_code=404, detail="No expenses found for this month")
    for expense in monthh:
         if "_id" in expense:
            expense["_id"] = str(expense["_id"])
    return monthh
# @app.get("/get-top-category")
# def get_top_category(email: str):
#     expenses = list(collection1.find({"user_email": email}))
#     if not expenses:
#         raise HTTPException(status_code=404, detail="No expenses found for this user")

#     category_totals = defaultdict(float)
#     for exp in expenses:
#         category_totals[exp["category"]] += exp["amount"]

#     top_category = max(category_totals, key=category_totals.get)
#     return {
#         "email": email,
#         "top_category": top_category,
#         "amount": category_totals[top_category]
#     }
@app.get("/get-top-categories")
def get_top_categories(email:str):
    expense = [{"$match":{"user_email":email}},{"$group": {"_id": "$category", "total_amount": {"$sum": "$amount"}}},
        {"$sort": {"total_amount": -1}},
        {"$limit": 3}
    ]
    return list(collection1.aggregate(expense))