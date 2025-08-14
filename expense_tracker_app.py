import streamlit as st
import requests
from datetime import date, datetime

API_URL = "http://127.0.0.1:8000"
ADMIN_EMAIL = "moinmj7@gmail.com"

st.set_page_config(page_title="Expense Tracker", layout="wide")

# Session state
if "email" not in st.session_state:
    st.session_state["email"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None

# Helpers
def api_get(path, params=None):
    try:
        r = requests.get(API_URL + path, params=params, timeout=8)
        return r
    except Exception as e:
        st.error(f"GET {path} failed: {e}")
        return None

def api_post(path, json=None, params=None):
    try:
        r = requests.post(API_URL + path, json=json, params=params, timeout=8)
        return r
    except Exception as e:
        st.error(f"POST {path} failed: {e}")
        return None

def api_put(path, json=None, params=None):
    try:
        r = requests.put(API_URL + path, json=json, params=params, timeout=8)
        return r
    except Exception as e:
        st.error(f"PUT {path} failed: {e}")
        return None

def api_delete(path, params=None):
    try:
        r = requests.delete(API_URL + path, params=params, timeout=8)
        return r
    except Exception as e:
        st.error(f"DELETE {path} failed: {e}")
        return None

# ---- Sidebar: Register / Login ----
st.sidebar.title("Account")
auth_tab = st.sidebar.radio("Auth", ["Register", "Login"], index=1 if st.session_state["email"] else 0)

if auth_tab == "Register":
    st.sidebar.markdown("### Create account")
    r_username = st.sidebar.text_input("Username", key="r_username")
    r_first = st.sidebar.text_input("First name", key="r_first")
    r_middle = st.sidebar.text_input("Middle name", key="r_middle")
    r_last = st.sidebar.text_input("Last name", key="r_last")
    r_email = st.sidebar.text_input("Email", key="r_email")
    r_password = st.sidebar.text_input("Password", type="password", key="r_password")
    if st.sidebar.button("Register"):
        payload = {
            "username": r_username,
            "email": r_email,
            "password": r_password,
            "First_name": r_first,
            "Middle_name": r_middle,
            "Last_name": r_last
        }
        res = api_post("/register", json=payload)
        if res:
            if res.status_code == 200:
                st.sidebar.success(f"Registered. Role: {res.json().get('role','user')}. Please login.")
            else:
                st.sidebar.error(res.json().get("detail", res.text))

elif auth_tab == "Login":
    st.sidebar.markdown("### Sign in")
    l_email = st.sidebar.text_input("Email", key="l_email")
    l_password = st.sidebar.text_input("Password", type="password", key="l_password")
    if st.sidebar.button("Login"):
        res = api_post("/login", json={"email": l_email, "password": l_password})
        if res:
            if res.status_code == 200:
                st.session_state["email"] = res.json().get("email", l_email)
                st.session_state["role"] = res.json().get("role", "user")
                st.sidebar.success(f"Logged in: {st.session_state['email']} ({st.session_state['role']})")
            else:
                st.sidebar.error(res.json().get("detail", res.text))

# Logout
if st.session_state["email"]:
    if st.sidebar.button("Log out"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]

# ---- Main ----
st.title("💸 Expense Tracker")

if not st.session_state.get("email"):
    st.info("Please register or login from the left sidebar to continue.")
    st.stop()

is_admin = st.session_state.get("role") == "admin" or st.session_state.get("email", "").lower() == ADMIN_EMAIL.lower()
st.markdown(f"**Logged in as:** `{st.session_state['email']}` — Role: **{st.session_state.get('role','user')}**")

# Tabs for user / admin
tabs = st.tabs(["User", "Admin" if is_admin else ""])

# --- USER TAB ---
with tabs[0]:
    st.header("User Dashboard")

    # Add expense
    st.subheader("Add Expense")
    with st.form("add_expense_form"):
        cats_r = api_get("/categories")
        cats = cats_r.json() if cats_r and cats_r.status_code == 200 else []
        col1, col2, col3 = st.columns(3)
        with col1:
            amount = st.number_input("Amount", min_value=0.0, step=1.0)
        with col2:
            if cats:
                category = st.selectbox("Category", options=cats)
            else:
                category = st.text_input("Category")
        with col3:
            dt = st.date_input("Date", value=date.today())
        description = st.text_input("Description (optional)")
        submitted = st.form_submit_button("Add Expense")
    if submitted:
        payload = {
            "amount": float(amount),
            "category": (category or "").lower(),
            "date": dt.strftime("%Y-%m-%d"),
            "description": description or "",
            "user_email": st.session_state["email"]
        }
        r = api_post("/add-expense", json=payload)
        if r and r.status_code == 200:
            st.success("Expense added successfully.")
        else:
            st.error((r.json().get("detail") if r else "Request failed"))

    # Show my expenses
    st.subheader("View My Expenses")
    if st.button("Load My Expenses"):
        r = api_get("/get-my-expenses", params={"email": st.session_state["email"]})
        if r and r.status_code == 200:
            ex = r.json().get("expenses", [])
            st.dataframe(ex)
        else:
            st.warning("No expenses or failed to fetch.")

    # Update expense
    st.subheader("Update My Expense")
    r = api_get("/get-my-expenses", params={"email": st.session_state["email"]})
    expenses = r.json().get("expenses", []) if r and r.status_code == 200 else []
    if expenses:
        option = st.selectbox("Select expense", [f"{e['_id']} — {e.get('description','')[:30]} (${e['amount']})" for e in expenses])
        expense_id = option.split(" — ")[0]
        exp = next(e for e in expenses if e["_id"] == expense_id)

        col_a, col_b = st.columns(2)
        with col_a:
            new_amount = st.number_input("Amount", value=float(exp["amount"]))
            new_category = st.selectbox("Category", options=cats, index=cats.index(exp["category"]) if exp["category"] in cats else 0) if cats else st.text_input("Category", value=exp["category"])
        with col_b:
            new_date = st.date_input("Date", value=datetime.strptime(exp["date"], "%Y-%m-%d"))
            new_desc = st.text_input("Description", value=exp.get("description",""))

        if st.button("Update selected expense"):
            payload = {
                "expense_id": expense_id,
                "amount": float(new_amount),
                "category": (new_category or "").lower(),
                "date": new_date.strftime("%Y-%m-%d"),
                "description": new_desc
            }
            upd = api_put("/update-my-expense", json=payload, params={"email": st.session_state["email"]})
            if upd and upd.status_code == 200:
                st.success("Expense updated.")
            else:
                st.error((upd.json().get("detail") if upd else "Update failed"))
    else:
        st.info("No expenses to update.")

    # View by month
    st.subheader("View by Month")
    month = st.number_input("Month (1-12)", min_value=1, max_value=12, value=date.today().month)
    if st.button("Filter by month"):
        r = api_get("/expensebymonth/", params={"email": st.session_state["email"], "month": int(month)})
        if r and r.status_code == 200:
            st.dataframe(r.json())
        else:
            st.info("No data or failed to fetch.")

    # Top categories
    st.subheader("Top 3 Categories")
    if st.button("Show Top 3"):
        r = api_get("/get-top-categories", params={"email": st.session_state["email"]})
        if r and r.status_code == 200:
            st.table(r.json())
        else:
            st.info("No data or failed to fetch.")

# --- ADMIN TAB ---
if is_admin:
    with tabs[1]:
        st.header("Admin Dashboard")

        # View all users
        st.subheader("Users")
        if st.button("Load Users"):
            r = api_get("/view-all-users", params={"email": st.session_state["email"]})
            if r and r.status_code == 200:
                st.dataframe(r.json().get("users", []))
            else:
                st.error("Failed to fetch users")

        # View all expenses
        st.subheader("All Expenses")
        if st.button("Load All Expenses"):
            r = api_get("/view-all-expenses", params={"email": st.session_state["email"]})
            if r and r.status_code == 200:
                st.dataframe(r.json().get("expenses", []))
            else:
                st.error("Failed to fetch expenses")

        # Categories management
        st.subheader("Categories (manage)")
        # get categories with ids
        categories_full = api_get("/categories-full")
        cats_full = categories_full.json().get("categories", []) if categories_full and categories_full.status_code == 200 else []

        # Add category
        st.markdown("**Add Category**")
        new_cat = st.text_input("New category name", key="admin_new_cat")
        if st.button("Add Category (admin)"):
            if new_cat.strip():
                r = api_post("/add-category", json={"category": new_cat.strip()}, params={"email": st.session_state["email"]})
                if r and r.status_code == 200:
                    st.success("Category added.")
                else:
                    st.error((r.json().get("detail") if r else "Failed to add"))

        # Show categories full
        if cats_full:
            st.markdown("**Existing categories (id — category)**")
            st.write([{ "_id": c["_id"], "category": c["category"] } for c in cats_full])
        else:
            st.info("No categories found")

        # Update category (by id)
        st.markdown("**Update Category**")
        cat_ids = [c["_id"] for c in cats_full]
        if cat_ids:
            selected_cat_id = st.selectbox("Select category id", options=cat_ids, key="upd_cat_id")
            new_name = st.text_input("New category name", key="upd_cat_name")
            if st.button("Update Category (admin)"):
                if new_name.strip():
                    payload = {"category_id": selected_cat_id, "category": new_name.strip()}
                    r = api_put("/update-category", json=payload, params={"email": st.session_state["email"]})
                    if r and r.status_code == 200:
                        st.success("Category updated.")
                    else:
                        st.error((r.json().get("detail") if r else "Failed to update"))
        else:
            st.info("No categories available to update")

        # Delete category (by id)
        st.markdown("**Delete Category**")
        if cat_ids:
            del_cat_id = st.selectbox("Select category id to delete", options=cat_ids, key="del_cat_id")
            if st.button("Delete Category (admin)"):
                r = api_delete(f"/delete-category/{del_cat_id}", params={"email": st.session_state["email"]})
                if r and r.status_code == 200:
                    st.success("Category deleted.")
                else:
                    st.error((r.json().get("detail") if r else "Failed to delete"))
        else:
            st.info("No categories available to delete")

        # Manage users: delete/update (by id)
        st.subheader("Manage Users")
        r = api_get("/view-all-users", params={"email": st.session_state["email"]})
        users = r.json().get("users", []) if r and r.status_code == 200 else []
        if users:
            st.write("Users (id — username — email)")
            st.write([{ "_id": u["_id"], "username": u.get("username"), "email": u.get("email")} for u in users])
            user_ids = [u["_id"] for u in users]

            sel_user_id = st.selectbox("Select user id", options=user_ids, key="admin_sel_user")
            new_username = st.text_input("New username (leave blank to skip)", key="admin_new_username")
            if st.button("Update User (admin)"):
                payload = {}
                if new_username.strip():
                    payload["username"] = new_username.strip()
                if payload:
                    r = api_put(f"/update-user/{sel_user_id}", json=payload, params={"email": st.session_state["email"]})
                    if r and r.status_code == 200:
                        st.success("User updated.")
                    else:
                        st.error((r.json().get("detail") if r else "Failed to update"))
                else:
                    st.warning("Enter a field to update.")
            if st.button("Delete User (admin)"):
                r = api_delete(f"/delete-user/{sel_user_id}", params={"email": st.session_state["email"]})
                if r and r.status_code == 200:
                    st.success("User deleted (and their expenses & role).")
                else:
                    st.error((r.json().get("detail") if r else "Failed to delete user"))
        else:
            st.info("No users found")

# Footer
st.caption(f"Backend: {API_URL}")
