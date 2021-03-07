from flask import Flask, render_template, url_for, request, redirect
import holidays
import os
import json
import datetime

app = Flask(__name__)
path_holidays = os.path.dirname(os.path.abspath(holidays.__file__))
@app.route('/', methods=['POST', 'GET'])
def index():
        list_of_countries = [name.split(".py")[0].replace("_"," ").upper() for name in os.listdir(path_holidays+"/countries/") if name.endswith(".py") and  not name.startswith("__")]
        return render_template('index.html', list_of_countries=sorted(list_of_countries))
@app.route('/states/<country>/<year>/', defaults={'state': None}, methods=['POST', 'GET'])
@app.route('/states/<country>/<year>/<state>/', methods=['POST', 'GET'])
def city(country, year=datetime.datetime.now().year, state=None):
        year = int(year)
        try: 
                prov_states = getattr(holidays,country.title().replace(" ","")).STATES
        except:
                prov_states = getattr(holidays,country.title().replace(" ","")).PROVINCES
        list_of_hols = []
        for  date, name in sorted(getattr(holidays,country.title().replace(" ",""))(years=year, state=state, prov=state).items()):
                list_of_hols.append({'date': str(date), 'name': name})
        return {'prov': json.dumps(prov_states), 'holidays' : json.dumps(list_of_hols, sort_keys=True, default=str)}
if __name__ == "__main__":
    app.run(debug=True)
