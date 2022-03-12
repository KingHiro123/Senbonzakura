from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
#from flask_sqlalchemy import SQLAlchemy

import shelve, User
from Forms import Signup_Form, Login_Form

app = Flask(__name__)
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = 'itoldmyselfiwontdothisbuthereweare'

@login_manager.user_loader
def load_user(user_id):
    db = shelve.open('user.db', 'r')
    signup_dict = db['Users']
    db.close()

    return signup_dict.get(user_id)


@app.route('/')
def admin():
    return render_template("Dashboard.html")

@app.route('/login', methods=['GET','POST'])
def login():

    login = Login_Form(request.form)
    if request.method == "POST" and login.validate():
        users_dict = {}
        
        try:
            db = shelve.open('user.db', 'r')
            users_dict = db['Users']

            for key in users_dict:
                user = users_dict[key]
                
                attempted_username = request.form['username']
                attempted_password = request.form['password']

                #the admin is still being tested, once the group has their code integrated
                if attempted_username == 'admin' and attempted_password == 'password':
                    login_user(user)

                    return redirect(url_for('acc_list'))
                else:
                    if login.username.data != user.get_username() or login.password.data != user.get_password():
                        flash(f'Invalid username or password! Please check your login details and try again.', 'warning')
                        return redirect(url_for('login'))
                
            flash(f'Successfully logged in!', 'success')
            db.close()
            login_user(user)
        
            return redirect(url_for('admin', current_user=current_user))   

        except IOError:
            print("Error, it does not exist")
    

    return render_template('Login.html', form=login)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    sign_up = Signup_Form(request.form)
    if request.method == 'POST' and sign_up.validate():
        signup_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            signup_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db")

        if len(signup_dict) > 0:
            for key in signup_dict:
                user = signup_dict[key]

                if sign_up.username.data == user.get_username():
                    flash('This username has already been used.', 'warning')

                    return redirect(url_for('signup'))

                elif sign_up.email.data == user.get_email():
                    flash('This email has already been used.', 'warning')

                    return redirect(url_for('signup'))

            signup = User.User(sign_up.username.data, sign_up.email.data, sign_up.birthday.data, sign_up.password.data, sign_up.confirmpass.data)
            flash(f'Account created for {sign_up.username.data}!', 'success')
            if len(signup_dict) > 0:
                signup.set_user_id(list(signup_dict)[-1]+1) 
            
            signup_dict[signup.get_user_id()] = signup
            db['Users'] = signup_dict
            db.close()

            return redirect(url_for('acc_list'))
        else:
            signup = User.User(sign_up.username.data, sign_up.email.data, sign_up.birthday.data, sign_up.password.data, sign_up.confirmpass.data)
            flash(f'Account created for {sign_up.username.data}!', 'success')
            if len(signup_dict) > 0:
                signup.set_user_id(list(signup_dict)[-1]+1) 
            
            signup_dict[signup.get_user_id()] = signup
            db['Users'] = signup_dict
            db.close()

            return redirect(url_for('acc_list'))
            
    return render_template('Register.html', form=sign_up)

@app.route('/account')
def acc_list():
    users_dict = {}
    try:
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()
    except IOError:
        print("Error has occurred while trying to read.")
    except:
        print('An unknown error has occurred.')

    user_list = []
    for key in users_dict:
        user = users_dict.get(key)
        user_list.append(user)

    return render_template('Account.html', count=len(user_list), user_list=user_list)

#Update
#@app.route('/Update/<int:id>/', methods=['GET','POST'])
#def update(id):
#    return render_template('', form=update_signup_form)
if __name__ == '__main__':
    app.run(debug=True)
