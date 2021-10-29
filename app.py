import os, sys
import io
import time
from datetime import datetime
from flask import render_template, request, redirect, url_for, session, send_file, jsonify
import numpy as np
from werkzeug.utils import send_from_directory
from db import *
from refuiling import *


UPLOAD_FOLDER = 'input/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = 'output/'

@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # name = request.form['name']
        uploaded = request.files['uploaded']
        uploaded.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded.filename))
        print(url_for('reading_file', file_name = uploaded.filename))
        return redirect(url_for('reading_file', file_name = uploaded.filename))
    return render_template('home.html')


@app.route('/proc/<file_name>', methods=['GET', 'POST'])
def reading_file(file_name):
    arr, pdc_name, _ = Average(file_name).average_burnup()
    if request.method == 'POST':
        print('detected_POST')
        option = request.form['options']
        numbers = request.form['numbers']
        if option == 'fresh':
            new, pdc_name_new, _ = Fresh(file_name, numbers, save=True).refueling()
            print(new)
        elif option == 'swap':
            new, pdc_name_new, _ = Swap(file_name, numbers, save=True).swap()
            print(new)
        session['old_core'] = (arr.tolist(), pdc_name)
        session['new_core'] = (new.tolist(), pdc_name_new)
        return redirect(url_for('core_refueling'))
        # print(option, numbers)

        # return redirect(url_for('refueling', file_name = uploaded.filename))

    return render_template('reading_file.html', burnup = arr)

tobytes = lambda x: bytes(''.join(x), 'UTF-8')

@app.route('/refueling', methods=['GET', 'POST'])
def core_refueling():
    old_core, pdc_data = np.array(session.get('old_core')[0]), tobytes(Refueling(session.get('old_core')[1]).load_data) # seems like loading of pdc file on this stage is useless (just memory consuming)
    new_core, pdc_data_new = np.array(session.get('new_core')[0]), tobytes(Refueling(session.get('new_core')[1]).load_data)
    form = RefuelList()
    form.add_existing.choices = [(data.refueling_name, data.refueling_name) for data in RefuelingDB.query.all()]
    if request.method == 'POST':
        name = request.form.get('new_refuel')
        new_core_b = new_core.tobytes() #* convert to bytes
        old_core_b = old_core.tobytes() #* convert to bytes
        desc = request.form.get('description')
        if len(name) == 0:
            name = request.form['add_existing']
            print(name)
            query_refueling = RefuelingDB.query.filter_by(refueling_name=name).first()
            print(type(query_refueling))
            date = query_refueling.date
            add_act = RefuelingActs(description=desc, current_configuration=pdc_data_new, burnup_data=new_core_b, refuel=query_refueling)
            db.session.add(add_act)
        else:
            if len(request.form.get('date')) > 0: date = request.form.get('date')
            else: date = datetime.now()
            new_refuel = RefuelingDB(refueling_name=name, initial_configuration=pdc_data, initial_burnup_data=old_core_b, date=date)
            add_act = RefuelingActs(description=desc, current_configuration=pdc_data_new, burnup_data=new_core_b, refuel=new_refuel)
            db.session.add_all([new_refuel, add_act])
        db.session.commit()
        return redirect(url_for('display_list'))
    return render_template('refueling.html', old_core=old_core, new_core=new_core, form=form)

@app.route('/list')
def display_list():
    time_before = time.time()
    refueling_list = db.session.query(RefuelingDB).options(load_only(RefuelingDB.date, RefuelingDB.refueling_name)).order_by(RefuelingDB.date).all()
    print(time.time() - time_before)
    print(sys.getsizeof(refueling_list))
    return render_template('list.html', list=refueling_list)

