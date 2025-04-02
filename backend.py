import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = "/project/myanmar_safe_bot/earthdb.db"
# Home Page - Display mdysafe

@app.route("/")
def home():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mdysafe")
    users = cursor.fetchall()
    conn.close()
    return render_template("index.html", users=users)

# Create User (Insert)
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    phone = request.form["phone"]
    location = request.form["location"]
    date = request.form["date"]
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mdysafe (name, phone, location,date) VALUES (?, ?, ?,?)", (name, phone, location,date))
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

# Update User (Edit)
@app.route("/edit/<int:user_id>", methods=["GET", "POST"])
def edit(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        location = request.form["location"]
        date = request.form["date"]
        cursor.execute("UPDATE mdysafe SET name=?, phone=?, location=?,date=?  WHERE id=?", (name, phone, location,date, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for("home"))

    cursor.execute("SELECT * FROM mdysafe WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return render_template("medit.html", user=user)

# Delete User
@app.route("/delete/<int:user_id>")
def delete(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mdysafe WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))


##mdyfood
@app.route("/mdydonate")
def home_mdy():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mdydonate")
    users = cursor.fetchall()
    conn.close()
    return render_template("mdy_food.html", users=users)

@app.route("/submitmd", methods=["POST"])
def submitmd():
    name = request.form["name"]
    phone = request.form["phone"]
    location = request.form["location"]
    date = request.form["date"]
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mdydonate (name, phone, location,date) VALUES (?, ?, ?,?)", (name, phone, location,date))
    conn.commit()
    conn.close()

    return redirect(url_for("home_mdy"))

@app.route("/mdydonate/delete/<int:user_id>")
def deletemdy(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mdydonate WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home_mdy"))

@app.route("/mdydonate/edit/<int:user_id>", methods=["GET", "POST"])
def editmdy(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        location = request.form["location"]
        date = request.form["date"]
        cursor.execute("UPDATE mdydonate SET name=?, phone=?, location=?,date=?  WHERE id=?", (name, phone, location,date, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for("home_mdy"))

    cursor.execute("SELECT * FROM mdydonate WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return render_template("mdy_food_edit.html", user=user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

