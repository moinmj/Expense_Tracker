from fastapi import FastAPI , Path , Query ,HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
import pymongo
from datetime import date, datetime
import Apifunction
# from motor.motor_asyncio import AsyncIOMotorClient
print("Welcome to pmongo")
client=pymongo.MongoClient("mongodb://localhost:27017/") #this here is connection to by database
print(client)
db=client["Learning"] #making database name,forming a database
collection=db["expense"]
collection1=db["categories"]

app=FastAPI()

class Expense(BaseModel):
    amount:int 
    # category:str
    date:str=Field(...,description="Provide in YYYY-MM-DD format",example="YYYY-MM-DD") #These here are fields especially given description to date field to provide format of date
    # start_date:Optional[date]=Query(None,description="Provide in YYYY-MM-DD format")
    # end_date:str=Field(...,description="Provide in YYYY-MM-DD format",example="YYYY-MM-DD")
    description:str
class Cat(BaseModel):
    item_id:int
    category:str
# inventory = {}
#experiments

# I am trying pull request

#what is happening
def break_date(date): #defined a function for breaking time

    date = date #format YYYY-MM-DD
    date_obj = datetime.strptime(date, "%Y-%m-%d") #This is a function or method that is used to break date in year,Month and day imported from datetime library
    # date_obj = datetime.strptime(date, "%Y-%m-%d") #This is a function or method that is used to break date in year,Month and day imported from datetime library
    # month = date_obj.month #seperated month and stored in variable month
    return date_obj




@app.post("/expense/{item_id}")
def add_expense(item_id: int, expense: Expense):
    if collection.find_one({"item_id": item_id}):
        raise HTTPException(status_code=400, detail="Item ID already exists")
    
    month = break_date(expense.date)
    
    expense_data = {
        "item_id": item_id,
        "amount": expense.amount,
        # "category": expense.category.lower(),
        "date":expense.date,
        "month": month,
        # "start_date": expense.start_date,
        # "end_date": expense.end_date,
        "description": expense.description
    }
    collection.insert_one(expense_data)
    return {"message": "Expenses added successfully"}
@app.post("/expense-by-category/{_id}")
def add_expense_by_category(_id: int = Path(description="Provide id in 0,1,2"),category: str = Query(description="only give these three items as food,salary,clothes"),cat:Cat =None):
    if cat is None:
        raise HTTPException(status_code=400, detail="Request body is required")
        
    category_data = {
        "_id": _id,
        "category": category.lower()
    }
    
    try:
        collection1.insert_one(category_data)
        return {"message": "Category added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @app.get("/bygategory/{_id}")
# def get_expense(_id: int = Path(description="The _id of the expense to retrieve,Should be in 0,1,2.....any number")):
#     expenseee = collection1.find_one({"_id":_id})
#     if not expenseee:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
#     if "_id" in expenseee:
#         expenseee["_id"] = str(expenseee["_id"])
    # return expenseee

@app.get("/allexpense/{item_id}")
def get_expense(item_id: int = Path(description="The ID of the expense to retrieve")):
    expense = collection.find_one({"item_id": item_id})
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    if "_id" in expense:
        expense["_id"] = str(expense["_id"])
    return expense
@app.get("/allexpenses")
def get_all_expenses():
    expenses = list(collection.find())
    for expense in expenses:
        if "_id" in expense:
            expense["_id"] = str(expense["_id"])
    return expenses
# @app.get("/expensebydate/{item_id}")
# def get_expense(*,item_id:int,start_date: date = Query(...), end_date: date = Query(...)):
# # def get_expense(*,item_id: int ,start_date:str,end_date:str,test:int):
#     expense = collection.find_one({"item_id": item_id})
#     if not expense:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
#     if "_id" in expense:
#         expense["_id"] = str(expense["_id"])
#     return expense
@app.get("/expensebydate/", summary="Get expenses by item ID and date range")
def get_expense(
    *,start_date: date = Query(description="Start date in YYYY-MM-DD format", example="2025-01-01"),  # item_id: int = Path(description="The ID of the expense to retrieve"),
    end_date: date = Query(description="End date in YYYY-MM-DD format", example="2025-01-31")
):
    query={
        "date": {
            "$gte": start_date.isoformat(),
            "$lte":end_date.isoformat()

        }
    }
    expenses=list(collection.find({query}))
    if not expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No expenses found for this categpry")
    for expense in expenses:
        if "_id" in expense:
            expense["_id"] = str(expense["_id"])
    return expenses

@app.get("/get-item-by-category/")
def get_item_by_category(*,category:str= Query(...,description="You can get any category")):
    expenses=list(collection1.find({"category":category}))
    if not expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No expenses found for this categpry")
    for expense in expenses:
        if "_id" in expense:
            expense["_id"] = str(expense["_id"])
    return expenses
@app.get("/categories")
def get_all_categories_from_collection1():
    categories = list(collection1.find())
    for category in categories:
        if "_id" in category:
            category["_id"] = str(category["_id"])
    return categories
@app.get("/categoriess")
def get_all_categories_from_collection():
    categoriess = list(collection.find({},{"_id":0,"category":1}))
    # for category in categoriess:
    #     if "_id" in category:
    #         category["_id"] = str(category["_id"])
    return [{"category": category["category"]} for category in categoriess]
    # return categoriess
@app.get("/get-item-by-category/")
def get_item_by_category(*,category:str= Query(...,description="You can get any category")):
    expenses=list(collection.find({"category":category}))
    if not expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No expenses found for this categpry")
    for expense in expenses:
        if "_id" in expense:
            expense["_id"] = str(expense["_id"])
    return expenses

@app.get("/expensebymonth/")
def get_expenses_by_month(month: int = Query(..., description="Month as a number (1-12)")):
    # Fetch all records
      # Use empty filter to get all documents
    expenses = list(collection.find({ "month":month}))
    # Filter based on the month extracted from string-formatted date
    # filtered_expenses = []
    for expense in expenses:
         if "_id" in expense:
            expense["_id"] = str(expense["_id"])
    return expenses
        # try:
        #     # Convert the date string to datetime object
        #     if "date" in expense:
        #         record_date = datetime.strptime(expense["date"], "%Y-%m-%d")
        #         if record_date.month == month:
        #             # Convert ObjectId to string before adding to results
        #             expense["_id"] = str(expense["_id"])
        #             filtered_expenses.append(expense)
        # except (ValueError, KeyError):
        #     continue  # skip if date is malformed or missing

    # if not filtered_expenses:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, 
    #         detail=f"No expenses found for month {month}"
    #     )

    # return filtered_expenses
@app.get("/top-categories")
def get_top_categories():
    expense = [{"$group": {"_id": "$category", "total_amount": {"$sum": "$amount"}}},
        {"$sort": {"total_amount": -1}},
        {"$limit": 3}
    ]
    # expense = [
    #     {"$group": {"_id": "$category", "total_amount": {"$sum": "$amount"}}},
    #     {"$sort": {"total_amount": -1}},
    #     {"$limit": 3}
    # ]
    expenses = list(collection.aggregate(expense))
    return expenses
    # result = list(collection.aggregate(expense))
    # return [{"category": r["_id"], "total_amount": r["total_amount"]} for r in result]

