from flask import Flask, render_template, request, redirect, session
import queries as q
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'cachelib'
Session(app)


@app.route('/')
def home():
    # get all the players from our table
    players = q.get_usernames()

    if session.get('player_id'):
        player = q.get_player_by_id(session.get('player_id'))
        username = player.get('username')
    else:
        username = None

    return render_template('index.html', players=players,
                                         username=username)


@app.route('/favorite', methods=["GET", "POST"])
def favorite():
    # store the selected player into a session
    if request.method == "POST":
        player_id = request.form.get("player")
        if not player_id:
            return redirect('/')
        else:
            # store the player_id in the session
            session["player_id"] = player_id
            # stoe the player's usernam as another session variable
            session["username"] = q.get_player_by_id(player_id).get('username')
            return redirect('/record_game')

@app.route('/record_game', methods=["GET", "POST"])
def record_game():
    # check for the session
    if not session.get('username'):
        # we haven't seleced a player
        return redirect('/')
    else:
        if request.method == "GET":
            # they have choosen a player
            # show a form that allows the user to enter games for their history
            # we will need list of all the games and their game_id
            games = q.get_all_games_by_title()
            return render_template('gamehistory.html', games=games)
        else:
            # add the game to the player history table
            game_id = request.form.get('game')
            score = int(request.form.get('score'))
            # we should do a try and except here to make sure it is a number
            date_played = request.form.get('date')

            #now add this data to the palyer_history table
            hist_id = q.add_history(session.get('player_id'), game_id, score, date_played)

            # TODO show all the game history for the player in this session
            game_history = q.get_history_by_player(session.get('player_id'))
            return game_history

@app.route('/logout')
def logout():
    # to delete a session variable
    # session["player_id"] = None
    # to delete all session variavles
    session.clear()
    return redirect('/')


@app.route('/players')
def players():

    players = q.get_all_players()
    return render_template('players.html', players=players)

@app.route('/join', methods=["GET", "POST"])
def join():
    if request.method == "GET":
        # show the form
        return render_template('add_player.html')
    else:
        # process the form
        username = request.form.get('username')
        if not username or username.strip() == "":
            return redirect('/join')
        email = request.form.get('email')
        if email.strip() == "":
            email = None
        # now add the username and email to the datatbase
        player_id = q.add_player(username, email)
        if player_id < 0:
            #ERROR
            message = f'ERROR, {email} is already taken!'
            return render_template('error.html', message=message)
        # on a real app, we would probably want to flash a message
        return redirect('/players')

@app.route('/delete/<int:id>', methods=["GET", "POST"])
def delete(id):
    if request.method == "GET":
        # always a good idea to make the user confirm a deletion
        return render_template('confirm.html', id=id)
    else: # they filled out the confirmation form
        email = request.form.get('email').strip()
        # make sure this email matches the one in the database
        player_email = q.get_player_email(id)
        # should check for None as a result

        if email == player_email:
            # form email matched the one in the database
            # now delete the player
            result = q.delete_player(id)
            if result == 1:
                # we should flash a message
                return redirect('/players')
        else:
            return render_template('error.html', message='Emails do not match, no players were deleted')

@app.route('/edit/<int:id>', methods=["POST"])
def edit(id):
    #TODO get the form data
    username = request.form.get('username').strip()
    if not username:
        return render_template('error.html', message='Username is required!')

    email = request.form.get('email').strip()
    if not email:
        email = None
    # need to make sure the email entered is unique.
    previous_email = q.get_player_email(id)
    if email != previous_email and not q.email_is_unique(email):
        msg = f'{email} is already taken, please provide a unique email address'
        return render_template('error.html', message=msg)


    join_date = request.form.get('join-date')
    # no need to validate the join_date

    player_info = {
        'username': username,
        'email':email,
        'join_date': join_date
    }

    # now we can update the player's information
    result = q.update_player(player_info, id)
    print(f'{result} player was updated')
    return redirect('/players')



@app.route('/player/<int:p_id>')
def player_info(p_id):
    # get all the info for this specific player
    player = q.get_player_by_id(p_id)
    if player:
        return render_template('edit_player.html', player=player)
    else:
        return render_template('error.html', message='Sorry no player found!')

