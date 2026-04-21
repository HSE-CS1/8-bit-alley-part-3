from cs50 import SQL

db = SQL("sqlite:///gamers.db")

def get_usernames():
    sql = "SELECT player_id, username FROM players ORDER BY username"
    rows = db.execute(sql)
    return rows

def get_all_players():
    sql = "SELECT * FROM players ORDER BY join_date DESC"
    players = db.execute(sql)
    # select statement return a list of dictionaries
    return players

def add_player(username, email):
    sql = "INSERT INTO players (username, email) VALUES (?, ?)"
    try:
        pk = db.execute(sql, username, email)
        # insert statements will return the primary key of the new row
        return pk
    except ValueError as e:
        return -99



# this will check if an email is already in the database
def is_unique_email(email_addr):
    sql = "SELECT email FROM players WHERE email = ?"
    emails = db.execute(sql, email_addr)
    if len(emails) == 0:
        return True
    else:
        return False

def record_player_game(player_id, game_id, score, date_played):
    sql = """INSERT INTO player_history (player_id, game_id, score, date_played)
    VALUES (?, ?, ?, ?)"""
    history_id = db.execute(sql, player_id, game_id, score, date_played)
    return history_id

def get_game_history(player_id):
    sql = """SELECT username, title, score, date_played FROM player_history
        JOIN players USING (player_id)
        JOIN games USING (game_id)
        WHERE player_id = ? ORDER BY date_played DESC"""
    rows = db.execute(sql, player_id)
    return rows



def get_all_games_by_title():
    sql = """SELECT game_id, title FROM games ORDER BY title"""
    return db.execute(sql)


def get_player_by_id(p_id):
    sql = "SELECT * FROM players WHERE player_id = ?"
    players = db.execute(sql, p_id)
    #remember we expect a list of dictionaries
    if len(players) != 1:
        return None
    else:
        # return the one dictionary in the list (at index 0)
        return players[0]


def validate_price(price):
    # price must be a number >= 0
    try:
        price = float(price)
    except ValueError as e:
        return f'Sorry {price} is not a number.'
    except:
        return 'Sorry, there was an error!'
    else: # this runs if there are no exceptions
        if price >= 0:
            return price
        else:
            return 'Sorry, price must be at least 0'

def get_username(id):
    sql = 'SELECT username FROM players WHERE player_id = ?'
    rows = db.execute(sql, id)
    if len(rows) == 1:
        return rows[0].get('username')
    else:
        return None

def get_player_email(id):
    sql = 'SELECT email FROM players WHERE player_id = ?'
    rows = db.execute(sql, id)
    if len(rows) == 1:
        email = rows[0].get('email')
        if email:
            return email
        else: # email was NULL in the database
            return -99
    else: # no players were found
        return None

def email_used(new_email):
    sql = 'SELECT email FROM players WHERE email = ?'
    rows = db.execute(sql, new_email)
    if len(rows) > 0: # found a matching email
        return True
    else:
        # no matches, so the new email is unique
        return False


def delete_player(id):
    sql = "DELETE FROM players WHERE player_id = ?"
    number_deleted = db.execute(sql, id)
    return number_deleted

def update_player(username, email, join_date, id):
    sql = 'UPDATE players SET username = ?, email = ?, join_date = ? WHERE player_id = ?'
    number_updated = db.execute(sql, username, email, join_date, id)
    return number_updated

