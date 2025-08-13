# # # import streamlit as st
# # # import requests #Used to send HTTP requests (GET, POST) to the FastAPI backend.
# # # from datetime import datetime, date

# # # API_URL = "http://127.0.0.1:8000"
# # # import streamlit as st
# # # import requests


# # # # Sidebar Title
# # # st.sidebar.title("Welcome to Expense Tracker")
# # # mode = st.sidebar.radio("Select Action", ["Register", "Login"])
# # # if mode == "Register":
# # #     st.sidebar.subheader("Create an Account")

# # #     username = st.sidebar.text_input("Username")
# # #     first_name = st.sidebar.text_input("First Name")
# # #     middle_name = st.sidebar.text_input("Middle Name")
# # #     last_name = st.sidebar.text_input("Last Name")
# # #     email = st.sidebar.text_input("Email")
# # #     password = st.sidebar.text_input("Password", type="password")  # hidden password

# # #     submit_button = st.sidebar.button("Register")

# # #     if submit_button:
# # #         if not username.strip() or not email.strip() or not password.strip():
# # #             st.sidebar.error("Username, Email, and Password are required.")
# # #         else:
# # #             user_data = {
# # #                 "username": username.strip(),
# # #                 "first_name": first_name.strip(),
# # #                 "middle_name": middle_name.strip(),
# # #                 "last_name": last_name.strip(),
# # #                 "email": email.strip(),
# # #                 "password": password.strip()
# # #             }

# # #             response = requests.post(f"http://127.0.0.1:8000/user_data/", json=user_data)

# # #             if response.status_code == 200:
# # #                 st.sidebar.success("Registration successful!")
# # #                 st.json(response.json())
# # #             else:
# # #                 st.sidebar.error(f"Error {response.status_code}: {"errorr"}")

# # # elif mode == "Login":
# # #     st.sidebar.subheader("Log In to Your Account")

# # #     login_username = st.sidebar.text_input("Username or Email")
# # #     login_password = st.sidebar.text_input("Password", type="password")

# # #     login_button = st.sidebar.button("Login")

# # #     if login_button:
# # #         if not login_username.strip() or not login_password.strip():
# # #             st.sidebar.error("Both fields are required.")
# # #         else:
# # #             login_data = {
# # #                 "username_or_email": login_username.strip(),
# # #                 "password": login_password.strip()
# # #             }

# # #             try:
# # #                 response = requests.post(f"{API_URL}/login/", json=login_data)

# # #                 if response.status_code == 200:
# # #                     st.sidebar.success("Login successful!")
# # #                     st.sidebar.write("Welcome back!")
# # #                     st.json(response.json())
# # #                 else:
# # #                     st.sidebar.error(f"Invalid credentials. ({response.status_code})")

# # #             except requests.exceptions.RequestException as e:
# # #                 st.sidebar.error(f"Connection error: {e}")

# # #         st.title("Expense Tracker")
# # #         action = st.sidebar.selectbox("Select Action", ("Add", "Get", "View by date", "view by category", "view by month", "top spending category"))   

# # #         if action == "Add":
# # #             tab1, tab2 = st.tabs(["Add Expense", "Add Category"])
    
# # #             with tab1:
# # #                 with st.form("expense_form"):
# # #                     item_id = st.text_input("Item ID")
# # #                     amount = st.number_input("Amount", min_value=0)
# # #                     response = requests.get("http://localhost:8000/categories")  
                

                
# # #                     if response.status_code == 200:
# # #                         categories = response.json()  
# # #                     # categories = [item["category"] for item in categories]
# # #                     else:
# # #                         st.error("Failed to fetch categories")
# # #                     # categories = []  # Fallback to empty list
# # #                     category = st.selectbox("Category", categories)

# # #                     date_val = st.date_input("Date")
# # #                     description = st.text_input("Description")
                
# # #                     submit_button = st.form_submit_button("Add Expense")
                
