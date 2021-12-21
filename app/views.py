from . import r, create_app
from .model import *
from .refuiling import *
from flask import request, render_template, url_for, redirect, send_file, Blueprint
from sqlalchemy.orm import load_only, subqueryload
from datetime import datetime
import time

view = Blueprint("view", __name__)

app = create_app()

tobytes = lambda x: bytes(''.join(x), 'UTF-8')

@view.route("/upload_PDC", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        uploaded = request.files['uploaded']
        bytes_upload = uploaded.read()
        r.hset("PDC_DATA", "current_pdc", bytes_upload)
        return redirect(url_for('view.reading_file'))
    return render_template('home.html')

@view.route('/reading_file', methods=['GET', 'POST'])
def reading_file():
    #* < x+\n > expression guarantee initail style of .PDC
    pdc = list(map(lambda x: x+"\n", r.hget("PDC_DATA", "current_pdc").decode("utf-8").split("\n")))
    before = time.time()
    current, _ = Average(pdc=pdc).average_burnup()
    print(time.time() - before)
    r.hset('PDC_DATA', 'current_core', current.tobytes())
    if request.method == 'POST':
        print('detected_POST')
        option = request.form['options']
        numbers = request.form['numbers']
        if option == 'fresh': new, new_config = Fresh(numbers, pdc=pdc).refueling()
        elif option == 'swap': new, new_config = Swap(numbers, pdc=pdc).swap()
        r.hset("PDC_DATA", 'new_pdc', tobytes(new_config))
        r.hset("PDC_DATA", 'new_core', new.tobytes())
        return redirect(url_for('view.core_refueling'))
    return render_template('reading_file.html', burnup = current)

@view.route('/refueling', methods=['GET', 'POST'])
def core_refueling():
    time_before = time.time()
    old_core, pdc_data = np.frombuffer(r.hget("PDC_DATA", 'current_core')).reshape((6,4)), r.hget("PDC_DATA", 'current_pdc')
    new_core, pdc_data_new = np.frombuffer(r.hget("PDC_DATA", 'new_core')).reshape((6,4)), r.hget("PDC_DATA", 'new_pdc')
    form = RefuelList()
    # form.add_existing.choices = [(data.refueling_name, data.refueling_name) for data in RefuelingDB.query.options(load_only("refueling_name")).all()]
    print(time.time() - time_before)
    if request.method == 'POST':
        name = request.form.get('new_refuel')
        new_core_b = r.hget("PDC_DATA", 'new_core')
        old_core_b = r.hget("PDC_DATA", 'current_core')
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
        return redirect(url_for('view.display_list'))
    return render_template('refueling.html', old_core=old_core, new_core=new_core, form=form)

@view.route('/list')
def display_list():
    time_before = time.time()
    refueling_list = db.session.query(RefuelingDB).options(load_only(RefuelingDB.date, RefuelingDB.refueling_name)).order_by(RefuelingDB.date).all()
    print(time.time() - time_before)
    return render_template('list.html', list=refueling_list)

@view.route('/detail/<name>', methods=['GET','POST'])
def detail(name):
    refuiel_data = db.session.query(RefuelingDB).filter(RefuelingDB.refueling_name==name).options(load_only("id", "refueling_name", "initial_burnup_data", "date"), subqueryload("acts").load_only("id", "description", "burnup_data")).first()
    print(f"id is {refuiel_data.id}")
    refuel_seq = refuiel_data.acts
    print(type(refuiel_data.initial_burnup_data))
    initial_burnup = np.frombuffer(refuiel_data.initial_burnup_data).reshape((6,4))
    processed_refuel_seq = sorted([{'id': i.id, 'description': i.description, 'burnup_data':np.frombuffer(i.burnup_data).reshape((6,4))} for i in refuel_seq], key=lambda x: x['id'])
    print(processed_refuel_seq[-1]["id"])
    if request.method == "POST":
        option = request.form['options']
        numbers = request.form['numbers']
        desc = request.form.get('description')
        latest_id = processed_refuel_seq[-1]["id"]
        refuiel_data_pdc = RefuelingActs.query.join(RefuelingDB).filter(RefuelingActs.id==latest_id, RefuelingDB.refueling_name==name).first()
        print(refuiel_data_pdc)
        pdc = map(lambda x: x+"\n", refuiel_data_pdc.current_configuration.decode("utf-8").split("\n"))
        if option == 'fresh': new, new_config = Fresh(numbers, pdc=pdc).refueling()
        elif option == 'swap': new, new_config = Swap(numbers, pdc=pdc).swap()
        # refuel_data = RefuelingDB.query.filter(RefuelingDB.refueling_name==name).first()
        add_act = RefuelingActs(description=desc, current_configuration=tobytes(new_config), burnup_data=new.tobytes(), refuel=refuiel_data)
        db.session.add(add_act)
        db.session.commit()
        return redirect(url_for('view.detail', name=name))
    return render_template('detail.html', initial_burnup=initial_burnup, refueling=refuiel_data, refuel_seq=processed_refuel_seq)

@view.route('/update/<name>-<seq>', methods=['POST', 'GET'])
def update(name, seq):
    time_before = time.time()
    seq = int(seq)
    refuiel_data = db.session.query(RefuelingActs).join(RefuelingDB).filter(RefuelingDB.refueling_name==name, RefuelingActs.id<=seq).order_by(RefuelingActs.id.desc()).all()
    print(time.time() - time_before)
    if len(refuiel_data) < 2:
        print('preparing to load initial core config and following step...')
        old_core, pdc_data = np.frombuffer(refuiel_data[0].refuel.initial_burnup_data).reshape((6,4)), map(lambda x: x+"\n",refuiel_data[0].refuel.initial_configuration.decode("utf-8").split("\n"))
        # print(old_core)
        current_core, description = np.frombuffer(refuiel_data[0].burnup_data).reshape((6,4)), refuiel_data[0].description
    else:
        print('preparing to load two latter steps...')
        old_core, pdc_data = np.frombuffer(refuiel_data[1].burnup_data).reshape((6,4)), map(lambda x: x+"\n",refuiel_data[1].current_configuration.decode("utf-8").split("\n"))
        current_core, description = np.frombuffer(refuiel_data[0].burnup_data).reshape((6,4)), refuiel_data[0].description
    if request.method == "POST":
        file_name = f'{name}_{seq}.PDC'
        option = request.form['options']
        numbers = request.form['numbers']
        description = request.form['description']
        if option == 'fresh':
            new_core, pdc_new = Fresh(numbers, pdc=pdc_data).refueling()
            new_core_b = new_core.tobytes() #* convert to bytes
            print(new_core)
        elif option == 'swap':
            new_core, pdc_new = Swap(numbers, pdc=pdc_data).swap()
            new_core_b = new_core.tobytes() #* convert to bytes
        db.session.query(RefuelingActs).filter(RefuelingActs.id==seq).update({RefuelingActs.burnup_data:new_core_b, RefuelingActs.description:description, RefuelingActs.current_configuration:tobytes(pdc_new)})
        db.session.commit()
        return redirect(url_for('view.detail', name=name))
    return render_template('update.html', name=name, id=seq, old_core=old_core, new_core=current_core, description=description)

@view.route("/<id>/delete", methods = ["POST"])
def delete(id):
    instance = RefuelingDB.query.get_or_404(id)
    db.session.delete(instance)
    db.session.commit()
    return redirect(url_for('view.display_list'))

@view.route("/<name>-<id>/delete", methods = ["POST"])
def delete_step(name, id):
    instance = RefuelingActs.query.get_or_404(id)
    db.session.delete(instance)
    db.session.commit()
    return redirect(url_for('view.detail', name=name))

@view.route('/download/<name>-<seq>', methods=['GET','POST'])
def download(name, seq):
    pdc = ''
    seq = int(seq)
    try:
        refuiel_data = db.session.query(RefuelingActs).join(RefuelingDB).filter(RefuelingDB.refueling_name==name, RefuelingActs.id==seq).first()
        gets_id = refuiel_data.id
        pdc = refuiel_data.current_configuration.decode("utf-8")
        print(f'Takes from child where id is {gets_id}')
    except AttributeError:
        refuiel_data = db.session.query(RefuelingActs).join(RefuelingDB).filter(RefuelingDB.refueling_name==name).first()
        gets_id = refuiel_data.refuel.id
        print(f'Takes from parent where id is {gets_id}')
        pdc = refuiel_data.refuel.initial_configuration.decode('utf-8')
    file_name = f'{name}_{gets_id}.PDC'
    Refueling(file_name, data=pdc).for_download
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], file_name), as_attachment=True)
