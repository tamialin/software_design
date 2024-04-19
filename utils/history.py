from utils.temp_db import quote_history_db

# Function to get quote history for a user
def get_quote_history(username, mysql):
    quote_history = []
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT quote_history.*, users.city, users.zip, users.states FROM quote_history JOIN users ON quote_history.username = users.username WHERE quote_history.username = %s", (username,))
        #cursor.execute("SELECT * FROM quote_history WHERE username = %s", (username,))
        quote_history = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print("Error fething quote history: ", str(e))
    return quote_history

