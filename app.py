import os
from flask import render_template, request
import numpy as np
from db import *



@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        name = request.form['name']
        oper_name = 'refueling #130'
        desc = 'refueled two 8-tube FA in cells 7-6, 6-6'
        date = datetime.now()
        data = np.array([0,0,0]).tobytes() #* convert to bytes
        rq = RefuelingDB(name=oper_name, description=desc, date=date, data=data)
        db.session.add(rq)
        db.session.commit()
        print(name)
    return render_template('home.html')