# # #                     if submit_button and amount and date_val:
# # #                         expense_data = {
# # #                         "amount": int(amount),
# # #                         "category": str(category).lower(),
# # #                         "date": date_val.strftime("%Y-%m-%d"),
# # #                         "description": str(description)}
                    
# # #                         response = requests.post(f"{API_URL}/expense/{item_id}", json=expense_data)
                    
# # #                     if response.status_code == 200:
# # #                         st.success("Expense added successfully!")
# # #                         st.json(response.json())
# # #                     else:
# # #                         st.error(f"Error: {response.json()['detail']}")
        
# # #             with tab2:

# # #                 with st.form("category_form"):
# # #                     _id = st.number_input("_id", min_value=0)
# # #                     category = st.selectbox("Category", categories if categories else ["No categories available"])
# # #                     submit_cat_button = st.form_submit_button("Add Category")
        
# # #                 if submit_cat_button and categories:
# # #                     body_data = {
# # #                     "category": category.lower()
# # #                 }

# # #                 try:
# # #                     response = requests.post(f"{API_URL}/expense-by-category/{_id}",params={"category": category.lower()},json=body_data
# # #                 )

# # #                     if response.status_code == 200:
# # #                         data = response.json()
# # #                         st.success(data["message"])
# # #                         st.subheader(f"Items in '{category}' category:")
# # #                         st.json(data["items_in_this_category"])
# # #                     else:
# # #                         st.error(f"Error: {response.json().get('detail')}")
# # #                 except Exception as e:
# # #                     st.error(f"Request failed: {str(e)}")
# # #         elif action == "Get":
# # #             with st.header("View Expense by ID"):
# # #                 item_id = st.number_input("Enter Item ID", min_value=1, step=1)
# # #             if st.button("Search"):
# # #                 try:
# # #                     response = requests.get(f"{API_URL}/allexpense/{item_id}") #get api hit
# # #                     if response.status_code == 200: #if success
# # #                         expense = response.json() #will send data to expense
# # #                         st.write("Expense Details")
# # #                         st.write(f"Amount: {expense['amount']}")
# # #                         st.write(f"Category:{expense['category']}") #all the data that will be displayed
# # #                         st.write(f"Date:{expense['date']}")
# # #                         st.write(f"Description:{expense['description']}")
# # #                     else:
# # #                         st.error(f"Error: {response.json()['detail']}")
# # #                 except requests.exceptions.RequestException as e:
# # #                     st.error(f"Failed to connect to the server: {str(e)}")
# # #         elif action=="View by date":
# # #             st.header("View Expenses by Date Range")
# # #             col1, col2 = st.columns(2) #This widget forms two cloumns
# # #             with col1:
# # #                     start_date = st.date_input("Start Date") #in col1 takes date input
# # #             with col2:
# # #                     end_date = st.date_input("End Date") #in col2 takes date input as well
                
# # #             if st.button("Search by Date"):
# # #                     # try:
# # #                         response = requests.get(f"{API_URL}/expensebydate/",  #as this get method takes 2 query method so we provide it with 2 parameters
# # #                             params={"start_date": start_date.strftime("%Y-%m-%d"),"end_date": end_date.strftime("%Y-%m-%d")}
# # #                         )
# # #                         if response.status_code == 200:
# # #                             expenses = response.json()
# # #                             st.write(expenses)
# # #                         else:
# # #                             st.error(f"Error: {response.json()['detail']}")
# # #                 # except requests.exceptions.RequestException as e:
# # #                 #     st.error(f"Failed to connect to the server: {str(e)}")

# # #         elif action=="view by category":
# # #             st.header("View Expenses by Category")
# # #             response = requests.get("http://localhost:8000/categories")  
                    

                    
# # #             if response.status_code == 200:
# # #                         categories = response.json()  # Assuming your API returns a JSON list like ["Food", "Salary", ...]
# # #                         # categoriesss = [item["category"] for item in categories]
# # #             else:
# # #                 st.error("Failed to fetch categories")
# # #                 # categories = []  # Fallback to empty list

