import os, sys
from flask import render_template, request, redirect, url_for   
import numpy as np
from db import *
from refuiling import *

UPLOAD_FOLDER = 'input/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # name = request.form['name']
        uploaded = request.files['uploaded']
        uploaded.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded.filename))
        print(url_for('reading_file', file_name = uploaded.filename, ))
        return redirect(url_for('reading_file', file_name = uploaded.filename))
    #     oper_name = 'refueling #130'
    #     desc = 'refueled two 8-tube FA in cells 7-6, 6-6'
    #     date = datetime.now()
    #     data = np.array([0,0,0]).tobytes() #* convert to bytes
    #     rq = RefuelingDB(name=oper_name, description=desc, date=date, data=data)
    #     db.session.add(rq)
    #     db.session.commit()
    #     print(name)
    return render_template('home.html')


@app.route('/proc/<file_name>', methods=['GET', 'POST'])
def reading_file(file_name):
    arr = ''
    arr = Average(file_name).average_burnup()
    print(arr)
    if request.method == 'POST':
        print('detected_POST')
        option = request.form['options']
        numbers = request.form['numbers']
        if option == 'fresh':
            new = Fresh(file_name, numbers).refueling()
            print(new)
        elif option == 'swap':
            new = Swap(file_name, numbers).swap()
            print(new)
        # print(option, numbers)

        # return redirect(url_for('refueling', file_name = uploaded.filename))

    return render_template('reading_file.html', burnup = arr)

@app.route('/refueling')
def core_refueling():
    return

@app.route('/list')
def list():
    refueling_list = RefuelingDB.query.order_by(RefuelingDB.date).all()
    return render_template('list.html', list=refueling_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)