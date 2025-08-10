import streamlit as st
import requests #Used to send HTTP requests (GET, POST) to the FastAPI backend.
from datetime import datetime, date

API_URL = "http://127.0.0.1:8000"


st.title("Expense Tracker")
action = st.sidebar.selectbox("Select Action", ("Add", "Get", "View by date", "view by category", "view by month", "top spending category"))   

if action == "Add":
    tab1, tab2 = st.tabs(["Add Expense", "Add Category"])
    
    with tab1:
        with st.form("expense_form"):
            item_id = st.text_input("Item ID")
            amount = st.number_input("Amount", min_value=0)
            category = st.selectbox("Category", ["Food", "Salary", "clothes"])
            date_val = st.date_input("Date")
            description = st.text_input("Description")
            
            submit_button = st.form_submit_button("Add Expense")
            
            if submit_button and amount and date_val:
                expense_data = {
                    "amount": int(amount),
                    # "category": str(category).lower(),
                    "date": date_val.strftime("%Y-%m-%d"),
                    "description": str(description)
                }
                
                response = requests.post(f"{API_URL}/expense/{item_id}", json=expense_data)
                
                if response.status_code == 200:
                    st.success("Expense added successfully!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.json()['detail']}")
    
    with tab2:
        with st.form("category_form"):
            _id = st.number_input("_id", min_value=0)
            category = st.selectbox("Category ", ["Food", "Salary", "clothes"])
            submit_cat_button = st.form_submit_button("Add Category")
            
            if submit_cat_button:
                category_data = {
                    "item_id": int(_id), 
                    "category": str(category).lower()
                }
                
                # try:
                response = requests.post(
                        f"{API_URL}/expense-by-category/{_id}",params={"category": category.lower()},json=category_data
                    )
                    
                if response.status_code == 200:
                        st.success("Category added successfully!")
                        st.json(response.json())
                else:
                        st.error(f"Error: {response.json()['ID already taken,Insert New Id to insert your category']}")
                # except Exception as e:
                #     st.error(f"Error: {str(e)}")
elif action == "Get":
    st.header("View Expense by ID")
    item_id = st.number_input("Enter Item ID", min_value=1, step=1)
    if st.button("Search"):
            try:
                response = requests.get(f"{API_URL}/allexpense/{item_id}") #get api hit
                if response.status_code == 200: #if success
                    expense = response.json() #will send data to expense
                    st.write("Expense Details")
                    st.write(f"Amount: {expense['amount']}")
                    st.write(f"Category:{expense['category']}") #all the data that will be displayed
                    st.write(f"Date:{expense['date']}")
                    st.write(f"Description:{expense['description']}")
                else:
                    st.error(f"Error: {response.json()['detail']}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the server: {str(e)}")

elif action=="View by date":
    st.header("View Expenses by Date Range")
    col1, col2 = st.columns(2) #This widget forms two cloumns
    with col1:
            start_date = st.date_input("Start Date") #in col1 takes date input
    with col2:
            end_date = st.date_input("End Date") #in col2 takes date input as well
        
    if st.button("Search by Date"):
            # try:
                response = requests.get(
                    f"{API_URL}/expensebydate/",  #as this get method takes 2 query method so we provide it with 2 parameters
                    params={"start_date": start_date.strftime("%Y-%m-%d"),"end_date": end_date.strftime("%Y-%m-%d")}
                )
                if response.status_code == 200:
                    expenses = response.json()
                    st.write(expenses)
                else:
                    st.error(f"Error: {response.json()['detail']}")
            # except requests.exceptions.RequestException as e:
            #     st.error(f"Failed to connect to the server: {str(e)}")

elif action=="view by category":
    st.header("View Expenses by Category")
    category = st.selectbox("Category",["Food","Salary","clothes"])
    # category = st.text_input("Enter Category")
    if st.button("Search by Category"):
                response = requests.get( f"{API_URL}/get-item-by-category/", params={"category": category.lower()}
                )  #this method here takes only 1 query parameter category
                if response.status_code == 200:
                    expenses = response.json()
                    st.write(expenses)
                else:
                    st.error(f"Error: {response.json()['detail']}")
elif action=="view by category":
    st.header("View Expenses by Category")
    category = st.selectbox("Category",["Food","Salary","clothes"])
    # category = st.text_input("Enter Category")
    if st.button("Search by Category"):
                response = requests.get( f"{API_URL}/get-item-by-category/", params={"category": category.lower()}
                )  #this method here takes only 1 query parameter category
                if response.status_code == 200:
                    expenses = response.json()
                    st.write(expenses)
                else:
                    st.error(f"Error: {response.json()['detail']}")

elif action=="view by month":
    st.header("View Expenses by Month")
    month = st.number_input("Enter Month (1-12)", min_value=1, max_value=12, step=1)
    if st.button("Search by Month"): 
                response = requests.get(f"{API_URL}/expensebymonth/",params={"month": month}
                ) #This get api method takes one query parameter that is month ,date i already broke down to year,month and day
                if response.status_code == 200:
                    expenses = response.json()
                    st.write(expenses)
                    
                else:
                    st.error(f"Error: {response.json()['detail']}")

elif action=="top spending category":
    st.header("Top Spending Categories")
    if st.button("Show Top Categories"):
                response = requests.get(f"{API_URL}/top-categories")
                if response.status_code == 200:
                    categories = response.json()
                    st.write("### Top 3 Spending Categories")
                    for idx, category in enumerate(categories, 1):
                        st.write(f"{idx}. **{category['_id']}**: ${category['total_amount']}")
                else:
                    st.error(f"Error: {response.json()['detail']}")

