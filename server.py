"""
Simple contacts web app using flask and sqlite3 database to store the contacts
"""
import hashlib
from flask import Flask, render_template, request, redirect
from db_con import ConnectionClass

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home_page():
    """
    The home page with request method
    """
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    global login_cred
    
    if request.method == 'GET':
        if login_cred is not None:
            return redirect('/contacts')
        else:
            return render_template('login.html')

    elif request.method == 'POST':
        email = request.form.get('email')
        password = get_hash_from_password(request.form.get('password'))
        print(email, password)

        login_cred = db_con.user_login_with_email(email, password)
        print(login_cred)
        if login_cred is not None:
            print('User logged in')
            return redirect('/contacts')

        else:
            print('User not logged in')
            return render_template('login.html', login_error='Wrong login credentials')


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    global login_cred
    
    if request.method == 'GET':
        if login_cred is not None:
            return redirect('/contacts')
        else:
            return render_template('signup.html')

    elif request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = get_hash_from_password(request.form.get('password'))
        unique_id = get_unique_id_from_data(name, email, password)

        print(unique_id, name, email, password)

        if db_con.check_whether_email_exists(email):
            print('Email already exists')
            return render_template('signup.html', signup_error='Email already exists')

        else:
            print('New user')
            login_cred = (unique_id, name, email, password)
            db_con.user_signup_with_email(unique_id, name, email, password)
            return redirect('/contacts')


@app.route('/contacts')
def contacts_page():
    global login_cred
    
    if login_cred is None:
        return redirect('/login')
    
    return render_template('contacts.html', user_name=login_cred[1])

@app.route('/logout')
def user_logout():
    global login_cred
    
    login_cred = None
    return redirect('/')


@app.route('/error')
def error_page():
    return render_template('error.html')


@app.route('/delete/<string:name>')
def delete_data(name):
    """
    The delete page with name as the parameter
    """

    db_con.delete_data_from_name(name)

    return redirect('/')


@app.route('/update/<string:name>', methods=['GET', 'POST'])
def update_data(name):
    """
    The update page with name as the parameter
    """
    if request.method == 'GET':

        number = db_con.get_data_from_name(name)

        return render_template('update.html', name=name, number=number)

    elif request.method == 'POST':
        number = int(request.form.get('number'))
        print(number, type(number))

        db_con.update_data(name, number)

        return redirect('/')


def get_unique_id_from_data(name, email, password):
    """
    Generate the unique id for the credentials
    """
    return hashlib.sha1((name + email + password).encode()).hexdigest()


def get_hash_from_password(password: str) -> str:
    """
    Get the hash from the password

    Args:
        password (str): The password of the user

    Returns:
        str: The hash of the password
    """
    return hashlib.sha256(password.encode()).hexdigest()


if __name__ == '__main__':
    print('Connecting to the database...')
    db_con = ConnectionClass()

    if db_con.check_connection():
        print('Connected to the database')
        
        # Global variable to store the login credentials
        # in the form of a (unique_id, name, email, password) tuple
        login_cred = None

        app.run(debug=True, host='0.0.0.0', port=5000)

        db_con.close_connection()
        print('Connection closed')

    else:
        print('Not connected to the database')
