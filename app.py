from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

connection = psycopg2.connect(
    host="127.0.0.1",
    database="bookswap",
    user="postgres",
    password="papaya"
)

@app.route("/")
def index():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Book")
    rows = cursor.fetchall()
    return render_template("index.html", rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
