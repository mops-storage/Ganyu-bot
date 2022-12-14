from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from oauth import Oauth
import sqlite3


app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY DATABASE_URI'] = 'sqlite:///./'



@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/auth')
def auth():
    return redirect(Oauth.discord_login_url)

@app.route("/login", methods = ["get"])
def login():
    code = request.args.get("code")
    at = Oauth.get_access_token(code)

    user_json = Oauth.get_user_json(at)
    username, usertag, useravatar, userid = user_json.get("username"), user_json.get("discriminator"), user_json.get("avatar"), user_json.get("id")
    user = [username, usertag, useravatar, userid] 
    #return f"{username}#{usertag}\nhttps://cdn.discordapp.com/avatars/{userid}/{useravatar}.png"
    return render_template('login.html', user=user)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('error/404.html')





if __name__ == "__main__":
    app.run(debug=True)
    logo = url_for( 'static', filename='assets/logo.gif')
    
