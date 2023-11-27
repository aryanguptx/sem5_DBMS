from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import random

app = Flask(__name__)

conn = mysql.connector.connect(host="localhost", user="springstudent", password="springstudent",
                               database="bank_management_system")
cursor = conn.cursor()


def delete_user(user_id_to_delete):
    user_id_to_delete = int(user_id_to_delete)

    query_delete_user = f"DELETE FROM Users WHERE user_id = {user_id_to_delete}"
    cursor.execute(query_delete_user)
    conn.commit()
    if cursor.rowcount >= 1:
        print("Delete query executed successfully.")
    else:
        print("No rows were deleted.")
    return "Account deleted successfully!"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    query_login = f"SELECT user_id, role FROM Users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query_login)
    user = cursor.fetchone()

    if user:
        user_id = user[0]
        role = user[1]

        if role == "admin":
            return redirect(url_for('admin_dashboard', user_id=user_id))
        else:
            return redirect(url_for('user_dashboard', user_id=user_id))

    return render_template('home.html', error="Invalid username or password")


@app.route('/admin_dashboard/<int:user_id>')
def admin_dashboard(user_id):
    query = "SELECT user_id FROM users WHERE role = 'user'"
    cursor.execute(query)
    data = cursor.fetchall()
    user_ids = [item[0] for item in data]

    return render_template('admin_dashboard.html', user_ids=user_ids)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user_route(user_id):
    result = delete_user(user_id)
    return result




@app.route('/user_dashboard/<int:user_id>')
def user_dashboard(user_id):
    return render_template('user_dashboard.html', user_id=user_id)


# app.py

# ... (previous code)

@app.route('/create_account/<int:user_id>', methods=['POST'])
def create_account(user_id):
    account_number = request.form['account_number']
    account_type = request.form['account_type']
    balance = request.form['balance']

    # Perform the logic to insert the new account into the database
    # Make sure to associate the account with the given user_id

    # Example SQL query (replace with your actual query)
    query_create_account = f"INSERT INTO Accounts (account_number, account_type, balance, user_id) VALUES ('{account_number}', '{account_type}', {balance}, {user_id})"
    cursor.execute(query_create_account)
    conn.commit()

    return "Account created successfully!"

# ... (rest of the code)
@app.route('/get_user_details/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    # Execute the stored procedure
    print(user_id)
    cursor.execute(f"call GetUserDetails({user_id});",multi=True)
    result = cursor.fetchall()
    print("result=",result)
    # Create a string to display the result
    user_details_str = "<h3>User Details:</h3><ul>"
    for row in result:
        user_details_str += f"<li>User ID: {row[0]}, Username: {row[1]}, Account Number: {row[2]}, First Name: {row[3]}, Last Name: {row[4]}</li>"
    user_details_str += "</ul>"

    return user_details_str



if __name__ == '__main__':
    app.run(debug=True)
