from flask import Flask
import socket
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    host="db",
    port=5432,
    dbname="testdb",
    user="testdb",
    password="testdb")

@app.route('/')
def hello_geek():

    cur = conn.cursor()
    cur.execute('SELECT 1')
    result = cur.fetchone()
    cur.close()

    return f'Hello, Container ID: {socket.gethostname()}<br>Database connection test: {result[0]}'


if __name__ == "__main__":
    app.run(debug=True)