# # #                 # Create the selectbox with fetched categories
# # #             category = st.selectbox("Category", categories)

# # #             # category = st.text_input("Enter Category")
# # #             if st.button("Search by Category"):
# # #                         response = requests.get( f"{API_URL}/get-item-by-category/", params={"category": category.lower()}
# # #                         )  #this method here takes only 1 query parameter category
# # #                         if response.status_code == 200:
# # #                             expenses = response.json()
# # #                             st.write(expenses)
# # #                         else:
# # #                             st.error(f"Error: {response.json()['detail']}")
# # # # elif action=="view by category":
# # # #     st.header("View Expenses by Category")
# # # #     category = st.selectbox("Category",["Food","Salary","clothes"])
# # # #     # category = st.text_input("Enter Category")
# # # #     if st.button("Search by Category"):
# # # #                 response = requests.get( f"{API_URL}/get-item-by-category/", params={"category": category.lower()}
# # # #                 )  #this method here takes only 1 query parameter category
# # # #                 if response.status_code == 200:
# # # #                     expenses = response.json()
# # # #                     st.write(expenses)
# # # #                 else:
# # # #                     st.error(f"Error: {response.json()['detail']}")

# # #         elif action=="view by month":
# # #             st.header("View Expenses by Month")
# # #             month = st.number_input("Enter Month (1-12)", min_value=1, max_value=12, step=1)
# # #             if st.button("Search by Month"): 
# # #                         response = requests.get(f"{API_URL}/expensebymonth/",params={"month": month}
# # #                         ) #This get api method takes one query parameter that is month ,date i already broke down to year,month and day
# # #                         if response.status_code == 200:
# # #                             expenses = response.json()
# # #                             st.write(expenses)
                            
# # #                         else:
# # #                             st.error(f"Error: {response.json()['detail']}")

# # #         elif action=="top spending category":
# # #             st.header("Top Spending Categories")
# # #             if st.button("Show Top Categories"):
# # #                         response = requests.get(f"{API_URL}/top-categories")
# # #                         if response.status_code == 200:
# # #                             categories = response.json()
# # #                             st.write("### Top 3 Spending Categories")
# # #                             for idx, category in enumerate(categories, 1):
# # #                                 st.write(f"{idx}. **{category['_id']}**: ${category['total_amount']}")
# # #                         else:
# # #                             st.error(f"Error: {response.json()['detail']}")
# # import streamlit as st
# # import requests
# # from datetime import datetime, date

# # API_URL = "http://127.0.0.1:8000"

# # # Sidebar Title
# # st.sidebar.title("Welcome to Expense Tracker")
# # mode = st.sidebar.radio("Select Action", ["Register", "Login"])

# # if mode == "Register":
# #     st.sidebar.subheader("Create an Account")

# #     username = st.sidebar.text_input("Username")
# #     first_name = st.sidebar.text_input("First Name")
# #     middle_name = st.sidebar.text_input("Middle Name")
# #     last_name = st.sidebar.text_input("Last Name")
# #     email = st.sidebar.text_input("Email")
# #     password = st.sidebar.text_input("Password", type="password")  # hidden password

# #     submit_button = st.sidebar.button("Register")

# #     if submit_button:
# #         if not username.strip() or not email.strip() or not password.strip():
# #             st.sidebar.error("Username, Email, and Password are required.")
# #         else:
# #             user_data = {
# #                 "username": username.strip(),
# #                 "first_name": first_name.strip(),
# #                 "middle_name": middle_name.strip(),
# #                 "last_name": last_name.strip(),
# #                 "email": email.strip(),
# #                 "password": password.strip()
# #             }

# #             response = requests.post(f"{API_URL}/user_data/", json=user_data)