# def add_expense(): #This function is called from API
#     st.title("Add New Expense")
    
#     with st.form("expense_form"): #Forms a Form -->We use with st.form(...) to group multiple input widgets together into a single form, so that they are only processed when a specific submit button is clicked.
#         item_id = st.text_input("Item ID")
#         amount = st.number_input("Amount", min_value=0)
#         category = st.text_input("Category")
#         date_val = st.date_input("Date")
#         description = st.text_input("Description")
        
#         submit_button = st.form_submit_button("Add Expense") #And here I formed submit button that triggers processing of all form inputs at once.
        
#         if submit_button and category and amount and date_val:  # Basic validation until these inputs are inserted it won't submit
#             expense_data = {
#                 "amount": int(amount),      #Prepares a JSON-like Python dict to send to the backend as HTTP doesn't take python object
#                 "category": str(category).lower(),
#                 "date": date_val.strftime("%Y-%m-%d"),
#                 "description": str(description)
#             }
            
            
#             response = requests.post( f"{API_URL}/expense/{item_id}",json=expense_data)  #request.post is a function that sends a post request to the backend route, and turns data into json   
                 
                
#             if response.status_code == 200: #status_code is an HTML code if 200 it means success, 404 is error 201 is created
#                     st.success("Expense added successfully!")
#                     st.json(response.json())
#             else:
#                     st.error(f"Error: {response.json()['detail']}") #returns error message that is item not found


# def view_expense_by_id():
#     st.header("View Expense by ID")
#     item_id = st.number_input("Enter Item ID", min_value=1, step=1)
#     if st.button("Search"):
#         try:
#             response = requests.get(f"{API_URL}/allexpense/{item_id}") #get api hit
#             if response.status_code == 200: #if success
#                 expense = response.json() #will send data to expense
#                 st.write("### Expense Details")
#                 st.write(f"**Amount:** ${expense['amount']}")
#                 st.write(f"**Category:** {expense['category']}") #all the data that will be displayed
#                 st.write(f"**Date:** {expense['date']}")
#                 st.write(f"**Description:** {expense['description']}")
#             else:
#                 st.error(f"Error: {response.json()['detail']}")
#         except requests.exceptions.RequestException as e:
#             st.error(f"Failed to connect to the server: {str(e)}")

# def view_expenses_by_date():
#     st.header("View Expenses by Date Range")
#     col1, col2 = st.columns(2) #This widget forms two cloumns
#     with col1:
#         start_date = st.date_input("Start Date") #in col1 takes date input
#     with col2:
#         end_date = st.date_input("End Date") #in col2 takes date input as well
    
#     if st.button("Search by Date"):
#         # try:
#             response = requests.get(
#                 f"{API_URL}/expensebydate/",  #as this get method takes 2 query method so we provide it with 2 parameters
#                 params={"start_date": start_date.strftime("%Y-%m-%d"),"end_date": end_date.strftime("%Y-%m-%d")}
#             )
#             if response.status_code == 200:
#                 expenses = response.json()
#                 display_expenses(expenses)
#             else:
#                 st.error(f"Error: {response.json()['detail']}")
#         # except requests.exceptions.RequestException as e:
#         #     st.error(f"Failed to connect to the server: {str(e)}")

# def view_expenses_by_category():
#     st.header("View Expenses by Category")
#     category = st.text_input("Enter Category")
#     if st.button("Search by Category"):
#             response = requests.get( f"{API_URL}/get-item-by-category/", params={"category": category.lower()}
#             )  #this method here takes only 1 query parameter category
#             if response.status_code == 200:
#                 expenses = response.json()
#                 display_expenses(expenses)
#             else:
#                 st.error(f"Error: {response.json()['detail']}")

# def view_expenses_by_month():
#     st.header("View Expenses by Month")
#     month = st.number_input("Enter Month (1-12)", min_value=1, max_value=12, step=1)
#     if st.button("Search by Month"): 
#             response = requests.get(f"{API_URL}/expensebymonth/",params={"month": month}
#             ) #This get api method takes one query parameter that is month ,date i already broke down to year,month and day
#             if response.status_code == 200:
#                 expenses = response.json()
#                 display_expenses(expenses)
#             else:
#                 st.error(f"Error: {response.json()['detail']}")

# def view_top_categories():
#     st.header("Top Spending Categories")
#     if st.button("Show Top Categories"):
#             response = requests.get(f"{API_URL}/top-categories")
#             if response.status_code == 200:
#                 categories = response.json()
#                 st.write("### Top 3 Spending Categories")
#                 for idx, category in enumerate(categories, 1):
#                     st.write(f"{idx}. **{category['_id']}**: ${category['total_amount']}")
#             else:
#                 st.error(f"Error: {response.json()['detail']}")

# def display_expenses(expenses): #Helper function to display expenses in a consistent format
   
#     if not expenses:
#         st.warning("No expenses found!")
#         return
    
#     for expense in expenses:
#         st.write("---")
#         st.write(f"**ID:** {expense['item_id']}")
#         st.write(f"**Amount:** ${expense['amount']}")
#         st.write(f"**Category:** {expense['category']}")
#         st.write(f"**Date:** {expense['date']}")
#         st.write(f"**Description:** {expense['description']}")
# add_expense()
# view_expense_by_id()
# view_expenses_by_date()
# view_expenses_by_category()
# view_expenses_by_month()
# view_top_categories()
