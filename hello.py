import os
import psycopg2
from flask import Flask, render_template, jsonify, request, Blueprint, url_for, redirect

#from sqlalchemy import create_engine

#engine = create_engine('postgresql://user:user@localhost:5432/test')

app = Flask(__name__)

from contact import contact_bp

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


#run bellow command on terminal to connect flaskdb
#export DB_USERNAME="flask"
#export DB_PASSWORD="flask123"

@app.route('/book/')
def book():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    books = cur.fetchall()
    cur.close()
    conn.close()
    print('book data', books)
    #return 'hey there'
    return render_template('book.html', books=books)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages_num = int(request.form['pages_num'])
        review = request.form['review']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO books (title, author, pages_num, review)'
                    'VALUES (%s, %s, %s, %s)',
                    (title, author, pages_num, review))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('book'))

    return render_template('create.html')


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/test/<name>')
def test_rakesh(name):
    return 'Hello %s' % name

@app.before_request
def before():
    print("This is executed BEFORE each request.")

@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    print('request data', request.data)
    app.logger.debug('This is a DEBUG message', request.data)
    return jsonify({'name':'Rakesh',
                    'address':'Hyderabad'})

app.register_blueprint(contact_bp, url_prefix='/contact')

if __name__ == '__main__':
   app.run(debug=True, use_reloader=True)