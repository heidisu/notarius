from flask import Flask, flash, render_template, request, redirect
from notat import get_notater, add_notat, get_notat, update_notat, delete_notat
from bruker import get_bruker, create_bruker
from werkzeug.security import generate_password_hash, check_password_hash
import os
import db

app = Flask(__name__)
app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'notarius.sqlite'),
    SECRET_KEY='dev'
)

db.init_app(app)

@app.route('/')
def notater():
    notater = get_notater(db.get_db())
    return render_template('index.html', notater = notater)

@app.route('/notat', methods=('GET', 'POST'))
def nytt_notat():
    if request.method == 'POST':
        tittel = request.form['tittel']
        tekst = request.form['tekst']
        add_notat(db.get_db(), tittel, tekst)
        return redirect('/')

    return render_template('nytt_notat.html')

@app.route('/<int:id>/rediger', methods=('GET', 'POST'))
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

    return render_template('login.html')

if __name__ == "__main__":
    app.run() #port='8000', host='127.0.0.1')