@app.route('/detail/<name>', methods=['GET','POST'])
def detail(name):
    time_before = time.time()
    refuiel_data = RefuelingDB.query.filter_by(refueling_name=name).first() #TODO add load_only method to avoiding querying and loading of pdc file
    print(time.time() - time_before)
    print(refuiel_data)
    refuel_seq = refuiel_data.acts
    refuiel_data.initial_burnup_data = np.frombuffer(refuiel_data.initial_burnup_data).reshape((6,4))
    processed_refuel_seq = sorted([{'id': i.id, 'description': i.description, 'burnup_data':np.frombuffer(i.burnup_data).reshape((6,4))} for i in refuel_seq], key=lambda x: x['id'])
    return render_template('detail.html', refueling=refuiel_data, refuel_seq=processed_refuel_seq)

@app.route('/update/<name>-<seq>', methods=['POST', 'GET'])
def update(name, seq):
    seq = int(seq)
    refuiel_data = db.session.query(RefuelingDB).join(RefuelingActs, RefuelingDB.refueling_name==name).filter(RefuelingActs.id<=seq).first().acts
    print(refuiel_data)
    bytes_pdc = refuiel_data[len(refuiel_data)-2].current_configuration
    splitted = bytes_pdc.decode().split("\n")
    added_newline = list(map(lambda x: x+"\n", splitted))
    if len(refuiel_data) < 2:
        print('preparing to load initial core config and following step...')
        initial_data = RefuelingDB.query.filter_by(refueling_name=name).first()
        old_core, pdc = np.frombuffer(initial_data.initial_burnup_data).reshape((6,4)), map(lambda x: x+"\n",refuiel_data[len(refuiel_data)-2].current_configuration.decode("utf-8").split("\n"))
        new_core, description = np.frombuffer(refuiel_data[0].burnup_data).reshape((6,4)), refuiel_data[0].description
    else:
        print('preparing to load two latter steps...')
        old_core, pdc = np.frombuffer(refuiel_data[len(refuiel_data)-2].burnup_data).reshape((6,4)), map(lambda x: x+"\n",refuiel_data[len(refuiel_data)-2].current_configuration.decode("utf-8").split("\n"))
        new_core, description = np.frombuffer(refuiel_data[len(refuiel_data)-1].burnup_data).reshape((6,4)), refuiel_data[len(refuiel_data)-1].description
    if request.method == "POST":
        file_name = f'{name}_{seq}.PDC'
        option = request.form['options']
        numbers = request.form['numbers']
        description = request.form['description']
        if option == 'fresh':
            new_core, pdc_name_new, pdc_new = Fresh(file_name, numbers, pdc=pdc).refueling()
            new_core_b = new_core.tobytes() #* convert to bytes
            print(new_core)
        elif option == 'swap':
            new_core, pdc_name_new, pdc_new = Swap(file_name, numbers, pdc=pdc).swap()
            new_core_b = new_core.tobytes() #* convert to bytes
        db.session.query(RefuelingActs).filter(RefuelingActs.id==seq).update({RefuelingActs.burnup_data:new_core_b, RefuelingActs.description:description, RefuelingActs.current_configuration:tobytes(pdc_new)})
        db.session.commit()
        return redirect(url_for('display_list'))
    return render_template('update.html', old_core=old_core, new_core=new_core, description=description)

@app.route('/download/<name>-<seq>', methods=['GET','POST'])
def download(name, seq):
    file_name = f'{name}_{seq}.PDC'
    pdc = ''
    seq = int(seq)
    refuiel_data = RefuelingDB.query.filter_by(refueling_name=name).first()
    refuel_seq = refuiel_data.acts
    try:
        gets_id = ((i.id, i.current_configuration) for i in refuel_seq if i.id==seq) #TODO rewrite it like sql query
        matched = next(gets_id)
        print(f'Takes from child where id is {matched[0]}')
        pdc =  matched[1].decode('utf-8')
        print(type(pdc))
    except:
        print(f'Takes from parent where id is {refuiel_data.id}')
    Refueling(file_name, data=pdc).for_download
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], file_name), as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)