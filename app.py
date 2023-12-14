from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdfgkjtjkkg45yfdb"

boggle_game = Boggle()


@app.route("/")
def homepage():
    """Show game board."""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    play_count = session.get("play_count", 0)

    return render_template("index.html", board=board,
                           highscore=highscore,
                           play_count=play_count)
    
@app.route('/start')
def restart_game():
    """Restart Game"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    play_count = session.get("play_count", 0)

    return render_template("index.html", board=board,
                           highscore=highscore,
                           play_count=play_count)


@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update play_count, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    play_count = session.get("play_count", 0)

    session['play_count'] = play_count + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
