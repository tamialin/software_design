# create history for 2 users and then display whenever session valid
quote_history = {
    'user1': [],
    'user2': []
}

# Function to update quote history for a user
def update_quote_history(username, quote_data):
    if username in quote_history:
        quote_history[username].append(quote_data)
        return True
    else:
        return False

# Function to get quote history for a user
def get_quote_history(username):
    if username in quote_history:
        return quote_history[username]
    else:
        return []


# create an object/list to store values passed from fuelModule and render it back to history.html