# #             if response.status_code == 200:
# #                 st.sidebar.success("Registration successful!")
# #                 st.json(response.json())
# #             else:
# #                 st.sidebar.error(f"Error {response.status_code}: {response.text}")

# # elif mode == "Login":
# #     st.sidebar.subheader("Log In to Your Account")

# #     login_username = st.sidebar.text_input("Username or Email")
# #     login_password = st.sidebar.text_input("Password", type="password")

# #     login_button = st.sidebar.button("Login")

# #     if login_button:
# #         if not login_username.strip() or not login_password.strip():
# #             st.sidebar.error("Both fields are required.")
# #         else:
# #             login_data = {
# #                 "username_or_email": login_username.strip(),
# #                 "password": login_password.strip()
# #             }

# #             try:
# #                 response = requests.post(f"{API_URL}/login/", json=login_data)

# #                 if response.status_code == 200:
# #                     st.sidebar.success("Login successful!")
# #                     st.sidebar.write("Welcome back!")
# #                     st.json(response.json())
# #                 else:
# #                     st.sidebar.error(f"Invalid credentials. ({response.status_code})")

# #             except requests.exceptions.RequestException as e:
# #                 st.sidebar.error(f"Connection error: {e}")

# #     # Actions after login
# #         st.title("Expense Tracker")
# #         action = st.sidebar.selectbox("Select Action", ("Add", "Get", "View by date", "view by category", "view by month", "top spending category"))

# #         if action == "Add":
# #             tab1, tab2 = st.tabs(["Add Expense", "Add Category"])

# #             # Tab 1: Add Expense
# #             with tab1:
# #                 with st.form("expense_form"):
# #                     item_id = st.text_input("Item ID")
# #                     amount = st.number_input("Amount", min_value=0)

# #                     response = requests.get(f"{API_URL}/categories")
# #                     if response.status_code == 200:
# #                         categories = response.json()
# #                     else:
# #                         st.error("Failed to fetch categories")
# #                         categories = []

# #                     category = st.selectbox("Category", categories)
# #                     date_val = st.date_input("Date")
# #                     description = st.text_input("Description")

# #                     submit_button = st.form_submit_button("Add Expense")

# #                     if submit_button and amount and date_val:
# #                         expense_data = {
# #                             "amount": int(amount),
# #                             "category": str(category).lower(),
# #                             "date": date_val.strftime("%Y-%m-%d"),
# #                             "description": str(description)
# #                         }

# #                         response = requests.post(f"{API_URL}/expense/{item_id}", json=expense_data)

# #                         if response.status_code == 200:
# #                             st.success("Expense added successfully!")
# #                             st.json(response.json())
# #                         else:
# #                             st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

# #             # Tab 2: Add Category
# #             with tab2:
# #                 with st.form("category_form"):
# #                     _id = st.number_input("_id", min_value=0)
# #                     category = st.text_input("Category Name")
# #                     submit_cat_button = st.form_submit_button("Add Category")

# #                 if submit_cat_button and category.strip():
# #                     body_data = {
# #                         "category": category.lower()
# #                     }

# #                     try:
# #                         response = requests.post(f"{API_URL}/expense-by-category/{_id}",
# #                                                 params={"category": category.lower()},
# #                                                 json=body_data)

# #                         if response.status_code == 200:
# #                             data = response.json()
# #                             st.success(data.get("message", "Category added successfully!"))
# #                             if "items_in_this_category" in data:
# #                                 st.subheader(f"Items in '{category}' category:")
# #                                 st.json(data["items_in_this_category"])
# #                         else:
# #                             st.error(f"Error: {response.json().get('detail')}")
# #                     except Exception as e:
# #                         st.error(f"Request failed: {str(e)}")

