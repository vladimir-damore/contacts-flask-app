from flask import Flask, render_template, request
import sqlite3

class Contacts:
    def __init__(self):
        self.__my_conn = sqlite3.connect('db/contacts.db')
        self.__my_curr = self.__my_conn.cursor()
    
    def put_data(self, name, number):
        self.__my_curr.execute(f'insert into identity values ("{name}", {number})')
        self.__my_conn.commit()

    def get_data(self):
        self.__my_curr.execute('select * from identity')
        return self.__my_curr.fetchall()

    def close_conn(self):
        self.__my_conn.close()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'GET':
        obj = Contacts()
        all_data = obj.get_data()
        obj.close_conn()

        return render_template('index.html', all_data=all_data)

    elif request.method == 'POST':
        name = request.form.get('name')
        number = request.form.get('number')
        obj = Contacts()
        obj.put_data(name, number)
        obj.close_conn()

        return render_template('success.html')
 
@app.route('/delete', methods=['GET', 'POST'])
def delete_data():
    if request.method == 'GET':
        return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')