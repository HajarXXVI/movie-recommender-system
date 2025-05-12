import streamlit as st

def login(userName: str, password: str) -> bool:
    if not userName or not password:
        return False
    try:
        args = [userName, password, 0]
        st.write(f"Executing CheckUser with args: {args}")  # Debugging line to print parameters
        result_args = execute_sql_query("CheckUser", args)
        st.write(f"Result from CheckUser stored procedure: {result_args}")  # Debugging line to print result
        return result_args[2] == 1  # Check the third element for success (1) or failure (0)
    except Exception as e:
        st.write(f"Error: {e}")  # Error handling
        return False

def execute_sql_query(query, args):
    config = ConfigParser()
    config.read("config.ini")
    cnx = mysql.connector.connect(
        host=config.get('MySQL', 'host'),
        port=config.get('MySQL', 'port'),
        database=config.get('MySQL', 'database'),
        user=config.get('MySQL', 'user'),
        password=config.get('MySQL', 'password')
    )
    
    cursor = cnx.cursor()
    try:
        result = cursor.callproc(query, args)
        cnx.commit()  # Commit the transaction
        return result
    except mysql.connector.Error as err:
        st.write(f"SQL Error: {err}")  # Log SQL errors
        return [None, None, 0]  # Return a default failure value in case of an error
    finally:
        cursor.close()
        cnx.close()
