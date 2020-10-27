from flask import Flask, flash, render_template, request, redirect, session, g
from notat import get_notater, add_notat, get_notat, update_notat, delete_notat
from bruker import get_bruker, create_bruker
from werkzeug.security import generate_password_hash, check_password_hash
import os
import db
import functools

app = Flask(__name__)
app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'notarius.sqlite'),
    SECRET_KEY='dev'
)

db.init_app(app)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect('/login')
        return view(**kwargs)
    return wrapped_view

@app.route('/')
def notater():
    notater = get_notater(db.get_db())
    return render_template('index.html', notater = notater)

@app.route('/notat', methods=('GET', 'POST'))
@login_required
def nytt_notat():
    if request.method == 'POST':
        tittel = request.form['tittel']
        tekst = request.form['tekst']
        add_notat(db.get_db(), tittel, tekst)
        return redirect('/')

    return render_template('nytt_notat.html')

@app.route('/<int:id>/rediger', methods=('GET', 'POST'))
@login_required
def rediger_notat(id):
    notat = get_notat(db.get_db(), id)
    if request.method == 'POST':
        tittel = request.form['tittel']
        tekst = request.form['tekst']
        if not tittel:
            flash('Tittel er påkrevd')
        else:
            update_notat(db.get_db(), id, tittel, tekst)
        return redirect('/')

    return render_template('rediger_notat.html', notat = notat)

@app.route('/<int:id>/slett', methods=('POST',))
@login_required
def slett_notat(id):
    delete_notat(db.get_db(), id)
    return redirect('/')

@app.route('/registrer', methods=('POST', 'GET'))
def registrer():
    if request.method == 'POST':
        brukernavn = request.form['brukernavn']
        passord = request.form['passord']

        error = None
        if not brukernavn:
            error = 'Brukernavn er påkrevd'
        elif not passord:
            error = 'Passord er påkrevd'
        elif get_bruker(db.get_db(), brukernavn) is not None:
            error = f'Bruker {brukernavn} er allerede registrert'
        if error:
            flash(error)
        else:
            create_bruker(db.get_db(), brukernavn, generate_password_hash(passord))
            return redirect('/')

    return render_template('login.html', tittel = 'Registrer')

@app.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        brukernavn = request.form['brukernavn']
        passord = request.form['passord']
        error = None

        bruker = get_bruker(db.get_db(), brukernavn)
        if bruker is None:
            error = 'Ugyldig brukernavn'
        elif not check_password_hash(bruker['passord'], passord):
            error = 'Ugyldig passord'
        flash(error)

        if error is None:
            session.clear()
            session['user_id'] = bruker['brukernavn']
            return redirect('/')

    return render_template('login.html', tittel = 'Logg inn')    

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.before_request
def load_innlogget_bruker():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_bruker(db.get_db(), user_id)

if __name__ == "__main__":
    app.run() #port='8000', host='127.0.0.1')