# #         elif action == "Get":
# #             st.header("View Expense by ID")
# #             item_id = st.number_input("Enter Item ID", min_value=1, step=1)
# #             if st.button("Search"):
# #                 try:
# #                     response = requests.get(f"{API_URL}/allexpense/{item_id}")
# #                     if response.status_code == 200:
# #                         expense = response.json()
# #                         st.write("Expense Details")
# #                         st.write(f"Amount: {expense['amount']}")
# #                         st.write(f"Category: {expense['category']}")
# #                         st.write(f"Date: {expense['date']}")
# #                         st.write(f"Description: {expense['description']}")
# #                     else:
# #                         st.error(f"Error: {response.json()['detail']}")
# #                 except requests.exceptions.RequestException as e:
# #                     st.error(f"Failed to connect to the server: {str(e)}")

# #         elif action == "View by date":
# #             st.header("View Expenses by Date Range")
# #             col1, col2 = st.columns(2)
# #             with col1:
# #                 start_date = st.date_input("Start Date")
# #             with col2:
# #                 end_date = st.date_input("End Date")

# #             if st.button("Search by Date"):
# #                 response = requests.get(f"{API_URL}/expensebydate/",
# #                                         params={"start_date": start_date.strftime("%Y-%m-%d"),
# #                                                 "end_date": end_date.strftime("%Y-%m-%d")})
# #                 if response.status_code == 200:
# #                     expenses = response.json()
# #                     st.write(expenses)
# #                 else:
# #                     st.error(f"Error: {response.json()['detail']}")

# #         elif action == "view by category":
# #             st.header("View Expenses by Category")
# #             response = requests.get(f"{API_URL}/categories")

# #             if response.status_code == 200:
# #                 categories = response.json()
# #             else:
# #                 st.error("Failed to fetch categories")
# #                 categories = []

# #             category = st.selectbox("Category", categories)

# #             if st.button("Search by Category"):
# #                 response = requests.get(f"{API_URL}/get-item-by-category/",
# #                                         params={"category": category.lower()})
# #                 if response.status_code == 200:
# #                     expenses = response.json()
# #                     st.write(expenses)
# #                 else:
# #                     st.error(f"Error: {response.json()['detail']}")

# #         elif action == "view by month":
# #             st.header("View Expenses by Month")
# #             month = st.number_input("Enter Month (1-12)", min_value=1, max_value=12, step=1)
# #             if st.button("Search by Month"):
# #                 response = requests.get(f"{API_URL}/expensebymonth/", params={"month": month})
# #                 if response.status_code == 200:
# #                     expenses = response.json()
# #                     st.write(expenses)
# #                 else:
# #                     st.error(f"Error: {response.json()['detail']}")

# #         elif action == "top spending category":
# #             st.header("Top Spending Categories")
# #             if st.button("Show Top Categories"):
# #                 response = requests.get(f"{API_URL}/top-categories")
# #                 if response.status_code == 200:
# #                     categories = response.json()
# #                     st.write("### Top 3 Spending Categories")
# #                     for idx, category in enumerate(categories, 1):
# #                             st.write(f"{idx}. **{category['_id']}**: ${category['total_amount']}")
# #                     else:
# #                         st.error(f"Error: {response.json()['detail']}")
# import streamlit as st
# import requests
# from datetime import datetime, date

# API_URL = "http://127.0.0.1:8000"

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# st.sidebar.title("Welcome to Expense Tracker")
# mode = st.sidebar.radio("Select Action", ["Register", "Login"])

# if mode == "Register":
#     st.sidebar.subheader("Create an Account")

