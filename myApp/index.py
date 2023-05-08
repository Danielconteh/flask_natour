from flask_htmlmin import HTMLMIN
from dotenv import load_dotenv
import os

from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import datetime


# APP GLOBAL CONFIG
app = Flask(__name__, template_folder='./templates')
# APP TEMPLATE CONFIG
app.config['MINIFY_HTML'] = True
htmlmin = HTMLMIN(app)

load_dotenv()

# CONNECTION TO MONGODB
client = MongoClient(os.getenv('DB_URI'))
db = client['natour']
tourDB = db['tours']
GuidesDB = db['guides']






# CUSTOM TEMPLATE TAG
@app.template_filter('strftime')
def filter_datetime(value): return datetime.strptime(value.split('T')[0], '%Y-%m-%d').strftime("%B, %Y")


@app.template_filter('slug')
def slug_text(value):
    val = value.split(' ')
    return '-'.join(val)


# HOME PAGE ROUTE
@app.route('/',  methods=['GET', 'POST'])
def tours():
   data = None
   filterData = False
   if(request.method == 'POST'):
       filterData = True
       data = tourDB.find({'name':request.form['search'].title()}) 
       
   else:
       filterData = False
       data = tourDB.find({}) 

   return  render_template('tour/home.html', tours=data, filterData=filterData)



# GET A SINGLE TOUR DETAILS  
@app.route('/<string:tour>')
def single_tour(tour):
   query = tour.split('-')

   data = tourDB.find_one({'name': ' '.join(query)})
   data_guide = []
   

   for index, item in enumerate(data['guides']):
       guide = GuidesDB.find({'_id':item})
       data_guide.append(guide[0])

   # data.update({'guide': guide})
   data.update({'guide': data_guide})
   



   return render_template('tour/single-tour.html', tour=data)



if __name__ == '__main__':
   app.run(debug = False, host='0.0.0.0')



