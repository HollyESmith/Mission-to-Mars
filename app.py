# This is where we'll use Flask and Mongo to begin creating Robin's web app.
import Mission_to_Mars_Challenge as scraping

# use Flask to render a template, redirecting to another url, and creating a URL
from flask import Flask, render_template, redirect, url_for

# use PyMongo to interact with our Mongo database
from flask_pymongo import PyMongo

# to use the scraping code, we will convert from Jupyter notebook to Python
#import scraping

#set up Flask
app = Flask(__name__)

# tell Python how to connect to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the route for the HTML page:
# tell Flask what to display when we're looking at the home page
@app.route("/")
def index(): 
   mars = mongo.db.mars.find_one() # use PyMongo to find the "mars" collection in our database
   return render_template("index.html", mars=mars) # tell Flask to return an HTML template using an index.html file, 
   # mars=mars tells Python to use the "mars" collection in MongoDB

# set up scraping code
@app.route("/scrape") #defines the route that Flask will be using, will run the following 'scrape' function
def scrape():
   mars = mongo.db.mars # assign a new variable that points to our Mongo database
   mars_data = scraping.scrape_all() # create a new variable to hold the newly scraped data
   
   print(mars_data)
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

# tell Flask to run
if __name__ == "__main__":
   app.run()
