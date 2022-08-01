from flask import Flask, render_template, request, jsonify
from database import save_to_db, connect_to_db

app = Flask(__name__)


@app.route('/')
def index():
    """Main page render function"""
    return render_template('index.html')


@app.route("/post_item", methods=["POST", "GET"])
def post_item():
    """Function to get data from form and save it to database"""
    # work with form
    if request.method == 'POST':
        # get all data from form
        items = request.form.getlist('data_input')
        # saving data from form with function from external module
        save_to_db(items)
        # When we click the submit button, we show a message
        return jsonify('Good! We\'ve send it to db!')


@app.route("/items", methods=["GET"])
def items():
    """Function to show all available data on the page"""
    # get connection to the db from external module function
    connection = connect_to_db()
    # use try...except to ignore errors related to empty db
    try:
        # get the cursor
        cursor = connection.cursor()
        # Get the data from table
        cursor.execute("SELECT id, info FROM items")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        # if all is OK, template with data is rendered
        return render_template('data_list.html', data=data)
    except ValueError:
        # if we find a problem, template without data is rendered
        return render_template('empty_page.html')


if __name__ == "__main__":
    app.run(debug=True)
