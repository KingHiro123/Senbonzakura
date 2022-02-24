from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy

#import shelve

db = SQLAlchemy()
 
app = Flask(__name__)

app.config['SECRET_KEY'] = 'itoldmyselfiwontdothisbuthereweare'

@app.route('/')
def admin():
    return render_template("Dashboard.html")

@app.route('/account')
def account_list():
    #users_dict = {}
    #db = shelve.open('user.db', 'r')
    #users_dict = db['Users']
    #db.close()
#
    #users_list = []
    #for key in users_dict:
    #    user = users_dict.get(key)
    #    users_list.append(user)

    return render_template('Account.html')


if __name__ == '__main__':
    app.run(debug=True)
