from flask import Flask, render_template, request, redirect, jsonify
import json
import os

app = Flask(__name__)

JSON_FILE = "mdy_resuce_data.json"

# Load JSON data
def load_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Save JSON data
def save_data(data):
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/")
def home():
    users = load_data()
    return render_template("index.html", users=users)



@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    phone = request.form["phone"]
    location = request.form["location"]

    
    new_entry = {"name": name, "phone": phone, "location": location}

    
    with open("mdy_resuce_data.json","r+") as hs:
            data = json.load(hs)
                
            data['rescue_name'].insert(0,name)
            data['location'].insert(0,phone)
            data['phone'].insert(0,location)
            hs.seek(0)
            json.dump(data,hs,indent=4)
    return redirect("/")

@app.route("/api/users", methods=["GET"])
def api_users():
    return jsonify(load_data())

if __name__ == "__main__":
    app.run(debug=True)
