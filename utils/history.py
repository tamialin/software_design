from utils.temp_db import quote_history_db

# Function to update quote history for a user
def update_quote_history(username, quote_data):
    if username in quote_history_db:
        quote_history_db[username].append(quote_data)
        return True
    else:
        return False

# Function to get quote history for a user
def get_quote_history(username):
    quote_history = []
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM quote_history WHERE username = %s", (username,))
        quote_history = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print("Error fething quote history: ", str(e))
    return quote_history


    # if username in quote_history_db:
    #     return quote_history_db[username]
    # else:
    #     return []
