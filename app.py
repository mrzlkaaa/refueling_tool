import os, sys
from datetime import datetime
from flask import render_template, request, redirect, url_for, session, send_file
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
    arr, pdc_name = Average(file_name).average_burnup()
    print(pdc_name)
    if request.method == 'POST':
        print('detected_POST')
        option = request.form['options']
        numbers = request.form['numbers']
        if option == 'fresh':
            new, pdc_name_new = Fresh(file_name, numbers).refueling()
            print(new)
        elif option == 'swap':
            new, pdc_name_new = Swap(file_name, numbers).swap()
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
    old_core, pdc_data = np.array(session.get('old_core')[0]), tobytes(Refueling(session.get('old_core')[1]).get_data)
    new_core, pdc_data_new = np.array(session.get('new_core')[0]), tobytes(Refueling(session.get('new_core')[1]).get_data)
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
            db.session.commit()
        else:
            if len(request.form.get('date')) > 0: date = request.form.get('date')
            else: date = datetime.now()
            new_refuel = RefuelingDB(refueling_name=name, initial_configuration=pdc_data, initial_burnup_data=old_core_b, date=date)
            add_act = RefuelingActs(description=desc, current_configuration=pdc_data_new, burnup_data=new_core_b, refuel=new_refuel)
            db.session.add_all([new_refuel, add_act])
            db.session.commit()
        return redirect(url_for('list'))
    return render_template('refueling.html', old_core=old_core, new_core=new_core, form=form)

@app.route('/list')
def list():
    refueling_list = RefuelingDB.query.order_by(RefuelingDB.date).all()
    print(RefuelingDB.query.all())
    return render_template('list.html', list=refueling_list)

@app.route('/detail/<name>', methods=['GET','POST'])
def detail(name):
    refuiel_data = RefuelingDB.query.filter_by(refueling_name=name).first()
    print(refuiel_data)
    refuel_seq = refuiel_data.acts
    refuiel_data.initial_burnup_data = np.frombuffer(refuiel_data.initial_burnup_data).reshape((6,4))
    processed_refuel_seq = ({'id': i.id, 'description': i.description, 'burnup_data':np.frombuffer(i.burnup_data).reshape((6,4))} for i in refuel_seq )
    print(sys.getsizeof(refuel_seq))
    # print(refuel_seq)
    # print(next(processed_refuel_seq))
    # refule_seq = np.frombuffer(refueling_data.burnup_data).reshape((6,4))
    # print(refueling_data)
    return render_template('detail.html', refueling=refuiel_data, refuel_seq=processed_refuel_seq)

@app.route('/download/<refueling_name>_<seq>', methods=['GET','POST'])
def download(refueling_name, seq):
    file_name = f'{refueling_name}_{seq}.PDC'
    pdc = ''
    seq = int(seq)
    # seq=3
    refuiel_data = RefuelingDB.query.filter_by(refueling_name=refueling_name).first()
    refuel_seq = refuiel_data.acts
    try:
        gets_id = ((i.id, i.current_configuration) for i in refuel_seq if i.id==seq)
        matched = next(gets_id)
        print(f'Takes from child where id is {matched[0]}')
        pdc =  matched[1].decode('utf-8')
        print(type(pdc))
    except Exception as e:
        print(e)
        print(f'Takes from parent where id is {refuiel_data.id}')
    Refueling(file_name, data=pdc).for_download
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], file_name), as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)