#     username = st.sidebar.text_input("Username")
#     first_name = st.sidebar.text_input("First Name")
#     middle_name = st.sidebar.text_input("Middle Name")
#     last_name = st.sidebar.text_input("Last Name")
#     email = st.sidebar.text_input("Email")
#     password = st.sidebar.text_input("Password", type="password")
#     Role = st.sidebar.radio("Role",["Admin","User"])
#     if st.sidebar.button("Register"):
#         if not username.strip() or not email.strip() or not password.strip():
#             st.sidebar.error("Username, Email, and Password are required.")
#         else:
#             user_data = {
#                 "username": username.strip(),
#                 "first_name": first_name.strip(),
#                 "middle_name": middle_name.strip(),
#                 "last_name": last_name.strip(),
#                 "email": email.strip(),
#                 "password": password.strip(),
#                 "Role":Role.strip()
#             }
#             response = requests.post(f"{API_URL}/user_data/", json=user_data)
#             if response.status_code == 200:
#                 st.sidebar.success("Registration successful!")
#                 st.json(response.json())
#             else:
#                 st.sidebar.error(f"Error {response.status_code}: {response.text}")

# elif mode == "Login" and not st.session_state.logged_in:
#     st.sidebar.subheader("Log In to Your Account")
#     # login_username = None
#     global login_username

#     login_username = st.sidebar.text_input("Username or Email")
#     login_password = st.sidebar.text_input("Password", type="password")
#     # login_role = st.sidebar.radio("Role",["Admin","User"])

#     if st.sidebar.button("Login"):
#         if not login_username.strip() or not login_password.strip():
#             st.sidebar.error("Both fields are required.")
#         else:
#             login_data = {
#                 "username_or_email": login_username.strip(),
#                 "password": login_password.strip(),
#                 # "Role": login_role.strip()
#             }
#             try:
#                 response = requests.post(f"{API_URL}/login/", json=login_data)
#                 if response.status_code == 200:
#                     st.session_state.logged_in = True
#                     st.session_state.user_info = response.json()
#                     st.sidebar.success("Login successful!")
#                 else:
#                     st.sidebar.error("Invalid credentials.")
#             except requests.exceptions.RequestException as e:
#                 st.sidebar.error(f"Connection error: {e}")

# if st.session_state.logged_in:
#     st.title("Expense Tracker")
#     st.sidebar.write(f"Welcome, {st.session_state.user_info.get('username', 'User')}!")

#     action = st.sidebar.selectbox(
#         "Select Action",
#         ("Add", "Get", "View by date", "view by category", "view by month", "top spending category")
#     )

#     if action == "Add":
#         tab1, tab2 = st.tabs(["Add Expense", "Add Category"])

#         with tab1:
#             with st.form("expense_form"):
#                 item_id = st.text_input("Item ID")
#                 amount = st.number_input("Amount", min_value=0)

#                 response = requests.get(f"{API_URL}/categories")
#                 categories = response.json() if response.status_code == 200 else []
#                 if not categories:
#                     st.warning("No categories available.")

#                 category = st.selectbox("Category", categories)
#                 date_val = st.date_input("Date")
#                 description = st.text_input("Description")
#                 submit_button = st.form_submit_button("Add Expense")

#                 if submit_button and amount and date_val:
#                     expense_data = {
#                         "amount": int(amount),
#                         "category": category.lower(),
#                         "date": date_val.strftime("%Y-%m-%d"),
#                         "description": description
#                     }
#                     response = requests.post(f"{API_URL}/expense/{item_id}",email=login_username, json=expense_data)
#                     if response.status_code == 200:
#                         st.success("Expense added successfully!")
#                         st.json(response.json())
#                     else:
#                         st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
#         with tab2:
#             with st.form("category_form"):
#                 _id = st.number_input("_id", min_value=0)
#                 category = st.text_input("Category Name")
#                 submit_cat_button = st.form_submit_button("Add Category")

#             if submit_cat_button and category.strip():
#                 body_data = {"category": category.lower()}
#                 try:
#                     response = requests.post(
#                         f"{API_URL}/expense-by-category/{_id}",
#                         params={"category": category.lower()},
#                         json=body_data
#                     )
#                     if response.status_code == 200:
#                         data = response.json()
#                         st.success(data.get("message", "Category added successfully!"))
#                         if "items_in_this_category" in data:
#                             st.subheader(f"Items in '{category}' category:")
#                             st.json(data["items_in_this_category"])
#                     else:
#                         st.error(f"Error: {response.json().get('detail')}")
#                 except Exception as e:
#                     st.error(f"Request failed: {str(e)}")

