from flask import Flask, render_template, request, redirect, session
import queries as q
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'cachelib'
Session(app)


@app.route('/')
def home():
    players = q.get_usernames()
    return render_template('index.html', players=players)

@app.route('/login', methods=["GET", "POST"])
def login():
    # when the user fills out the form
    if request.method == "POST":
        player_id = request.form.get('player')
        # make sure they selected a player
        if not player_id:
            return redirect('/')
        else:
            # add the player to the session
            session["player_id"] = player_id
            player = q.get_player_by_id(player_id)
            session['username'] = player.get('username')
            return redirect('/record_game')

@app.route('/record_game', methods=["GET","POST"])
def record_game():
    # make sure a player has been selected
    if not session.get('player_id'):
        return redirect('/')
    else:
        #they have selected a player from the drop-down
        if request.method == "GET":
            # show a form to add a game to the player's history
            # we need the title and id for all games
            games = q.get_all_games_by_title()
            return render_template('gamehistory.html', games=games)
        else:
            # process the form data
            # grab the data from the form
            game_id = int(request.form.get('game')) # not error checking
            score = int(request.form.get('score')) # not error checking
            date_played = request.form.get('date')

            # now add the data to the player_history table
            history_id = q.record_player_game(session.get('player_id'), game_id, score, date_played)

            # now show all the games the player has played
            return redirect(f'/game_history/{session.get("player_id")}')

@app.route('/game_history/<int:player_id>')
def game_history(player_id):
    g_history = q.get_game_history(player_id)
    return g_history





@app.route('/logout')
def logout():
    # remove or delete session variables
    session['username'] = None

    # to remove all the session keys
    session.clear()
    # go back to the home page
    return redirect('/')


@app.route('/players')
def players():
    # get all the players
    all_players = q.get_all_players()
    return render_template('players.html', all_players=all_players)

@app.route('/join', methods=["GET", "POST"])
def new_member():
    if request.method == "GET":
        # show the form
        return render_template('add_player.html')
    else:
        # process the form --> add the user to the database
        username = request.form.get("username")
        if not username or username.strip() == "":
            # in a real app we would want to flash a message
            return redirect('/join')
        email = request.form.get("email")
        if email.strip() == "":
            email = None
        player_id = q.add_player(username, email)
        if player_id < 0:
            err = 'SORRY That email is already taken'
            return render_template('error.html', message=err)
        else:
            # in real life we would want to flash a message
            return redirect('/players')

@app.route('/edit/<int:p_id>')
def edit_player(p_id):
    # we need to get all the info about this specific player
    player = q.get_player_by_id(p_id)
    if not player:
        return render_template('error.html', message=f'SORRY, player {p_id} not found')
    else:
        return render_template('edit_player.html', player=player)

@app.route('/add')
def add():
       msg="Add ability to add new games"
       return render_template('error.html', message=msg)





@app.route('/delete/<int:id>', methods=["GET", "POST"])
def delete(id):
    if request.method == "GET":
        # show a confirmation page
        return render_template('confirm.html', id=id)
    else:
        # make sure the username they typed into the form matches the one in the
        # database
        username = request.form.get('username').strip()
        player_username = q.get_username(id)
        if username == player_username:
            result = q.delete_player(id)
            if result > 0:
                # we would want to falsh a message or show a success page
                return redirect('/players')
        else:
            msg = f'Sorry {username} did not match, no players were deleted.'
            return render_template('error.html', message=msg)

@app.route('/update/<int:id>', methods=["POST"])
def update(id):
    # get the data from the form
    username = request.form.get('username').strip()
    if not username:
        msg = 'A username is required!'
        return render_template('error.html', message=msg)

    email = request.form.get('email').strip()
    if not email:
        email = None
    if q.email_used(email) and email != q.get_player_email(id):
        # email has been changed and it is not unique
        msg = f'Sorry, {email} has already been used.'
        return render_template('error.html', message=msg)


    join_date = request.form.get('join-date')

    # now update the players table
    result = q.update_player(username, email, join_date, id)
    #flash a message or show success page
    return redirect('/players')

















@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

