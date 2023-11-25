#conn = mysql.connector.connect(host="localhost",user="root",password="root", database="banking_management_system_dbms")
import streamlit as st
import mysql.connector
import random

conn = mysql.connector.connect(host="localhost",user="root",password="root", database="banking_management_system_dbms")

cursor = conn.cursor()

if "user_creation" not in st.session_state:
    st.session_state.user_creation = {
        "new_username": "",
        "new_password": "",
        "new_first_name": ""
    }

st.title("Bank Management System")

navigation = st.sidebar.radio("Navigation", ["Home", "Create User"])

if navigation == "Home":
    st.subheader("Home Page")

    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        query_login = f"SELECT user_id, role FROM Users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query_login)
        user = cursor.fetchone()

        if user:
            st.success("Login successful!")
            st.subheader("User Information:")
            st.write(f"User ID: {user[0]}")
            st.write(f"Role: {user[1]}")

            if user[1] == "admin":
                st.subheader("Admin Options:")
                user_id_to_delete = st.text_input("Enter User ID to Delete:")
                if st.button("Delete Account"):
                    # Perform account deletion logic here
                    if user_id_to_delete.isdigit():
                        user_id_to_delete = int(user_id_to_delete)


                        query_delete_user = f"DELETE FROM Users WHERE user_id = {user_id_to_delete}"
                        cursor.execute(query_delete_user)
                        conn.commit()
                        st.success("Account deleted successfully!")

                        st.rerun()

            else:
                st.subheader("User Options:")
                if st.button("Create Account"):
                    account_number = random.randint(1000000000, 9999999999)
                    query_create_account = f"INSERT INTO Accounts (account_number, account_type, balance, user_id) VALUES ({account_number}, 'Savings', 0, {user[0]})"
                    cursor.execute(query_create_account)
                    conn.commit()
                    st.success(f"Account created successfully! Account Number: {account_number}")

                transaction_amount = st.number_input("Enter Transaction Amount:", min_value=0.01)
                destination_account = st.text_input("Enter Destination Account Number:")

                if st.button("Perform Transaction"):
                    sender_account = "get_user_account_number_based_on_user_id"  # Replace with actual logic
                    query_balance = f"SELECT balance FROM Accounts WHERE account_number = '{sender_account}'"
                    cursor.execute(query_balance)
                    sender_balance = cursor.fetchone()[0]

                    if sender_balance >= transaction_amount:
                        query_update_sender = f"UPDATE Accounts SET balance = balance - {transaction_amount} WHERE account_number = '{sender_account}'"
                        cursor.execute(query_update_sender)

                        query_destination_exists = f"SELECT * FROM Accounts WHERE account_number = '{destination_account}'"
                        cursor.execute(query_destination_exists)
                        destination_exists = cursor.fetchone()

                        if destination_exists:
                            query_update_destination = f"UPDATE Accounts SET balance = balance + {transaction_amount} WHERE account_number = '{destination_account}'"
                            cursor.execute(query_update_destination)

                            st.success("Transaction successful!")
                        else:
                            st.error("Destination account does not exist!")
                    else:
                        st.error("Insufficient balance!")

        else:
            st.error("Invalid username or password")

elif navigation == "Create User":
    st.subheader("Create User Page")
    new_username_landing = st.text_input("New Username:")
    new_password_landing = st.text_input("New Password:", type="password")
    new_first_name_landing = st.text_input("First Name:")
    if st.button("Create User"):


        query_create_user = f"INSERT INTO Users (username, password, role) VALUES ('{new_username_landing}', '{new_password_landing}', 'User')"
        cursor.execute(query_create_user)
        conn.commit()
        st.success("User created successfully!")

        st.session_state.user_creation = {
            "new_username": "",
            "new_password": "",
            "new_first_name": ""
        }

        st.experimental_rerun()

# elif navigation == "Create Account":
#     st.subheader("Create Account Page")
#
#     if st.button("Create Account"):
#         query_fetch_user_id = f"SELECT user_id FROM Users WHERE username = '{username}' AND password = '{password}'"
#         cursor.execute(query_fetch_user_id)
#         user_id = cursor.fetchone()[0]
#
#         account_number = random.randint(1000000000, 9999999999)
#         query_create_account = f"INSERT INTO Accounts (account_number, account_type, balance, user_id) VALUES ({account_number}, 'Savings', 0, {user_id})"
#         cursor.execute(query_create_account)
#         conn.commit()
#         st.success(f"Account created successfully! Account Number: {account_number}")
#
#         st.experimental_rerun()

conn.close()