#     elif action == "Get":
#         st.header("View Expense by ID")
#         # item_id = st.number_input("Enter Item ID", min_value=1, step=1)
#         if st.button("Search"):
#             try:
#                 response = requests.get(f"{API_URL}/allexpense/{login_username}")
#                 if response.status_code == 200:
#                     expense = response.json()
#                     st.write(expense)
#                 else:
#                     st.error(f"Error: {response.json()['detail']}")
#             except requests.exceptions.RequestException as e:
#                 st.error(f"Failed to connect: {str(e)}")

#     elif action == "View by date":
#         st.header("View Expenses by Date Range")
#         col1, col2 = st.columns(2)
#         with col1:
#             start_date = st.date_input("Start Date")
#         with col2:
#             end_date = st.date_input("End Date")

#         if st.button("Search by Date"):
#             response = requests.get(
#                 f"{API_URL}/expensebydate/",
#                 params={"start_date": start_date.strftime("%Y-%m-%d"),
#                         "end_date": end_date.strftime("%Y-%m-%d")}
#             )
#             if response.status_code == 200:
#                 st.write(response.json())
#             else:
#                 st.error(f"Error: {response.json()['detail']}")

#     elif action == "view by category":
#         st.header("View Expenses by Category")
#         response = requests.get(f"{API_URL}/categories")
#         categories = response.json() if response.status_code == 200 else []
#         category = st.selectbox("Category", categories)
#         if st.button("Search by Category"):
#             response = requests.get(
#                 f"{API_URL}/get-item-by-category/",
#                 params={"category": category.lower()}
#             )
#             if response.status_code == 200:
#                 st.write(response.json())
#             else:
#                 st.error(f"Error: {response.json()['detail']}")
#     elif action == "view by month":
#         st.header("View Expenses by Month")
#         month = st.number_input("Enter Month (1-12)", min_value=1, max_value=12, step=1)
#         if st.button("Search by Month"):
#             response = requests.get(f"{API_URL}/expensebymonth/", params={"month": month})
#             if response.status_code == 200:
#                 st.write(response.json())
#             else:
#                 st.error(f"Error: {response.json()['detail']}")
#     elif action == "top spending category":
#         st.header("Top Spending Categories")
#         if st.button("Show Top Categories"):
#             response = requests.get(f"{API_URL}/top-categories")
#             if response.status_code == 200:
#                 categories = response.json()
#                 st.write("### Top 3 Spending Categories")
#                 for idx, category in enumerate(categories, 1):
#                     st.write(f"{idx}. **{category['_id']}**: ${category['total_amount']}")
#             else:
#                 st.error(f"Error: {response.json()['detail']}")

import streamlit as st
import requests
API_URL = "http://127.0.0.1:8000"

st.title("Expense Tracker")
mode = st.sidebar.selectbox("Select Action", ["Register", "Login", "Add Expense", "View Expenses", "View Categories", "Top Spending Category","view by month"])

if mode == "Register":
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    First_name = st.text_input("First_name")
    Middle_name = st.text_input("Middle_name")
    Last_name = st.text_input("Last_name")

    if st.button("Register"):
        response = requests.post(f"{API_URL}/register", params={"username": username, "email": email, "password": password,"First_name":First_name,"Middle_name":Middle_name,"Last_name":Last_name})
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(response.json()["detail"])

if mode == "Login":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post(f"{API_URL}/login", params={"email": email, "password": password})
        if response.status_code == 200:
            st.session_state["email"] = response.json()["email"]
            st.success("Logged in successfully")
        else:
            st.error(response.json()["detail"])
