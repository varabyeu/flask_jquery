from flask import Flask, render_template, request, jsonify
from database import save_to_db, connect_to_db

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/post_item", methods=["POST", "GET"])
def post_item():
    if request.method == 'POST':
        items = request.form.getlist('data_input')
        save_to_db(items)
        return jsonify('Good! We\'ve send it to db!')


@app.route("/items", methods=["GET"])
def items():
    connection = connect_to_db()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, info FROM items")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('data_list.html', data=data)
    except ValueError:
        return render_template('empty_page.html')


if __name__ == "__main__":
    app.run(debug=True)
