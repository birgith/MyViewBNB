from flask import render_template
from app import app
from flask import request
import sys
sys.path.append('project/')
from Run_Analysis import *


@app.route('/')

@app.route('/index')
def index():
   #user = '' # fake user
   #return render_template("index.html",
   #    title = 'Home',
   #    user = user)
   return render_template("index.html")
   
@app.route('/output')
def call_output():
    city = int(request.args.get('Location')); print type(city)
    view = int(request.args.get('View')); print type(view)

	##TODO: error handling!!! xxx
    
    # SF & Bay/Ocean:
    if city == 1 and view == 1:
    	run_prep('SF', 'Bay view')
    # SF & Golden Gate Bridge:
    elif city == 1 and view == 2:
    	run_prep('SF', 'GGB')
    # Paris & Eiffel tower:
    elif city == 2 and view == 1:
    	run_prep('Paris', 'Eiffel') 
    # Paris & Montmartre:
    elif city == 2 and view == 2:
    	run_prep('Paris', 'Montmartre') 
    # Paris & Sacre Coeur:
    elif city == 2 and view == 3:
    	run_prep('Paris', 'Sacre Coeur')  
    # Paris & Notre Dame:
    elif city == 2 and view == 4:
    	run_prep('Paris', 'Notre Dame') 
    
    #
    if city == 2:
    	map_name2 = 'static/js/paris_avr.js'
    elif city == 1:
    	map_name2 = 'static/js/sf_avr.js'
   	   	
    
    map_name = 'map_airbnb.html' 
    # one can either enter: map_name = '...', otherwise, it has to be the same name!!! (map_name=var won't work)
    return render_template("output.html", map_name=map_name, map_name2=map_name2)
    title = 'Home',
#       user = user)