elif mode == "Add Expense":
    if "email" in st.session_state:
        amount = st.number_input("Amount", min_value=0, step=1)
        try:
            response = requests.get(f"{API_URL}/categories")
            if response.status_code == 200:
                categories = response.json()
            else:
                st.error(f"Failed to fetch categories: {response.text}")
                categories = []
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to server: {e}")
            categories = []
        category = st.selectbox("Category", categories)
        date_input = st.date_input("Date")
        date_str = date_input.strftime("%Y-%m-%d")
        description = st.text_input("Description")
        if st.button("Add Expense"):
            expense_data = {
                "amount": amount,
                "category": category.lower(),
                "date": date_str,
                "description": description,
                "user_email": st.session_state["email"]
            }

            try:
                response = requests.post(f"{API_URL}/add-expense",json=expense_data,timeout=10
                )
                if response.status_code == 200:
                    try:
                        st.success(response.json().get("message", "Expense added successfully!"))
                    except ValueError:
                        st.success("Expense added successfully!")
                else:
                    try:
                        st.error(response.json().get("detail", "Failed to add expense"))
                    except ValueError:
                        st.error(f"Failed to add expense: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {e}")

    else:
        st.warning("Please log in first")

if mode == "View Expenses":
    if "email" in st.session_state:
        if st.button("Show My Expenses"):
            res = requests.get(f"{API_URL}/get-my-expenses", params={"email": st.session_state["email"]})
            if res.status_code == 200:
                st.table(res.json()["expenses"])
            else:
                st.error(res.json()["detail"])
    else:
        st.warning("Please log in first")

if mode == "View Categories":
    if "email" in st.session_state:
        if st.button("Show My Categories"):
            res = requests.get(f"{API_URL}/get-my-categories", params={"email": st.session_state["email"]})
            if res.status_code == 200:
                st.table(res.json()["categories"])
            else:
                st.error(res.json()["detail"])
    else:
        st.warning("Please log in first")
if mode == "view by month":
    if "email" in st.session_state:
        st.header("View Expenses by Month")
        month = st.number_input("Enter Month (1-12)", min_value=1, max_value=12, step=1)
        if st.button("Search by Month"):
            response = requests.get(f"{API_URL}/expensebymonth/", params={"email": st.session_state["email"],"month":month})
            if response.status_code == 200:
                st.table(response.json())
            else:
                st.error(f"Error: {response.json()['detail']}")
    else:
        st.warning("Please Log in first")

if mode == "Top Spending Category":
    # if "email" in st.session_state:
    #     if st.button("Show Top Category"):
    #         res = requests.get(f"{API_URL}/get-top-category", params={"email": st.session_state["email"]})
    #         if res.status_code == 200:
    #             data = res.json()
    #             st.success(f"Your top spending category is '{data['top_category']}' with total {data['amount']}")
    #         else:
    #             st.error(res.json()["detail"])
    # else:
    #     st.warning("Please log in first")
    #     if "email" in st.session_state:
    st.subheader("Top 3 Spending Categories")

    try:
        response = requests.get(f"{API_URL}/get-top-categories", params={"email": st.session_state["email"]})

        if response.status_code == 200:
            top_categories = response.json()

            if top_categories:
                display_data = [
                    {"Category": item["_id"], "Total Amount": item["total_amount"]}
                    for item in top_categories
                ]

                # Show in table format
                st.table(display_data)
            else:
                st.info("No expenses found.")
        else:
            st.error(f"Error fetching top categories: {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to backend: {e}")
# Example: Check if user is logged in
if "email" in st.session_state:
    st.sidebar.write(f"Logged in as: {st.session_state['email']}")
    
    # Logout button in sidebar
    if st.sidebar.button("Log Out"):
        # Clear all stored session state values
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("You have been logged out.")
        # st.experimental_rerun()  # Refresh the page
else:
    st.sidebar.warning("You are not logged in.")
