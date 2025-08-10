from pydantic import BaseModel, Field
import databasee
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