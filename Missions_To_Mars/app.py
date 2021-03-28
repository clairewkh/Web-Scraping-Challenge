# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars 

# Creates application
app = Flask(__name__)

# setup mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

print(mongo)


# Home Route
@app.route("/")
def index():
    
    storing_dict = mongo.db.storing_dict.find_one()
    return render_template("index.html",storing_dict=storing_dict)
    

# Scrape Route
@app.route("/scrape")
def scrape():
    storing_dict = mongo.db.storing_dict
    storing_dict_data = scrape_mars.scrape()
    storing_dict.update({}, storing_dict_data, upsert=True)
    return redirect("/", code=302)

# Runs application
if __name__ == "__main__":
    app.run(debug=True)